#!/usr/local/bin/python
import pegpy.rule as pe
import pegpy.parser as pg
import unittest as ut

def eval(p, conv = None):
    pg.setting('eval')
    return pg.generate_parser(pg.generate(p, 'eval'), conv)

def nez(p, conv = None):
    pg.setting('nez')
    return pg.generate_parser(pg.generate(p, 'nez'), conv)

def dasm(p, conv = None):
    pg.setting('dasm')
    return pg.generate_parser(pg.generate(p, 'dasm'), conv)

## Grammar

class Grammar(object):
    __slots__ = ['ns', 'rules', 'rulemap', 'memo', 'examples']

    def __init__(self, ns = None):
        self.ns = ns
        self.rules = []
        self.rulemap = {}
        self.memo = {}
        self.examples = []

    def __getitem__(self, item):
        return self.rulemap[item]

    def __setattr__(self, key, value):
        if isinstance(value, pe.ParsingExpression):
            self.add(key, value)
            #print(key, '=', value)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, key):
        if key in self.rulemap:
            return self.rulemap[key]
        return super().__getattr__(key)

    def namespace(self):
        return 'g'+id(self) if self.ns is None else self.ns

    def start(self):
        if len(self.rules) > 0: return self.rules[0]
        return pe.EMPTY

    def isDefined(self, name):
        return name in self.rulemap

    def add(self, key: str, x: pe.ParsingExpression):
        x.setpeg(self)
        if not isinstance(x, pe.Rule):
            x = pe.Rule(self, key, x)
        self.rules.append(x)
        self.rulemap[key] = x

    def generate(self, algo = 'eval', conv = None):
        pg.setting(algo)
        return pg.generate_parser(pg.generate(self.start().deref(), 'dasm'), conv)

    def hasmemo(self, key): return key in self.memo
    def getmemo(self, key): return self.memo[key] if key in self.memo else None
    def setmemo(self, key, value): self.memo[key] = value

    def example(self, prod, input, output = None):
        for name in prod.split(','):
            self.examples.append((name, input, output))

    def dump(self):
        for r  in self.rules: print(r)

    def testAll(self, combinator = nez, unittest = None):

        p = {}

        if isinstance(unittest, ut.TestCase):
            for testcase in self.examples:
                name, input, output = testcase
                if not name in p:
                    p[name] = combinator(pe.Ref(name, self))
                res = p[name](input)
                t = str(res).replace(" b'", " '")
                with unittest.subTest(example = name):
                    if output == None:
                        unittest.assertNotEqual(res, 'err')
                    else:
                        unittest.assertEqual(t, output)
            return 

        test = 0
        ok = 0
        for testcase in self.examples:
            name, input, output = testcase
            if not name in p:
                p[name] = combinator(pe.Ref(name, self))
            res = p[name](input)
            t = str(res).replace(" b'", " '")
            if output == None:
                if res == 'err':
                    er = res.getpos()
                    print('NG {}({}:{}:{}+{})'.format(name, er[0], er[2], er[3], er[1]), '\n', er[4], '\n', er[5])
                else:
                    print('OK', name, '=>', t)
            else:
                test += 1
                if t == output:
                    print('OK', name, input)
                    ok += 1
                else:
                    print('NG', name, input, output, '!=', t)
        if test > 0:
            print('OK', ok, 'FAIL', test - ok, ok / test * 100.0, '%')

pe.setup_loader(Grammar, nez)
