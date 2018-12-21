import pegpy.expression as exp


def exp_transer(e: exp.ParsingExpression):
  e = e.inner
  if isinstance(e, exp.Seq) and isFoldMany(e.right):
    fold = e.right.inner
    return Fold(e.left, fold.left, fold.inner, fold.name)
  if isinstance(e, exp.Seq) and (isinstance(e.right, exp.Ore) or isinstance(e.right, exp.Alt)) and isFoldMany(e.right) and isFoldMany(e.left):
    fold1 = e.right.left.inner
    fold2 = e.right.right.inner
    return exp.Ore(Fold(e.left, fold1.left, fold1.inner, fold1.name), Fold(e.left, fold1.left, fold2.inner, fold2.name))
  return e


def isFoldMany(e: exp.ParsingExpression):
  if (isinstance(e, exp.Many) or isinstance(e, exp.Many1)) and isinstance(e.inner, exp.FoldAs):
    return True
  return False


class Fold(exp.ParsingExpression):
  __slots__ = ['e1', 'left', 'e2', 'name']

  def __init__(self, e1, left, e2, name):
    self.e1 = exp.ParsingExpression.new(e1)
    self.e2 = exp.ParsingExpression.new(e2)
    self.name = name
    self.left = left

  def __str__(self):
    e1 = str(self.e1) 
    prefix = e1 + '(^' if self.left == '' else e1 + '(' + self.left + ':^ '
    tag = ' #' + self.name if self.name != '' else ''
    return prefix + '{ ' + str(self.e2) + tag + ' })*'

'''
test
import pegpy.expression as exp
import pegpy.ttp.ttpexpr as t
e = exp.Seq(exp.Char('a'), exp.Many(exp.FoldAs('', 'AB', exp.Char('b'))))
t.exp_transer(e)
'''
