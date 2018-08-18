from pegpy.parsefunc import *

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

def union(old, new, mtree):
    result = {}
    for pos in set(old) & set(new):
        result[pos] = mtree("Ambiguity", old[pos], new[pos])
    for pos in set(old) - set(new):
        result[pos] = old[pos]
    for pos in set(new) - set(old):
        result[pos] = new[pos]
    return result
    

#GChar

def emit_GChar(pe):
    if len(pe.a)>1:
        return mresult(multi(pe.a, len(pe.a)))
    if not pe.a in pf_char:
        pf_char[pe.a] = mresult(char(pe.a))
    return pf_char[pe.a]

#GByte

def emit_GByte(pe):
    if len(pe.a)>1:
        b = bytes(pe.a, 'utf-8')
        return mresult(multi(b, len(b)))
    c = ord(pe.a)
    key = str(c)
    if not key in pf_char:
        pf_char[key] = mresult(char(c))
    return pf_char[key]

#GRange

def emit_GByteRange(pe):
    n = 0
    for c in pe.chars:
        n |= (1 << ord(c))
    for r in pe.ranges:
        for c in range(ord(r[0]), ord(r[1])+1):
            n |= (1 << c)
    return mresult(bits(n))

def emit_GCharRange(pe):
    chars = pe.chars
    ranges = pe.ranges
    def curry(px) :
        if px.pos < px.length and isCharRange(px.inputs[px.pos], ranges, chars):
            px.pos += 1
            px.headpos = max(px.pos, px.headpos)
            return True
        return False
    return mresult(curry)
        
# GSeq

def gseq2(left, right, mtree):
    def curry(px):
        result = {}
        if left(px):
            lresult = px.result
            for pos, ast in lresult.items():
                px.result = {}
                px.pos = pos
                px.ast = ast
                if right(px):
                    result = union(result, px.result, mtree)
            px.result = result
            return False if len(px.result) == 0 else True
        return False
    return curry


def gseq(ls, mtree):
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
                    result = union(result, px.result, mtree)
                else:
                    return False
            px.result = result
            result = {}
        return False if len(px.result) == 0 else True
    return curry

def emit_GSeq(pe, emit, mtree):
    ls = tuple(map(emit, pe.flatten([])))
    if len(ls) == 2:
        return gseq2(ls[0], ls[1], mtree)
    return gseq(ls, mtree)

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

def alt2(left, right, mtree):
    def curry(px):
        pos = px.pos
        ast = px.ast
        if not left(px):
            px.pos = pos
            px.ast = ast
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
                px.result = union(lresult, px.result, mtree)
        return True
    return curry

def alt(ls, mtree):
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
                result = union(result, px.result, mtree)
                px.result = {}
        px.result = result
        return False if len(px.result) == 0 else True
    return curry

def emit_GAlt(pe, emit, mtree):
    ls = tuple(map(emit, pe.flatten([])))
    if len(ls) == 2:
        return alt2(ls[0], ls[1], mtree)
    return alt(ls, mtree)

# Many

def rec_gmany(pf, px, mtree):
    fresult = {}
    sresult = {}
    presult = px.result
    for pos, ast in presult.items():
        px.result = {}
        px.ast = ast
        px.pos = pos
        if pf(px) and pos < px.pos:
            sresult = union(sresult, rec_gmany(pf, px, mtree), mtree)
        else:
            fresult[pos] = ast
    return union(fresult, sresult, mtree)

def gmany(pf, mtree):
    def curry(px):
        pos = px.pos
        ast = px.ast
        if pf(px) and pos < px.pos:
            px.result = rec_gmany(pf, px, mtree)
        else:
            px.pos = pos
            px.ast = ast
            px.result[pos] = ast
        return True
    return curry

def emit_GMany(pe, emit, mtree):
    return gmany(emit(pe.inner), mtree)

def emit_GMany1(pe, emit, mtree):
    return gseq2(emit(pe.inner), gmany(emit(pe.inner), mtree), mtree)

#Not
def gnot(pf):
    def curry(px):
        pos = px.pos
        ast = px.ast
        if not pf(px):
            px.pos = pos
            px.ast = ast
            px.result = {pos:ast}
            return True
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
    return gtree(pe.tag, emit(pe.inner), mtree)

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
    return glink(pe.tag, emit(pe.inner), mlink)

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
    return gfold(pe.ltag, pe.tag, emit(pe.inner), mtree, mlink)

def gunit(pf):
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

def emit_GUnit(pe, emit):
    return gunit(emit(pe.inner))