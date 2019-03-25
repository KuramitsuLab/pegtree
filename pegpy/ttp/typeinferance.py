from pegpy.ttp.tree_types import String, KeyValue, Tuple, List, Union, Option, Variable, Error, Rec


class Env(object):

  __slots__ = ['E', 'Gamma']

  def __init__(self):
    self.E = {}
    self.Gamma = {}


def TEmpty():
  return lambda: String()


def TNt(nonterm, pf):
  def curry(env):
    if not (nonterm in env.E):
      env.E[nonterm] = Rec()
      tau = pf(env)
      if isinstance(tau, Rec):
        # TODO: env.E[nonterm] =
        env.E[nonterm] = pf(env)
      else:
        env.E[nonterm] = tau
    elif isinstance(env.E[nonterm], Rec):

    return env.E[nonterm]
  return curry


def TSeq(pf1, pf2):
  def curry(env):
    tau1, tau2 = pf1(env), pf2(env)
    if isinstance(tau1, String) or isinstance(tau2, List):
      return tau2
    if isinstance(tau2, String) or isinstance(tau1, List):
      return tau1
    if isinstance(tau1, KeyValue) and isinstance(tau2, KeyValue):
      # TODO: L1 != L2
      tau1.inner.update(tau2.inner)
      return tau1
    if isinstance(tau1, Node) and isinstance(tau2, Node):
      return Tuple([tau1, tau2])
    return Error(f'Inference Error ocurred in TSeq({tau1}, {tau2})')
  return curry


def TAnd(pf):
  return lambda env: pf(env)


def TNRep(pf):
  return lambda env: List(pf(env))


def TNode(nlabel, pf):
  def curry(env):
    if not (nlabel in env.Gamma):
      env.Gamma[nlabel] = pf(env)
    return Variable(nlabel)
  return curry


def TEdge(elabel, pf):
  return lambda env: KeyValue({elabel: pf(env)}) 
