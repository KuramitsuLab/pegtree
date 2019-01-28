#!/usr/local/bin/python

from functools import lru_cache

import re

pat = re.compile(r'\$\{@([a-z0-9.]*)\((-?\w\:?-?\d?)\)\}')

#print(pat.findall('${@ret(-1)}'))

@lru_cache(maxsize=32)
def desugar_find(s):
    fs = pat.findall(s)
    if len(fs) > 0:
        fs2 = []
        for f,idx in fs:
            if '.' in f:
                ff = f.split('.')
                idxs = [idx] * len(ff)
                fs2.extend(zip(ff, idxs))
            else:
                fs2.append((f,idx))
        return fs2
    return fs

def nop(expr):
    return expr

def block(expr):
    if expr == '#Block': return expr
    return expr.new('#Block', expr)

def ret(expr):
    if expr == '#Block':
        if len(expr) == 1:
            expr.data = [expr.new('#Return')]
        else:
            expr[-1] = ret(expr[-1])
        return expr
    if expr == '#IfStmt':
        expr[2] = ret(expr[2])
        expr[3] = ret(expr[3])
        return expr
    if expr == '#Match':
        for i in range(1, len(expr)):
            expr[i] = ret(expr[i])
        return expr
    if expr == '#MatchCase':
        expr[1] = ret(expr[1])
        return expr
    return expr.new('#Return', expr)

def safegroup(expr):
    if expr == '#Infix':
        return expr.new('#Group', expr)
    return expr

funclist = globals()

def desugar_func(name):
    if name in funclist:
        return funclist[name]
    if name == '':
        return safegroup
    #print('@TODO(desugar)', name)
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
        try:
            i = int(args)
            e[i] = f(e[i])
        except ValueError:
            i = e.find(args)
            if i != -1: e[i] = f(e[i])


def desugar(env, e):
    for key in e.keys():
        defined = env[key]
        if defined is not None and defined.code is not None:
            code = desugar_find(defined.code)
            #print('@desugar', key, code)
            for func, args in code:
                f = desugar_func(func)
                desugar_apply(f, e, args)
