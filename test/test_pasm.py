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

    def test_NullFold(self):
        parser = generate(pFold('', pChar('a'), 'A', 0))
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
        #print('@', repr(tree))
        self.assertEqual(str(tree), 'ab')
        self.assertEqual(repr(tree), "[# [#A 'a'][#B 'b']]")
        # print(tree.dump())

    def test_NodeNodeFold(self):
        parser = generate(pSeq3(pNode(pChar('a'), 'A', 0),
                                pNode(pChar('b'), 'B', 0),
                                pFold('', pChar('c'), 'C', 0)))
        tree = parser('abc')
        #print('@', repr(tree))
        self.assertEqual(str(tree), 'abc')
        self.assertEqual(repr(tree), "[# [#A 'a'][#C [#B 'b']]]")
        # print(tree.dump())

    def test_NodeFoldFold(self):
        parser = generate(pSeq3(pNode(pChar('a'), 'A', 0),
                                pFold('', pChar('b'), 'B', 0),
                                pFold('', pChar('c'), 'C', 0)))
        tree = parser('abc')
        #print('@', repr(tree))
        self.assertEqual(str(tree), 'abc')
        self.assertEqual(repr(tree), "[#C [#B [#A 'a']]]")
        # print(tree.dump())

    def test_NodeEdgeNode(self):
        parser = generate(pNode(pEdge('x', pNode(pChar('a'), 'A', 0)), 'B', 0))
        tree = parser('abc')
        #print('@', repr(tree))
        self.assertEqual(str(tree), 'a')
        self.assertEqual(repr(tree), "[#B x: [#A 'a']]")

    def test_NodeEdge(self):
        parser = generate(pNode(pEdge('x', pChar('a')), 'A', 0))
        tree = parser('abc')
        #print('@', repr(tree))
        self.assertEqual(str(tree), 'a')
        self.assertEqual(repr(tree), "[#A x: [# 'a']]")

    def test_Edge(self):
        parser = generate(pEdge('x', pChar('a')))
        tree = parser('abc')
        #print('@', repr(tree))
        self.assertEqual(str(tree), 'a')
        self.assertEqual(repr(tree), "[# x: [# 'a']]")

    def test_EdgeEdge(self):
        parser = generate(pEdge('x', pEdge('y', pChar('a'))))
        tree = parser('abc')
        #print('@', repr(tree))
        self.assertEqual(str(tree), 'a')
        self.assertEqual(repr(tree), "[# x: [# y: [# 'a']]]")


if __name__ == '__main__':
    unittest.main()
