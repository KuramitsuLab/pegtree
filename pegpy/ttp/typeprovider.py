from pegpy.ttp.shape import Array, Nullable, Null, Record, Common, Value, Variable, Error, NullableShape, NonNullableShape


class Formater(object):
  __slots__ = ['array', 'null', 'nullable', 'record', 'common', 'value', 'variable', 'typedef', 'commondef']

  def __init__(self, array, null, nullable, record, common, value, variable, typedef, commondef):
    self.array = array
    self.null = null
    self.nullable = nullable
    self.record = record
    self.common = common
    self.value = value
    self.variable = variable
    self.typedef = typedef
    self.commondef = commondef


def emit_typedef(self):
  def typedef(name, s):
    if self.first:
      setattr(Formater, 'first', False)
      return f'type {name} = {{{s}}}'
    else:
      return f'and {name} = {{{s}}}'
  return typedef


def emit_commondef(self):
  def commondef(name, s):
    if self.first:
      setattr(Formater, 'first', False)
      return f'type {name} = {s}'
    else:
      return f'and {name} = {s}'
  return commondef


def fsharp():
  adt_formater = Formater(
    lambda t: f'{t}[]',
    lambda: f'Nullable<string>',
    lambda t: f'Nullable<{t}>',
    lambda b: '; '.join(map(lambda item: f'{item[0]}: {item[1]}', b.items())),
    lambda name, b: ' | '.join(map(lambda item, name: f'{name}{item[0] + 1} of {item[1]}', enumerate(b), [name for _ in range(0, len(b))])),
    lambda: 'string',
    lambda X: X,
    emit_typedef,
    emit_commondef
  )
  setattr(Formater, 'first', True)
  adt_formater.typedef = adt_formater.typedef(adt_formater)
  adt_formater.commondef = adt_formater.commondef(adt_formater)
  return adt_formater

def emit_python_record(tab):
  def python_record(b):
    args = ', '.join(map(lambda item: f'{item[0]}: {item[1]}', b.items()))
    inits = '\n'.join(map(lambda key: f'{tab}{tab}self.{key} = {key}', b.keys()))
    return f'def __init__(self, {args}):\n{inits}'
  return python_record


def python():
  tab = '  '
  return Formater(
      lambda t: f'list',
      lambda: f'None',
      lambda t: f'{t}',
      emit_python_record(tab),
      lambda name, b: '\n'.join(map(lambda item, name: f'class {name}{item[0] + 1}({name}):\n{tab}def __init__(self, {item[1]}):\n{tab}{tab}self.{item[1]} = {item[1]}\n', enumerate(b), [name for _ in range(0, len(b))])),
      lambda: 'str',
      lambda X: X,
      lambda name, s: f'class {name}(object):\n{tab}{s}',
      lambda name, s: f'class {name}(object):\n{tab}pass\n\n{s}'
  )


def provider(env, f='typeprovider', form=fsharp()):
    setting(form, env.start, f)
    env.variable2source(env.start, generate(env, f)(env), form)
    return env.get_source()


def generate(env, f='typeprovider'):
    return getattr(env.start_shape(), f)()


def ADTarray(s, form):
  def curry(env):
    return form.array(s)
  return curry


def emit_ADTarray(s, emit, form):
  return ADTarray(s.s.emit(), form)


def ADTnull(form):
  def curry(env):
    return form.null()
  return curry


def ADTnullable(s, form):
  def curry(env):
    return form.nullable(s)
  return curry


def emit_ADTnullable(s, emit, form):
  return ADTnullable(s.s.emit(), form)


def ADTrecord(b, form):
  def curry(env):
    return form.record(dict(map(lambda item: (item[0], item[1](env)), b.items())))
  return curry


def emit_ADTrecord(s, emit, form):
  print(s)
  s.map(emit)
  return ADTrecord(s.b, form)


def emit_ADTcommon(s, emit, form, memo):
  key = s.get_name()
  s.map(emit)
  def curry(env):
    if not(key in memo):
      memo[key] = key
      env.common2source(key, form.common(key, list(map(lambda f: f(env), s.b))), form)
    return memo[key]
  return curry


def ADTvalue(form):
  def curry(env):
    return form.value()
  return curry


def emit_ADTVariable(s, emit, form, memo):
  key = s.X
  def curry(env):
    if not(key in memo):
      memo[key] = key
      env.variable2source(key, emit(env.vars[key])(env), form)
    return memo[key]
  return curry


def setting(form, start, f='typeprovider'):

  def emit(pe): return getattr(pe, f)()
  memo = {start: start}
  
  setattr(Array, f, lambda s: emit_ADTarray(s, emit, form))
  setattr(Null, f, lambda self: ADTnull(form))
  setattr(Nullable, f, lambda s: emit_ADTnullable(s, emit, form))
  setattr(Record, f, lambda s: emit_ADTrecord(s, emit, form))
  setattr(Common, f, lambda s: emit_ADTcommon(s, emit, form, memo))
  setattr(Value, f, lambda self: ADTvalue(form))
  setattr(Variable, f, lambda s: emit_ADTVariable(s, emit, form, memo))

