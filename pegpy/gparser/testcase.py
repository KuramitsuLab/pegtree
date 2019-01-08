import pegpy.utils as u
from pegpy.peg import *
from pegpy.expression import *

def example(g, pgen):
    p = {}
    test = 0
    ok = 0
    for testcase in g.examples:
        name, inputs, output = testcase
        if not name in g: continue
        if not name in p:
            p[name] = pgen(pe.Ref(name, g))
        res = p[name](inputs)
        if output == None:
            if res == 'err':
                u.perror(res.pos3(), 'NG ' + name)
            else:
                print('OK', name, '=>', str(res))
        else:
            t = str(res).replace(" b'", " '")
            test += 1
            if t == output:
                print('OK', name, inputs, output)
                ok += 1
            else:
                print('NG', name, inputs, output, '!=', t)
    if test > 0:
        print('OK', ok, 'FAIL', test - ok, ok / test * 100.0, '%')

def testcase(g):
    g.Char = ParsingExpression.new('aa')
    g.Range = Range.new('ab')

    g.Ref = Ref('Char')
    g.Seq = Range.new('ab') & ParsingExpression.new('aa')
    g.Ore = ParsingExpression.new('aa') | ParsingExpression.new('ab')

    g.example("Char,Ref", "aaa", "[# 'aa']")
    g.example("Range", "baa", "[# 'b']")
    g.example("Seq", "baa", "[# 'baa']")
    g.example("Ore", "abc", "[# 'ab']")

    g.Many = (~ParsingExpression.new('b') & ANY)* 0

    g.example("Many", "aab", "[# 'aa']")

    g.EOF = ~ANY
    g.EOL = ParsingExpression.new('\n') | ParsingExpression.new('\r\n') | N%'EOF'
    g.COMMENT = '/*' & (~ParsingExpression.new('*/') & ANY)* 0 & '*/' | '//' & (~(N%'EOL') & ANY)* 0

    g.example("EOF", "", "[# '']")

    g.example("COMMENT", "/*hoge*/hoge", "[# '/*hoge*/']")
    g.example("COMMENT", "//hoge\nhoge", "[# '//hoge']")

    return g

g = testcase(Grammar('sample'))

example(g, nez)

#g = load_tpeg(Grammar('tpeg'))
#example(g, nez)