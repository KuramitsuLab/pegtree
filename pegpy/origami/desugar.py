#!/usr/local/bin/python

from pegpy.origami.sexpr import SExpr
from functools import lru_cache

import re

pat = re.compile(r'\$\{@([a-z0-9]*)\((-?\d\:?-?\d?)\)\}')

#print(pat.findall('${@ret(-1)}'))

@lru_cache(maxsize=32)
def desugar_find(s):
    return pat.findall(s)

def nop(expr):
    return expr

def safegroup(expr):
    if expr.asSymbol() == '#Infix':
        return SExpr.new('#Group', expr)
    return expr

def ret(expr):
    return SExpr.new('#Return', expr)

funclist = globals()

def desugar_func(name):
    if name in funclist:
        return funclist[name]
    if name == '':
        return safegroup
    #print('@TODO undefined desugar', name)
    return nop

def desugar_apply(f, e, args):
    if args.find(':') > 0:
        if args.ends(':'):
            args += int(len(e))
        start, end = map(int, args.split(':'))
        for i, e2 in enumerate(e[start: end], start):
            e[i] = f(e2)
    elif args == '*':
        for i, e2 in enumerate(e[1:], 1):
            e[i] = f(e2)
    else:
        i = int(args)
        e[i] = f(e[i])

def desugar(env, e):
    defined = env[e.asSymbol()]
    if defined is not None and defined.code is not None:
        code = desugar_find(defined.code)
        #print('@desugar', e.asSymbol(), code)
        for func, args in code:
            f = desugar_func(func)
            desugar_apply(f, e, args)
