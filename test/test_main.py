import unittest
#import tests
from pegtree.main import main


class TestMain(unittest.TestCase):

    def test_peg(self):
        print('pegtree peg -g math.tpeg')
        main(['', 'peg', '-g', 'math.tpeg'])

    def test_pasm0(self):
        print('pegtree pasm0 -g math.tpeg')
        main(['', 'pasm0', '-g', 'math.tpeg'])


if __name__ == '__main__':
    unittest.main()
