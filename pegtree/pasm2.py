from collections import namedtuple


def pRule(peg, name, pf):
    peg[name] = pf

# Generator

def pEmpty():
    return match_empty

def pFail():
    return match_fail

def pAny():
    return match_any

def match_empty(px): 
    return True

def match_fail(px): 
    return False

def match_any(px):
    if px.pos < px.epos:
        px.pos += 1
        return True
    return False

## Characters

Name2ParseFunc = {
    '': (match_empty, match_empty)
}

Range2ParseFunc = {
}

def find_match(pfunc):
    for func, funcmove in Name2ParseFunc.values():
        if pfunc == funcmove:
            return func
    for func, funcmove in Range2ParseFunc.values():
        if pfunc == funcmove:
            return func
    return None

def string_pfunc(text):
    clen = len(text)
    def match_char(px):
        if px.inputs.startswith(text, px.pos):
            px.pos += clen
            return True
        return False
    match_andchar = lambda px: px.inputs.startswith(text, px.pos)
    Name2ParseFunc[text] = (match, match_move)
    return Name2ParseFunc[text]

## range

def range_keys_append(keys, s, e):
    if s > e:
        s, e = e, s
    for i in range(len(keys)):
        skey, ekey = keys[i]
        if skey <= s and s <= ekey:
            if ekey < e:
                keys[i] = (skey, e)
            return
        elif skey <= e and e <= ekey:
            if s < skey:
                keys[i] = (s, ekey)
            return
        elif ord(ekey)+1 == ord(s):
            keys[i] = (skey, e)
        elif ord(e)+1 == ord(skey):
            keys[i] = (s, ekey)
    keys.append((s, e))

def range_unique(chars, ranges):
    keys=[]
    for c in chars:
        range_keys_append(keys,c,c)
    for i in range(0, len(ranges), 2):
        range_keys_append(keys,ranges[i],ranges[i+1])
    chars = []
    ranges = []
    for s, e in sorted(keys):
        if s == e:
            chars.append(s)
        else:
            ranges.append(s+e)
    return ''.join(chars), ''.join(ranges)

def move1(pf):
    def move(px):
        if pf(px):
            px.pos+=1
            return True
        return False
    return move

def range_pfunc(chars, ranges):
    chars, ranges = range_unique(chars, ranges)
    key = (chars, ranges)
    if key in Range2ParseFunc:
        return Range2ParseFunc[key]
    long_ranges = []
    for i in range(0, len(ranges), 2):
        s, e = ord(ranges[i]), ord(ranges[i+1])
        if e - s < 255:
            chars += ''.join(ord(c) for c in range(s, e+1))
        else:
            long_ranges.append(ranges[i])
            long_ranges.append(ranges[i+1])
    r = ''.join(long_ranges)
    if len(r) == 0:
        def match(px):
            return px.pos < px.epos and chars.find(px.inputs[px.pos]) != -1
        Range2ParseFunc[key] = (match, move1(match))
    elif len(long_ranges) == 2:
        def match(px):
            if px.pos < px.epos:
                c = px.inputs[px.pos]
                return chars.find(c) != -1 or r[0] <= c <= r[1]
            return False
        Range2ParseFunc[key] = (match, move1(match))
    elif len(long_ranges) == 4:
        def match(px):
            if px.pos < px.epos:
                c = px.inputs[px.pos]
                return chars.find(c) != -1 or r[0] <= c <= r[1] or r[2] <= c <= r[3]
            return False
        Range2ParseFunc[key] = (match, move1(match))
    else:
        def match(px):
            if px.pos < px.epos:
                c = px.inputs[px.pos]
                if chars.find(c) != -1: return True
                for i in range(0, r, 2):
                    if r[i] <= c <= r[i+1]: return True
            return False
        Range2ParseFunc[key] = (match, move1(match))
    return Range2ParseFunc[key]

def pChar(text):
    _, pf = string_pfunc(text)
    return pf

def pRange(chars, ranges):
    _, pf = range_pfunc(chars, ranges)
    return pf

## and

