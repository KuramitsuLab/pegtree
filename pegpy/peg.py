#!/usr/local/bin/python
import pegpy.rule as pe
import pegpy.parser as pg
import pegpy.gparser.base as pg2
import pegpy.gparser.optimized as pg3

def eval(p, conv = None):
    return pg.generate2(p, method='eval', conv=conv)

def nez(p, conv = None):
    return pg.generate2(p, method='nez', conv=conv)

def nez1(p, conv = None):
    def emit(pe, **option) : return pe.nez(**option)
    return pg2.generate(p, method='nez', pg=pg3, emit=emit, memo={}, conv=conv)

def dasm(p, conv = None):
    return pg.generate2(p, method='dasm', conv=conv)

## Grammar

class Grammar(object):
    __slots__ = ['ns', 'rules', 'rulemap', 'min', 'max', 'memo', 'examples']

    def __init__(self, ns = None):
        self.ns = ns
        self.rules = []
        self.rulemap = {}
        self.min = 1 << 20
        self.max = 0
        self.memo = {}
        self.examples = []
        if isinstance(ns, str) and ns.find('=') > 0:
            self.ns = None
            self.load(ns)

    def __setattr__(self, key, value):
        if isinstance(value, pe.ParsingExpression):
            self.add(key, value)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, key):
        if key in self.rulemap:
            return self.rulemap[key]
        return super().__getattr__(key)

    def __contains__(self, item):
        return item in self.rulemap

    def __getitem__(self, item):
        return self.rulemap[item]

    def namespace(self):
        return 'g'+str(id(self)) if self.ns is None else self.ns

    def start(self):
        if len(self.rules) > 0: return self.rules[0]
        return pe.Rule(self, 'undefined', pe.EMPTY)

    def add(self, key: str, x: pe.ParsingExpression, pos3=None):
        x.setpeg(self)
        if not isinstance(x, pe.Rule):
            x = pe.Rule(self, key, x, pos3)
        if not pe.Ref.isInlineName(key):
            self.rules.append(x)
        self.rulemap[key] = x

    def forEachRule(self, f):
        for rule in self.rules[:]:
            rule.inner = f(rule)

    def hasmemo(self, key):
        return key in self.memo

    def getmemo(self, key):
        return self.memo[key] if key in self.memo else None

    def setmemo(self, key, value): self.memo[key] = value

    def example(self, prod, input, output = None):
        for name in prod.split(','):
            self.examples.append((name, input, output))

    def dump(self, out, indent=''):
        for rule in self.rules: out.println(rule)

    def pgen(self, name:str, combinator=nez):
        return combinator(pe.Ref(name, self))

pe.setup_loader(Grammar, eval)
