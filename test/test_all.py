import unittest
#from test_pegtree import TestTPEG
from test.test_pegtree import TestPEGTree
from test.test_pasm import TestPAsm
from test.test_main import TestMain
from test.test_peg import TestPeg


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestPAsm))
    suite.addTests(unittest.makeSuite(TestPeg))
    suite.addTests(unittest.makeSuite(TestPEGTree))
    suite.addTests(unittest.makeSuite(TestMain))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
