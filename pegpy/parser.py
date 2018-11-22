#!/usr/local/bin/python

import pegpy.utils as u
from pegpy.expression import *
from pegpy.ast import *

class ParserOption(object):
    def __init__(self):
        self.isByte = False
        self.isOptimized = False
        self.treeFunc = ParseTree
        self.linkFunc = TreeLink

# Empty
def empty(px): return True

def ggen_Empty(emit, option: ParserOption):
    def gen(pe):
        return empty
    return gen

def fail(px): return False

def gen_NotEmpty(pe: Empty):
    return fail

# Char

def nop(px): pass
def inc(px): px.pos += 1

def charlen(pe: Char, isByte: bool):
    if isByte:
        b = bytes(pe.a, 'utf-8')
        return b, len(b)
    else:
        return pe.a, len(pe.a)

def ggen_Char(emit, option: ParserOption):
    def multichar(s, slen):
        def matched(px):
            if px.inputs.startswith(s, px.pos):
                px.pos += slen
                return True
            return False
        return matched

    return lambda pe: multichar(*charlen(pe, option.isByte))

def gen_AndChar(pe: Char, isByte: bool):
    def andmultichar(s, slen):
        def andchar(px):
            return px.inputs.startswith(s, px.pos)
        return andchar
    return andmultichar(*charlen(pe, isByte))

def gen_NotChar(pe: Char, isByte: bool):
    def notmultichar(s, slen):
        def notchar(px):
            return not px.inputs.startswith(s, px.pos)
        return notchar
    return notmultichar(*charlen(pe, isByte))

def gen_ManyChar(pe: Char, isByte: bool):
    def manymultichar(s, slen):
        def manychar(px):
            while (px.inputs.startswith(s, px.pos)):
                px.pos += slen
            return True
        return manychar
    return manymultichar(*charlen(pe, isByte))

def gen_Many1Char(pe: Char, isByte: bool):
    def many1multichar(s, slen):
        def many1char(px):
            c = 0
            while (px.inputs.startswith(s, px.pos)):
                px.pos += slen
                c += 1
            return c > 0
        return many1char
    return many1multichar(*charlen(pe, isByte))

# Any

def ggen_Any(emit, option: ParserOption):
    def any(px):
        if px.pos < px.length:
            px.pos += 1
            return True
        return False
    return lambda pe: any

def gen_AndAny():
    def andany(px):
        return px.pos < px.length
    return andany

def gen_NotAny():
    def notany(px):
        return px.pos >= px.length
    return notany

def gen_ManyAny():
    def manyany(px):
        px.pos = px.length
        return True
    return manyany

def gen_Many1Any():
    def many1any(px):
        if px.pos < px.length:
            px.pos = px.length
            return True
        return False
    return many1any

# Range

def isbitset(pe):
    for c in pe.chars:
        if ord(c) > 255: return False
    for r in pe.ranges:
        if ord(r[1]) > 255: return False
    return True

def encode_bitset(pe):
    n = 0
    for c in pe.chars:
        n |= (1 << ord(c))
    for r in pe.ranges:
        for c in range(ord(r[0]), ord(r[1])+1):
            n |= (1 << c)
    return n

def decode_char(inputs, pos):
    try:
        return inputs[pos:pos + 4].decode('utf-8', 'replace')[0]
    except IndexError:
        return '\0'

def isRangeChar(c, ranges, chars):
    for r in ranges:
        if r[0] <= c and c <= r[1]: return True
    return c in chars and chars != ''

def isRange(c, ranges):
    for r in ranges:
        if r[0] <= c and c <= r[1]: return True
    return False

def gen_BRange(pe):
    if isbitset(pe):
        n = encode_bitset(pe)
        def bitmatch(px):
            if px.pos < px.length and (n & (1 << px.inputs[px.pos])) != 0:
                px.pos += 1
                return True
            return False
        return bitmatch
    # urange
    chars = pe.chars
    ranges = pe.ranges
    def urange(px):
        c = decode_char(px.inputs, px.pos)
        if isRangeChar(c, ranges, chars):
            px.pos += 1
            return True
        return False
    return urange

def gen_CRange(chars, ranges):
    def crange(px) :
        if px.pos < px.length and isRangeChar(px.inputs[px.pos], ranges, chars):
            px.pos += 1
            return True
        return False
    return crange

