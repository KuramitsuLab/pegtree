from pegpy.ttp.tree_types import String, KeyValue, Tuple, List, Union, Option, Variable, Error


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


def TSeq(pe1, pe2, emit):
  return TSeqFunc(emit(pe1), emit(pe2))


def TOreFunc(tf1, tf2):
  def curry(env):
    tau1, tau2 = tf1(env), tf2(env)
    if isinstance(tau1, String) and isinstance(tau2, String):
      return tau2
    if isinstance(tau1, Variable) and isinstance(tau2, Variable):
      return Union([tau1, tau2])
    if isinstance(tau1, KeyValue) and isinstance(tau2, KeyValue):
      # TODO: Option
      tau1.inner.update(tau2.inner)
      return tau1
    return Error(f'Inference Error ocurred in TOre({tau1}, {tau2})')
  return curry


def TOre(pe1, pe2, emit):
  return TOreFunc(emit(pe1), emit(pe2))


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
  return TNodeFunc(pe.label, emit(pe))


def TEdgeFunc(elabel, tf):
  def curry(env):
    return KeyValue({elabel: tf(env)})
  return curry


def TEdge(pe, emit):
  return TEdgeFunc(pe.label, emit(pe))


def TAbs():
  return lambda _: String()
