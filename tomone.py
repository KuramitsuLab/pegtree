from pegpy.peg import *
from pegpy.gpeg.gdasm import gdasm

g = Grammar('tm')
g.load('grammar/sample.gpeg')

# sample.gpeg の example がテストされる
g.testAll(gdasm)

# parser が作られる
parser = gdasm(g)

# 文字列から ParseTree が得られる
t = parser('aa')

# ParseTree の表示
print(t)

