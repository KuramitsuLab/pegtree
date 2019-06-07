# cython: profile=True

from pegpy.tpeg import Ref, Char, Seq, Ore, Alt, Node, Edge, Grammar
# from pegpy.gparser.gchar import GChar

import cython
import pickle as cPickle

import copy

# deepcopy = lambda obj: cPickle.loads(cPickle.dumps(obj, -1))
deepcopy = lambda obj: copy.copy(obj)

# if cython.compiled:
#   print('use cython')
#   @cython.ccall
#   @cython.locals(inputs=cython.p_char, pos=cython.int, bs=cython.p_char, blen=cython.int)
#   def char_memcmp(inputs, pos, bs, blen): return memcmp(inputs + pos, bs, blen) == 0
# else:
#   char_memcmp = lambda inputs, pos, bs, blen: inputs[pos:pos + blen] == bs


char_memcmp = lambda inputs, pos, bs, blen: inputs[pos:pos + blen] == bs


emp = bytes('', 'utf-8')
err = bytes('err', 'utf-8')
amb = bytes('?', 'utf-8')

@cython.cclass
class Tree:
  tag: object
  inputs: object
  spos: cython.int
  epos: cython.int
  child: object

  def __init__(self, tag: object, inputs: object, spos: cython.int, epos: cython.int, child: object):
    self.tag = tag
    self.inputs = inputs
    self.spos = spos
    self.epos = epos
    self.child = child

  def __str__(self):
    if self.child:
      return f'[#{self.tag.decode("utf-8")} {str(self.child)}]'
    else:
      return self.inputs.decode('utf-8')[self.spos:self.epos]


@cython.cclass
class Link:
  inner: object
  prev: object

  def __init__(self, inner: object, prev: object):
    self.inner = inner
    self.prev = prev

  def __str__(self):
    sb = self.strOut([])
    return ''.join(sb)

  def strOut(self, sb):
    if self.prev:
      sb = self.prev.strOut(sb)
    sb.append(str(self.inner))
    return sb


@cython.cclass
class GParserContext:

  inputs: object
  length: cython.int
  headpos: cython.int
  pos2ast: dict
  memo: dict

  def __init__(self, inputs: object, pos: cython.int, slen: cython.int):
    # s = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
    s = inputs
    # self.inputs, self.pos, self.length = u.encsrc(urn, inputs, pos, slen)
    self.inputs, self.length = s, len(s)
    self.headpos = 0
    self.pos2ast = {pos: None}
    self.memo = {}


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
  bs: object
  blen: cython.int

  def __init__(self, bs: object, blen: int):
    self.blen = blen
    self.bs = bs

  @cython.ccall
  @cython.locals(new_pos2ast=dict, pos=cython.int, ast=object)
  def p(self, px: GParserContext) -> cython.bint:
    new_pos2ast = {}
    for pos, ast in px.pos2ast.items():
      if char_memcmp(px.inputs, pos, self.bs, self.blen):
        new_pos2ast[pos + self.blen] = Link(Tree(emp, px.inputs, pos, pos + self.blen, None), ast)
        px.headpos = max(pos, px.headpos)
    return check_empty(px, new_pos2ast)


def gen_GChar(pe: Char, **option):
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
    for pos, ast in deepcopy(px.pos2ast).items():
      px.pos2ast = {pos:ast}
      if self.left.p(px):
        for pos, ast in deepcopy(px.pos2ast).items():
          px.pos2ast = {pos:ast}
          if self.right.p(px):
            new_pos2ast = merge(new_pos2ast, px.pos2ast)
    return check_empty(px, new_pos2ast)


def gen_GSeq(pe: Seq, **option):
  return GSeq(pe.left.gen(**option), pe.right.gen(**option))


# Ore
@cython.cclass
class GOre(ParseFunc):
  left: ParseFunc
  right: ParseFunc

  def __init__(self, left: ParseFunc, right: ParseFunc):
    self.left = left
    self.right = right

  @cython.ccall
  @cython.locals(new_pos2ast=dict)
  def p(self, px: GParserContext) -> cython.bint:
    new_pos2ast = {}
    for pos, ast in deepcopy(px.pos2ast).items():
      px.pos2ast = {pos: ast}
      if self.left.p(px):
        new_pos2ast = merge(new_pos2ast, px.pos2ast)
      else:
        px.pos2ast = {pos:ast}
        if self.right.p(px):
          new_pos2ast = merge(new_pos2ast, px.pos2ast)
    return check_empty(px, new_pos2ast)


def gen_GOre(pe: Ore, **option):
  return GOre(pe.left.gen(**option), pe.right.gen(**option))

# Alt
@cython.cclass
class GAlt(ParseFunc):
  left: ParseFunc
  right: ParseFunc

  def __init__(self, left: ParseFunc, right: ParseFunc):
    self.left = left
    self.right = right

  @cython.ccall
  @cython.locals(new_pos2ast=dict)
  def p(self, px: GParserContext) -> cython.bint:
    new_pos2ast = {}
    for pos, ast in deepcopy(px.pos2ast).items():
      px.pos2ast = {pos: ast}
      if self.left.p(px):
        new_pos2ast = merge(new_pos2ast, px.pos2ast)
        px.pos2ast = {pos: ast}
        if self.right.p(px):
          new_pos2ast = merge(new_pos2ast, px.pos2ast)
      else:
        px.pos2ast = {pos: ast}
        if self.right.p(px):
          new_pos2ast = merge(new_pos2ast, px.pos2ast)
    return check_empty(px, new_pos2ast)


