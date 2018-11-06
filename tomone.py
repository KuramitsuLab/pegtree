from pegpy.peg import *
from pegpy.gpeg.gdasm import gdasm

g = Grammar('tm')
g.load('grammar/sample.gpeg')
g.testAll(gdasm)


