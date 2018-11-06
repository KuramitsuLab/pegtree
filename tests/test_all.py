import unittest
from test_gpeg import TestGPEG
from test_npeg import TestNPEG

def suite():
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(TestGPEG))
  suite.addTests(unittest.makeSuite(TestNPEG))
  return suite
