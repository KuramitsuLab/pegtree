from collections import namedtuple
from .tree import ParseTree

# PContext


class PContext:
    __slots__ = ['inputs', 'pos', 'epos',
                 'headpos', 'ptree', 'state', 'memo', 'dic']

    def __init__(self, inputs, spos, epos):
        self.inputs = inputs
        self.pos = spos
        self.epos = epos
        self.headpos = spos
        self.ptree = None
        self.state = None
        self.memo = [PMemo() for x in range(1789)]
        self.dic = {}


# '' pEmpty()

def match_empty(px: PContext):
    return True


def pEmpty():
    return match_empty


# !'' pFail()

def pFail():
    return lambda px: False

# . pAny()


def match_any(px: PContext):
    if px.pos < px.epos:
        px.pos += 1
        return True
    return False


def pAny():
    return match_any

# a pChar(a)


CharDB = {
    '': match_empty
}


def pChar(text):
    if text in CharDB:
        return CharDB[text]

    clen = len(text)

    def match(px: PContext):
        if px.inputs.startswith(text, px.pos):
            px.pos += clen
            return True
        return False
    CharDB[text] = match
    return match


# [abcA-Z] pRange('abc', 'A-Z')


def make_allchars(chars, ranges):
    cs = set(list(chars))
    rs = ranges
    while len(rs) > 0:
        r = range(ord(rs[0]), ord(rs[1])+1)
        cs |= set(map(chr, r))
        rs = rs[2:]
    return ''.join(sorted(cs))


