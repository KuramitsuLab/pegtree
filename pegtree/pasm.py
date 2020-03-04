from collections import namedtuple


def pRule(peg, name, pf):
    peg[name] = pf

# Generator


def match_empty(px): return True


def pEmpty():
    return match_empty


def pFail():
    return lambda px: False


def match_any(px):
    if px.pos < px.epos:
        px.pos += 1
        return True
    return False


def pAny():
    return match_any


CharCache = {
    '': match_empty
}


def pChar(text):
    if text in CharCache:
        return CharCache[text]
    clen = len(text)

    def match_char(px):
        if px.inputs.startswith(text, px.pos):
            px.pos += clen
            return True
        return False
    CharCache[text] = match_char
    return match_char

# Range


def unique_range(chars, ranges, memo=None):
    cs = 0
    for c in chars:
        cs |= 1 << ord(c)
    r = ranges
    while len(r) > 1:
        for c in range(ord(r[0]), ord(r[1])+1):
            cs |= 1 << c
        r = r[2:]
    if memo is not None:
        if cs in memo:
            return memo[cs]
        memo[cs] = cs
    return cs


def minimum_range(chars, ranges):
    cs = 0xffff
    for c in chars:
        cs = min(cs, ord(c))
    r = ranges
    while len(r) > 1:
        cs = min(cs, ord(r[0]))
        cs = min(cs, ord(r[1]))
        r = r[2:]
    return cs


BitmapCache = {}


def bitmap(chars, ranges):
    key = (chars, ranges)
    if key in BitmapCache:
        return BitmapCache[key]
    offset = minimum_range(chars, ranges)
    bitset = unique_range(chars, ranges) >> offset
    BitmapCache[key] = (bitset, offset)
    return BitmapCache[key]


def pRange(chars, ranges):
    bitset, offset = bitmap(chars, ranges)

    def match_bitset(px):
        if px.pos < px.epos:
            shift = ord(px.inputs[px.pos]) - offset
            if shift >= 0 and (bitset & (1 << shift)) != 0:
                px.pos += 1
                return True
        return False
    return match_bitset


