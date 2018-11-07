from pegpy.peg import *
from pegpy.gparser.gnez import nnez
from pathlib import Path

g = Grammar('tm')
g.load(Path('pegpy') / 'grammar' / 'npl.gpeg')

# sample.gpeg の example がテストされる
g.testAll(nnez)

# parser が作られる
parser = nnez(g)

# 文字列から ParseTree が得られる
t = parser('ああ')

# ParseTree の表示
print(t)
