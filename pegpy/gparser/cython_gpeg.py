from pegpy.expression import Char, Empty, Any, Range, Seq, Ore, Alt, Not, And, Many, Many1, TreeAs, LinkAs, FoldAs, Detree, Ref
from pegpy.ast import ParseTree, TreeLink
import pegpy.utils as u
from pegpy.peg import Grammar
from pegpy.expression import ParsingExpression, Ref

import cython


class GParserContext:
  __slots__ = ['inputs', 'length', 'headpos', 'pos2ast']

  def __init__(self, inputs, urn, pos, slen):
    # s = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
    s = inputs
    # self.inputs, self.pos, self.length = u.encsrc(urn, inputs, pos, slen)
    self.inputs, self.length = s, len(s)
    self.headpos = 0
    self.pos2ast = {pos: None}


def check_empty(prev_pos2ast: dict, new_pos2ast: dict) -> bool:
  if len(new_pos2ast) == 0:
    return False
  else:
    prev_pos2ast = new_pos2ast
    return True


def emit_char(c):
  def curry(px: GParserContext):
    new_pos2ast = {}
    for pos, ast in px.pos2ast.items():
      if pos < px.length and px.inputs[pos] == c:
        new_pos2ast[pos + 1] = ast
        px.headpos = max(pos, px.headpos)
    return check_empty(px.pos2ast, new_pos2ast)
  return curry


def emit_multi(s, slen):
  def curry(px):
    new_pos2ast = {}
    for pos, ast in px.pos2ast.items():
      if px.inputs.startswith(s, pos):
        new_pos2ast[pos + slen] = ast
        px.headpos = max(pos, px.headpos)
    return check_empty(px.pos2ast, new_pos2ast)
  return curry


pf_char = {}

def gen_GChar(pe):
  if len(pe.a) > 1:
    return emit_multi(pe.a, len(pe.a))
  if not pe.a in pf_char:
    pf_char[pe.a] = emit_char(pe.a)
  return pf_char[pe.a]


def emit_GRef(ref: Ref, memo: dict, emit):
    key = ref.uname()
    if not key in memo:
        memo[key] = lambda px: memo[key](px)
        memo[key] = emit(ref.deref())
    return memo[key]


def cgpeg(p, conv=None):
  gsetting('cgpeg')
  return generate_gparser(ggenerate(p, 'cgpeg'), conv)


def gsetting(f: str):
  if not hasattr(Char, f):
    def emit(pe): return getattr(pe, f)()

    #setattr(Empty, f, lambda self: gparser.p_GTrue)
    #setattr(Any, f, lambda self: gparser.mresult(gparser.p_GAny))
    setattr(Char, f, gen_GChar)
    #setattr(Range, f, gparser.emit_GByteRange)

    #setattr(Seq, f, lambda pe: gparser.emit_GSeq(pe, emit, ParseTree, TreeLink))
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
    memo = {}
    setattr(Ref, f, lambda pe: emit_GRef(pe, memo, emit))
    return True
  return False


def ggenerate(p, f='cgpeg'):
  if not isinstance(p, ParsingExpression):  # Grammar
    p = Ref(p.start().name, p)
  return getattr(p, f)()


def collect_amb(s, pos, result):
  is_first = True
  for result_pos, r in result.items():
    if r == None:
      r = ParseTree("", s, pos, result_pos, None)
    if is_first:
      prev = TreeLink("", r, None)
      is_first = False
    else:
      prev = TreeLink("", r, prev)
  return prev


def generate_gparser(f, conv=None):
  def parse(inputs, urn='(unknown)', pos=0, epos=None):
    if u.issrc(inputs):
      urn, inputs, spos, epos = u.decsrc(inputs)
      pos = spos + pos
    else:
      #if isByte:
      #    inputs = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
      if epos is None:
        epos = len(inputs)
    px = GParserContext(inputs, urn, pos, epos)
    if not f(px):
      return ParseTree("err", px.inputs, px.headpos, epos, None)
    elif len(px.pos2ast) == 1:
      (result_pos, result_ast) = list(px.pos2ast.items())[0]
      if result_ast == None:
        return ParseTree("", px.inputs, pos, result_pos, None)
      else:
        return result_ast
    return ParseTree("?", px.inputs, pos, max(px.pos2ast.keys()), collect_amb(px.inputs, pos, px.pos2ast))
  return parse
