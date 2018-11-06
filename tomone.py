from pegpy.peg import *
from pegpy.npeg.ndasm import ndasm

g = Grammar('tm')
g.load('grammar/npl.gpeg')

# sample.gpeg の example がテストされる
g.testAll(ndasm)

# parser が作られる
parser = ndasm(g)

# 文字列から ParseTree が得られる
t = parser('ああ')

# ParseTree の表示
print(t)

