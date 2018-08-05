#!/usr/local/bin/python

'''
def timeit(f):
    s = time.time()
    f()
    print(time.time() - s)
'''

def true(px): return True
def false(px): return False

def any(px):
    if px.pos < px.length:
        px.pos += 1
        px.headpos = max(px.pos, px.headpos)
        return True
    return False

def char(c):
    def curry(px):
        if px.pos < px.length and px.inputs[px.pos] == c:
            px.pos += 1
            px.headpos = max(px.pos, px.headpos)
            return True
        return False
    return curry

# Str
def multi(s, slen):
    def curry(px):
        pos = px.pos
        if pos + slen <= px.length:
            i = 0
            while i < slen:
                if px.inputs[pos + i] != s[i]: return False
                i += 1
            px.pos += slen
            px.headpos = max(px.pos, px.headpos)
            return True
        return False
    return curry

pf_char = {}

def emit_Char(pe):
    if len(pe.a)>1:
        return multi(pe.a, len(pe.a))
    if not pe.a in pf_char:
        pf_char[pe.a] = char(pe.a)
    return pf_char[pe.a]

def emit_Byte(pe):
    if len(pe.a)>1:
        b = bytes(pe.a, 'utf-8')
        return multi(b, len(b))
    c = ord(pe.a)
    key = str(c)
    if not key in pf_char:
        pf_char[key] = char(c)
    return pf_char[key]

def bits(n):
    def curry(px) :
        if px.pos < px.length and (n & (1 << px.inputs[px.pos])) != 0:
            px.pos += 1
            px.headpos = max(px.pos, px.headpos)
            return True
        return False
    return curry

def emit_ByteRange(pe):
    n = 0
    for c in pe.chars:
        n |= (1 << ord(c))
    for r in pe.ranges:
        for c in range(ord(r[0]), ord(r[1])+1):
            n |= (1 << c)
    return bits(n)

def isCharRange(c, ranges, chars):
    for r in ranges:
        if r[0] <= c and c <= r[1]: return True
    for c2 in chars:
        if c is c2: return True
    return False

def emit_CharRange(pe):
    chars = pe.chars
    ranges = pe.ranges
    def curry(px) :
        if px.pos < px.length and isCharRange(px.inputs[px.pos], ranges, chars):
            px.pos += 1
            px.headpos = max(px.pos, px.headpos)
            return True
        return False
    return curry

# Ref
def emit_Ref(peg, name, prefix, emit):
    key = prefix + name
    if not peg.hasmemo(key):
        peg.setmemo(key, lambda px: peg.getmemo(key)(px))
        pe = getattr(peg, name)
        ff = emit(pe)
        peg.setmemo(key, ff)
        return ff
    return peg.getmemo(key)

# Seq

def seq2(left, right):
    return lambda px: left(px) and right(px)

def seq(ls):
    def curry(px):
        for p in ls:
            if not p(px): return False
        return True
    return curry

def emit_Seq(pe, emit):
    ls = tuple(map(emit, pe.flatten([])))
    if len(ls) == 2:
        return seq2(ls[0], ls[1])
    return seq(ls)

# OrElse

def or2(left, right):
    def curry(px):
        pos = px.pos
        ast = px.ast
        if not left(px):
            px.pos = pos
            px.ast = ast
            return right(px)
        return True
    return curry

def _or(ls):
    def curry(px):
        pos = px.pos
        ast = px.ast
        for p in ls:
            if p(px): return True
            px.pos = pos
            px.ast = ast
        return False
    return curry

def emit_Or(pe, emit):
    ls = tuple(map(emit, pe.flatten([])))
    if len(ls) == 2:
        return or2(ls[0], ls[1])
    return _or(ls)

#Not
def _not(pf):
    def curry(px):
        pos = px.pos
        ast = px.ast
        if not pf(px):
            px.pos = pos
            px.ast = ast
            return True
        return False
    return curry

def emit_Not(pe, emit):
    return _not(emit(pe.inner))

# And
def _and(pf):
    def curry(px):
        pos = px.pos
        if pf(px):
            px.pos = pos
            return True
        return False
    return curry

def emit_And(pe, emit):
    return _and(emit(pe.inner))

