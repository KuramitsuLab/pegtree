

class RET(object):
  pass


class RETEmpty(RET):
  
  def __str__(self):
    return 'Empty'


class RETString(RET):

  def __str__(self):
    return 'String'


class RETSeq(RET):
  __slots__ = ['left', 'right']

  def __init__(self, left: RET, right: RET):
    self.left = left
    self.right = right
  
  def __str__(self):
    return str(self.left) + ', ' + str(self.right)


class RETUnion(RET):
  __slots__ = ['left', 'right']

  def __init__(self, left: RET, right: RET):
    self.left = left
    self.right = right
  
  def __str__(self):
    return str(self.left) + ' | ' + str(self.right)


class RETRep(RET):
  __slots__ = ['inner']

  def __init__(self, inner: RET):
    self.inner = inner
  
  def __str__(self):
    return str(self.inner) + '*'


class RETLabel(RET):
  __slots__ = ['label', 'inner']

  def __init__(self, label: str, inner: RET):
    self.label = label
    self.inner = inner
  
  def __str__(self):
    return self.label + '[' + str(self.inner) + ']'


class RETVar(RET):
  __slots__ = ['name']

  def __init__(self, name: str):
    self.name = name
  
  def __str__(self):
    return self.name