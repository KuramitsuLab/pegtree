

class Shape(object):
  pass


class NullableShape(Shape):
  pass


class NonNullableShape(Shape):
  pass


class Array(NullableShape):
  __slots__ = ['s']

  def __init__(self, s:NullableShape):
    self.s = s
  

  def __str__(self):
    return str(self.s) + '[]'


class Nullable(NullableShape):
  __slots__ = ['s']

  def __init__(self, s: NonNullableShape):
    self.s = s

  def __str__(self):
    return f'nullable<{str(self.s)}>'


class Null(NullableShape):
  
  def __str__(self):
    return 'null'


class Record(NonNullableShape):
  __slots__ = ['b']

  def __init__(self, b):
    self.b = b

  
  def __str__(self):
    st = '{'
    f = True
    for l, s in self.b.items():
      if f:
        f = False
        st += f'{l} = {s}'
        continue
      st += f', {l} = {s}'
    return st + '}'


class Common(NonNullableShape):
  __slots__ = ['b']

  def __init__(self, l, r):
    self.b = [l, r]

  def __str__(self):
    st = ''
    f = True
    for s in self.b:
      if f:
        f = False
        st += f'{s}'
        continue
      st += f' | {s}'
    return st


class Value(NonNullableShape):

  def __str__(self):
    return 'value'


class Error(Exception):

  def __init__(self):
    self.message = "error"

  def __str__(self):
    return self.message


class Variable(NonNullableShape):
  __slots__ = ['X']

  def __init__(self, X:str):
    self.X = X
  

  def __str__(self):
    return self.X
