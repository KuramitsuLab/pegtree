#!/usr/local/bin/python

from pegpy.expression import *
from pegpy.ast import *
import pegpy.utils as u

class ParserContext:
  __slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast']

  def __init__(self, inputs, urn='(unknown)', pos=0):
    s = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
    self.inputs, self.pos = u.encode_source(s, urn, pos)
    self.length = len(self.inputs)
    self.headpos = self.pos
    self.ast = None

def p_True(px): return True
def p_False(px): return False

def p_Any(px):
    if px.pos < px.length:
        px.pos += 1
        px.headpos = max(px.pos, px.headpos)
        return True
    return False

def emit_char(c):
    def curry(px):
        if px.pos < px.length and px.inputs[px.pos] == c:
            px.pos += 1
            px.headpos = max(px.pos, px.headpos)
            return True
        return False
    return curry

# Str
def emit_multi0(s, slen):
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

def emit_multi(s, slen):
    def curry(px):
        if px.inputs.startswith(s,px.pos):
            px.pos += slen
            px.headpos = max(px.pos, px.headpos)
            return True
        return False
    return curry

pf_char = {}

def emit_Char(pe):
    if len(pe.a) > 1:
        return emit_multi(pe.a, len(pe.a))
    if not pe.a in pf_char:
        pf_char[pe.a] = emit_char(pe.a)
    return pf_char[pe.a]

def emit_Byte(pe):
    if len(pe.a) > 1:
        b = bytes(pe.a, 'utf-8')
        return emit_multi(b, len(b))
    c = ord(pe.a)
    key = str(c)
    if not key in pf_char:
        pf_char[key] = emit_char(c)
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
        if c == c2: return True
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

# Seq

def emit_Seq2(left, right):
    return lambda px: left(px) and right(px)

def emit_Seq(pe, emit):
    ls = tuple(map(emit, pe.flatten([])))
    if len(ls) == 2:
        return emit_Seq2(ls[0], ls[1])
    def curry(px):
        for p in ls:
            if not p(px): return False
        return True
    return curry

# OrElse

def emit_Or2(left, right):
    def curry(px):
        pos = px.pos
        ast = px.ast
        if not left(px):
            px.pos = pos
            px.ast = ast
            return right(px)
        return True
    return curry

def emit_Or(pe, emit):
    ls = tuple(map(emit, pe.flatten([])))
    if len(ls) == 2:
        return emit_Or2(ls[0], ls[1])
    def curry(px):
        pos = px.pos
        ast = px.ast
        for p in ls:
            if p(px): return True
            px.pos = pos
            px.ast = ast
        return False
    return curry

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
    return emit_Seq2(emit(pe.inner), many(emit(pe.inner)))

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
    return tree(pe.name, emit(pe.inner), mtree)

def link(tag, pf, mlink):
    def curry(px):
        ast = px.ast
        if pf(px):
            px.ast = mlink(tag, px.ast, ast)
            return True
        return False
    return curry

def emit_LinkAs(pe, emit, mlink):
    return link(pe.name, emit(pe.inner), mlink)

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
    return fold(pe.left, pe.name, emit(pe.inner), mtree, mlink)

def emit_Detree(pe, emit):
    pf = emit(pe.inner)
    def curry(px):
        ast = px.ast
        if pf(px):
            px.ast = ast
            return True
        return False
    return curry

def emit_trace(ref: Ref, pf):
    key = ref.uname()
    def curry(px):
        print("+", key, px.pos)
        return pf(px)
    return curry

# Ref
def emit_Ref(ref: Ref, memo: dict, emit):
    key = ref.uname()
    if not key in memo:
        memo[key] = lambda px: memo[key](px)
        memo[key] = emit(ref.deref())
        #memo[key] = emit_trace(ref, emit(ref.deref()))
    return memo[key]

# Setting Parser

def setting(f: str):
    if not hasattr(Char, f):
        def emit(pe): return getattr(pe, f)()

        setattr(Empty,f, lambda self: p_True)
        setattr(Any, f, lambda self: p_Any)
        setattr(Char, f, emit_Byte)
        setattr(Range, f, emit_ByteRange)

        setattr(Seq, f, lambda pe: emit_Seq(pe, emit))
        setattr(Ore, f, lambda pe: emit_Or(pe, emit))
        setattr(Alt, f, lambda pe: emit_Or(pe, emit))
        setattr(Not, f, lambda pe: emit_Not(pe, emit))
        setattr(And, f, lambda pe: emit_And(pe, emit))
        setattr(Many, f, lambda pe: emit_Many(pe, emit))
        setattr(Many1, f, lambda pe: emit_Many1(pe, emit))

        setattr(TreeAs, f, lambda pe: emit_TreeAs(pe, emit, ParseTree))
        setattr(LinkAs, f, lambda pe: emit_LinkAs(pe, emit, TreeLink))
        setattr(FoldAs, f, lambda pe: emit_FoldAs(pe, emit, ParseTree, TreeLink))
        setattr(Detree, f, lambda pe: emit_Detree(pe, emit))

        # Ref
        memo = {}
        setattr(Ref, f, lambda pe: emit_Ref(pe, memo, emit))
        return True
    return False

def generate(p, f = 'dasm'):
    setting(f)
    if not isinstance(p, ParsingExpression): # Grammar
        p = Ref(p.start().name, p)
    return getattr(p, f)()

def generate_parser(f, conv = None):
    def parse(s, urn = '(unknown)', pos = 0):
        px = ParserContext(s, urn, pos)
        pos = px.pos
        result = None
        if not f(px):
            result = ParseTree("err", px.inputs, px.headpos, len(s), None)
        else:
            result = px.ast if px.ast is not None else ParseTree("", px.inputs, pos, px.pos, None)
        return conv(result) if conv is not None else result
    return parse
