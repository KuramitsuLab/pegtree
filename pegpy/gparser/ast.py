import cython


@cython.cclass
class Tree:
  tag = cython.declare(cython.p_char, visibility='public')
  inputs = cython.declare(cython.p_char, visibility='public')
  spos = cython.declare(cython.int, visibility='public')
  epos = cython.declare(cython.int, visibility='public')
  child = cython.declare(object, visibility='public')

  def __init__(self, tag: cython.p_char, inputs: cython.p_char, spos: cython.int, epos: cython.int, child: object):
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
  inner = cython.declare(object, visibility='public')
  prev = cython.declare(object, visibility='public')

  def __init__(self, inner: object, prev: object):
    self.inner = inner
    self.prev = prev

  def __str__(self):
    sb = self.strOut([])
    return ''.join(sb)

  def strOut(self, sb):
    if self.prev:
      sb = self.prev.strOut(sb)
    return sb.append(str(self.inner))

