import unittest

from pegpy.peg import nez, Grammar
import pegpy.expression as pe

def exTest(self, grammar, combinator=nez):

  p = {}

  for testcase in grammar.examples:
      name, input, output = testcase
      if not name in p:
          p[name] = combinator(pe.Ref(name, grammar))
      res = p[name](input)
      t = str(res).replace(" b'", " '")
      with self.subTest(example=name):
          if output == None:
              self.assertNotEqual(res, 'err')
          else:
              self.assertEqual(t, output)
  return


unittest.TestCase.exTest = exTest
