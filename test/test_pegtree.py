import unittest
#import tests
from pegtree import grammar, generate, ParseTree


class TestPEGTree(unittest.TestCase):

    def test_int(self):
        peg = grammar("math.tpeg")
        parser = generate(peg)
        tree = parser('1+')
        self.assertEqual(str(tree), '1')
        self.assertEqual(repr(tree), "[#Int '1']")

    def test_math(self):
        peg = grammar("math.tpeg")
        parser = generate(peg)
        tree = parser('1+2*3')
        self.assertEqual(str(tree), '1+2*3')
        self.assertEqual(
            repr(tree), "[#Add [#Int '1'][#Mul [#Int '2'][#Int '3']]]")
        tree = parser('1*2+3')
        self.assertEqual(str(tree), '1*2+3')
        self.assertEqual(
            repr(tree), "[#Add [#Mul [#Int '1'][#Int '2']][#Int '3']]")


if __name__ == '__main__':
    unittest.main()
