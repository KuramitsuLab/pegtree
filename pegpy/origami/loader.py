#!/usr/local/bin/python

from pegpy.peg import *
from pegpy.origami.sexpr import *

g = Grammar('konoha6')
g.load('grammar/konoha6.tpeg')
origami_parser = nez(g['OrigamiFile'])

def load_origami(path):
    f = open(path)
    data = f.read()
    f.close()
    t = origami_parser(data, path)
    if t == 'err':
        er = t.getpos()
        print('SyntaxError ({}:{}:{}+{})'.format(er[0], er[2], er[3], er[1]), '\n', er[4], '\n', er[5])
        return
    for _, stmt in t:
        print(stmt)

