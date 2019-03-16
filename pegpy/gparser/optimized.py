#from pegpy.gparser.base import *

import pegpy.gparser.base as base

gen_Empty = base.gen_Empty
gen_Empty= base.gen_Empty
gen_Any= base.gen_Any
gen_Char= base.gen_Char
gen_Range= base.gen_Range

gen_And= base.gen_And
gen_Not= base.gen_Not
gen_Many= base.gen_Many
gen_Many1= base.gen_Many1

gen_Seq= base.gen_Seq
gen_Ore= base.gen_Ore

gen_TreeAs= base.gen_TreeAs
gen_LinkAs= base.gen_LinkAs
gen_FoldAs= base.gen_FoldAs
gen_Detree= base.gen_Detree

# State
gen_State= base.gen_State
gen_Move = base.gen_Move

# Ref
gen_Ref= base.gen_Ref

### utils

def deref(pe):
    if isinstance(pe, base.Ref):
        pe2 = pe.deref()
        if isinstance(pe2, base.Char) or isinstance(pe2, base.Range) or pe2 == base.ANY or pe2 == base.EMPTY:
            return pe2
        return deref(pe2)
    return pe

def mov(pf, plen):
    def match(px):
        if pf(px):
            px.pos += plen
            return True
        return False
    return match

def not0(pf):
    return lambda px: not pf(px)

def many(pf):
    def match_many(px):
        while pf(px):
            px.pos += 1
        return True

    return match_many

def many1(pf):
    def match_many1(px):
        if pf(px):
            while pf(px): px.pos += 1
            return True
        return False

    return match_many1

# Empty

def gen_NotEmpty(pe, **option):
    def fail(px): return False
    return fail

# Char

def gen_AndChar(pe, **option):
    chars = pe.a
    return lambda px: px.inputs.startswith(chars, px.pos)

def gen_NotChar(pe, **option):
    chars = pe.a
    return lambda px: not px.inputs.startswith(chars, px.pos)

def gen_ManyChar(pe, **option):
    chars = pe.a
    clen = len(pe.a)
    def match(px):
        while px.inputs.startswith(chars, px.pos):
            px.pos += clen
        return True

    return match

def gen_Many1Char(pe, **option):
    chars = pe.a
    clen = len(pe.a)
    def match(px):
        if not px.inputs.startswith(chars, px.pos):
            return False
        px.pos += clen
        while px.inputs.startswith(chars, px.pos):
            px.pos += clen
        return True

    return match

# Range

def gen_AndRange(pe, **option):
    offset = pe.min()
    bitset = base.first(pe) >> offset
    def bitmatch(px):
        if px.pos < px.length:
            shift = ord(px.inputs[px.pos]) - offset
            if shift >= 0 and (bitset & (1 << shift)) != 0:
                return True
        return False

    return bitmatch

def gen_NotRange(pe, **option):
    return not0(gen_AndRange(pe, **option))

def gen_ManyRange(pe, **option):
    return many(gen_AndRange(pe, **option))

def gen_Many1Range(pe, **option):
    return many1(gen_AndRange(pe, **option))

def gen_Range(pe, **option):
    offset = pe.min()
    bitset = base.first(pe) >> offset
    def bitmatch(px):
        if px.pos < px.length:
            shift = ord(px.inputs[px.pos]) - offset
            if shift >= 0 and (bitset & (1 << shift)) != 0:
                px.pos += 1
                return True
        return False

    return bitmatch

# Any

def gen_AndAny(pe, **option):
    return lambda px : px.pos < px.length

def gen_NotAny(pe, **option):
    return lambda px : px.pos >= px.length

def gen_ManyAny(pe, **option):
    def match(px):
        px.pos = px.length
        return True
    return match

def gen_Many1Any(pe, **option):
    def match(px):
        if px.pos < px.length:
            px.pos = px.length
            return True
        return False
    return match

# Not

