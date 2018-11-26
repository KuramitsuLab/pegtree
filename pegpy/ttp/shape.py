

class Shape(object):
  pass


class HasTreeShape(Shape):
  pass


class SBranchList(HasTreeShape):
  __slots__ = ['inners']

  def __init__(self, inners):
    self.inners = inners
  
  def __str__(self):
    s = '{'
    first = True
    for key, val in self.inners.items():
      if not first:
        s += ', '
      s += key + ' -> ' + str(val)
    return s + '}'


class SRecode(HasTreeShape):
  __slots__ = ['tag', 'branch_list']

  def __init__(self, tag, branch_list):
    self.tag = tag
    self.branch_list = branch_list
  
  def __str__(self):
    return self.tag + str(self.branch_list)


class SArray(Shape):
  __slots__ = ['inner']

  def __init__(self, inner):
    self.inner = inner
  
  def __str__(self):
    return str(self.inner) + '[]'


class SOption(Shape):
  __slots__ = ['inner']

  def __init__(self, inner):
    self.inner = inner
  
  def __str__(self):
    return 'Option<' + str(self.inner) + '>'


class SCommon(Shape):
  __slots__ = ['inners']

  def __init__(self, inners):
    self.inners = inners
  
  def __str__(self):
    s = ''
    first = True
    for inner in self.inners:
      if not first:
        s += ' | '
      s += str(inner)
      first = False
    return s


class Value(HasTreeShape):
  __slots__ = ['name', 'inner']

  def __init__(self, name, inner):
    self.inner = inner
    self.name = name

  def __str__(self):
    return self.name + ': ' + self.inner


class SVariable(Shape):
  __slots__ = ['name']

  def __init__(self, name):
    self.name = name
  
  def __str__(self):
    return self.name


class SString(Shape):
  
  def __str__(self):
    return 'String'


class SEmpty(Shape):
  
  def __str__(self):
    return 'Empty'

