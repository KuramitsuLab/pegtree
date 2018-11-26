from pegpy.ttp.ttpexpr import Fold, exp_transer
from pegpy.expression import ParsingExpression, Empty, Any, Char, Range, Seq, Ore, Alt, Not, And, Many, Many1, TreeAs, LinkAs, Detree, State, Ref
from pegpy.ttp.shape import SRecode, SArray, SOption, SCommon, SVariable, SString, SBranchList, SEmpty


def Sempty():
  def curry(type_set):
    return SEmpty()
  return curry


def Sstring():
  def curry(type_set):
    return SString()
  return curry


def concat(left, right):
  pass


def emit_SSeq(pe, emit):
  return concat(emit(pe.left), emit(pe.right))


def union(left, right):
  pass


def emit_SOre(pe, emit):
  return union(emit(pe.left), emit(pe.right))


def Smany(s):
  return SArray(s)


def emit_SMany(pe, emit):
  return Smany(emit(pe.inner))


def emit_SMany1(pe, emit):
  return Smany(emit(pe.inner))


def emit_STreeAs(pe, emit):
  pass


def emit_SLinkAs(pe, emit):
  pass


def emit_SFold(pe, emit):
  pass


def emit_SRef(pe, memo, emit):
  def curry(type_set):
    key = pe.uname()
    if not key in memo:
      memo[key] = SVariable(key)
      inner = emit(pe.deref())(type_set)
      type_set.add(key, inner)
    return memo[key]
  return curry


def setting(f = 'shapeinference'):

  def emit(pe): return getattr(pe, f)()
  setattr(Empty, f, lambda self: Sempty())
  setattr(Any, f, lambda self: Sstring())
  setattr(Char, f, lambda self: Sstring())
  setattr(Range, f, lambda self: Sstring())

  setattr(Seq, f, lambda pe: emit_SSeq(pe, emit))
  setattr(Ore, f, lambda pe: emit_SOre(pe, emit))
  setattr(Alt, f, lambda pe: emit_SOre(pe, emit))
  setattr(Not, f, lambda self: Sempty())
  setattr(And, f, lambda self: Sempty())
  setattr(Many, f, lambda pe: emit_SMany(pe, emit))
  setattr(Many1, f, lambda pe: emit_SMany1(pe, emit))

  setattr(TreeAs, f, lambda pe: emit_STreeAs(pe, emit))
  setattr(LinkAs, f, lambda pe: emit_SLinkAs(pe, emit))
  setattr(Fold, f, lambda pe: emit_SFold(pe, emit))
  setattr(Detree, f, lambda self: Sempty())

  memo = {}
  # Ref
  setattr(Ref, f, lambda pe: emit_SRef(pe, memo, emit))