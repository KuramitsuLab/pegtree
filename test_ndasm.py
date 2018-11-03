from pegpy.npeg.ndasm import *


def math2(peg=None):
    if peg == None:
        peg = Grammar('math')
    peg.Expression = N % 'Product' ^ TreeAs('Infix', N % '$AddSub $Product') * 0
    peg.Product = N % 'Value' ^ TreeAs('Infix', N % '$MulDiv $Value') * 0
    peg.Value = N % 'Int' | '(' & N % 'Expression' & ')'
    peg.Int = TreeAs('Int', Range('0-9') + 0)
    peg.AddSub = TreeAs('', Range('+-'))
    peg.MulDiv = TreeAs('', Range('*/%'))
    peg.example('Expression,Int', '123', "[#Int '123']")
    peg.example('Expression', '1+2*3',"[#Infix [#Int '1'] [# '+'] [#Infix [#Int '2'] [# '*'] [#Int '3']]]")
    return peg


peg2 = math2(Grammar("math"))
peg2.testAll(ndasm)


def TestGrammar(peg=None):
    if peg == None:
        peg = Grammar('p')
    peg.ABC = Char('abc')
    peg.ABSeq = Char('a') & Char('b')
    peg.ABCSeq = Char('a') & Char('b') & Char('c')
    peg.ManyAny = ANY * 0
    peg.NotAlpha = ~Range("A-Z", 'a-z') & ANY
    peg.ManyNotAlpha = '1' & (~Range("A-Z", 'a-z') & ANY)*0
    peg.Str = '"' & ((Char(r'\"') | ~Range('"\n') & ANY)*0) & '"'
    peg.Str2 = '"' & (~Range('"\n') & ANY)*0 & '"'
    peg.Name = (~Range(' \t\r\n(,){};<>[|/*+?=\'`') & ANY)+0
    peg.AMB_AB = Char('a') | Char('ab')
    peg.DET_AB = Char('b') | Char('ab')
    peg.AMB_ABB = (Char('a') | Char('ab')) & Char('b')
    peg.Rec =  Char('b') & N % 'Rec' | Char('b')

    peg.example('ABC', 'abcd', "[# 'abc']")
    peg.example('ABSeq', 'abcd', "[# 'ab']")
    peg.example('ABCSeq', 'abcd', "[# 'abc']")
    peg.example('ManyAny', '123', "[# '123']")
    peg.example('NotAlpha', '123', "[# '1']")
    peg.example('ManyNotAlpha', '123a', "[# '123']")
    peg.example('AMB_AB', 'ab', "[#Ambiguity [# 'a'] [# 'ab']]")
    peg.example('DET_AB', 'ab', "[# 'ab']")
    peg.example('AMB_ABB', 'abb', "[#Ambiguity [# 'ab'] [# 'abb']]")
    peg.example('Str', '"abc"')
    peg.example('Str2', '"abc"')
    peg.example('Rec', 'bbb', "[#Ambiguity [# 'bb'] [# 'bbb'] [# 'b']]")
    return peg


peg2 = TestGrammar()
peg2.testAll(ndasm)


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
    peg.kanji = Range("\u3005", "\u3007", "\u303b",
                      "\u3400-\u4DB5", "\u4E00-\u9FA0")*0

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


peg2 = NLGrammar()
peg2.testAll(ndasm)


def NLPGrammar(peg=None):
    if peg == None:
        peg = Grammar('nlp')
    peg.Assign = TreeAs('Assign', N % '$VARIABLENAME' & Char('を') & N % '$Expression' & Range('とおく', 'とする'))
    peg.Const = TreeAs('Const', N % '$VARIABLENAME' & Char('は') & N % '$Expression' & Range('である'))

    peg.Expression = N % 'Product' ^ TreeAs(
        'Infix', N % '$AddSub $Product') * 0
    peg.Product = N % 'Value' ^ TreeAs('Infix', N % '$MulDiv $Value') * 0
    peg.Value = N % 'Int' | '(' & N % 'Expression' & ')'
    peg.Int = TreeAs('Int', Range('0-9') + 0)
    peg.AddSub = TreeAs('', Range('+-'))
    peg.MulDiv = TreeAs('', Range('*/%'))

    peg.VARIABLENAME = TreeAs('Variable', Range(
        'A-Z', 'a-z') & Range('A-Z', 'a-z', '0-9') * 0)

    peg.example('Assign', 'Xを1+2*3とおく',
                "[#Assign [#Variable 'X'] [#Infix [#Int '1'] [# '+'] [#Infix [#Int '2'] [# '*'] [#Int '3']]]]")
    peg.example('Const', 'Xは5である', "[#Const [#Variable 'X'] [#Int '5']]")
    return peg


peg2 = NLPGrammar()
peg2.testAll(ndasm)
