from pegpy.ttp.ret import RETEmpty, RETSeq, RETUnion, RETRep, RETLabel, RETVar
from pegpy.expression import ParsingExpression, Empty, Any, Char, Range, Seq, Ore, Alt, Not, And, Many, Many1, TreeAs, LinkAs, FoldAs, Detree, State, Ref
from functools import reduce


def inference(p):
    setting()
    type_set = E()
    generate(p)(E())
    return type_set


def generate(p):
    if not isinstance(p, ParsingExpression):  # Grammar
        p = Ref(p.start().name, p)
    return getattr(p, 'inference')()


class E(object):
  __slots__ = ["vars"]

  def __init__(self):
    self.vars = {}
  
  def add(self, name, inner):
    self.vars[name] = inner
  
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
    return RETEmpty
  return curry


def Tseq2(e1, e2):
  def curry(type_set):
    left = e1(type_set)
    right = e2(type_set)
    return RETSeq(left, right)
  return curry


def Tseq(es):
  def curry(type_set):
    return reduce(lambda acc, val: RETSeq(acc, val(type_set)) if acc else val(type_set), es)
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
  def carry(type_set):
    inner = e(type_set)
    return RETRep(inner)
  return carry


def emit_TMany(pe, emit):
  return Tmany(emit(pe.inner))


def emit_TMany1(pe, emit):
  return Tseq2(emit(pe.inner), Tmany(emit(pe.inner)))


def Ttreeas(label, e):
  def carry(type_set):
    inner = e(type_set)
    return RETLabel(label, inner)
  return carry


def emit_TTreeAs(pe, emit):
  return Ttreeas(pe.name, emit(pe.inner))


def Tlinkas(e):
  def carry(type_set):
    return e(type_set)
  return carry


def emit_TLinkAs(pe, emit):
  return Tlinkas(emit(pe.inner))


def Tfoldas(label, e, suffix):
  def carry(type_set):
    right = e(type_set)
    suffix[0] += 1
    name = 'X' + str(suffix[0])
    inner = RETLabel(label, RETSeq(RETVar(name), right))
    type_set.add(name, inner)
    return RETVar(name)
  return carry


def emit_TFoldAs(pe, suffix, emit):
  return Tfoldas(pe.name, emit(pe.inner), suffix)


def Tref(suffix, e):
  def carry(type_set):
    inner = e(type_set)
    suffix[0] += 1
    name = 'X' + str(suffix[0])
    type_set.add(name, inner)
    return RETVar(name)
  return carry


def emit_TRef(pe, suffix, emit):
  return Tref(suffix, emit(pe.deref()))


def setting():

  suffix = [0]

  def emit(pe): return getattr(pe, 'inference')()
  setattr(Empty, "inference", lambda self: Tempty())
  setattr(Any, "inference", lambda self: Tempty())
  setattr(Char, "inference", lambda self: Tempty())
  setattr(Range, "inference", lambda self: Tempty())

  setattr(Seq, "inference", lambda pe: emit_TSeq(pe, emit))
  setattr(Ore, "inference", lambda pe: emit_TOre(pe, emit))
  setattr(Alt, "inference", lambda pe: emit_TOre(pe, emit))
  setattr(Not, "inference", lambda self: Tempty())
  setattr(And, "inference", lambda self: Tempty())
  setattr(Many, "inference", lambda pe: emit_TMany(pe, emit))
  setattr(Many1, "inference", lambda pe: emit_TMany1(pe, emit))

  setattr(TreeAs, "inference", lambda pe: emit_TTreeAs(pe, emit))
  setattr(LinkAs, "inference", lambda pe: emit_TLinkAs(pe, emit))
  setattr(FoldAs, "inference", lambda pe: emit_TFoldAs(pe, suffix, emit))
  setattr(Detree, "inference", lambda self: Tempty())

  # Ref
  setattr(Ref, "inference", lambda pe: emit_TRef(pe, suffix, emit))
