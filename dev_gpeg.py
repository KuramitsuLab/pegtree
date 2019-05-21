from pegpy.gparser.gnez import Grammar, gnez

g = Grammar("test")
g.load('test.gpeg')
parser = gnez(g)
print(parser('a'))