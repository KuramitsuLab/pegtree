import unittest
import tests
from pegpy.gparser.cython_gpeg import cgpeg
from pegpy.tpeg import grammar
from pathlib import Path

class TestCythonGPEG(unittest.TestCase):

  def test_exps(self):
    test_grammar = grammar('gpeg_grammar_test.gpeg')
    self.exTest(test_grammar, cgpeg)

if __name__ == '__main__':
  unittest.main()