def pfunc(string_or_pfunc):
    if isinstance(string_or_pfunc, str):
        return pChar(string_or_pfunc)
    return string_or_pfunc

def pAnd(pf):
    pf = pfunc(pf)
    text = find_string(pf)
    if text is not None:
        return pAndChar(text)
    pfa = find_andmatch(pf)
    if match is not None:
        return match
    def match_and(px):
        pos = px.pos
        if pf(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            return True
        return False
    return match_and

def pAndChar(text):
    def match_andchar(px):
        return px.inputs.startswith(text, px.pos)
    return match_andchar

def pNot(pf):
    text = get_string(pf)
    if text is not None:
        return pNotChar(text)
    def match_not(px):
        pos = px.pos
        ptree = px.ptree
        if not pf(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ptree = ptree
            return True
        return False
    return match_not

def pNotChar(text):
    def match_notchar(px):
        return not px.inputs.startswith(text, px.pos)
    return match_notchar

def pMany(pf):
    text = get_string(pf)
    if text is not None:
        return pManyChar(text)
    def match_many(px):
        pos = px.pos
        ptree = px.ptree
        while pf(px) and pos < px.pos:
            pos = px.pos
            ptree = px.ptree
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        return True
    return match_many

def pManyChar(text):
    clen = len(text)

    def match_manychar(px):
        while px.inputs.startswith(text, px.pos):
            px.pos += clen
        return True
    return match_manychar

def pOneMany(pf):
    text = get_string(pf)
    if text is not None:
        return pOneManyChar(text)

    def match_OneMany(px):
        if pf(px):
            pos = px.pos
            ptree = px.ptree
            while pf(px) and pos < px.pos:
                pos = px.pos
                ptree = px.ptree
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ptree = ptree
            return True
        return False
    return match_OneMany

def pOneManyChar(text):
    clen = len(text)
    def match_OneManychar(px):
        if px.inputs.startswith(text, px.pos):
            px.pos += clen
            while px.inputs.startswith(text, px.pos):
                px.pos += clen
            return True
        return False
    return match_OneManychar

def pOption(pf):
    text = get_string(pf)
    if text is not None:
        return pOptionChar(text)
    def match_option(px):
        pos = px.pos
        ptree = px.ptree
        if not pf(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ptree = ptree
        return True
    return match_option

def pOptionChar(text):
    clen = len(text)
    def match_optionchar(px):
        if px.inputs.startswith(text, px.pos):
            px.pos += clen
        return True
    return match_optionchar

# Seq

def pSeq(*pfs):
    if len(pfs) == 1:
        return pfs[0]
    elif len(pfs) == 2:
        return pSeq2(pfs[0], pfs[1])
    elif len(pfs) == 3:
        return pSeq3(pfs[0], pfs[1], pfs[2])
    elif len(pfs) == 4:
        return pSeq4(pfs[0], pfs[1], pfs[2], pfs[3])
    def match_seq(px):
        for pf in pfs:
            if not pf(px):
                return False
        return True
    return match_seq


def pSeq2(pf, pf2):
    def match_seq2(px):
        return pf(px) and pf2(px)
    return match_seq2


def pSeq3(pf, pf2, pf3):
    def match_seq3(px):
        return pf(px) and pf2(px) and pf3(px)
    return match_seq3


def pSeq4(pf, pf2, pf3, pf4):
    def match_seq4(px):
        return pf(px) and pf2(px) and pf3(px) and pf4(px)
    return match_seq4



# Ore

def pOre(*pfs):
    if len(pfs) == 1:
        return pfs[0]
    elif len(pfs) == 2:
        return pOre2(pfs[0], pfs[1])
    elif len(pfs) == 3:
        return pOre3(pfs[0], pfs[1], pfs[2])
    elif len(pfs) == 4:
        return pOre4(pfs[0], pfs[1], pfs[2], pfs[3])

    def match_ore(px):
        pos = px.pos
        ptree = px.ptree
        for pf in pfs:
            if pf(px):
                return True
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ptree = ptree
        return False
    return match_ore

def pOre2(pf, pf2):
    def match_ore2(px):
        pos = px.pos
        ptree = px.ptree
        if pf(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        return pf2(px)
    return match_ore2


def pOre3(pf, pf2, pf3):
    def match_ore3(px):
        pos = px.pos
        ptree = px.ptree
        if pf(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        if pf2(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        return pf3(px)
    return match_ore3


def pOre4(pf, pf2, pf3, pf4):
    def match_ore4(px):
        pos = px.pos
        ptree = px.ptree
        if pf(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        if pf2(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        if pf3(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ptree = ptree
        return pf4(px)
    return match_ore4




# def make_trie(dic):
#     if '' in dic or len(dic) < 10:
#         return dic
#     d = {}
#     for s in dic:
#         s0, s = s[0], s[1:]
#         if s0 in d:
#             ss = d[s0]
#             if not s in ss:
#                 ss.append(s)
#         else:
#             d[s0] = [s]
#     for key in d:
#         d[key] = make_trie(d[key])
#     return d


# def match_trie(px, d):
#     if px.pos >= px.epos:
#         return False
#     if isinstance(d, dict):
#         c = px.inputs[px.pos]
#         if c in d:
#             px.pos += 1
#             return match_trie(px, d[c])
#         return False
#     pos = px.pos
#     inputs = px.inputs
#     for s in d:
#         if inputs.startswith(s, pos):
#             px.pos += len(s)
#             return True
#     return False


# def pDict(words):
#     if isinstance(words, str):
#         words = words.split(' ')
#     dic = make_trie(words)
#     return lambda px: match_trie(px, dic)


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

# def pLeft(pf):
#     def match(px):
#         key = (px.pos, uname)
#         if key in px.rec:
#             return False
#         px.rec[key] = True
#         result = pf
#         del px.rec[key]
#         return result
#     return match

# def pDyRef(uname, default_pf=match_fail):
#     def match(px):
#         pf = px.pfmap.get(uname, default_pf)
#         return pf(px)
#     return match

# def pApply(pf, name, param):
#     def match(px):
#         px.pfmap[name] = param
#         return pf(px)
#     return match


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

    def match_memo(px):
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
    return match_memo


def pMemoDebug(name, fs, mp, mps):
    disabled = False
    hit = 0
    miss = 0
    mpsize = len(mps)

    def match_memo(px):
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
    return match_memo


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

# Node (tag, spos, epos, child)
# Edge (prev, edge, node)

def pNode(pf, tag, shift):
    def make_node(px):
        pos = px.pos
        prev = px.ptree
        px.ptree = None
        if pf(px):
            node = (tag, pos+shift, px.pos, px.ptree)
            px.ptree = (prev, '', node)
            return True
        return False
    return make_node

def pEdge(edge, pf, shift=0):
    def make_edge(px):
        pos = px.pos
        prev = px.ptree
        if pf(px):
            if px.ptree is prev:
                node = (tag, pos+shift, px.pos, None)
                px.ptree = (prev, edge, node)
            else:
                p = px.tree
                px.ptree = (p[1], edge, p[2])
            return True
        return False
    return make_edge

def make_ptree(urn, inputs, tag, spos, epos, ptree):
    if ptree is None:
        return ParseTree(tag, inputs, spos, epos, urn)
    prev, edge, node = ptree
    if prev is None and tag == '':
        return make_ptree(urn, inputs, *node)
    t = ParseTree(tag, inputs, spos, epos, urn)
    t.append(edge, make_ptree(urn, inputs, *node))
    while prev is not None:
        prev, edge, node = ptree
        t.append(edge, make_ptree(urn, inputs, *node))
    for i in range(len(t)//2):
        t[i], t[-(1+i)] = t[-(1+i)], t[i]
    return t

# def popPTree(px):
#     pt = px.ptree
#     if pt is None:
#         return px.pos, None
#     if pt.prev is None:
#         px.ptree = pt
#         return pt.spos, None
#     px.ptree = PTree(None, pt.tag, pt.spos, pt.epos, pt.child)
#     return pt.spos, pt.prev

def pFold(edge, pf, tag, shift):
    def match_fold(px):
        if px.ptree is None:
            spos = px.pos
            prev = None
            px.ptree = None
        else:
            prev, _, ptree = px.ptree
            spos = ptree.spos
            px.ptree = (None, edge, ptree)
        if pf(px):
            node = (tag, spos, px.pos, px.ptree)
            px.ptree = (prev, '', node)
            return True
        return False
    return match_fold

def pAbs(pf):
    def match_abs(px):
        ptree = px.ptree
        if pf(px):
            px.ptree = ptree
            return True
        return False
    return match_abs

def rechain(mprev, mtree, ptree):
    prev, tree = mtree
    if prev is mprev:
        prev 

def pMemo(fs, mp, mpsize):
    disabled = False
    hit = 0
    miss = 0

    def match_tree(px):
        nonlocal disabled, hit, miss
        if disabled:
            return fs(px)
        key = (mpsize * px.pos) + mp
        m = px.memo[key % 1789]
        if m.key == key:
            hit += 1
            if m.treeModified:
                if m.prev is px.ptree:
                    px.pos = m.pos
                    px.ptree = m.ptree
                    return m.result
                else:
                    px.tree = rechain(m.prev, px.tree, m.tree)
            else:
                px.pos = m.pos
                hit += 1
                return m.result
        prev = px.ptree
        m.result = fs(px)
        m.pos = px.pos
        m.key = key
        if m.result and prev is not px.ptree:
            m.treeModified = True
            m.prev = prev
            m.ptree = px.ptree
        else:
            m.treeModified = False
        miss += 1
        if miss % 100 == 0:
            if hit / miss < 5:
                disabled = True
        return m.result
    return match_memo



def pSkip():  # @skip()
    def skip(px):
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


def pSymbol(pf, sid):  # @symbol(A)
    def match_symbol(px):
        pos = px.pos
        if pf(px):
            px.state = State(sid, px.inputs[pos:px.pos], px.state)
            return True
        return False
    return match_symbol


def pScope(pf):
    def scope(px):
        state = px.state
        res = pf(px)
        px.state = state
        return res
    return scope


def pExists(sid):  # @Match(A)
    return lambda px: getstate(px.state, sid) != None


def pMatch(sid):  # @Match(A)
    def match(px):
        state = getstate(px.state, sid)
        if state is not None and px.inputs.startswith(state.val, px.pos):
            px.pos += len(state.val)
            return True
        return False
    return match

# params = pe.params
# name = str(params[0])
# pf = self.emit(pe.e, step)


def pDef(name, pf):
    def define_dic(px):
        pos = px.pos
        if pf(px):
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


# params = pe.params
# name = str(params[0])

def pIn(name):  # @in(NAME)
    def match_dic(px):
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
    return match_dic

def pNotRange(chars, ranges):
    pf = pAndRange(chars, ranges)

    def match_ranges(px):
        return not pf(px)
    return match_ranges


def pManyRange(chars, ranges):
    pf = pAndRange(chars, ranges)

    def match_manybitset(px):
        while pf(px):
            px.pos += 1
        return True
    return match_manybitset


def pOneManyRange(chars, ranges):
    pf = pAndRange(chars, ranges)

    def match_onemanybitset(px):
        c = 0
        while pf(px):
            px.pos += 1
            c += 1
        return c > 0
    return match_onemanybitset


def pOptionRange(chars, ranges):
    pf = pAndRange(chars, ranges)

    def match_optionbitset(px):
        if pf(px):
            px.pos += 1
        return True
    return match_optionbitset

# generate


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

# ParseTree


def rowcol(urn, inputs, spos):
    inputs = inputs[:spos + (1 if len(inputs) > spos else 0)]
    rows = inputs.split(b'\n' if isinstance(inputs, bytes) else '\n')
    return urn, spos, len(rows), len(rows[-1])-1


def nop(s): return s


UNKNOWN_SOURCE = '(unknown source)'




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

def treeConvAsList(urn, inputs, ptree):
    if len(ptree) > 2:
        tag, spos, epos, child = ptree

    if len(ptree) == 2: #(prev, node)
        t = ParseTree(tag, inputs, spos, epos, urn)
        prev, node = ptree
        tag, spos, epos, 


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
