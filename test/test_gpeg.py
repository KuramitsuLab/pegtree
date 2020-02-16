import unittest
import tests
from pegpy.gparser.gnez import *
from pathlib import Path

def TestGrammar(peg=None):
    if peg == None:
        peg = Grammar('p')
    peg.ABC = Char('abc')
    peg.ABSeq = Char('a') & Char('b')
    peg.ABCSeq = Char('a') & Char('b') & Char('c')
    peg.ManyAny = ANY * 0
    peg.NotAlpha = ~Range.new("A-Z", 'a-z') & ANY
    peg.ManyNotAlpha = '1' & (~Range.new("A-Z", 'a-z') & ANY)*0
    peg.Str = '"' & ((Char(r'\"') | ~Range.new('"\n') & ANY)*0) & '"'
    peg.Str2 = '"' & (~Range.new('"\n') & ANY)*0 & '"'
    peg.Name = (~Range.new(' \t\r\n(,){};<>[|/*+?=\'`') & ANY)+0
    peg.AMB_AB = Char('a') | Char('ab')
    peg.AMB_ABB = (Char('a') | Char('ab')) & Char('b')

    peg.example('ABC', 'abcd', "[# 'abc']")
    peg.example('ABSeq', 'abcd', "[# 'ab']")
    peg.example('ABCSeq', 'abcd', "[# 'abc']")
    peg.example('ManyAny', '123', "[# '123']")
    peg.example('NotAlpha', '123', "[# '1']")
    peg.example('ManyNotAlpha', '123a', "[# '123']")
    peg.example('AMB_AB', 'ab', "[#? [# 'a'] [# 'ab']]")
    peg.example('AMB_ABB', 'abb', "[#? [# 'ab'] [# 'abb']]")
    peg.example('Str', '"abc"')
    peg.example('Str2', '"abc"')
    return peg


def AmbGrammar(peg=None):
  if peg == None:
      peg = Grammar('amb')
  peg.S = TreeAs('S', N % '$NP0' & N % '$VP0')
  peg.NP0 = TreeAs('NP', N % '$NP1' & N % '$PP') | TreeAs('NP', N % '$DT' & N % '$NN')
  peg.NP1 = TreeAs('NP', N % '$DT' & N % '$NN' & N % '$NP1' & N % '$PP') | TreeAs('NP', N % '$DT' & N % '$NN')
  peg.VP0 = TreeAs('VP', N % '$VP1' & N % '$PP') | TreeAs('VP', (N % '$Vt' & N % '$NP0'))
  peg.VP1 = TreeAs('VP', N % '$Vt' & N % '$NP0' & N % '$VP1' & N % '$PP') | TreeAs('VP', N % '$Vt' & N % '$NP0')
  peg.PP = TreeAs('PP', N % '$IN' & N % '$NP0')
  peg.DT = TreeAs('DT', Char('the'))
  peg.NN = TreeAs('NN', Char('man') / Char('dog') / Char('telescope'))
  peg.IN = TreeAs('IN', Char('with'))
  peg.Vt = TreeAs('Vt', Char('saw'))
  peg.example('S', 'themansawthedogwiththetelescope')
  return peg


def NLPGrammar(peg=None):
    if peg == None:
        peg = Grammar('nlp')
    peg.Assign = TreeAs('Assign', N % '$VARIABLENAME' & Char('を') & N % '$Expression' & Range.new('とおく', 'とする'))
    peg.Const = TreeAs('Const', N % '$VARIABLENAME' & Char('は') & N % '$Expression' & Range.new('である'))

    peg.Expression = N % 'Product' ^ TreeAs('Infix', N % '$AddSub $Product') * 0
    peg.Product = N % 'Value' ^ TreeAs('Infix', N % '$MulDiv $Value') * 0
    peg.Value = N % 'Int' | '(' & N % 'Expression' & ')'
    peg.Int = TreeAs('Int', Range.new('0-9') + 0)
    peg.AddSub = TreeAs('', Range.new('+-'))
    peg.MulDiv = TreeAs('', Range.new('*/%'))

    peg.VARIABLENAME = TreeAs('Variable', Range.new('A-Z', 'a-z') & Range.new('A-Z', 'a-z', '0-9') * 0)

    peg.example('Assign', 'Xを1+2*3とおく', "[#Assign [#Variable 'X'] [#Infix [#Int '1'] [# '+'] [#Infix [#Int '2'] [# '*'] [#Int '3']]]]")
    peg.example('Const', 'Xは5である', "[#Const [#Variable 'X'] [#Int '5']]")
    return peg

class TestGPEG(unittest.TestCase):

    def test_math(self):
        g = Grammar("math")
        g.load('math.tpeg')
        g.example('Expression,Int', '123', "[#Int '123']")
        g.example('Expression', '1+2*3', "[#Infix left=[#Int '1'] name=[# '+'] right=[#Infix left=[#Int '2'] name=[# '*'] right=[#Int '3']]]")
        self.exTest(g, gnez)

    def test_grammar(self):
        g = TestGrammar()
        self.exTest(g, gnez)

    def test_amb(self):
        g = AmbGrammar()
        self.exTest(g, gnez)
    
    def test_manyb(self):
        g = Grammar("manyb")
        g.load('manyb.gpeg')
        self.exTest(g, gnez)
    
    def test_nl(self):
        g = Grammar("nl")
        g.load('sample.gpeg')
        self.exTest(g, gnez)
    
    def test_nlp(self):
        g = NLPGrammar()
        self.exTest(g, gnez)


if __name__ == '__main__':
    unittest.main()
