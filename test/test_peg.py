import unittest
from pegtree.peg import *


class TestPeg(unittest.TestCase):

    def test_Empty(self):
        pe = PChar('')
        # print(pe)
        self.assertFalse(isAlwaysConsumed(pe))

    def test_Char(self):
        pe = PChar('a')
        # print(pe)
        self.assertTrue(isAlwaysConsumed(pe))

    def test_String(self):
        pe = PChar('abc')
        # print(pe)
        self.assertTrue(isAlwaysConsumed(pe))

    def test_Range(self):
        pe = PRange('0123456789', 'AZaz')
        # print(pe)
        self.assertTrue(isAlwaysConsumed(pe))

    def test_Any(self):
        pe = PAny()
        # print(pe)
        self.assertTrue(isAlwaysConsumed(pe))

    def test_Seq(self):
        pe = PSeq(PChar('abc'), PRange('', 'AZaz'))
        # print(pe)
        self.assertTrue(isAlwaysConsumed(pe))

    def test_And(self):
        pe = PAnd(PChar('a'))
        # print(pe)
        self.assertFalse(isAlwaysConsumed(pe))

    def test_Not(self):
        pe = PNot(PChar('a'))
        # print(pe)
        self.assertFalse(isAlwaysConsumed(pe))

    def test_Many(self):
        pe = PMany(PChar('a'))
        # print(pe)
        self.assertFalse(isAlwaysConsumed(pe))

    def test_OneMany(self):
        pe = POneMany(PChar('a'))
        # print(pe)
        self.assertTrue(isAlwaysConsumed(pe))

    def test_Option(self):
        pe = POption(PChar('a'))
        # print(pe)
        self.assertFalse(isAlwaysConsumed(pe))

    def test_Ref(self):
        peg = Grammar()
        peg['A'] = PChar('a')
        pe = peg.newRef('A')
        # print(pe)
        self.assertTrue(isAlwaysConsumed(pe))

    # def test_Choice(self):
    #     print(PE.mergeRange(PChar('A'),
    #                         PRange('0', 'AZ'),
    #                         ))
    #     print(PE.mergeRange(PChar('a'),
    #                         PChar('b'),
    #                         ))
    #     print(PE.mergeRange(PChar('a'),
    #                         PChar('c'),
    #                         ))
    #     es = [
    #         PChar('return'),
    #         PChar('r'),
    #         PChar('ab'),
    #         PChar('a'),
    #         PChar('b'),
    #         PChar('ba'),
    #         PChar('ret'),
    #     ]
    #     print(PE.newChoice(es))
    #     es = [
    #         PChar('r'),
    #         PChar('a'),
    #         PChar('c'),
    #         PChar('b'),
    #     ]
    #     print(PE.newChoice(es))

    # def test_Char(self):
    #     parser = generate(pChar('a'))
    #     tree = parser('aa')
    #     self.assertEqual(str(tree), 'a')
    #     self.assertEqual(repr(tree), "[# 'a']")

    # def test_Node(self):
    #     parser = generate(pNode(pChar('a'), 'A', 0))
    #     tree = parser('aa')
    #     self.assertEqual(str(tree), 'a')
    #     self.assertEqual(repr(tree), "[#A 'a']")

    # def test_NestedNode(self):
    #     parser = generate(pNode(pSeq2(pNode(pChar('a'), 'A', 0),
    #                                   pNode(pChar('b'), 'B', 0)), "AB", 0))
    #     tree = parser('ab')
    #     self.assertEqual(str(tree), 'ab')
    #     self.assertEqual(repr(tree), "[#AB [#A 'a'][#B 'b']]")

    # def test_FoldNode(self):
    #     parser = generate(pSeq2(pNode(pChar('a'), 'A', 0),
    #                             pFold('', pChar('b'), 'B', 0)))
    #     tree = parser('ab')
    #     self.assertEqual(str(tree), 'ab')
    #     self.assertEqual(repr(tree), "[#B [#A 'a']]")

    # def test_NodeNode(self):
    #     parser = generate(pSeq2(pNode(pChar('a'), 'A', 0),
    #                             pNode(pChar('b'), 'B', 0)))
    #     tree = parser('ab')
    #     self.assertEqual(str(tree), 'ab')
    #     self.assertEqual(repr(tree), "[# [#A 'a'][#B 'b']]")
    #     print(tree.dump())


if __name__ == '__main__':
    unittest.main()
