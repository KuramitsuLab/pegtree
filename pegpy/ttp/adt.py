

class ADT(object):
  __slots__ = ['variant', 'suffix']

  def __init__(self):
    self.variant = {}
    self.suffix = 0
  

  def add(self, name, val):
    self.variant[name] = val
  

  def append(self, ve):
    self.suffix += 1
    self.variant['l' + str(self.suffix)] = ve
  
  def __str__(self):
    s = ''
    first = True
    for key, val in self.variant.items():
      if not first:
        s += ' | '
      first = False
      s += key + ' of ' + str(val)
    return s


class ComposedType(object):
  pass


class ADTEmpty(ComposedType):

  def __str__(self):
    return 'empty'


class ADTString(ComposedType):

  def __str__(self):
    return 'string'


class ADTProduct(ComposedType):
  __slots__ = ['left', 'right']

  def __init__(self, left, right):
    self.left = left
    self.right = right
  
  def __str__(self):
    return str(self.left) + ' * ' + str(self.right)


class ADTList(ComposedType):
  __slots__ = ['inner']

  def __init__(self, inner):
    self.inner = inner
  
  def __str__(self):
    return str(self.inner) + ' list'


class ADTUnit(ComposedType):

  def __str__(self):
    return 'unit'


class ADTVar(ComposedType):
  __slots__ = ['name']

  def __init__(self, name):
    self.name = name
  
  def __str__(self):
    return self.name
