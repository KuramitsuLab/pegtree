from pegpy.dasm import *

def math(peg = None):
    if peg == None: peg = PEG('math')
    left = LinkAs('left')
    right = LinkAs('right')
    op = LinkAs('name')
    peg.Expression = N % 'Product' & (left ^ TreeAs('Infix', (op <= N % 'AddSub') & (right <= N % 'Product'))) * 0
    peg.Product = N % 'Value' & (left ^ TreeAs('Infix', (op <= N % 'MulDiv') & (right <= N % 'Value')) * 0)
    peg.Value = N % 'Int' | '(' & N % 'Expression' & ')'
    peg.Int = TreeAs('Int', Range('0-9')+ 0)
    peg.AddSub = TreeAs('', Range('+-'))
    peg.MulDiv = TreeAs('', Range('*/%'))
    peg.example('Expression,Int', '123', "[#Int '123']")
    peg.example('Expression', '1+2*3')
    return peg

#peg2 = math(PEG("math"))
#f = dasm(peg2)

def math2(peg = None):
    if peg == None: peg = PEG('math')
    peg.Expression = N % 'Product' ^ TreeAs('Infix', N % '$AddSub $Product') * 0
    peg.Product = N % 'Value' ^ TreeAs('Infix', N % '$MulDiv $Value') * 0
    peg.Value = N % 'Int' | '(' & N % 'Expression' & ')'
    peg.Int = TreeAs('Int', Range('0-9')+ 0)
    peg.AddSub = TreeAs('', Range('+-'))
    peg.MulDiv = TreeAs('', Range('*/%'))
    peg.example('Expression,Int', '123', "[#Int '123']")
    peg.example('Expression', '1+2*3', "[#Infix [#Int '1'] [# '+'] [#Infix [#Int '2'] [# '*'] [#Int '3']]]")
    return peg

peg2 = math2(PEG("math"))
peg2.testAll(dasm)
testRules(peg2)

def TestGrammar(peg = None):
    if peg == None: peg = PEG('p')
    peg.ABC = pe('abc')
    peg.ABSeq = pe('a') & pe('b')
    peg.ABCSeq = pe('a') & pe('b') & pe('c')
    peg.ManyAny = ANY * 0
    peg.NotAlpha = ~Range("A-Z", 'a-z') & ANY
    peg.ManyNotAlpha = '1' & (~Range("A-Z", 'a-z') & ANY)*0
    peg.Str = '"' & ((pe(r'\"') | ~Range('"\n') & ANY)*0) & '"'
    peg.Str2 = '"' & (~Range('"\n') & ANY)*0 & '"'
    peg.Name= (~Range(' \t\r\n(,){};<>[|/*+?=\'`') & ANY)+0

    peg.example('ABC', 'abcd', "[# 'abc']")
    peg.example('ABSeq', 'abcd', "[# 'ab']")
    peg.example('ABCSeq', 'abcd', "[# 'abc']")
    peg.example('ManyAny', '123', "[# '123']")
    peg.example('NotAlpha', '123', "[# '1']")
    peg.example('ManyNotAlpha', '123a', "[# '123']")
    peg.example('Str', '"abc"')
    peg.example('Str2', '"abc"')
    return peg

peg2 = TestGrammar()
peg2.testAll(dasm)

peg3 = TPEGGrammar()
peg3.testAll(dasm)
testRules(peg3)

parse = dasm(peg3)
ast = parse('''
A = / a / b / c
A = a 'b c'
A = !(a .)
''')

#conv = TPEGConv(PEG("test"))
#conv.parse(ast)