# Many

def many(pf):
    def curry(px):
        pos = px.pos
        ast = px.ast
        while pf(px) and pos < px.pos:
            pos = px.pos
            ast = px.ast
        px.pos = pos
        px.ast = ast
        return True
    return curry

def emit_Many(pe, emit):
    return many(emit(pe.inner))

def emit_Many1(pe, emit):
    return seq2(emit(pe.inner), many(emit(pe.inner)))

# Tree

def tree(tag, pf, mtree):
    def curry(px):
        pos = px.pos
        px.ast = None
        if pf(px):
            px.ast = mtree(tag, px.inputs, pos, px.pos, px.ast)
            return True
        return False
    return curry

def emit_TreeAs(pe, emit, mtree):
    return tree(pe.tag, emit(pe.inner), mtree)

def link(tag, pf, mlink):
    def curry(px):
        ast = px.ast
        if pf(px):
            px.ast = mlink(tag, px.ast, ast)
            return True
        return False
    return curry

def emit_LinkAs(pe, emit, mlink):
    return link(pe.tag, emit(pe.inner), mlink)

def fold(ltag, tag, pf, mtree, mlink):
    def curry(px):
        pos = px.pos
        px.ast = mlink(ltag, px.ast, None)
        if pf(px):
            px.ast = mtree(tag, px.inputs, pos, px.pos, px.ast)
            return True
        return False
    return curry

def emit_FoldAs(pe, emit, mtree, mlink):
    return fold(pe.ltag, pe.tag, emit(pe.inner), mtree, mlink)

def unit(pf):
    def curry(px):
        ast = px.ast
        if pf(px):
            px.ast = ast
            return True
        return False
    return curry

def emit_Unit(pe, emit):
    return unit(emit(pe.inner))

def emit_Rule(pe, emit):
    return emit(pe.inner)


# dasm

'''
from tpeg import *
import parsefunc

# ParserFunction

def dasm_setup():
    def emit(pe): return pe.dasm()

    Empty.dasm = lambda self: parsefunc.true
    Any.dasm = lambda self: parsefunc.any
    Char.dasm = parsefunc.emit_Byte
    Range.dasm = parsefunc.emit_ByteRange

    Seq.dasm = lambda pe: parsefunc.emit_Seq(pe,emit)
    Or.dasm = lambda pe: parsefunc.emit_Or(pe,emit)
    Not.dasm = lambda pe: parsefunc.emit_Not(pe, emit)
    And.dasm = lambda pe: parsefunc.emit_And(pe, emit)
    Many.dasm = lambda pe: parsefunc.emit_Many(pe, emit)
    Many1.dasm = lambda pe: parsefunc.emit_Many1(pe, emit)

    TreeAs.dasm = lambda pe: parsefunc.emit_TreeAs(pe,emit, ParseTree)
    LinkAs.dasm = lambda pe: parsefunc.emit_LinkAs(pe,emit, TreeLink)
    FoldAs.dasm = lambda pe: parsefunc.emit_FoldAs(pe,emit, ParseTree, TreeLink)
    Detree.dasm = lambda pe: parsefunc.emit_Unit(pe,emit)

    # Ref
    Ref.dasm = lambda pe: parsefunc.emit_Ref(pe.peg, pe.name, "_DAsm_", emit)
    Rule.dasm = lambda pe: parsefunc.emit_Rule(pe, emit)

class DAsmContext:
    __slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast']
    def __init__(self, inputs, pos = 0):
        self.inputs = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
        self.length = len(self.inputs)
        self.pos = pos
        self.headpos = pos
        self.ast = None

def dasm(peg: PEG, name = None):
    if isinstance(peg, Pe):
        f = peg.dasm()
    else:
        if name == None: name = "start"
        f = parsefunc.emit_Ref(peg, name, "_DAsm_", lambda pe: pe.dasm())
    def parse(s, pos = 0):
        px = DAsmContext(s, pos)
        if not f(px):
            return ParseTree("err", s, px.pos, len(s), None)
        if px.ast == None:
            return ParseTree("", s, pos, px.pos, None)
        return px.ast
    return parse

dasm_setup()
'''