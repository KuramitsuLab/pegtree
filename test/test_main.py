import unittest
#import tests
from pegtree.main import main


class TestMain(unittest.TestCase):

    def test_sample(self):
        print('pegtree sample')
        main(['', 'sample'])

    def test_example(self):
        print('pegtree sample')
        main(['', 'example', '-g', 'math.pegtree'])

    def test_peg(self):
        print('pegtree peg -g math.tpeg')
        main(['', 'peg', '-g', 'math.tpeg'])

    def test_pasm(self):
        print('pegtree pasm -g math.tpeg')
        main(['', 'pasm', '-g', 'math.tpeg'])


if __name__ == '__main__':
    unittest.main()
