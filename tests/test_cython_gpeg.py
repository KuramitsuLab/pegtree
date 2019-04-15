import unittest
import tests
from pegpy.gparser.cgpeg import Grammar, cgpeg
from pegpy.expression import ParsingExpression
from pathlib import Path

class TestCythonGPEG(unittest.TestCase):

  def test_exps(self):
    g = Grammar("gpeg_grammar_test")
    g.load('gpeg_grammar_test.gpeg')
    self.exTest(g, cgpeg)

if __name__ == '__main__':
  unittest.main()