def gen_CRange2(chars, ranges, mov):
    clen = len(chars)
    rlen = len(ranges)
    if clen == 0:
        if rlen == 0:
            return lambda px: False
        elif rlen == 1:
            s1 = ranges[0][0]
            e1 = ranges[0][1]
            def range1(px):
                if px.pos < px.length:
                    c = px.inputs[px.pos]
                    if s1 <= c <= e1:
                        mov(px)
                        return True
                return False
            return range1
        elif rlen == 2:
            s1 = ranges[0][0]
            e1 = ranges[0][1]
            s2 = ranges[1][0]
            e2 = ranges[1][1]
            def range2(px):
                if px.pos < px.length:
                    c = px.inputs[px.pos]
                    if s1 <= c <= e1 or s2 <= c <= e2:
                        mov(px)
                        return True
                return False
            return range2
        else:
            #print('@range', rlen, clen, repr(chars))
            def crange(px):
                if px.pos < px.length and isRange(px.inputs[px.pos], ranges):
                    mov(px)
                    return True
                return False
            return crange
    else: # clen > 0
        if rlen == 0:
            def range0(px):
                if px.pos < px.length:
                    c = px.inputs[px.pos]
                    if c in chars:
                        mov(px)
                        return True
                return False
            return range0
        elif rlen == 1:
            s1 = ranges[0][0]
            e1 = ranges[0][1]
            def range1(px):
                if px.pos < px.length:
                    c = px.inputs[px.pos]
                    if s1 <= c <= e1 or c in chars:
                        mov(px)
                        return True
                return False
            return range1
        elif rlen == 2:
            s1 = ranges[0][0]
            e1 = ranges[0][1]
            s2 = ranges[1][0]
            e2 = ranges[1][1]
            def range2(px):
                if px.pos < px.length:
                    c = px.inputs[px.pos]
                    if s1 <= c <= e1 or s2 <= c <= e2 or c in chars:
                        mov(px)
                        return True
                return False
            return range2
        else:
            #print('@range', rlen, clen, repr(chars))
            def crange(px):
                if px.pos < px.length:
                    c = px.inputs[px.pos]
                    if isRange(c, ranges) or c in chars:
                        mov(px)
                        return True
                return False
            return crange

def ggen_Range(emit, option: ParserOption):
    if option.isByte:
        return lambda pe: gen_BRange(pe)
    else:
        return lambda pe: gen_CRange2(pe.chars, pe.ranges, mov=inc)

def gen_AndRange(pe: Range, isByte):
    pass

def gen_NotRange(pe: Range, isByte):
    pass

def gen_ManyRange(pe: Range, isByte):
    pass

def gen_Many1Range(pe: Range):
    pass

# Seq

def seq2(pfl, pfr):
    return lambda px: pfl(px) and pfr(px)

def seq3(pfa, pfb, pfc):
    return lambda px: pfa(px) and pfb(px) and pfc(px)

def seq4(pfa, pfb, pfc, pfd):
    return lambda px: pfa(px) and pfb(px) and pfc(px) and pfd(px)

def ggen_Seq(emit, option: ParserOption):
    def gen(pe):
        pfs = tuple(map(emit, pe.flatten([])))
        flen = len(pfs)
        if flen == 2:
            return seq2(pfs[0], pfs[1])
        elif flen == 3:
            return seq3(pfs[0], pfs[1], pfs[2])
        elif flen == 4:
            return seq4(pfs[0], pfs[1], pfs[2], pfs[3])
        #print('@seq', len(pfs))
        def seq(px):
            for pf in pfs:
                if not pf(px): return False
            return True
        return seq
    return gen

# Ore

