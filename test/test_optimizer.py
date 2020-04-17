import unittest
from pegtree.optimizer import *


class TestOptimizer(unittest.TestCase):

    def test_Node(self):
        pe = PNode(PChar('a'), 'A', 0)
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "'a' {/*-1*/ '' #A }")

    def test_Node2(self):
        pe = PNode(PChar('abc'), 'A', 0)
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "'abc' {/*-3*/ '' #A }")

    def test_NodeMany(self):
        pe = PNode(PMany(PChar('abc')), 'A', 0)
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "{ 'abc'* #A }")

    def test_NodeMany(self):
        pe = PNode(PSeq(PChar('a'), PMany(PChar('b'))), 'A', 0)
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "'a' {/*-1*/ 'b'* #A }")

    def test_NodeNot(self):
        pe = PNode(PNot(PChar('a')), 'A', 0)
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "!'a' { '' #A }")

    def test_NodeNode(self):
        pe = PNode(PNode(PChar('a'), 'A', 0), 'B', 0)
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "'a' {/*-1*/ {/*-1*/ '' #A } #B }")

    def test_Edge(self):
        pe = PEdge('x', PChar('a'), 0)
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "'a' x/*-1*/: ''")

    def test_Fold(self):
        pe = PFold('', PChar('a'), 'A', 0)
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "'a' { ^/*-1*/ '' #A }")

    def test_RangeOrRange(self):
        pe = POre(PRange('abc', ''), PRange('ABC', ''))
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "[A-Ca-c]")

    def test_RangeOrChar(self):
        pe = POre(PRange('abc', ''), PChar('A'))
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "[Aa-c]")

    def test_RangeOrAny(self):
        pe = POre(PRange('abc', ''), ANY)
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), ".")

    def test_Dict(self):
        pe = POre(PChar('int'), PChar('if'))
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "'i' ('nt' / 'f')")

    def test_Dict2(self):
        pe = POre(PChar('int'), PChar('i'), PChar('if'))
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "'i' 'nt'?")

    def test_Dict3(self):
        pe = POre(PChar('int'), PChar('a'), PChar('b'), PChar('if'))
        po = optimize(pe)
        #print(pe, '=>', po)
        self.assertEqual(str(po), "'i' ('nt' / 'f') / [ab]")


if __name__ == '__main__':
    unittest.main()
