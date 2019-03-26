

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
    if isinstance(self.s, Common):
      return f'({self.s})[]'
    return str(self.s) + '[]'

  def __eq__(self, other):
    if not isinstance(other, Array):
      return False
    return self.s == other.s


class Nullable(NullableShape):
  __slots__ = ['s']

  def __init__(self, s: NonNullableShape):
    self.s = s

  def __str__(self):
    return f'nullable<{str(self.s)}>'

  def __eq__(self, other):
    if not isinstance(other, Nullable):
      return False
    return self.s == other.s


class Null(NullableShape):
  
  def __str__(self):
    return 'null'

  def __eq__(self, other):
    return isinstance(other, Null)


class Record(NonNullableShape):
  __slots__ = ['b']

  def __init__(self, b):
    self.b = b
  
  
  def map(self, f):
    b = {}
    for l, s in self.b.items():
      b[l] = f(s)
    return b


  def __str__(self):
    st = '{'
    f = True
    if isinstance(self.b, Error):
      return self.b.message
    for l, s in self.b.items():
      if f:
        f = False
        st += f'{l} = {s}'
        continue
      st += f', {l} = {s}'
    return st + '}'
  
  def __eq__(self, other):
    if not isinstance(other, Record):
      return False
    return self.b == other.b


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
  
  def map(self, f):
    return list(map(lambda x: f(x), self.b))

  def push(self, s):
    for belem in self.b:
      if s == belem:
        return
    self.b.append(s)

  def get_name(self):
    return ''.join(map(lambda s: s.X.capitalize(), self.b))
  
  def __eq__(self, other):
    if not isinstance(other, Common):
      return False
    for elem in self.b:
      if not (elem in other.b):
        return False
    return True
        


class Value(NonNullableShape):

  def __str__(self):
    return 'value'
  
  def __eq__(self, other):
    return isinstance(other, Value)


class Error(Exception):

  def __init__(self, message='error'):
    self.message = message

  def __str__(self):
    return self.message
  
  def __eq__(self, other):
    return isinstance(other, Error)


class Variable(NonNullableShape):
  __slots__ = ['X']

  def __init__(self, X:str):
    self.X = X
  
  def __str__(self):
    return self.X

  def __eq__(self, other):
    if not isinstance(other, Variable):
      return False
    return self.X == other.X