def make_bitset(chars, ranges, NBITS=8):
    cmin = min(map(ord, list(chars+ranges)))-1
    bitmap = [0] * ((max(map(ord, list(chars+ranges))) - cmin) // NBITS + 1)
    for c in chars:
        n = (ord(c) - cmin) // NBITS
        mask = 1 << (ord(c) - cmin) % NBITS
        bitmap[n] |= mask
    r = ranges
    while len(r) > 1:
        for c in range(ord(r[0]), ord(r[1])+1):
            n = (c - cmin) // NBITS
            mask = 1 << (c - cmin) % NBITS
            bitmap[n] |= mask
        r = r[2:]
    return bitmap, cmin, len(bitmap)*NBITS


# def match_chars(px, chars):
#     return px.pos < px.epos and chars.find(px.inputs[px.pos]) != -1

# def match_bitset(px, bitset, offset, maxlen):
#     if px.pos < px.epos:
#         c = ord(px.inputs[px.pos]) - offset
#         if c < 0 or c >= maxlen:
#             return False
#         mask = 1 << c % 8
#         return bitset[c//8] & mask == mask
#     return False

BitsetDB = {}


def check_range(chars, ranges=''):
    if isinstance(chars, tuple):
        return chars[0], chars[1]
    return chars, ranges


def pAndRange(chars, ranges=''):
    chars, ranges = check_range(chars, ranges)
    allchars = make_allchars(chars, ranges)

    if len(allchars) < 1000:
        def match(px):
            return px.pos < px.epos and allchars.find(px.inputs[px.pos]) != -1
        return match

    if allchars not in BitsetDB:
        BitsetDB[allchars] = make_bitset(chars, ranges)

    bitset, offset, maxlen = BitsetDB[allchars]

    def match(px: PContext):
        if px.pos < px.epos:
            c = ord(px.inputs[px.pos]) - offset
            if c < 0 or c >= maxlen:
                return False
            mask = 1 << (c % 8)
            return bitset[c//8] & mask == mask
        return False
    return match


def pRange(chars, ranges=''):
    pf = pAndRange(chars, ranges)

    def match(px: PContext):
        if pf(px):
            px.pos += 1
            return True
        return False
    return match

# &e, pAnd(e)


def pAnd_(e):
    def match(px: PContext):
        pos = px.pos
        if e(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            return True
        return False
    return match


def pAndChar(text):
    def match(px: PContext):
        return px.inputs.startswith(text, px.pos)
    return match


def pAnd(e):
    if isinstance(e, str):
        return pAndChar(e)
    elif isinstance(e, tuple):
        return pAndRange(e)
    else:
        return pAnd_(e)

# !e pNot(e)


def pNot_(e):
    def match(px: PContext):
        pos = px.pos
        ptree = px.ptree
        if not e(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ptree = ptree
            return True
        return False
    return match


def pNotChar(text):
    def match_notchar(px: PContext):
        return not px.inputs.startswith(text, px.pos)
    return match_notchar


def pNotRange(chars, ranges=''):
    e = pAndRange(chars, ranges)
    return lambda px: not e(px)


def pNot(e):
    if isinstance(e, str):
        return pNotChar(e)
    elif isinstance(e, tuple):
        return pNotRange(e)
    else:
        return pNot_(e)


# e* pMany(e)

def pMany_(e):
    def match(px: PContext):
        pos = px.pos
        ptree = px.ptree
        while e(px) and pos < px.pos:
            pos = px.pos
            ptree = px.ptree
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        return True
    return match


def pManyChar(text):
    clen = len(text)

    def match(px: PContext):
        while px.inputs.startswith(text, px.pos):
            px.pos += clen
        return True
    return match


def pManyRange(chars, ranges=''):
    e = pAndRange(chars, ranges)

    def match(px: PContext):
        while e(px):
            px.pos += 1
        return True
    return match


def pMany(e):
    if isinstance(e, str):
        return pManyChar(e)
    elif isinstance(e, tuple):
        return pManyRange(e)
    else:
        return pMany_(e)

# e! pOneMany(e)


def pOneMany_(e):
    def match(px: PContext):
        if e(px):
            pos = px.pos
            ptree = px.ptree
            while e(px) and pos < px.pos:
                pos = px.pos
                ptree = px.ptree
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ptree = ptree
            return True
        return False
    return match


def pOneManyChar(text):
    clen = len(text)

    def match(px: PContext):
        if px.inputs.startswith(text, px.pos):
            px.pos += clen
            while px.inputs.startswith(text, px.pos):
                px.pos += clen
            return True
        return False
    return match


def pOneManyRange(chars, ranges=''):
    e = pAndRange(chars, ranges)

    def match(px: PContext):
        c = 0
        while e(px):
            px.pos += 1
            c += 1
        return c > 0
    return match


def pOneMany(e):
    if isinstance(e, str):
        return pOneManyChar(e)
    elif isinstance(e, tuple):
        return pOneManyRange(e)
    else:
        return pOneMany_(e)


# e? pOption(e)

def pOption_(e):
    def match(px: PContext):
        pos = px.pos
        ptree = px.ptree
        if not e(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ptree = ptree
        return True
    return match


def pOptionChar(text):
    clen = len(text)

    def match(px: PContext):
        if px.inputs.startswith(text, px.pos):
            px.pos += clen
        return True
    return match


def pOptionRange(chars, ranges):
    e = pAndRange(chars, ranges)

    def match(px: PContext):
        if e(px):
            px.pos += 1
        return True
    return match


def pOption(e):
    if isinstance(e, str):
        return pOptionChar(e)
    elif isinstance(e, tuple):
        return pOptionRange(e)
    else:
        return pOption_(e)


# Seq

def pSeq2(e, e2):
    def match(px: PContext):
        return e(px) and e2(px)
    return match


def pSeq3(e, e2, e3):
    def match(px: PContext):
        return e(px) and e2(px) and e3(px)
    return match


def pSeq4(e, e2, e3, e4):
    def match(px: PContext):
        return e(px) and e2(px) and e3(px) and e4(px)
    return match


def pSeq(*es):
    def match(px: PContext):
        for e in es:
            if not e(px):
                return False
        return True
    return match

# Ore


def pOre2(e, e2):
    def match(px: PContext):
        pos = px.pos
        ptree = px.ptree
        if e(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        return e2(px)
    return match


def pOre3(e, e2, e3):
    def match(px: PContext):
        pos = px.pos
        ptree = px.ptree
        if e(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        if e2(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        return e3(px)
    return match


def pOre4(e, e2, e3, e4):
    def match(px: PContext):
        pos = px.pos
        ptree = px.ptree
        if e(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        if e2(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        if e3(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        return e4(px)
    return match


def pOre(*es):
    def match(px: PContext):
        pos = px.pos
        ptree = px.ptree
        for e in es:
            if e(px):
                return True
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ptree = ptree
        return False
    return match

# pDict('a b c')


def make_trie(dic):
    if '' in dic or len(dic) < 10:
        return dic
    d = {}
    for s in dic:
        s0, s = s[0], s[1:]
        if s0 in d:
            ss = d[s0]
            if not s in ss:
                ss.append(s)
        else:
            d[s0] = [s]
    for key in d:
        d[key] = make_trie(d[key])
    return d


def match_trie(px, d):
    if px.pos >= px.epos:
        return False
    if isinstance(d, dict):
        c = px.inputs[px.pos]
        if c in d:
            px.pos += 1
            return match_trie(px, d[c])
        return False
    pos = px.pos
    inputs = px.inputs
    for s in d:
        if inputs.startswith(s, pos):
            px.pos += len(s)
            return True
    return False


def pDict(words):
    if isinstance(words, str):
        words = words.split(' ')
    dic = make_trie(words)
    return lambda px: match_trie(px, dic)


# def pRef(generated, uname):
#     if uname not in generated:
#         fs = None

#         def match_deref(px):
#             nonlocal fs
#             if fs is None:
#                 fs = generated[uname]
#             return fs(px)
#         generated[uname] = match_deref
#     return generated[uname]


def pRef(generated, uname):
    if uname not in generated:
        generated[uname] = lambda px: generated[uname](px)
    return generated[uname]


class PMemo(object):
    __slots__ = ['key', 'pos', 'treeState', 'ptree', 'prev', 'result']

    def __init__(self):
        self.key = -1
        self.pos = 0
        self.treeState = False
        self.ptree = None
        self.prev = None
        self.result = False


def pMemo(fs, mp, mpsize):
    disabled = False
    hit = 0
    miss = 0

    def match(px: PContext):
        nonlocal disabled, hit, miss
        if disabled:
            return fs(px)
        key = (mpsize * px.pos) + mp
        m = px.memo[key % 1789]
        if m.key == key:
            if m.treeState:
                if m.prev == px.ptree:
                    px.pos = m.pos
                    px.ptree = m.ptree
                    hit += 1
                    return m.result
            else:
                px.pos = m.pos
                hit += 1
                return m.result
        prev = px.ptree
        m.result = fs(px)
        m.pos = px.pos
        m.key = key
        if m.result and prev != px.ptree:
            m.treeState = True
            m.prev = prev
            m.ptree = px.ptree
        else:
            m.treeState = False
        miss += 1
        if miss % 100 == 0:
            if hit / miss < 5:
                disabled = True
        return m.result
    return match


def pMemoDebug(name, fs, mp, mps):
    disabled = False
    hit = 0
    miss = 0
    mpsize = len(mps)

    def match(px: PContext):
        nonlocal disabled, hit, miss
        if disabled:
            return fs(px)
        key = (mpsize * px.pos) + mp
        m = px.memo[key % 1789]
        if m.key == key:
            if m.treeState:
                if m.prev == px.ptree:
                    px.pos = m.pos
                    px.ptree = m.ptree
                    hit += 1
                    return m.result
            else:
                px.pos = m.pos
                hit += 1
                return m.result
        prev = px.ptree
        m.result = fs(px)
        m.pos = px.pos
        m.key = key
        if m.result and prev != px.ptree:
            m.treeState = True
            m.prev = prev
            m.ptree = px.ptree
        else:
            m.treeState = False
        miss += 1
        if miss % 100 == 0:
            if hit / miss < 5:
                mps.remove(name)
                print('enabled', mps)
                disabled = True
        return m.result
    return match


# Tree Construction


class PTree(object):
    __slots__ = ['prev', 'tag', 'spos', 'epos', 'child']

    def __init__(self, prev, tag, spos, epos, child):
        self.prev = prev
        self.tag = tag
        self.spos = spos
        self.epos = epos
        self.child = child

    def isEdge(self):
        return self.epos < 0

    def dump(self, inputs):
        sb = []
        if self.prev is not None:
            sb.append(self.prev.dump(inputs))
            sb.append(',')
        sb.append(f'{{#{self.tag} ')
        if self.child is None:
            sb.append(repr(inputs[self.spos:self.epos]))
        else:
            sb.append(self.child.dump(inputs))
        sb.append('}')
        return ''.join(sb)


def pNode(e, tag, shift):
    def make(px: PContext):
        pos = px.pos
        prev = px.ptree
        px.ptree = None
        if e(px):
            px.ptree = PTree(prev, tag, pos+shift, px.pos, px.ptree)
            return True
        return False
    return make


def pEdge(edge, e, shift=0):
    def match(px: PContext):
        pos = px.pos
        prev = px.ptree
        px.ptree = None
        if e(px):
            if px.ptree is None:
                px.ptree = PTree(None, '', pos+shift, px.pos, px.ptree)
            px.ptree = PTree(prev, edge, -1, -1, px.ptree)
            return True
        return False
    return match


def popPTree(px):
    pt = px.ptree
    if pt is None:
        return px.pos, None
    if pt.prev is None:
        px.ptree = pt
        return pt.spos, None
    px.ptree = PTree(None, pt.tag, pt.spos, pt.epos, pt.child)
    return pt.spos, pt.prev


def pFold(edge, e, tag, shift):
    if edge == '':
        def match(px: PContext):
            pos, prev = popPTree(px)
            if e(px):
                px.ptree = PTree(prev, tag, pos, px.pos, px.ptree)
                return True
            return False
        return match
    else:
        def match(px: PContext):
            pos, prev = popPTree(px)
            px.ptree = PTree(None, edge, -1, -1, px.ptree)
            if e(px):
                px.ptree = PTree(prev, tag, pos, px.pos, px.ptree)
                return True
            return False
        return match


def pAbs(e):
    def match(px: PContext):
        ptree = px.ptree
        if e(px):
            px.ptree = ptree
            return True
        return False
    return match


def pSkip():  # @skip()
    def skip(px: PContext):
        px.pos = min(px.headpos, px.epos)
        return True
    return skip


# State


State = namedtuple('State', 'sid val prev')


def getstate(state, sid):
    while state is not None:
        if state.sid == sid:
            return state
        state = state.prev
    return None


def pSymbol(e, sid):  # @symbol(A)
    def match(px: PContext):
        pos = px.pos
        if e(px):
            px.state = State(sid, px.inputs[pos:px.pos], px.state)
            return True
        return False
    return match


def pScope(e):
    def match(px: PContext):
        state = px.state
        res = e(px)
        px.state = state
        return res
    return match


def pExists(sid):  # @Match(A)
    return lambda px: getstate(px.state, sid) != None


def pMatch(sid):  # @Match(A)
    def match(px: PContext):
        state = getstate(px.state, sid)
        if state is not None and px.inputs.startswith(state.val, px.pos):
            px.pos += len(state.val)
            return True
        return False
    return match


def pDef(name, e):
    def define_dic(px: PContext):
        pos = px.pos
        if e(px):
            s = px.inputs[pos:px.pos]
            if len(s) == 0:
                return True
            if name not in px.dic:
                px.dic[name] = []
            ss = px.dic[name]
            ss.append(s)
            px.dic[name] = sorted(ss, key=lambda x: len(x))[::-1]
            # print(px.dic[name])
            return True
        return False
    return define_dic


def pIn(name):  # @in(NAME)
    def match(px: PContext):
        # print('@matching', name, px.inputs, px.pos)
        if name in px.dic:
            ss = px.dic[name]
            for s in ss:
                if px.inputs.startswith(s, px.pos):
                    # print('@matched', s)
                    px.pos += len(s)
                    return True
            # print('@', px.inputs[px.pos:], ss)
        return False
    return match

# generate


def PTreeConv(pt: PTree, urn, inputs):
    if pt.prev != None:
        ct = pt
        while ct.prev is not None:
            ct = ct.prev
        return PTreeConvNode('', urn, inputs, ct.spos, pt.epos, pt)
    if pt.isEdge():
        ct = PTreeConv(pt.child, urn, inputs)
        t = ParseTree('', inputs, ct.spos_, ct.epos_, urn)
        t.set(pt.tag, ct)
        return t
    else:
        return PTreeConvNode(pt.tag, urn, inputs, pt.spos, pt.epos, pt.child)


def PTreeConvNode(tag, urn, inputs, spos, epos, subnode):
    t = ParseTree(tag, inputs, spos, epos, urn)
    while subnode != None:
        if subnode.isEdge():
            # if subnode.child == None:
            #     tt = PTreeConvNode(
            #         '', urn, inputs, subnode.spos, abs(subnode.epos), None)
            # else:
            assert subnode.child != None
            tt = PTreeConv(subnode.child, urn, inputs)
            t.set(subnode.tag, tt)
        else:
            t.append(PTreeConvNode(subnode.tag, urn, inputs,
                                   subnode.spos, abs(subnode.epos), subnode.child))
        subnode = subnode.prev
    for i in range(len(t)//2):
        t[i], t[-(1+i)] = t[-(1+i)], t[i]
    return t


def pRule(peg, name, pf):
    peg[name] = pf


def generate(pf):
    # pf = self.generated[start.uname()]
    def parse(inputs, urn='(unknown source)', pos=0, epos=None, conv=PTreeConv):
        if epos is None:
            epos = len(inputs)
        px = PContext(inputs, pos, epos)
        if not pf(px):
            result = PTree(None, "err", px.headpos, px.headpos, None)
        else:
            result = px.ptree if px.ptree is not None else PTree(None,
                                                                 "", pos, px.pos, None)
        return conv(result, urn, inputs)
    return parse
