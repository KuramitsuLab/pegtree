import pegpy.utils as u
from pegpy.expression import *
from pegpy.ast import *


def mresult(pf):
    def curry(px):
        if pf(px):
            px.result[px.pos] = px.ast
            return True
        else:
            px.result[px.pos] = px.ast
            return False
    return curry

def union(px, old, pos, mtree, mlink):
    result = {}
    new = px.result
    umtree = lambda tag, child: mtree(tag, px.inputs, pos, px.pos, child)
    for pos in set(old) & set(new):
        result[pos] = mlink('', umtree('?', mlink('', umtree('?l', new[pos]), mlink('', umtree('?r', old[pos]), None))), None)
    for pos in set(old) - set(new):
        result[pos] = old[pos]
    for pos in set(new) - set(old):
        result[pos] = new[pos]
    return result
