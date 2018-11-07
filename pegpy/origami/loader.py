#!/usr/local/bin/python

from pegpy.peg import Grammar, nez
from pegpy.origami.sexpr import SExpr

g = Grammar('konoha6')
g.load('grammar/konoha6.tpeg')
origami_parser = nez(g['OrigamiFile'])

def getkeys(stmt):
    name = stmt['name'].asString()
    expr = stmt['expr'].asString()
    keys = []
    if 'from' in stmt:
        fromty = SExpr.of(stmt['from'])
        key = name + '@' + str(fromty)
        if 'to' in stmt:
            toty = SExpr.of(stmt['to'])
            keys.append(key + '@' + str(toty))
        keys.append(key)
    keys.append(name)
    if '@' in name:
        keys.append(name.split('@')[0])
    return keys

def load_origami(path):
    f = open(path)
    data = f.read()
    f.close()
    t = origami_parser(data, path)
    if t == 'err':
        er = t.getpos()
        print('SyntaxError ({}:{}:{}+{})'.format(er[0], er[2], er[3], er[1]), '\n', er[4], '\n', er[5])
        return
    env = {}
    for _, stmt in t:
        print(stmt)
        if stmt == 'CodeMap':
            keys = getkeys(stmt)
            expr = stmt['expr'].asString()
            env[keys[0]] = expr
            for key in keys[1:]:
                if not key in env:
                    env[key] = expr
        elif stmt == 'TypeMap':
            keys = getkeys(stmt)
            keys = list(map(lambda x: ' ' + x, keys))
            ty = SExpr.of(stmt['type'])
            env[keys[0]] = expr
            for key in keys[1:]:
                if not key in env:
                    env[key] = expr
    print(env)


class Env(object):
    __slots__ = ['parent', 'nameMap']

    def __init__(self, parent = None):
        self.parent = parent
        self.nameMap = {}

    def __contains__(self, item):
        if item in self.nameMap:
            return True
        if self.parent is not None:
            return item in self.parent
        return False

    def __getitem__(self, item):
        if item in self.nameMap:
            return self.nameMap[item]
        if self.parent is not None:
            return self.parent[item]
        return None

    def __setitem__(self, item, value):
        self.nameMap[item] = value

    def getType(self, iname):
        return self[iname]

    def getSyntax(self, iname):
        return self[iname]



    def parse(self, t):
        for _, stmt in t:
            print(stmt)
            if stmt == 'CodeMap':
                keys = getkeys(stmt)
                expr = stmt['expr'].asString()
                self[keys[0]] = expr
                for key in keys[1:]:
                    if not key in self:
                        self[key] = expr
            elif stmt == 'TypeMap':
                keys = getkeys(stmt)
                keys = list(map(lambda x: ' ' + x, keys))
                ty = SExpr.of(stmt['type'])
                self[keys[0]] = expr
                for key in keys[1:]:
                    if not key in self:
                        self[key] = expr