def gen_GAlt(pe: Alt, **option):
  return GAlt(pe.left.gen(**option), pe.right.gen(**option))


memo = {}

# RecRef
@cython.cclass
class RecRef(ParseFunc):

  key: object
  generated: dict

  def __init__(self, key: object, generated: dict):
    self.key = key
    self.generated = generated

  @cython.ccall
  @cython.locals(ps=ParseFunc)
  def p(self, px: GParserContext) -> cython.bint:
    ps = self.generated[self.key]
    return ps.p(px)


# GMemo
@cython.cclass
class GMemo(ParseFunc):

  name: object
  inner: ParseFunc

  def __init__(self, name: object, inner: ParseFunc):
    self.name = name
    self.inner = inner

  @cython.ccall
  @cython.locals(pos=cython.int, epos=cython.int, ast=object, east=object, new_pos2ast=dict)
  def p(self, px: GParserContext) -> cython.bint:
    new_pos2ast = {}
    for pos, ast in px.pos2ast.items():
      entry = (pos, self.name)
      if entry in px.memo:
        memo = px.memo[entry]
        if memo:
          linked_memo = {}
          for epos, east in memo.items():
            linked_memo[epos] = Link(Tree(self.name, px.inputs, pos, epos, east), ast)
          new_pos2ast = merge(new_pos2ast, linked_memo)
      else:
        px.pos2ast = {pos:None}
        if self.inner.p(px):
          px.memo[entry] = deepcopy(px.pos2ast)
          for epos, east in px.pos2ast.items():
            px.pos2ast[epos] = Link(Tree(self.name, px.inputs, pos, epos, east), ast)
          new_pos2ast = merge(new_pos2ast, px.pos2ast)
        else:
          px.memo[entry] = None
    return check_empty(px, new_pos2ast)


# Ref
def emit_GRef(ref: Ref, **option):
  key = ref.uname()
  generated = option['generated']
  if not key in generated:
    generated[key] = RecRef(key, generated)
    generated[key] = GMemo(bytes(ref.name, 'utf-8'), ref.deref().gen(**option))
  return generated[key]


def gen_GRef(pe, **option):
  return emit_GRef(pe, **option)


#Node
@cython.cclass
class GNode(ParseFunc):
  inner: ParseFunc
  node: object

  def __init__ (self, inner: ParseFunc, node: object):
    self.inner = inner
    self.node = node
  
  @cython.ccall
  @cython.locals(spos=cython.int, epos=cython.int, sast=object, east=object, new_pos2ast=dict)
  def p(self, px: GParserContext) -> cython.bint:
    new_pos2ast = {}
    for spos, sast in deepcopy(px.pos2ast).items():
      px.pos2ast = {spos: sast}
      if self.inner.p(px):
        for epos, east in deepcopy(px.pos2ast).items():
          px.pos2ast[epos] = Link(Tree(self.node, px.inputs, spos, epos, east), None)
        new_pos2ast = merge(new_pos2ast, px.pos2ast)
    return check_empty(px, new_pos2ast)


def gen_GNode(pe: Node, **option):
  # GNode(pe.inner.gen(**option), pe.node)
  return pe.inner.gen(**option)


# Edge
@cython.cclass
class GEdge(ParseFunc):
  inner: ParseFunc
  edge: object

  def __init__(self, inner: ParseFunc, edge: object):
    self.inner = inner
    self.edge = edge

  @cython.ccall
  def p(self, px: GParserContext) -> cython.bint:
    return self.inner.p(px)


def gen_GEdge(pe, **option):
  # return GEdge(pe.inner.gen(**option), pe.edge)
  return pe.inner.gen(**option)


Ref.gen = gen_GRef
Char.gen = gen_GChar
Seq.gen = gen_GSeq
Ore.gen = gen_GOre
Alt.gen = gen_GAlt
Node.gen = gen_GNode
Edge.gen = gen_GEdge


def collect_amb(s, urn, pos, result):
  is_first = True
  for result_pos, r in result.items():
    if r == None:
      r = Tree(emp, s, pos, result_pos, None)
    if is_first:
      prev = Link(r, None)
      is_first = False
    else:
      prev = Link(r, prev)
  return prev


def cgpeg(peg, **option):
  name = option.get('start', peg.start())
  option['peg'] = peg
  option['generated'] = {}
  f = gen_GRef(Ref(name, peg, {}), **option)
  def parse(inputs, urn='(unknown)', pos=0, epos=None):
    if not epos:
      epos = len(inputs)
    px = GParserContext(bytes(inputs, 'UTF-8'), pos, epos)
    if not f.p(px):
      return Tree(err, px.inputs, px.headpos, epos, None)
    elif len(px.pos2ast) == 1:
      (result_pos, result_ast) = list(px.pos2ast.items())[0]
      if result_ast == None:
        return Tree(emp, px.inputs, pos, result_pos, None)
      else:
        return result_ast
    return Tree(amb, px.inputs, pos, max(px.pos2ast.keys()), collect_amb(px.inputs, urn, pos, px.pos2ast))
  return parse