def gen_And(pe, **option):
    pi = deref(pe.inner)
    if isinstance(pi, base.Char):
        return gen_AndChar(pi, **option)
    elif isinstance(pi, base.Range):
        return gen_AndRange(pi, **option)
    elif pi == base.ANY:
        return gen_AndAny(pi, **option)
    elif pi == base.EMPTY:
        return gen_Empty(pi, **option)
    return base.gen_And(pe, **option)

# Not

def gen_Not(pe, **option):
    pi = deref(pe.inner)
    if isinstance(pi, base.Char):
        return gen_NotChar(pi, **option)
    elif isinstance(pi, base.Range):
        return gen_NotRange(pi, **option)
    elif pi == base.ANY:
        return gen_NotAny(pi, **option)
    elif pi == base.EMPTY:
        return gen_NotEmpty(pi, **option)
    return base.gen_Not(pe, **option)

# Many

def gen_Many(pe, **option):
    pi = deref(pe.inner)
    if isinstance(pi, base.Char):
        return gen_ManyChar(pi, **option)
    elif isinstance(pi, base.Range):
        return gen_ManyRange(pi, **option)
    elif pi == base.ANY:
        return gen_ManyAny(pi, **option)
    return base.gen_Many(pe, **option)

def gen_Many1(pe, **option):
    pi = deref(pe.inner)
    if isinstance(pi, base.Char):
        return gen_Many1Char(pi, **option)
    elif isinstance(pi, base.Range):
        return gen_Many1Range(pi, **option)
    elif pi == base.ANY:
        return gen_Many1Any(pi, **option)
    return base.gen_Many1(pe, **option)

#Seq

def seq2(pfa, pfb):
    return lambda px: pfa(px) and pfb(px)

def seq3(pfa, pfb, pfc):
    return lambda px: pfa(px) and pfb(px) and pfc(px)

def seq4(pfa, pfb, pfc, pfd):
    return lambda px: pfa(px) and pfb(px) and pfc(px) and pfd(px)

def seq(fs):
    flen = len(fs)
    if flen == 2:
        return seq2(fs[0], fs[1])
    elif flen == 3:
        return seq3(fs[0], fs[1], fs[2])
    elif flen == 4:
        return seq4(fs[0], fs[1], fs[2], fs[3])
    else:
        return seq4(fs[0], fs[1], fs[2], seq(fs[3:]))

def opz_Seq(es, **option):
    return es

def gen_Seq(pe, **option):
    emit = option['emit']
    es = base.flatten(pe, [], base.Seq)
    es = opz_Seq(es, **option)
    return seq(list(map(lambda p: emit(p, **option), es)))

#Ore, Alt

def ore2(pfa, pfb):
    def match(px):
        pos = px.pos
        ast = px.ast
        if pfa(px): return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        return pfb(px)

    return match

def ore3(pfa, pfb, pfc):
    def match(px):
        pos = px.pos
        ast = px.ast
        if pfa(px): return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        if pfb(px): return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        return pfc(px)

    return match

def ore4(pfa, pfb, pfc, pfd):
    def match(px):
        pos = px.pos
        ast = px.ast
        if pfa(px): return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        if pfb(px): return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        if pfc(px): return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        return pfd(px)

    return match

def ore(fs):
    flen = len(fs)
    if flen == 2:
        return ore2(fs[0], fs[1])
    elif flen == 3:
        return ore3(fs[0], fs[1], fs[2])
    elif flen == 4:
        return ore4(fs[0], fs[1], fs[2], fs[3])
    else:
        return ore4(fs[0], fs[1], fs[2], ore(fs[3:]))

def gen_Ore(pe, **option):
    emit = option['emit']
    #es = pe.flatten([])
    es2 = base.flatten(pe, [], base.Ore)
    #print(es)
    #print(es2)
    return ore(list(map(lambda p: emit(p, **option), es2)))

gen_Alt= gen_Ore

