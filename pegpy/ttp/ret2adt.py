from pegpy.ttp.ret import RETEmpty, RETSeq, RETUnion, RETRep, RETLabel, RETVar, RETString
from pegpy.ttp.adt import ADT, ADTEmpty, ADTString, ADTList, ADTVar, ADTProduct
from pegpy.ttp.retinference import E


def ret2adt(type_set, mf='mapping', tf='tau'):
    setting(mf, tf)
    new_type_set = E()
    for ty in type_set.vars.values():
      getattr(ty, tf)()(new_type_set)
    type_set.vars.update(new_type_set.vars)
    return type_set


def Mempty(ret):
  def curry(type_set):
    return ret(type_set)
  return curry


def emit_MEmpty(ret, temit):
  return Mempty(temit(ret))


def Mstring(ret):
  def curry(type_set):
    return ret(type_set)
  return curry


def emit_MString(ret, temit):
  return Mstring(temit(ret))


def Mseq(ret):
  def curry(type_set):
    return ret(type_set)
  return curry


def emit_MSeq(ret, temit):
  return Mseq(temit(ret))



def Munion(lret, rret, lislabel=False, rislabel=False):
  def curry(type_set):
    adt = ADT()
    if lislabel:
      adt.variant.update(lret(type_set).variant)
    else:
      adt.append(lret(type_set))
    if rislabel:
      adt.variant.update(rret(type_set).variant)
    else:
      adt.append(rret(type_set))
    return adt
  return curry


def emit_MUnion(ret, memit, temit):
  lis = isinstance(ret.left, RETLabel)
  ris = isinstance(ret.right, RETLabel)
  if lis and ris:
    return Munion(memit(ret.left), memit(ret.right), lislabel=True, rislabel=True)
  elif lis:
    return Munion(memit(ret.left), temit(ret.right), lislabel=True)
  elif ris:
    return Munion(temit(ret.left), memit(ret.right), rislabel=True)
  else:
    return Munion(temit(ret), temit(ret))


def Mrep(ret):
  def curry(type_set):
    return ret(type_set)
  return curry


def emit_MRep(ret, temit):
  return Mrep(temit(ret))


def Mlabel(label, ret):
  def curry(type_set):
    adt = ADT()
    adt.add(label, ret(type_set))
    return adt
  return curry


def emit_MLabel(ret, temit):
  if isinstance(ret.inner, RETEmpty):
    return Mlabel(ret.label, TEmpty())
  return Mlabel(ret.label, temit(ret.inner))


def Mvar(ret):
  def curry(type_set):
    return ret(type_set)
  return curry


def emit_MVar(ret, temit):
  return Mvar(temit(ret))


def TEmpty():
  def curry(type_set):
    return ADTEmpty()
  return curry


def TString():
  def curry(type_set):
    return ADTString()
  return curry


def Tseq1(ret):
  def curry(type_set):
    return ret(type_set)
  return curry


def Tseq2(lret, rret):
  def curry(type_set):
    return ADTProduct(lret(type_set), rret(type_set))
  return curry


def emit_TSeq(ret, temit):
  if isinstance(ret.left, RETEmpty):
    return Tseq1(temit(ret.right))
  if isinstance(ret.right, RETEmpty):
    return Tseq1(temit(ret.left))
  return Tseq2(temit(ret.left), temit(ret.right))


def emit_TUnion(ret, memit, memo):
  def curry(type_set):
    key = id(ret)
    if not key in memo:
      name = type_set.new_name()
      memo[key] = ADTVar(name)
      type_set.add(name, memit(ret)(type_set))
    return memo[key]
  return curry


def Trep(ret):
  def curry(type_set):
    return ADTList(ret(type_set))
  return curry


def emit_TRep(ret, temit):
  return Trep(temit(ret.inner))


def emit_TLabel(ret, memit, memo):
  def curry(type_set):
    key = id(ret)
    if not key in memo:
      name = type_set.new_name()
      memo[key] = ADTVar(name)
      type_set.add(name, memit(ret)(type_set))
    return memo[key]
  return curry


def emit_TVar(ret):
  def curry(type_set):
    return ADTVar(ret.name)
  return curry


def setting(mf = 'mapping', tf = 'tau'):

  def memit(ret): return getattr(ret, mf)()
  def temit(ret): return getattr(ret, tf)()
  
  setattr(RETEmpty, mf, lambda ret: emit_MEmpty(ret, temit))
  setattr(RETString, mf, lambda ret: emit_MString(ret, temit))
  setattr(RETSeq, mf, lambda ret: emit_MSeq(ret, temit))
  setattr(RETUnion, mf, lambda ret: emit_MUnion(ret, memit, temit))
  setattr(RETRep, mf, lambda ret: emit_MRep(ret, temit))
  setattr(RETLabel, mf, lambda ret: emit_MLabel(ret, temit))
  setattr(RETVar, mf, lambda ret: emit_MVar(ret, temit))
  
  memo = {}
  setattr(RETEmpty, tf, lambda self: TEmpty())
  setattr(RETString, tf, lambda self: TString())
  setattr(RETSeq, tf, lambda ret: emit_TSeq(ret, temit))
  setattr(RETUnion, tf, lambda ret: emit_TUnion(ret, memit, memo))
  setattr(RETRep, tf, lambda ret: emit_TRep(ret, temit))
  setattr(RETLabel, tf, lambda ret: emit_TLabel(ret, memit, memo))
  setattr(RETVar, tf, lambda ret: emit_TVar(ret))

