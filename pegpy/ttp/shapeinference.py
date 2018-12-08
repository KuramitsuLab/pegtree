from pegpy.ttp.ttpexpr import Fold, exp_transer
from pegpy.expression import ParsingExpression, Empty, Any, Char, Range, Seq, Ore, Alt, Not, And, Many, Many1, TreeAs, LinkAs, Detree, State, Ref
from pegpy.ttp.shape import Array, Nullable, Null, Record, Common, Value, Variable, Error, NullableShape, NonNullableShape


def inference(p, f='shapeinference', l='link'):
    setting(f, l)
    env= Env()
    generate(p, f, l)(env)
    return env


def generate(p, f='retinference', l='link'):
    if not isinstance(p, ParsingExpression):  # Grammar
        p.map(exp_transer)
        p = Ref(p.start().name, p)
    elif isinstance(p, Ref):
      p.peg.map(exp_transer)
    else:
      p = exp_transer(p)
    return getattr(p, f, l)()


class Env(object):

  __slots__ = ['vars']

  def __init__(self):
    self.vars = {}
  
  
  def append(self, name, record):
    self.vars[name] = record
  

  def __str__(self):
    s = 'Env = {\n'
    for l, r in self.vars.items():
      s += f' {l}: {str(r)}\n'
    return s + '}'


def Sempty():
  def curry(env):
    return Null()
  return curry


def Sstring():
  def curry(env):
    return Value()
  return curry


def exisinstance(lobj, robj, lclass, rclass):
  return (isinstance(lobj, lclass) and isinstance(robj, rclass)) or (isinstance(robj, lclass) and isinstance(lobj, rclass))


def concat(l, r):
  if exisinstance(l, r, Null, NonNullableShape):
    return Null()
  if isinstance(l, Null) and isinstance(r, NonNullableShape):
    return r
  if isinstance(l, NonNullableShape) and isinstance(r, Null):
    return l
  if exisinstance(l, r, Value, Value):
    return Value()
  return Error()



def Sseq(left, right):
  def curry(env):
    return concat(left(env), right(env))
  return curry


def emit_SSeq(pe, emit):
  return Sseq(emit(pe.left), emit(pe.right))


def union(l, r):
  if exisinstance(l, r, Null, NonNullableShape):
    return Null()
  if isinstance(l, Null) and isinstance(r, NonNullableShape):
    return Nullable(r)
  if isinstance(l, NonNullableShape) and isinstance(r, Null):
    return Nullable(l)
  if isinstance(l, Error) or isinstance(r, Error):
    return Error()
  return Common(l, r)


def Sore(left, right):
  def curry(env):
    return union(left(env), right(env))
  return curry


def emit_SOre(pe, emit):
  return Sore(emit(pe.left), emit(pe.right))


def Smany(pf):
  def curry(env):
    return Array(pf(env))
  return curry


def emit_SMany(pe, emit):
  return Smany(emit(pe.inner))


def emit_SMany1(pe, emit):
  return Smany(emit(pe.inner))


def Stree(label, xi):
  def curry(env):
    if not label in env.vars:
      env.append(label, Variable(label))
      env.vars[label] = Record(xi(env))
    return Variable(label)
  return curry


def Sleaf(pf):
  def curry(env):
    return pf(env)
  return curry


def emit_STreeAs(pe, emit, xiemit):
  if pe.name == '':
    return Sleaf(emit(pe.inner))
  return Stree(pe.name, xiemit(pe.inner))


def emit_SLinkAs(pe, emit):
  pass


def Sfold(pf1, left, pf2, label):
  def curry(env):
    s = pf1(env)
    if not label in env.vars:
      env.append(label, Variable(label))
      xi = {left: union(Variable(label), s)}
      xi.update(pf2(env))
      env.vars[label] = Record(xi)
    return union(Variable(label), s)
  return curry


def emit_SFold(pe, emit, xiemit):
  return Sfold(emit(pe.e1), pe.left, xiemit(pe.e2), pe.name)


def emit_SRef(pe, memo, emit):
  def curry(env):
    key = pe.uname()
    if not key in memo:
      inner = emit(pe.deref())(env)
      memo[key] = inner
    return memo[key]
  return curry


def Lseq(left, right):
  def curry(env):
    l = left(env)
    l.update(right(env))
    return l
  return curry


def xiemit_LSeq(pe, xiemit):
  return Lseq(xiemit(pe.left), xiemit(pe.right))


def Llink(tag, pf):
  def curry(env):
    return {tag: pf(env)}
  return curry


def xiemit_LLinkAs(pe, emit):
  return Llink(pe.name, emit(pe.inner))


def Labsorb():
  def curry(env):
    return {}
  return curry


def setting(f = 'shapeinference', l = 'link'):

  def emit(pe): return getattr(pe, f)()

  def xiemit(pe): return getattr(pe, l)()
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

  setattr(TreeAs, f, lambda pe: emit_STreeAs(pe, emit, xiemit))
  setattr(LinkAs, f, lambda pe: emit_SLinkAs(pe, emit))
  setattr(Fold, f, lambda pe: emit_SFold(pe, emit, xiemit))
  setattr(Detree, f, lambda self: Sempty())

  memo = {}
  # Ref
  setattr(Ref, f, lambda pe: emit_SRef(pe, memo, emit))

  setattr(Empty, l, lambda self: Labsorb())
  setattr(Any, l, lambda self: Labsorb())
  setattr(Char, l, lambda self: Labsorb())
  setattr(Range, l, lambda self: Labsorb())

  setattr(Seq, l, lambda pe: xiemit_LSeq(pe, xiemit))
  setattr(Ore, l, lambda self: Labsorb())
  setattr(Alt, l, lambda self: Labsorb())
  setattr(Not, l, lambda self: Labsorb())
  setattr(And, l, lambda self: Labsorb())
  setattr(Many, l, lambda self: Labsorb())
  setattr(Many1, l, lambda self: Labsorb())

  setattr(TreeAs, l, lambda self: Labsorb())
  setattr(LinkAs, l, lambda pe: xiemit_LLinkAs(pe, emit))
  setattr(Fold, l, lambda self: Labsorb())
  setattr(Detree, l, lambda self: Labsorb())
  setattr(Ref, l, lambda self: Labsorb())
