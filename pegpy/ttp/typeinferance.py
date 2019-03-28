from pegpy.ttp.tree_types import String, KeyValue, Tuple, List, Union, Option, Variable, Error
from pegpy.expression import ParsingExpression, Empty, Any, Char, Range, Seq, Ore, Alt, Not, And, Many, Many1, TreeAs, LinkAs, Detree, State, Ref
from pegpy.ttp.ttpexpr import Fold, exp_transer

class Env(object):

  __slots__ = ['E', 'Gamma']

  def __init__(self):
    self.E = {}
    self.Gamma = {}


def TEmpty():
  return lambda _: String()


def TChar():
  return lambda _: String()


def TValue():
  return lambda _: String()


def TNtFunc(nonterm, tf):
  def curry(env):
    if not (nonterm in env.Gamma):
      env.Gamma[nonterm] = Variable(nonterm)
      env.E[nonterm] = tf(env)
    return env.Gamma[nonterm]
  return curry


def TNt(pe, emit):
  return TNtFunc(pe.uname(), emit(pe.deref()))


def TSeqFunc(tf1, tf2):
  def curry(env):
    tau1, tau2 = tf1(env), tf2(env)
    if isinstance(tau1, String):
      return tau2
    if isinstance(tau2, String):
      return tau1
    if isinstance(tau1, List) and isinstance(tau1.inner, type(tau2)):
      return tau1
    if isinstance(tau2, List) and isinstance(tau2.inner, type(tau1)):
      return tau2
    if isinstance(tau1, List) and isinstance(tau2, List) and isinstance(tau2.inner, type(tau1.inner)):
      return tau1
    if isinstance(tau1, KeyValue) and isinstance(tau2, KeyValue):
      # TODO: L1 != L2
      tau1.inner.update(tau2.inner)
      return tau1
    if isinstance(tau1, Variable) and isinstance(tau2, Variable):
      return Tuple([tau1, tau2])
    return Error(f'Inference Error ocurred in TSeq({tau1}, {tau2})')
  return curry


def TSeq(pe, emit):
  return TSeqFunc(emit(pe.left), emit(pe.right))


def TOreFunc(tf1, tf2):
  def curry(env):
    tau1, tau2 = tf1(env), tf2(env)
    if isinstance(tau1, String) and isinstance(tau2, String):
      return tau2
    if isinstance(tau1, Variable) and isinstance(tau2, Variable):
      return Union([tau1, tau2])
    if isinstance(tau1, KeyValue) and isinstance(tau2, KeyValue):
      tau = dict([(key, Option(val)) for key, val in tau1.items()])
      for key, val in tau2:
        if key in tau:
          # TODO: SubType
          tau[key] = tau[key].inner
        else:
          tau[key] = val
      return tau
    return Error(f'Inference Error ocurred in TOre({tau1}, {tau2})')
  return curry


def TOre(pe, emit):
  return TOreFunc(emit(pe.left), emit(pe.right))


def TAndFunc(tf):
  def curry(env):
    return tf(env)
  return curry


def TAnd(pe, emit):
  return TAndFunc(emit(pe))


def TNot():
  return lambda _: String()


def TRepFunc(tf):
  def curry(env):
    tau = tf(env)
    if isinstance(tau, String):
      return tau
    return List(tau)
  return curry


def TRep(pe, emit):
  return TRepFunc(emit(pe))


def TNodeFunc(nlabel, tf):
  def curry(env):
    if not (nlabel in env.Gamma):
      env.Gamma[nlabel] = Variable(nlabel)
      env.E[nlabel] = Variable(tf(env))
    return env.Gamma[nlabel]
  return curry


def TNode(pe, emit):
  return TNodeFunc(pe.name, emit(pe))


def TEdgeFunc(elabel, tf):
  def curry(env):
    return KeyValue({elabel: tf(env)})
  return curry


def TEdge(pe, emit):
  return TEdgeFunc(pe.name, emit(pe))


def TFoldFunc(tf1, elabel, tf2, nlabel):
  def curry(env):
    tau1, tau2 = tf1(env), tf2(env)
    if elabel == '' and isinstance(tau2, Variable):
      env.E[nlabel] = Union([tau1, Tuple([Variable(nlabel), tau2])])
      return Variable(nlabel)
    elif elabel != '' and isinstance(tau2, KeyValue):
      tau2[elabel] = Variable(nlabel)
      env.E[nlabel] = Union([tau1, tau2])
      return Variable(nlabel)
    return Error(f'Inference Error ocurred in TFord({tau1}, {elabel}, {tau2}, {nlabel})')
  return curry


def TFold(pe, emit):
  return TFoldFunc(emit(pe.e1), pe.left, emit(pe.e2), pe.name)


def TAbs():
  return lambda _: String()


def setting(f='typeinference'):

  def emit(pe): return getattr(pe, f)()
  
  setattr(Empty, f, lambda self: TEmpty())
  setattr(Any, f, lambda self: TChar())
  setattr(Char, f, lambda self: TChar())
  setattr(Range, f, lambda self: TChar())

  setattr(Seq, f, lambda pe: TSeq(pe, emit))
  setattr(Ore, f, lambda pe: TOre(pe, emit))
  setattr(Alt, f, lambda pe: TOre(pe, emit))
  setattr(Not, f, lambda self: TNot())
  setattr(And, f, lambda pe: TAnd(pe, emit))
  setattr(Many, f, lambda pe: TRep(pe, emit))
  setattr(Many1, f, lambda pe: TRep(pe, emit))

  setattr(TreeAs, f, lambda pe: TNode(pe, emit))
  setattr(LinkAs, f, lambda pe: TEdge(pe, emit))
  setattr(Fold, f, lambda pe: TFold(pe, emit))
  setattr(Detree, f, lambda self: TAbs())

  # Ref
  setattr(Ref, f, lambda pe: TNt(pe, emit))