def pAnd(pf):
    def match_and(px):
        pos = px.pos
        if pf(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            return True
        return False
    return match_and


def pNot(pf):
    def match_not(px):
        pos = px.pos
        ast = px.ast
        if not pf(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return True
        return False
    return match_not


def pMany(pf):
    def match_many(px):
        pos = px.pos
        ast = px.ast
        while pf(px) and pos < px.pos:
            pos = px.pos
            ast = px.ast
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        return True
    return match_many


def pMany1(pf):
    def match_many1(px):
        if pf(px):
            pos = px.pos
            ast = px.ast
            while pf(px) and pos < px.pos:
                pos = px.pos
                ast = px.ast
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return True
        return False
    return match_many1


def pOption(pf):
    def match_option(px):
        pos = px.pos
        ast = px.ast
        if not pf(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
        return True
    return match_option

# Seq


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


def pSeq(*pfs):
    def match_seq(px):
        for pf in pfs:
            if not pf(px):
                return False
        return True
    return match_seq

# Ore


def pOre2(pf, pf2):
    def match_ore2(px):
        pos = px.pos
        ast = px.ast
        if pf(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        return pf2(px)
    return match_ore2


def pOre3(pf, pf2, pf3):
    def match_ore3(px):
        pos = px.pos
        ast = px.ast
        if pf(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        if pf2(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        return pf3(px)
    return match_ore3


def pOre4(pf, pf2, pf3, pf4):
    def match_ore4(px):
        pos = px.pos
        ast = px.ast
        if pf(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        if pf2(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        if pf3(px):
            return True
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        return pf4(px)
    return match_ore4


def pOre(*pfs):
    def match_ore(px):
        pos = px.pos
        ast = px.ast
        for pf in pfs:
            if pf(px):
                return True
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
        return False
    return match_ore


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


def pRef(generated, uname):
    if uname not in generated:
        fs = None

        def match_deref(px):
            nonlocal fs
            if fs is None:
                fs = generated[uname]
            return fs(px)
        generated[uname] = match_deref
    return generated[uname]


def pRef(generated, uname):
    if uname not in generated:
        generated[uname] = lambda px: generated[uname](px)
    return generated[uname]


class PMemo(object):
    __slots__ = ['key', 'pos', 'treeState', 'ast', 'prev', 'result']

    def __init__(self):
        self.key = -1
        self.pos = 0
        self.treeState = False
        self.ast = None
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
                if m.prev == px.ast:
                    px.pos = m.pos
                    px.ast = m.ast
                    hit += 1
                    return m.result
            else:
                px.pos = m.pos
                hit += 1
                return m.result
        prev = px.ast
        m.result = fs(px)
        m.pos = px.pos
        m.key = key
        if m.result and prev != px.ast:
            m.treeState = True
            m.prev = prev
            m.ast = px.ast
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
                if m.prev == px.ast:
                    px.pos = m.pos
                    px.ast = m.ast
                    hit += 1
                    return m.result
            else:
                px.pos = m.pos
                hit += 1
                return m.result
        prev = px.ast
        m.result = fs(px)
        m.pos = px.pos
        m.key = key
        if m.result and prev != px.ast:
            m.treeState = True
            m.prev = prev
            m.ast = px.ast
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


def splitPTree(pt):
    if pt is None:
        return None, None
    if pt.prev is None:
        return None, pt
    return pt.prev, PTree(None, pt.tag, pt.spos, pt.epos, pt.child)


def makePTree(pt: PTree, inputs: str):
    ns = []
    while pt != None:
        if pt.child == None:
            child = repr(inputs[pt.spos:pt.epos])
        else:
            child = makePTree(pt.child)
        child = (pt.tag, child)
        ns.append(child)
        pt = pt.prev
    if len(ns) == 1:
        return ns[0]
    return list(reversed(ns))


def pNode(pf, tag, shift):
    def make_tree(px):
        pos = px.pos
        prev = px.ast
        px.ast = None
        if pf(px):
            px.ast = PTree(prev, tag, pos+shift, px.pos, px.ast)
            return True
        return False
    return make_tree


def pEdge(edge, pf):
    def match_edge(px):
        pos = px.pos
        prev = px.ast
        px.ast = None
        if pf(px):
            px.ast = PTree(prev, edge, pos, -px.pos, px.ast)
            return True
        return False
    return match_edge


def pFold(edge, pf, tag, shift):
    if edge == '':
        def match_fold(px):
            pos = px.pos
            prev, px.ast = splitPTree(px.ast)
            if pf(px):
                px.ast = PTree(prev, tag, pos+shift, px.pos, px.ast)
                return True
            return False
        return match_fold
    else:
        def match_fold2(px):
            pos = px.pos
            # pprev = px.ast
            prev, pt = splitPTree(px.ast)
            px.ast = PTree(None, edge, 0, -pos, pt)
            if pf(px):
                px.ast = PTree(prev, tag, pos+shift, px.pos, px.ast)
                return True
            return False
        return match_fold2


def pAbs(pf):
    def match_abs(px):
        ast = px.ast
        if pf(px):
            px.ast = ast
            return True
        return False
    return match_abs


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

#params = pe.params
#name = str(params[0])
#pf = self.emit(pe.e, step)


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


#params = pe.params
#name = str(params[0])

def pIn(name):  # @in(NAME)
    def match_dic(px):
        #print('@matching', name, px.inputs, px.pos)
        if name in px.dic:
            ss = px.dic[name]
            for s in ss:
                if px.inputs.startswith(s, px.pos):
                    #print('@matched', s)
                    px.pos += len(s)
                    return True
            #print('@', px.inputs[px.pos:], ss)
        return False
    return match_dic


# Optimized


def pAndChar(text):
    def match_andchar(px):
        return px.inputs.startswith(text, px.pos)
    return match_andchar


def pNotChar(text):
    def match_notchar(px):
        return not px.inputs.startswith(text, px.pos)
    return match_notchar


def pManyChar(text):
    clen = len(text)

    def match_manychar(px):
        while px.inputs.startswith(text, px.pos):
            px.pos += clen
        return True
    return match_manychar


def pMany1Char(text):
    clen = len(text)

    def match_many1char(px):
        if px.inputs.startswith(text, px.pos):
            px.pos += clen
            while px.inputs.startswith(text, px.pos):
                px.pos += clen
            return True
        return False
    return match_many1char


def pOptionChar(text):
    clen = len(text)

    def match_optionchar(px):
        if px.inputs.startswith(text, px.pos):
            px.pos += clen
        return True
    return match_optionchar


def pAndRange(chars, ranges):
    bitset, offset = bitmap(chars, ranges)  # >> offset

    def match_andbitset(px):
        if px.pos < px.epos:
            shift = ord(px.inputs[px.pos])  # - offset
            if shift >= 0 and (bitset & (1 << shift)) != 0:
                return True
        return False
    return match_andbitset


def pAndRange(chars, ranges):
    bitset, offset = bitmap(chars, ranges)  # >> offset

    def match_andbitset(px):
        if px.pos < px.epos:
            shift = ord(px.inputs[px.pos]) - offset
            if shift >= 0 and (bitset & (1 << shift)) != 0:
                return True
        return False
    return match_andbitset


def pNotRange(chars, ranges):
    bitset, offset = bitmap(chars, ranges)  # >> offset

    def match_notbitset(px):
        if px.pos < px.epos:
            shift = ord(px.inputs[px.pos]) - offset
            if shift >= 0 and (bitset & (1 << shift)) != 0:
                return False
        return True
    return match_notbitset


def pManyRange(chars, ranges):
    bitset, offset = bitmap(chars, ranges)  # >> offset

    def match_manybitset(px):
        while px.pos < px.epos:
            shift = ord(px.inputs[px.pos]) - offset
            if shift >= 0 and (bitset & (1 << shift)) != 0:
                px.pos += 1
            else:
                break
        return True
    return match_manybitset


def pMany1Range(chars, ranges):
    return pSeq2(pRange(chars, ranges), pManyRange(chars, ranges))


def pOptionRange(chars, ranges):
    bitset, offset = bitmap(chars, ranges)  # >> offset

    def match_optionbitset(px):
        if px.pos < px.epos:
            shift = ord(px.inputs[px.pos]) - offset
            if shift >= 0 and (bitset & (1 << shift)) != 0:
                px.pos += 1
        return True
    return match_optionbitset

# generate


# PContext


class PContext:
    __slots__ = ['inputs', 'pos', 'epos',
                 'headpos', 'ast', 'state', 'memo', 'dic']

    def __init__(self, inputs, spos, epos):
        self.inputs = inputs
        self.pos = spos
        self.epos = epos
        self.headpos = spos
        self.ast = None
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


class ParseTree(list):
    def __init__(self, tag, inputs, spos=0, epos=None, urn=UNKNOWN_SOURCE):
        self.tag_ = tag
        self.inputs_ = inputs
        self.spos_ = spos
        self.epos_ = epos if epos is not None else len(inputs)
        self.urn_ = urn

    def gettag(self):
        return self.tag_

    def start(self):
        return rowcol(self.urn_, self.inputs_, self.spos_)

    def end(self):
        return rowcol(self.urn_, self.inputs_, self.epos_)

    def decode(self):
        inputs, spos, epos = self.inputs_, self.spos_, self.epos_
        LF = b'\n' if isinstance(inputs, bytes) else '\n'
        rows = inputs[:spos + (1 if len(inputs) > spos else 0)]
        rows = rows.split(LF)
        linenum, column = len(rows), len(rows[-1])-1
        begin = inputs.rfind(LF, 0, spos) + 1
        # print('@', spos, begin, inputs)
        end = inputs.find(LF, spos)
        # print('@', spos, begin, inputs)
        if end == -1:
            end = len(inputs)
        # print('@[', begin, spos, end, ']', epos)
        line = inputs[begin:end]  # .replace('\t', '   ')
        mark = []
        endcolumn = column + (epos - spos)
        for i, c in enumerate(line):
            if column <= i and i <= endcolumn:
                mark.append('^' if ord(c) < 256 else '^^')
            else:
                mark.append(' ' if ord(c) < 256 else '  ')
        mark = ''.join(mark)
        return (self.urn_, spos, linenum, column, line, mark)

    def message(self, msg='Syntax Error'):
        urn, pos, linenum, cols, line, mark = self.decode()
        return '{} ({}:{}:{}+{})\n{}\n{}'.format(msg, urn, linenum, cols, pos, line, mark)

    def __eq__(self, tag):
        return self.tag_ == tag

    def isSyntaxError(self):
        return self.tag_ == 'err'

    def keys(self):
        ks = []
        for key in self.__dict__:
            v = self.__dict__[key]
            if isinstance(v, ParseTree):
                ks.append(v)
        return ks

    def subs(self):
        es = []
        for i, child in enumerate(self):
            es.append((child.spos_, '', child))
        for key in self.__dict__:
            v = self.__dict__[key]
            if isinstance(v, ParseTree):
                es.append((v.spos_, key, v))
        es.sort()
        return [(x[1], x[2]) for x in es]

    def get(self, key):
        return getattr(self, key)

    def set(self, key, t):
        assert isinstance(t, ParseTree)
        if key == '':
            self.append(key, t)
        else:
            setattr(self, key, t)

    def __str__(self):
        s = self.inputs_[self.spos_:self.epos_]
        return s.decode('utf-8') if isinstance(s, bytes) else s

    def __repr__(self):
        if self.isSyntaxError():
            return self.message('Syntax Error')
        sb = []
        self.strOut(sb)
        return "".join(sb)

    def dump(self, indent='\n', tab='  ', tag=nop, edge=nop, token=nop):
        if self.isSyntaxError():
            print(self.message('Syntax Error'))
        else:
            sb = []
            self.strOut(sb, indent, tab, '', tag, edge, token)
            print("".join(sb))

    def strOut(self, sb, indent='\n  ', tab='  ', prefix='', tag=nop, edge=nop, token=nop):
        sb.append(indent + prefix + "[" + tag(f'#{self.tag_}'))
        subs = self.subs()
        if len(subs) > 0:
            next_indent = indent + tab
            for label, child in subs:
                prefix = edge(label) + ': ' if label != '' else ''
                child.strOut(sb, next_indent, tab, prefix, tag, edge, token)
            sb.append(indent + "]")
        else:
            sb.append(' ' + token(repr(str(self))))
            sb.append("]")

    # def strOut2(self, sb, indent='\n  ', tab='  ', tag=nop, edge=nop, token=nop):
    #     sb.append("[" + tag(f'#{self.tag_}'))
    #     hasContent = False
    #     next_indent = indent + tab
    #     for child in self:
    #         hasContent = True
    #         sb.append(indent)
    #         if hasattr(child, 'strOut'):
    #             child.strOut(sb, next_indent, tab, tag, edge, token)
    #         else:
    #             sb.append(repr(child))
    #     for key in self.__dict__:
    #         v = self.__dict__[key]
    #         if isinstance(v, ParseTree):
    #             hasContent = True
    #             sb.append(indent)
    #             sb.append(edge(key) + ': ')
    #             v.strOut(sb, next_indent, tab, tag, edge, token)
    #     if not hasContent:
    #         sb.append(' ' + token(repr(str(self))))
    #     sb.append("]")


def PTree2ParseTree(pt: PTree, urn, inputs):
    if pt.prev != None:
        return PTree2ParseTreeImpl('', urn, inputs, pt.spos, pt.epos, pt)
    else:
        return PTree2ParseTreeImpl(pt.tag, urn, inputs, pt.spos, pt.epos, pt.child)


def PTree2ParseTreeImpl(tag, urn, inputs, spos, epos, subnode):
    t = ParseTree(tag, inputs, spos, epos, urn)
    while subnode != None:
        if subnode.isEdge():
            if subnode.child == None:
                tt = PTree2ParseTreeImpl(
                    '', urn, inputs, subnode.spos, abs(subnode.epos), None)
            else:
                tt = PTree2ParseTree(subnode.child, urn, inputs)
            if subnode.tag == '':
                t.append(tt)
            else:
                setattr(t, subnode.tag, tt)
        else:
            t.append(PTree2ParseTreeImpl(subnode.tag, urn, inputs,
                                         subnode.spos, abs(subnode.epos), subnode.child))
        subnode = subnode.prev
    for i in range(len(t)//2):
        t[i], t[-(1+i)] = t[-(1+i)], t[i]
    return t


def generate(pf):
    # pf = self.generated[start.uname()]
    def parse(inputs, urn='(unknown source)', pos=0, epos=None, conv=PTree2ParseTree):
        if epos is None:
            epos = len(inputs)
        px = PContext(inputs, pos, epos)
        if not pf(px):
            result = PTree(None, "err", px.headpos, px.headpos, None)
        else:
            result = px.ast if px.ast is not None else PTree(None,
                                                             "", pos, px.pos, None)
        return conv(result, urn, inputs)
    return parse


# TPEG
