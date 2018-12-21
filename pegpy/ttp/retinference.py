from pegpy.ttp.ret import RETEmpty, RETString, RETSeq, RETUnion, RETRep, RETLabel, RETVar
from pegpy.ttp.ttpexpr import Fold, exp_transer
from pegpy.expression import ParsingExpression, Empty, Any, Char, Range, Seq, Ore, Alt, Not, And, Many, Many1, TreeAs, LinkAs, Detree, State, Ref
from functools import reduce


def inference(p, f = 'retinference'):
    setting(f)
    type_set = E()
    generate(p, f)(type_set)
    return type_set


def generate(p, f = 'retinference'):
    if not isinstance(p, ParsingExpression):  # Grammar
        print(p.rules)
        p.forEachRule(exp_transer)
        p = Ref(p.start().name, p)
    elif isinstance(p, Ref):
      p.peg.forEachRule(exp_transer)
    else:
      p = exp_transer(p)
    return getattr(p, f)()


class E(object):
  __slots__ = ["vars", "suffix"]

  def __init__(self):
    self.vars = {}
    self.suffix = 0
  
  def add(self, name, inner):
    self.vars[name] = inner
  
  def new_name(self):
    self.suffix += 1
    return 'X' + str(self.suffix)
  
  def __str__(self):
    s = "E = {"
    first = True
    for name, inner in self.vars.items():
      if not first:
        s += ', '
      else:
        first = False
      s += "type " + name + ' = ' + str(inner)
    s += "}"
    return s


def Tempty():
  def curry(type_set):
    return RETEmpty()
  return curry


def Tstring():
  def curry(type_set):
    return RETString()
  return curry


def concat(left, right):
  if isinstance(left, RETEmpty):
    return right
  if isinstance(left, RETEmpty):
    return right
  if isinstance(left, RETString) and isinstance(right, RETString):
    return RETString()
  if isinstance(left, RETSeq):
    concated = concat(left.right, right)
    left = left.left
    return RETSeq(left, concated)
  if isinstance(right, RETSeq):
    concated = concat(left, right.left)
    right = right.right
    return RETSeq(concated, right)
  return RETSeq(left, right)


def Tseq2(e1, e2):
  def curry(type_set):
    return concat(e1(type_set), e2(type_set))
  return curry


def Tseq(es):
  def curry(type_set):
    return reduce(lambda acc, val: concat(acc(type_set), val(type_set)) if acc == es[0] else concat(acc, val(type_set)), es)
  return curry


def emit_TSeq(pe, emit):
    ls = tuple(map(emit, pe.flatten([])))
    if len(ls) == 2:
        return Tseq2(ls[0], ls[1])
    return Tseq(ls)


def Tore2(e1, e2):
  def curry(type_set):
    left = e1(type_set)
    right = e2(type_set)
    return RETUnion(left, right)
  return curry


def Tore(es):
  def curry(type_set):
    return reduce(lambda acc, val: RETUnion(acc, val(type_set)) if acc else val(type_set), es)
  return curry


def emit_TOre(pe, emit):
  ls = tuple(map(emit, pe.flatten([])))
  if len(ls) == 2:
      return Tore2(ls[0], ls[1])
  return Tore(ls)


def Tmany(e):
  def curry(type_set):
    inner = e(type_set)
    return RETRep(inner)
  return curry


def emit_TMany(pe, emit):
  return Tmany(emit(pe.inner))


def emit_TMany1(pe, emit):
  return Tseq2(emit(pe.inner), Tmany(emit(pe.inner)))


def Ttreeas(label, pe):
  def carry(type_set):
    inner = pe(type_set)
    return RETLabel(label, inner)
  return carry


def emit_TTreeAs(pe, emit):
  return Ttreeas(pe.name, emit(pe.inner))


def Tlinkas(pe):
  def curry(type_set):
    return pe(type_set)
  return curry


def emit_TLinkAs(pe, emit):
  return Tlinkas(emit(pe.inner))


def Tfold(label, e1, e2):
  def curry(type_set):
    left = e1(type_set)
    right = e2(type_set)
    name = type_set.new_name()
    inner = RETUnion( RETLabel(label, RETSeq(RETVar(name), right)), left)
    type_set.add(name, inner)
    return RETVar(name)
  return curry


def emit_TFold(pe, emit):
  return Tfold(pe.name ,emit(pe.e1), emit(pe.e2))


def emit_TRef(pe, memo, emit):
  def curry(type_set):
    key = pe.uname()
    if not key in memo:
      name = type_set.new_name()
      memo[key] = RETVar(name)
      inner = emit(pe.deref())(type_set)
      type_set.add(name, inner)
    return memo[key]
  return curry


def setting(f = 'retinference'):

  def emit(pe): return getattr(pe, f)()
  setattr(Empty, f, lambda self: Tempty())
  setattr(Any, f, lambda self: Tstring())
  setattr(Char, f, lambda self: Tstring())
  setattr(Range, f, lambda self: Tstring())

  setattr(Seq, f, lambda pe: emit_TSeq(pe, emit))
  setattr(Ore, f, lambda pe: emit_TOre(pe, emit))
  setattr(Alt, f, lambda pe: emit_TOre(pe, emit))
  setattr(Not, f, lambda self: Tempty())
  setattr(And, f, lambda self: Tempty())
  setattr(Many, f, lambda pe: emit_TMany(pe, emit))
  setattr(Many1, f, lambda pe: emit_TMany1(pe, emit))

  setattr(TreeAs, f, lambda pe: emit_TTreeAs(pe, emit))
  setattr(LinkAs, f, lambda pe: emit_TLinkAs(pe, emit))
  setattr(Fold, f, lambda pe: emit_TFold(pe, emit))
  setattr(Detree, f, lambda self: Tempty())

  memo = {}
  # Ref
  setattr(Ref, f, lambda pe: emit_TRef(pe, memo, emit))
