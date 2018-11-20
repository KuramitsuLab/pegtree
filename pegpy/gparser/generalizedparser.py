from pegpy.parser import *
import functools

check_header = [1] * 0xc0 + [2] * (0xe0 - 0xc0) + [3] * (0xf0 - 0xe0) + [4] * (0xff - 0xf0 + 1)

# generalized parse function

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

def p_GTrue(px): return True


def emit_char(c):
    def curry(px):
        if px.pos < px.length and px.inputs[px.pos] == c:
            px.pos += 1
            px.headpos = max(px.pos, px.headpos)
            return True
        return False
    return curry

# Str

def emit_multi(s, slen):
    def curry(px):
        if px.inputs.startswith(s, px.pos):
            px.pos += slen
            px.headpos = max(px.pos, px.headpos)
            return True
        return False
    return curry


pf_char = {}


def bits(n, offset=0):
    def curry(px):
        if px.pos < px.length:
            shift = px.inputs[px.pos] - offset
            if shift >= 0 and (n & (1 << shift)) != 0:
                px.pos += 1
                px.headpos = max(px.pos, px.headpos)
                return True
        return False
    return curry


def multi_bits(n, offset=0):
    def curry(px):
        if px.pos < px.length:
            move = px.pos + check_header[px.inputs[px.pos]]
            shift = ord(str(px.inputs[px.pos:move], 'utf-8')) - offset
            if shift >= 0 and (n & (1 << shift)) != 0:
                px.pos = move
                px.headpos = max(px.pos, px.headpos)
                return True
        return False
    return curry


def isCharRange(c, ranges, chars):
    for r in ranges:
        if r[0] <= c and c <= r[1]:
            return True
    for c2 in chars:
        if c == c2:
            return True
    return False

#GAny

def p_GAny(px):
    if px.pos < px.length:
        px.pos += check_header[px.inputs[px.pos]]
        px.headpos = max(px.pos, px.headpos)
        return True
    return False

#GChar

def emit_GChar(pe):
    if len(pe.a)>1:
        return mresult(emit_multi(pe.a, len(pe.a)))
    if not pe.a in pf_char:
        pf_char[pe.a] = mresult(emit_char(pe.a))
    return pf_char[pe.a]

#GByte

def emit_GByte(pe):
    b = bytes(pe.a, 'utf-8')
    if len(b)>1:
        return mresult(emit_multi(b, len(b)))
    c = ord(pe.a)
    key = str(c)
    if not key in pf_char:
        pf_char[key] = emit_char(c)
    return mresult(pf_char[key])

#GRange

def emit_GByteRange(pe):
    n = 0
    offset = min(list(map(lambda c: ord(c), pe.chars)) + [ord(x[0]) for x in pe.ranges])
    for c in pe.chars:
        n |= (1 << (ord(c) - offset))
    for r in pe.ranges:
        for c in range(ord(r[0])-offset, ord(r[1])+1-offset):
            n |= (1 << c)
    return mresult(bits(n, offset)) if offset < 0x80 and n < (1 << (0x80 - offset)) else mresult(multi_bits(n, offset))


def emit_GCharRange(pe):
    chars = pe.chars
    ranges = pe.ranges

    def curry(px):
        if px.pos < px.length and isCharRange(px.inputs[px.pos], ranges, chars):
            px.pos += 1
            px.headpos = max(px.pos, px.headpos)
            return True
        return False
    return mresult(curry)

# GSeq

def gseq2(left, right, mtree, mlink):
    def curry(px):
        result = {}
        if left(px):
            lresult = px.result
            for pos, ast in lresult.items():
                px.result = {}
                px.pos = pos
                px.ast = ast
                if right(px):
                    result = union(px, result, pos, mtree, mlink)
            px.result = result
            return False if len(px.result) == 0 else True
        return False
    return curry


def gseq(ls, mtree, mlink):
    def curry(px):
        result = {}
        if not ls[0](px):
            return False
        for p in ls[1:]:
            presult = px.result
            for pos, ast in presult.items():
                px.result = {}
                px.pos = pos
                px.ast = ast
                if p(px):
                    result = union(px, result, pos, mtree, mlink)
            px.result = result
            result = {}
        return False if len(px.result) == 0 else True
    return curry

def emit_GSeq(pe, emit, mtree, mlink):
    ls = tuple(map(emit, pe.flatten([])))
    if len(ls) == 2:
        return gseq2(ls[0], ls[1], mtree, mlink)
    return gseq(ls, mtree, mlink)

# OrElse

def gor2(left, right):
    def curry(px):
        pos = px.pos
        ast = px.ast
        if not left(px):
            px.pos = pos
            px.ast = ast
            px.result = {pos:ast}
            return right(px)
        return True
    return curry

def gor(ls):
    def curry(px):
        pos = px.pos
        ast = px.ast
        for p in ls:
            if p(px): return True
            px.pos = pos
            px.ast = ast
            px.result = {pos:ast}
        return False
    return curry

