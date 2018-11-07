import unittest
from pegpy.gparser.gnez import *
from test_gpeg import TestGrammar
from pathlib import Path


def NLGrammar(peg=None):
    if peg == None:
        peg = Grammar('nl')
    peg.iroha = Char('いろは')
    peg.iroSeq = Char('い') & Char('ろ')
    peg.irohaSeq = Char('い') & Char('ろ') & Char('は')
    peg.any = ANY & ANY
    peg.chclass = Range('い', 'ろ', 'は')*0
    peg.hiragana = Range('ぁ-ん')*0
    peg.katakana = Range('ァ-ヶ')*0
    peg.kanji = Range("\u3005", "\u3007", "\u303b","\u3400-\u4DB5", "\u4E00-\u9FA0")*0

    peg.wait = (N % 'NP' | N % 'VP') & N % 'PP' & N % 'VP'

    peg.example('iroha', 'いろは', "[# 'いろは']")
    peg.example('iroSeq', 'いろは', "[# 'いろ']")
    peg.example('irohaSeq', 'いろは', "[# 'いろは']")
    peg.example('any', 'いろは', "[# 'いろ']")
    peg.example('chclass', 'いろは', "[# 'いろは']")
    peg.example('hiragana', 'あかさたなはまやらわを', "[# 'あかさたなはまやらわを']")
    peg.example('katakana', 'アカサタナハマヤラワヲ', "[# 'アカサタナハマヤラワヲ']")
    peg.example('kanji', '倉光研究室です', "[# '倉光研究室']")

    return peg


def NLPGrammar(peg=None):
    if peg == None:
        peg = Grammar('nlp')
    peg.Assign = TreeAs('Assign', N % '$VARIABLENAME' & Char('を') & N % '$Expression' & Range('とおく', 'とする'))
    peg.Const = TreeAs('Const', N % '$VARIABLENAME' & Char('は') & N % '$Expression' & Range('である'))

    peg.Expression = N % 'Product' ^ TreeAs('Infix', N % '$AddSub $Product') * 0
    peg.Product = N % 'Value' ^ TreeAs('Infix', N % '$MulDiv $Value') * 0
    peg.Value = N % 'Int' | '(' & N % 'Expression' & ')'
    peg.Int = TreeAs('Int', Range('0-9') + 0)
    peg.AddSub = TreeAs('', Range('+-'))
    peg.MulDiv = TreeAs('', Range('*/%'))

    peg.VARIABLENAME = TreeAs('Variable', Range('A-Z', 'a-z') & Range('A-Z', 'a-z', '0-9') * 0)

    peg.example('Assign', 'Xを1+2*3とおく', "[#Assign [#Variable 'X'] [#Infix [#Int '1'] [# '+'] [#Infix [#Int '2'] [# '*'] [#Int '3']]]]")
    peg.example('Const', 'Xは5である', "[#Const [#Variable 'X'] [#Int '5']]")
    return peg

class TestNPEG(unittest.TestCase):

    def test_math(self):
        g = Grammar("math")
        g.load('math.tpeg')
        g.example('Expression,Int', '123', "[#Int '123']")
        g.example('Expression', '1+2*3',"[#Infix left=[#Int '1'] name=[# '+'] right=[#Infix left=[#Int '2'] name=[# '*'] right=[#Int '3']]]")
        self.exTest(g, nnez)

    def test_grammar(self):
        g = TestGrammar()
        self.exTest(g, nnez)

    def test_amb(self):
        g = NLGrammar()
        self.exTest(g, nnez)

    def test_manyb(self):
        g = NLPGrammar()
        self.exTest(g, nnez)
