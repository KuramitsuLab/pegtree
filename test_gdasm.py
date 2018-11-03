from pegpy.gpeg.gdasm import *

def math2(peg = None):
    if peg == None: peg = Grammar('math')
    peg.Expression = N % 'Product' ^ TreeAs('Infix', N % '$AddSub $Product') * 0
    peg.Product = N % 'Value' ^ TreeAs('Infix', N % '$MulDiv $Value') * 0
    peg.Value = N % 'Int' | '(' & N % 'Expression' & ')'
    peg.Int = TreeAs('Int', Range('0-9')+ 0)
    peg.AddSub = TreeAs('', Range('+-'))
    peg.MulDiv = TreeAs('', Range('*/%'))
    peg.example('Expression,Int', '123', "[#Int '123']")
    peg.example('Expression', '1+2*3', "[#Infix [#Int '1'] [# '+'] [#Infix [#Int '2'] [# '*'] [#Int '3']]]")
    return peg

peg2 = math2(Grammar("math"))
peg2.testAll(gdasm)

def TestGrammar(peg = None):
    if peg == None: peg = Grammar('p')
    peg.ABC = Char('abc')
    peg.ABSeq = Char('a') & Char('b')
    peg.ABCSeq =Char('a') & Char('b') & Char('c')
    peg.ManyAny = ANY * 0
    peg.NotAlpha = ~Range("A-Z", 'a-z') & ANY
    peg.ManyNotAlpha = '1' & (~Range("A-Z", 'a-z') & ANY)*0
    peg.Str = '"' & ((Char(r'\"') | ~Range('"\n') & ANY)*0) & '"'
    peg.Str2 = '"' & (~Range('"\n') & ANY)*0 & '"'
    peg.Name= (~Range(' \t\r\n(,){};<>[|/*+?=\'`') & ANY)+0
    peg.AMB_AB = Char('a') | Char('ab')
    peg.AMB_ABB = ( Char('a') | Char('ab') ) & Char('b')

    peg.example('ABC', 'abcd', "[# 'abc']")
    peg.example('ABSeq', 'abcd', "[# 'ab']")
    peg.example('ABCSeq', 'abcd', "[# 'abc']")
    peg.example('ManyAny', '123', "[# '123']")
    peg.example('NotAlpha', '123', "[# '1']")
    peg.example('ManyNotAlpha', '123a', "[# '123']")
    peg.example('AMB_AB', 'ab', "[#Ambiguity [# 'a'] [# 'ab']]")
    peg.example('AMB_ABB', 'abb', "[#Ambiguity [# 'ab'] [# 'abb']]")
    peg.example('Str', '"abc"')
    peg.example('Str2', '"abc"')
    return peg

peg2 = TestGrammar()
peg2.testAll(gdasm)

def AmbGrammar(peg = None):
  if peg == None: peg = Grammar('amb')
  peg.S = TreeAs('S', N % '$NP0' & N % '$VP0' )
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

peg2 = AmbGrammar()
peg2.testAll(gdasm)


def ManyBGrammar(peg=None):
  if peg == None:
    peg = Grammar('manyB')
  peg.S = TreeAs('S', Char('b') & N % '$S' & N % '$S' | N % '$S1')
  peg.S1 = TreeAs('S\'', Char('b') & N % '$S' | Char('b'))

  peg.example('S', 'bbb')
  return peg


peg2 = ManyBGrammar()
peg2.testAll(gdasm)