def emit_GOr(pe, emit):
    ls = tuple(map(emit, pe.flatten([])))
    if len(ls) == 2:
        return gor2(ls[0], ls[1])
    return gor(ls)

#GAlt

def alt2(left, right, mtree, mlink):
    def curry(px):
        pos = px.pos
        ast = px.ast
        if not left(px):
            px.pos = pos
            px.ast = ast
            px.result = {}
            return right(px)
        else:
            px.pos = pos
            px.ast = ast
            lresult = px.result
            px.result = {}
            if not right(px):
                px.result = lresult
                return True
            else:
                px.result = union(px, lresult, pos, mtree, mlink)
        return True
    return curry

def alt(ls, mtree, mlink):
    def curry(px):
        result = {}
        for p in ls:
            pos = px.pos
            ast = px.ast
            if not p(px):
                px.pos = pos
                px.ast = ast
                continue
            else:
                result = union(px, result, pos, mtree, mlink)
                px.result = {}
        px.result = result
        return False if len(px.result) == 0 else True
    return curry

def emit_GAlt(pe, emit, mtree, mlink):
    ls = tuple(map(emit, pe.flatten([])))
    if len(ls) == 2:
        return alt2(ls[0], ls[1], mtree, mlink)
    return alt(ls, mtree, mlink)

# Many

def rec_gmany(pf, px, mtree, mlink):
    fresult = {}
    sresult = {}
    presult = px.result
    ppos = px.pos
    for pos, ast in presult.items():
        px.result = {}
        px.ast = ast
        px.pos = pos
        if pf(px) and pos < px.pos:
            px.result = rec_gmany(pf, px, mtree, mlink)
            sresult = union(px, sresult, pos, mtree, mlink)
        else:
            fresult[pos] = ast
    px.result = sresult
    return union(px, fresult, ppos, mtree, mlink)

def gmany(pf, mtree, mlink):
    def curry(px):
        pos = px.pos
        ast = px.ast
        if pf(px) and pos < px.pos:
            px.result = rec_gmany(pf, px, mtree, mlink)
        else:
            px.pos = pos
            px.ast = ast
            px.result[pos] = ast
        return True
    return curry

def emit_GMany(pe, emit, mtree, mlink):
    return gmany(emit(pe.inner), mtree, mlink)

def emit_GMany1(pe, emit, mtree, mlink):
    return gseq2(emit(pe.inner), gmany(emit(pe.inner), mtree, mlink), mtree, mlink)

#Not
def gnot(pf):
    def curry(px):
        pos = px.pos
        ast = px.ast
        if not pf(px):
            px.pos = pos
            px.ast = ast
            px.result = {pos: ast}
            return True
        px.pos = pos
        px.ast = ast
        px.result = {}
        return False
    return curry

def emit_GNot(pe, emit):
    return gnot(emit(pe.inner))

# And
def gand(pf):
    def curry(px):
        pos = px.pos
        if pf(px):
            px.pos = pos
            px.result = {px.pos:px.ast}
            return True
        return False
    return curry

def emit_GAnd(pe, emit):
    return gand(emit(pe.inner))

# Ref
def emit_GRef(ref: Ref, memo: dict, emit):
    key = ref.uname()
    if not key in memo:
        memo[key] = lambda px: memo[key](px)
        memo[key] = emit(ref.deref())
        #memo[key] = emit_trace(ref, emit(ref.deref()))
    return memo[key]


#GTree
def gtree(tag, pf, mtree):
    def curry(px):
        ppos = px.pos
        px.ast = None
        if pf(px):
            for pos, ast in px.result.items():
                px.result[pos] = mtree(tag, px.inputs, ppos, pos, ast)
            return True
        px.result[ppos] = None
        return False
    return curry

def emit_GTreeAs(pe, emit, mtree):
    return gtree(pe.name, emit(pe.inner), mtree)

def glink(tag, pf, mlink):
    def curry(px):
        ppos = px.pos
        past = px.ast
        if pf(px):
            for pos, ast in px.result.items():
                px.result[pos] = mlink(tag, ast, past)
            return True
        px.result[ppos] = past
        return False
    return curry

def emit_GLinkAs(pe, emit, mlink):
    return glink(pe.name, emit(pe.inner), mlink)

def gfold(ltag, tag, pf, mtree, mlink):
    def curry(px):
        ppos = px.pos
        px.ast = mlink(ltag, px.ast, None)
        past = px.ast
        if pf(px):
            for pos, ast in px.result.items():
                px.result[pos] = mtree(tag, px.inputs, ppos, pos, ast)
            return True
        px.result[ppos] = past
        return False
    return curry

def emit_GFoldAs(pe, emit, mtree, mlink):
    return gfold(pe.left, pe.name, emit(pe.inner), mtree, mlink)

def gdetree(pf):
    def curry(px):
        ppos = px.pos
        past = px.ast
        if pf(px):
            for pos, _ in px.result.items():
                px.result[pos] = past
            return True
        px.result[ppos] = past
        return False
    return curry

def emit_GDetree(pe, emit):
    return gdetree(emit(pe.inner))
