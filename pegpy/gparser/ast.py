import cython


@cython.cclass
class Tree:
  tag: object
  inputs: cython.p_char
  spos: cython.int
  epos: cython.int
  child: object

  def __init__(self, tag: object, inputs: cython.p_char, spos: cython.int, epos: cython.int, child: object):
    self.tag = tag
    self.inputs = inputs
    self.spos = spos
    self.epos = epos
    self.child = child
  
  def __str__(self):
    if self.child:
      return f'[#{self.tag} {str(self.child)}]'
    else:
      return str(self.inputs[self.spos:self.epos])


@cython.cclass
class Link:
  inner: object
  prev: object

  def __init__(self, inner: object, prev: object):
    self.inner = inner
    self.prev = prev

  def __str__(self):
    sb = self.strOut([])
    return ''.join(sb)

  def strOut(self, sb):
    if self.prev:
      sb = self.prev.strOut(sb)
    sb.append(str(self.inner))
    return sb

