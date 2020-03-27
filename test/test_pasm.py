import unittest
from pegtree.pasm import *


class TestPAsm(unittest.TestCase):

    def test_Empty(self):
        parser = generate(pChar(''))
        tree = parser('aa')
        self.assertEqual(str(tree), '')
        self.assertEqual(repr(tree), "[# '']")

    def test_Char(self):
        parser = generate(pChar('a'))
        tree = parser('aa')
        self.assertEqual(str(tree), 'a')
        self.assertEqual(repr(tree), "[# 'a']")

    def test_Node(self):
        parser = generate(pNode(pChar('a'), 'A', 0))
        tree = parser('aa')
        self.assertEqual(str(tree), 'a')
        self.assertEqual(repr(tree), "[#A 'a']")

    def test_NestedNode(self):
        parser = generate(pNode(pSeq2(pNode(pChar('a'), 'A', 0),
                                      pNode(pChar('b'), 'B', 0)), "AB", 0))
        tree = parser('ab')
        self.assertEqual(str(tree), 'ab')
        self.assertEqual(repr(tree), "[#AB [#A 'a'][#B 'b']]")

    def test_FoldNode(self):
        parser = generate(pSeq2(pNode(pChar('a'), 'A', 0),
                                pFold('', pChar('b'), 'B', 0)))
        tree = parser('ab')
        self.assertEqual(str(tree), 'ab')
        self.assertEqual(repr(tree), "[#B [#A 'a']]")

    def test_NodeNode(self):
        parser = generate(pSeq2(pNode(pChar('a'), 'A', 0),
                                pNode(pChar('b'), 'B', 0)))
        tree = parser('ab')
        self.assertEqual(str(tree), 'ab')
        self.assertEqual(repr(tree), "[# [#A 'a'][#B 'b']]")
        print(tree.dump())


if __name__ == '__main__':
    unittest.main()
