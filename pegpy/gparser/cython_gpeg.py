from pegpy.tpeg import Ref, Char, Seq, Grammar
from pegpy.gparser.ast import Tree, Link
import copy

import cython

if cython.compiled:
  @cython.ccall
  @cython.locals(inputs=cython.p_char, pos=cython.int, bs=cython.p_char, blen=cython.int)
  def char_memcmp(inputs, pos, bs, blen): return memcmp(inputs + pos, bs, blen) == 0
else:
  char_memcmp = lambda inputs, pos, bs, blen: inputs[pos:pos + blen] == bs

@cython.cclass
class GParserContext:

  inputs: cython.p_char
  length: cython.int
  headpos: cython.int
  pos2ast: dict

  def __init__(self, inputs: cython.p_char, pos: cython.int, slen: cython.int):
    # s = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
    s = inputs
    # self.inputs, self.pos, self.length = u.encsrc(urn, inputs, pos, slen)
    self.inputs, self.length = s, len(s)
    self.headpos = 0
    self.pos2ast = {pos: None}


@cython.cfunc
@cython.returns(cython.bint)
def check_empty(px: GParserContext, new_pos2ast: dict) -> cython.bint:
  if len(new_pos2ast) == 0:
    return False
  else:
    px.pos2ast = new_pos2ast
    return True


@cython.cfunc
@cython.returns(dict)
def merge(new_pos2ast: dict, pos2ast: dict) -> dict:
  for i in set(new_pos2ast) & set(pos2ast):
    new_pos2ast[i] = Link(pos2ast[i], Link(new_pos2ast[i], None))
  for i in set(pos2ast) - set(new_pos2ast):
    new_pos2ast[i] = pos2ast[i]
  return new_pos2ast

# ParseFunc

# Empty

@cython.cclass
class ParseFunc:
  def __init__(self):
    pass

  @cython.cfunc
  def p(self, px: GParserContext) -> cython.bint:
    return True


# Char
@cython.cclass
class GChar(ParseFunc):
  bs: cython.p_char
  blen: cython.int

  def __init__(self, chars: bytes, blen: int):
    self.bs = chars
    self.blen = blen

  @cython.ccall
  @cython.locals(new_pos2ast=dict, pos=cython.int, ast=object)
  def p(self, px: GParserContext) -> cython.bint:
    new_pos2ast = {}
    for pos, ast in px.pos2ast.items():
      if char_memcmp(px.inputs, pos, self.bs, self.blen):
        new_pos2ast[pos + self.blen] = Link(Tree('', px.inputs, pos, pos + self.blen, None), ast)
        px.headpos = max(pos, px.headpos)
    return check_empty(px, new_pos2ast)


def gen_GChar(pe: Char):
  return GChar(bytes(pe.text, 'UTF-8'), len(bytes(pe.text, 'UTF-8')))


# Seq
@cython.cclass
class GSeq(ParseFunc):
  left: ParseFunc
  right: ParseFunc

  def __init__(self, left: ParseFunc, right: ParseFunc):
    self.left = left
    self.right = right
  
  @cython.ccall
  @cython.locals(new_pos2ast=dict)
  def p(self, px: GParserContext) -> cython.bint:
    new_pos2ast = {}
    for pos, ast in copy.deepcopy(px.pos2ast).items():
      px.pos2ast = {pos:ast}
      if self.left.p(px):
        for pos, ast in copy.deepcopy(px.pos2ast).items():
          px.pos2ast = {pos:ast}
          if self.right.p(px):
            new_pos2ast = merge(new_pos2ast, px.pos2ast)
    return check_empty(px, new_pos2ast)


def gen_GSeq(pe: Seq):
  return GSeq(pe.left.gen(), pe.right.gen())


# Ref
def emit_GRef(ref: Ref, memo: dict):
  key = ref.uname()
  if not key in memo:
    memo[key] = lambda px: memo[key].p(px)
    p = ref.deref()
    memo[key] = p.gen()
  return memo[key]


def gen_GRef(pe):
  return emit_GRef(pe, {})


def cgpeg(p, **option):
  gsetting('cgpeg')
  return generate_gparser(ggenerate(p, **option), **option)


def gsetting(f: str):
  if not hasattr(Char, f):

    #setattr(Empty, f, lambda self: gparser.p_GTrue)
    #setattr(Any, f, lambda self: gparser.mresult(gparser.p_GAny))
    setattr(Char, f, gen_GChar)
    #setattr(Range, f, gparser.emit_GByteRange)

    setattr(Seq, f, gen_GSeq)
    #setattr(Ore, f, lambda pe: gparser.emit_GOr(pe, emit))
    #setattr(Alt, f, lambda pe: gparser.emit_GAlt(pe, emit, ParseTree, TreeLink))
    #setattr(Not, f, lambda pe: gparser.emit_GNot(pe, emit))
    #setattr(And, f, lambda pe: gparser.emit_GAnd(pe, emit))
    #setattr(Many, f, lambda pe: gparser.emit_GMany(pe, emit, ParseTree, TreeLink))
    #setattr(Many1, f, lambda pe: gparser.emit_GMany1(pe, emit, ParseTree, TreeLink))

    #setattr(TreeAs, f, lambda pe: gparser.emit_GTreeAs(pe, emit, ParseTree))
    #setattr(LinkAs, f, lambda pe: gparser.emit_GLinkAs(pe, emit, TreeLink))
    #setattr(FoldAs, f, lambda pe: gparser.emit_GFoldAs(pe, emit, ParseTree, TreeLink))
    #setattr(Detree, f, lambda pe: gparser.emit_GDetree(pe, emit))

    # Ref
    setattr(Ref, f, gen_GRef)
    return True
  return False


Ref.gen = gen_GRef
Char.gen = gen_GChar
Seq.gen = gen_GSeq

def ggenerate(peg, **option):
  if option['start']:
    p = peg[option['start']]
  else:
    p = peg.newRef(peg.start())
  option['peg'] = peg
  option['generated'] = {}
  return p.gen()


def collect_amb(s, urn, pos, result):
  is_first = True
  for result_pos, r in result.items():
    if r == None:
      r = Tree("", s, pos, result_pos, None)
    if is_first:
      prev = Link(r, None)
      is_first = False
    else:
      prev = Link(r, prev)
  return prev


def generate_gparser(f, **option):
  def parse(inputs, urn='(unknown)', pos=0, epos=None):
    px = GParserContext(bytes(inputs, 'UTF-8'), pos, epos)
    if not f.p(px):
      return Tree("err", px.inputs, px.headpos, epos, None)
    elif len(px.pos2ast) == 1:
      (result_pos, result_ast) = list(px.pos2ast.items())[0]
      if result_ast == None:
        return Tree("", px.inputs, pos, result_pos, None)
      else:
        return result_ast
    return Tree("?", px.inputs, pos, max(px.pos2ast.keys()), collect_amb(px.inputs, urn, pos, px.pos2ast))
  return parse