def ore2(pfl, pfr):
    def curry(px):
        pos = px.pos
        ast = px.ast
        if not pfl(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return pfr(px)
        return True
    return curry

def ggen_Ore(emit, option: ParserOption):
    def gen(pe):
        pfs = tuple(map(emit, pe.flatten([])))
        if len(pfs) == 2:
            return ore2(pfs[0], pfs[1])
        #print('@ore', len(pfs), pe)
        def ore(px):
            pos = px.pos
            ast = px.ast
            for pf in pfs:
                if pf(px): return True
                px.headpos = max(px.pos, px.headpos)
                px.pos = pos
                px.ast = ast
            return False
        return ore
    return gen

# And
def ggen_And(emit, option: ParserOption):
    def gen(pe):
        if option.isOptimized:
            if isinstance(pe.inner, Char):
                return gen_AndChar(pe.inner)
            pass
        pf = emit(pe.inner)
        def andp(px):
            pos = px.pos
            if pf(px):
                px.headpos = max(px.pos, px.headpos)
                px.pos = pos
                return True
            return False
        return andp
    return gen

# Not

def ggen_Not(emit, option: ParserOption):
    def gen(pe):
        if option.isOptimized:
            if isinstance(pe.inner, Char):
                return gen_NotChar(pe.inner)
            pass
        pf = emit(pe.inner)
        def notp(px):
            pos = px.pos
            ast = px.ast
            if not pf(px):
                px.headpos = max(px.pos, px.headpos)
                px.pos = pos
                px.ast = ast
                return True
            return False
        return notp
    return gen

# Many

def ggen_Many(emit, option: ParserOption):
    def gen(pe):
        if option.isOptimized:
            if isinstance(pe.inner, Char):
                return gen_ManyChar(pe.inner)
            pass
        pf = emit(pe.inner)
        def many(px):
            pos = px.pos
            ast = px.ast
            while pf(px) and pos < px.pos:
                pos = px.pos
                ast = px.ast
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return True
        return many
    return gen

def ggen_Many1(emit, option: ParserOption):
    def gen(pe):
        if option.isOptimized:
            if isinstance(pe.inner, Char):
                return gen_Many1Char(pe.inner)
            pass
        pf = emit(pe.inner)
        def many1(px):
            pos = px.pos
            ast = px.ast
            c = 0
            while pf(px) and pos < px.pos:
                pos = px.pos
                ast = px.ast
                c += 1
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return c > 0
        return many1
    return gen


# Many1

# Tree

def ggen_TreeAs(emit, option: ParserOption):
    def gen(pe):
        tag = pe.name
        pf = emit(pe.inner)
        mtree = option.treeFunc
        def tree(px):
            pos = px.pos
            px.ast = None
            if pf(px):
                px.ast = mtree(tag, px.inputs, pos, px.pos, px.ast)
                return True
            return False
        return tree
    return gen

def ggen_LinkAs(emit, option: ParserOption):
    def gen(pe):
        tag = pe.name
        pf = emit(pe.inner)
        mlink = option.linkFunc
        def link(px):
            ast = px.ast
            if pf(px):
                px.ast = mlink(tag, px.ast, ast)
                return True
            return False
        return link
    return gen

def ggen_FoldAs(emit, option):
    def gen(pe):
        ltag = pe.left
        tag = pe.name
        pf = emit(pe.inner)
        mtree = option.treeFunc
        mlink = option.linkFunc

        def fold(px):
            pos = px.pos
            px.ast = mlink(ltag, px.ast, None)
            if pf(px):
                px.ast = mtree(tag, px.inputs, pos, px.pos, px.ast)
                return True
            return False
        return fold
    return gen

def ggen_Detree(emit, option):
    def gen(pe):
        pf = emit(pe.inner)
        def unit(px):
            ast = px.ast
            if pf(px):
                px.ast = ast
                return True
            return False
        return unit
    return gen

# SymbolTable

class StateTable(object):
    __slots__ = ['nameid', 'val', 'sprev']

    def __init__(self, nameid, val, sprev):
        self.nameid = nameid
        self.val = val
        self.sprev = sprev

STATEIDs = {}
def state_id(name):
    if not name in STATEIDs:
        STATEIDs[name] = len(STATEIDs)
    return STATEIDs[name]

def getstate(state, nameid):
    while state is not None:
        if state.nameid == nameid: return state
        state = state.sprev
    return None

def ggen_State(emit, option):
    def gen(pe):
        if pe.func == '@scope':
            pf = emit(pe.inner)
            def scope(px):
                state = px.state
                if pf(px):
                    px.state = state
                    return True
                return False
            return scope

        elif pe.func == '@newscope':
            pf = emit(pe.inner)
            def scope(px):
                state = px.state
                state = None
                if pf(px):
                    px.state = state
                    return True
                return False
            return scope

        elif pe.func == '@symbol':
            pf = emit(pe.inner)
            nid = state_id(pe.name)
            def symbol(px):
                pos = px.pos
                if pf(px):
                    px.state = StateTable(nid, px.inputs[pos:px.pos], px.state)
                    return True
                return False
            return symbol

        elif pe.func == '@exists':
            nid = state_id(pe.name)
            return lambda px: getstate(px.state, nid) != None

        elif pe.func == '@match':
            nid = state_id(pe.name)
            def match(px):
                state = getstate(px.state, nid)
                return state is not None and px.inputs.startswith(state.val, px.pos)
            return match

        elif pe.func == '@equals':
            pf = emit(pe.inner)
            nid = state_id(pe.name)
            def equals(px):
                pos = px.pos
                state = getstate(px.state, nid)
                return state is not None and pf(px) and px.inputs[pos:px:pos] == state.val
            return equals

        elif pe.func == '@contains':
            pf = emit(pe.inner)
            nid = state_id(pe.name)
            def contains(px):
                pos = px.pos
                state = getstate(px.state, nid)
                if state is not None and pf(px):
                    val = px.inputs[pos:px:pos]
                    while state is not None:
                        if state.val == val : return True
                        state = getstate(state)
                return False
            return contains

        else:
            def unknown(px):
                print('unknown', pe)
                return False
            return unknown

    return gen


# Ref

class MemoEntry(object):
    __slots__ = ['key', 'matched', 'mpos', 'mtree', 'mstate']
    def __init__(self):
        self.key = -1
        self.matched = False
        self.mpos = -1
        self.mtree = None
        self.mstate = None

class MemoPoint(object):
    __slots__ = ['name', 'nid', 'nterms', 'isTree']
    def __init__(self, name, nid, nterms, isTree):
        self.name = name
        self.nid = nid
        self.nterms = nterms
        self.isTree = isTree

def memoize(mp, pf):
    msize = mp.size
    mid = mp.mp
    if mp.isTree:
        def tmemo(px):
            if mp is None:
                return pf(px)
            else:
                key = msize * px.pos + mid
                memo = px.memos[key % 127]
                if memo.key == key and px.state is memo.state:
                    px.pos = memo.pos
                    px.ast = memo.ast
                    return memo.result
                memo.result = pf(px)
                memo.key = key
                memo.pos = px.pos
                memo.ast = px.ast
                memo.state = px.state
                return memo.result
        return tmemo
    else:
        def pmemo(px):
            if mp is None:
                return pf(px)
            else:
                key = msize * px.pos + mid
                memo = px.memos[key % 127]
                if memo.key == key and px.state is memo.state:
                    px.pos = memo.pos
                    return memo.result
                memo.result = pf(px)
                memo.key = key
                memo.pos = px.pos
                memo.state = px.state
                return memo.result
        return pmemo

def ggen_Ref(emit, memo: dict, option: ParserOption):
    def gen(ref):
        key = ref.uname()
        if not key in memo:
            memo[key] = lambda px: memo[key](px)
            memo[key] = emit(ref.deref())
            #memo[key] = emit_trace(ref, emit(ref.deref()))
        return memo[key]
    return gen

def setting(method, option: ParserOption):
    def emit(pe): return getattr(pe, method)()
    setattr(Empty, method, ggen_Empty(emit, option))
    setattr(Any, method, ggen_Any(emit, option))
    setattr(Char, method, ggen_Char(emit, option))
    setattr(Range, method, ggen_Range(emit, option))

    setattr(Seq, method, ggen_Seq(emit, option))
    setattr(Ore, method, ggen_Ore(emit, option))
    setattr(Alt, method, ggen_Ore(emit, option))
    setattr(Not, method, ggen_Not(emit, option))
    setattr(And, method, ggen_And(emit, option))
    setattr(Many, method, ggen_Many(emit, option))
    setattr(Many1, method, ggen_Many1(emit, option))

    setattr(TreeAs, method, ggen_TreeAs(emit, option))
    setattr(LinkAs, method, ggen_LinkAs(emit, option))
    setattr(FoldAs, method, ggen_FoldAs(emit, option))
    setattr(Detree, method, ggen_Detree(emit, option))

    # State
    setattr(State, method, ggen_State(emit, option))

    # Ref
    memo = {}
    setattr(Ref, method, ggen_Ref(emit, memo, option))

class ParserContext:
  __slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast', 'state']

  def __init__(self, inputs, urn='(unknown)', pos=0):
      self.inputs, self.pos = u.encode_source(inputs, urn, pos)
      self.length = len(self.inputs)
      self.headpos = self.pos
      self.ast = None
      self.state = None

def generate2(p, method = 'eval', isByte=False, conv = None):
    if not hasattr(Char, method):
        option = ParserOption()
        option.isByte = isByte
        setting(method, option)

    if not isinstance(p, ParsingExpression): # Grammar
        p = Ref(p.start().name, p)
    f = getattr(p, method)()

    def parse(s, urn = '(unknown)', pos = 0):
        if isByte:
            s = bytes(s, 'utf-8') if isinstance(s, str) else bytes(s)
        px = ParserContext(s, urn, pos)
        pos = px.pos
        result = None
        if not f(px):
            result = ParseTree("err", px.inputs, px.headpos, len(s), None)
        else:
            result = px.ast if px.ast is not None else ParseTree("", px.inputs, pos, px.pos, None)
        return conv(result) if conv is not None else result
    return parse

