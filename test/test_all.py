import unittest
from test_gpeg import TestGPEG
from test_tpeg import TestTPEG

def suite():
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(TestGPEG))
  suite.addTests(unittest.makeSuite(TestTPEG))
  return suite
