from pegtree.pasm import unique_range
#from pegtree.terminal import DEBUG, VERBOSE

import os

DebugFlag = 'DEBUG' in os.environ
VerboseFlag = 'VERBOSE' in os.environ


def DEBUG(*x):
    if DebugFlag:
        print('DEBUG', *x)


def VERBOSE(*x):
    if DebugFlag:
        print(*x)


# Grammar

GrammarId = 0


class Grammar(dict):
    def __init__(self, source=None):
        global GrammarId
        self.ns = str(GrammarId)
        self.N = []
        GrammarId += 1
        super().__setitem__('@@example', [])
        super().__setitem__('@@refs', {})

    def __repr__(self):
        ss = []
        for rule in self.N:
            ss.append(rule)
            ss.append(' = ')
            ss.append(repr(self[rule]))
            ss.append('\n')
        return ''.join(ss)

    def __setitem__(self, key, item):
        if not key in self:
            self.N.append(key)
        super().__setitem__(key, item)

    def newRef(self, name):
        refs = self['@@refs']
        if name not in refs:
            refs[name] = PRef(self, name)
        return refs[name]

    def start(self):
        if len(self.N) == 0:
            self['EMPTY'] = EMPTY
        return self.N[0]


class PExpr(object):
    def __iter__(self): pass
    def __len__(self): return 0

    def cname(self):
        return self.__class__.__name__


class PUnary(PExpr):
    __slot__ = ['e']

    def __init__(self, e):
        self.e = e

    def __iter__(self):
        yield self.e

    def __len__(self):
        return 1

    def minLen(self): return self.e.minLen()

    def grouping(self, e):
        if isinstance(e, POre) or isinstance(e, PSeq) or isinstance(e, PEdge) or isinstance(e, PAlt):
            return '(' + repr(e) + ')'
        return repr(e)


class PTuple(PExpr):
    __slots__ = ['es']

    def __init__(self, *es):
        self.es = list(es)

    def __iter__(self):
        return iter(self.es)

    def __len__(self):
        return len(self.es)

    def minLen(self):
        if not hasattr(self, 'minlen'):
            self.minlen = min(map(lambda e: e.minLen(), self.es))
        return self.minlen

    def grouping(self, e):
        if isinstance(e, POre) or isinstance(e, PAlt):
            return '(' + repr(e) + ')'
        return repr(e)

# Parsing Expression


class PAny(PExpr):
    def __repr__(self): return '.'
    def minLen(self): return 1


class PChar(PExpr):
    __slots__ = ['text']
    ESCTBL = str.maketrans(
        {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\v': '\\v', '\f': '\\f',
         '\\': '\\\\', "'": "\\'"})

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "'" + self.text.translate(PChar.ESCTBL) + "'"

    def minLen(self): return len(self.text)

    @classmethod
    def new(cls, text):
        if len(text) == 0:
            return EMPTY
        return PChar(text)


class PRange(PExpr):
    __slots__ = ['chars', 'ranges', 'neg']
    ESCTBL = str.maketrans(
        {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\v': '\\v', '\f': '\\f',
         '\\': '\\\\', ']': '\\]', '-': '\\-'})

    def __init__(self, chars, ranges, neg=False):
        self.chars = chars
        self.ranges = ranges
        self.neg = neg

    def __repr__(self):
        sb = []
        if(self.neg):
            sb.append('(!')
        sb.append('[')
        sb.append(self.chars.translate(PRange.ESCTBL))
        r = self.ranges
        while len(r) > 1:
            sb.append(r[0].translate(PRange.ESCTBL))
            sb.append('-')
            sb.append(r[1].translate(PRange.ESCTBL))
            r = r[2:]
        sb.append(']')
        if(self.neg):
            sb.append('. )')
        return ''.join(sb)

    def minLen(self): return 1

    @classmethod
    def new(cls, chars, ranges, neg=False):
        if len(chars) == 0 and len(ranges) == 0:
            return ANY if neg else FAIL
        if len(chars) == 1 and len(ranges) == 0 and neg == False:
            return PChar(chars)
        return PRange(chars, ranges, neg)


class PRef(PExpr):
    def __init__(self, peg, name):
        self.peg = peg
        self.name = name

    def __repr__(self):
        return self.name

    def uname(self, peg=None):
        if self.peg == peg:
            return self.name
        return f'{self.peg.ns}{self.name}'

    def deref(self):
        return self.peg[self.name]

    def minLen(self):
        if not hasattr(self, 'minlen'):
            self.minlen = 0
            self.minlen = self.deref().minLen()
        return self.minlen


class PName(PUnary):
    __slot__ = ['e', 'name', 'position', 'isLeftRec']

    def __init__(self, e, name: str, position):
        super().__init__(e)
        self.name = name
        self.position = position
        self.isLeftRec = False

    def __repr__(self):
        return repr(self.e)

    def minLen(self):
        return self.e.minLen()


class PSeq(PTuple):
    def __repr__(self):
        return ' '.join(map(lambda e: self.grouping(e), self.es))

    def minLen(self):
        if not hasattr(self, 'minlen'):
            self.minlen = sum(map(lambda e: e.minLen(), self.es))
        return self.minlen

    @classmethod
    def new(cls, *es):
        newes = []
        for e in es:
            PE.appendSeq(e, newes)
        return newes[0] if len(newes) == 1 else PSeq(*newes)


class PAlt(PTuple):
    def __repr__(self):
        return ' | '.join(map(repr, self))


class POre(PTuple):
    def __repr__(self):
        return ' / '.join(map(repr, self))

    def isDict(self):
        for e in self:
            if not isinstance(e, PChar):
                return False
        return True

    def listDict(self):
        dic = [e.text for e in self if isinstance(e, PChar)]
        dic2 = []
        for s in dic:
            if s == '':
                break
            dic2.append(s)
        return dic2

    @classmethod
    def new(cls, *es):
        if len(es) == 0:
            return FAIL
        newes = [es[0]]
        for e in es[1:]:
            if e == EMPTY:
                break
            e2 = PE.mergeRange(newes[-1], e)
            if e2 is None:
                newes.append(e)
            else:
                VERBOSE('MERGE', newes[-1], e, '=>', e2)
                newes[-1] = es
        return newes[0] if len(newes) == 1 else POre(*newes)


class PAnd(PUnary):
    def __repr__(self):
        return '&'+self.grouping(self.e)

    def minLen(self): return 0


class PNot(PUnary):
    def __repr__(self):
        return '!'+self.grouping(self.e)

    def minLen(self): return 0


class PMany(PUnary):
    def __repr__(self):
        return self.grouping(self.e)+'*'

    def minLen(self): return 0


class POneMany(PUnary):
    def __repr__(self):
        return self.grouping(self.e)+'+'


class POption(PUnary):
    def __repr__(self):
        return self.grouping(self.e)+'?'

    def minLen(self): return 0


class PNode(PUnary):
    __slot__ = ['e', 'tag', 'shift']

    def __init__(self, e, tag='', shift=0):
        self.e = e
        self.tag = tag
        self.shift = shift

    def __repr__(self):
        shift = '' if self.shift == 0 else f'/*shift={self.shift}*/'
        tag = '' if self.tag == '' else f' #{self.tag} '
        return '{' + shift + ' ' + repr(self.e) + tag + '}'


class PEdge(PUnary):
    __slot__ = ['e', 'edge']

    def __init__(self, edge, e):
        self.e = e
        self.edge = edge

    def __repr__(self):
        return self.edge + ': ' + self.grouping(self.e)


class PFold(PUnary):
    __slot__ = ['e', 'edge', 'tag', 'shift']

    def __init__(self, edge, e, tag='', shift=0):
        self.e = e
        self.edge = edge
        self.tag = tag
        self.shift = shift

    def __repr__(self):
        shift = '' if self.shift == 0 else f'/*shift={self.shift}*/'
        edge = '^' if self.edge == '' else f'{self.edge}:^'
        tag = '' if self.tag == '' else f' #{self.tag} '
        return '{ ' + edge + shift + ' ' + repr(self.e) + tag + '}'


class PAbs(PUnary):
    __slot__ = ['e']

    def __init__(self, e):
        self.e = e

    def __repr__(self):
        return f'@abs({self.e})'

# Action


class PAction(PUnary):
    __slots__ = ['e', 'func', 'params']

    def __init__(self, e, func, params, pos4=None):
        self.e = e
        self.func = func
        self.params = params

    def __repr__(self):
        return f'@{self.func}{self.params}'

    def cname(self):
        return self.func.capitalize()

# repr


'''
def grouping(e, f):
    return '(' + repr(e) + ')' if f(e) else repr(e)


def inUnary(e):
    return isinstance(e, POre) \
        or isinstance(e, PSeq) or isinstance(e, PAlt) \
        or (isinstance(e, PEdge))


def ss(e):
    return grouping(e, lambda e: isinstance(e, POre) or isinstance(e, PAlt))
'''

# CONSTANT
EMPTY = PChar('')
ANY = PAny()
FAIL = PNot(EMPTY)


class PVisitor(object):
    def visit(self, pe: PExpr):
        key = self.cname(pe)
        f = getattr(self, key)
        return f(pe)

    def cname(self, pe):
        return pe.cname()


class Nullable(PVisitor):
    def PChar(self, pe): return 1 if len(pe.text) > 0 else 0
    def PAny(self, pe): return 1
    def PRange(self, pe): return 1

    def PRef(self, pe):
        if not hasattr(pe, 'nullable') or pe.nullable is None:
            pe.nullable = 0
            pe.nullable = self.visit(pe.deref())
        return pe.nullable

    def PAnd(self, pe): return 0
    def PNot(self, pe): return 0
    def PMany(self, pe): return 0
    def POneMany(self, pe): return self.visit(pe.e)
    def POption(self, pe): return 0

    def PSeq(self, pe):
        for e in pe:
            if(self.visit(e) == 1):
                return 1
        return 0

    def POre(self, pe):
        for e in pe:
            if(self.visit(e) == 0):
                return 0
        return 1

    def PNode(self, pe): return self.visit(pe.e)
    def PFold(self, pe): return self.visit(pe.e)
    def PEdge(self, pe): return self.visit(pe.e)
    def PAbs(self, pe): return self.visit(pe.e)

    def PAction(self, pe): return self.visit(pe.e)


class LeftRef(PVisitor):
    EMPTYSET = set()

    def __init__(self, checkLeftRec=True):
        self.checkLeftRec = checkLeftRec
        self.memos = {}

    def PChar(self, pe): return LeftRef.EMPTYSET
    def PAny(self, pe): return LeftRef.EMPTYSET
    def PRange(self, pe): return LeftRef.EMPTYSET

    def PRef(self, pe):
        uname = pe.uname()
        if uname not in self.memos:
            memos[uname] = LeftRef.EMPTYSET
            memos[uname] = self.visit(pe.deref())
        return set(pe)

    def PName(self, pe):
        if self.checkLeftRec:
            self.visit(pe.e)
            return set(pe)
        return self.visit(pe.e)

    def PAnd(self, pe): return self.visit(pe.e)
    def PNot(self, pe): return self.visit(pe.e)
    def PMany(self, pe): return self.visit(pe.e)
    def POneMany(self, pe): return self.visit(pe.e)
    def POption(self, pe): return self.visit(pe.e)

    def PSeq(self, pe):
        result = set()
        for e in pe:
            result |= self.visit(e)
            if self.checkLeftRec & PE.isAlwaysConsumed(e):
                break
        return result

    def POre(self, pe):
        result = set()
        for e in pe:
            result |= self.visit(e)
        return result

    def PNode(self, pe): return self.visit(pe.e)
    def PFold(self, pe): return self.visit(pe.e)
    def PEdge(self, pe): return self.visit(pe.e)
    def PAbs(self, pe): return self.visit(pe.e)

    def PAction(self, pe): return self.visit(pe.e)


class First(PVisitor):

    def __init__(self):
        self.memos = {}

    def PChar(self, pe):
        if len(pe.text) == 0:
            return (0, 0)
        return (1 << ord(pe.text[0]), 0)

    def PAny(self, pe):
        return (-1, 0)

    def PRange(self, pe):
        if(pe.neg):
            return (-1, unique_range(pe.chars, pe.ranges))
        return (unique_range(pe.chars, pe.ranges), 0)

    def PRef(self, pe):
        uname = pe.uname()
        if(uname not in self.memos):
            self.memos[uname] = (-1, 0)
            self.memos[uname] = self.visit(pe.deref())
        return self.memos[uname]

    def PNot(self, pe):
        if PE.isSingleCharacter(pe.e):
            pos, neg = self.visit(pe.e)
            return (neg, pos)
        return LeftRef.EMPTYSET

    def PAnd(self, pe): return self.visit(pe.e)
    def PMany(self, pe): return self.visit(pe.e)
    def POneMany(self, pe): return self.visit(pe.e)
    def POption(self, pe): return self.visit(pe.e)

    def PSeq(self, pe):
        pos, neg = 0, 0
        for e in pe:
            pos1, neg1 = self.visit(e)
            pos |= pos1
            neg |= neg1
            if PE.isAlwaysConsumed(e):
                break
        return (pos, neg)

    def POre(self, pe):
        pos, neg = 0, 0
        for e in pe:
            pos1, neg1 = self.visit(e)
            pos |= pos1
            neg |= neg1
        return (pos, neg)

    def PNode(self, pe): return self.visit(pe.e)
    def PFold(self, pe): return self.visit(pe.e)
    def PEdge(self, pe): return self.visit(pe.e)
    def PAbs(self, pe): return self.visit(pe.e)

    def PAction(self, pe): return self.visit(pe.e)


defaultNullableChecker = Nullable()


class PE:

    @classmethod
    def isAlwaysConsumed(cls, pe):
        return defaultNullableChecker.visit(pe)

    @classmethod
    def isEmpty(cls, pe):
        return pe == EMPTY or isinstance(pe, PChar) and len(pe.text) == 0

    @classmethod
    def isSingleCharacter(cls, pe):
        return (isinstance(pe, PChar) and len(pe.text) == 1) or isinstance(pe, PRange) or isinstance(pe, PAny)

    @classmethod
    def mergeRange(cls, e, e2):
        if PE.isSingleCharacter(e) and PE.isSingleCharacter(e2):
            if e == ANY or e2 == ANY:
                return ANY
            chars = ''
            ranges = ''
            if isinstance(e, PChar):
                chars += e.text
            if isinstance(e2, PChar):
                chars += e2.text
            if isinstance(e, PRange):
                chars += e.chars
                ranges += e.ranges
            if isinstance(e2, PRange):
                chars += e2.chars
                ranges += e2.ranges
            chars, ranges = PE.uniqueRange(chars, ranges)
            return PRange.new(chars, ranges)
        return None

    @classmethod
    def range_bitset(cls, chars, ranges):
        cs = 0
        for c in chars:
            cs |= 1 << ord(c)
        r = ranges
        while len(r) > 1:
            for c in range(ord(r[0]), ord(r[1])+1):
                cs |= 1 << c
            r = r[2:]
        return cs

    @classmethod
    def stringfyRange(cls, bits):
        c = 0
        s = None
        p = None
        chars = []
        ranges = []
        while bits > 0:
            if bits & 1 == 1:
                if s is None:
                    s = c
                    p = c
                elif p + 1 == c:
                    p = c
                else:
                    PE._appendRange(s, p, chars, ranges)
                    s = c
                    p = c
            bits >>= 1
            c += 1
        if s is not None:
            PE._appendRange(s, p, chars, ranges)
        return ''.join(chars), ''.join(ranges)

    @classmethod
    def _appendRange(cls, s, p, chars, ranges):
        if s == p:
            chars.append(chr(s))
        elif s+1 == p:
            chars.append(chr(s))
            chars.append(chr(p))
        else:
            ranges.append(chr(s))
            ranges.append(chr(p))

    @classmethod
    def uniqueRange(cls, chars, ranges):
        bits = PE.range_bitset(chars, ranges)
        newchars, newranges = PE.stringfyRange(bits)
        checkbits = PE.range_bitset(chars, ranges)
        assert bits == checkbits
        return newchars, newranges

    @classmethod
    def appendSeq(cls, pe, es):
        if isinstance(pe, PSeq):
            for e in pe:
                PE.appendSeq(e, es)
        elif pe == EMPTY:
            pass
        elif isinstance(pe, PChar) and len(es) > 0 and isinstance(es[-1], PChar):
            e0 = es[-1]
            es[-1] = PChar(e0.text+pe.text)
        else:
            es.append(pe)

    @classmethod
    def prefixChar(cls, pe):
        if isinstance(pe, PChar) and len(pe.text) > 0:
            return pe.text[0]
        if isinstance(pe, PSeq):
            return PE.prefix(pe.es[0])
        if isinstance(pe, PNode):
            return PE.prefix(pe.e)
        return None

    @classmethod
    def dc(cls, pe):
        if isinstance(pe, PChar) and len(pe.text) > 0:
            return PChar.new(pe.text[1:])
        if isinstance(pe, PSeq):
            es = pe.es[:]
            es[0] = PE.dc(es[0])
            return PSeq.new(*es)
        if isinstance(pe, PNode):
            return PNode(PE.dc(pe.e), pe.tag, pe.shift-1)
        return FAIL

    @classmethod
    def appendChoice(cls, pe, es, cmap=None, deref=False):
        start = pe
        while deref and isinstance(pe, PRef):
            pe = pe.deref()
        if isinstance(pe, POre):
            for e in pe:
                PE.appendChoice(e, es, cmap, deref)
            return
        elif PE.isEmpty(pe):
            es.append(EMPTY)
            return
        elif len(es) > 0:
            e2 = PE.mergeRange(es[-1], pe)
            if e2 is not None:
                es[-1] = e2
                return
        if cmap != None:
            c = PE.prefixChar(pe)
            if c is not None:
                if c in cmap:
                    x = es[cmap[c]]
                    if not isinstance(x, list):
                        x = [x]
                        es[cmap[c]] = x
                    x.append(pe)
                else:
                    cmap[c] = len(es)
                    es.append(pe)
                return
        if len(es) > 0 and PE.isEmpty(es[-1]):
            return
        es.append(start)

    @classmethod
    def newChoice(cls, choices, deref=False):
        es = []
        for e in choices:
            PE.appendChoice(e, es, {}, deref)
        print('@@', es)
        newes = []
        for e in es:
            if isinstance(e, list):
                if isinstance(e, list):
                    c = PChar(PE.prefixChar(e[0]))
                    ecs = []
                    for ec in e:
                        ec = PE.dc(ec)
                        PE.appendChoice(ec, ecs)
                    newes.append(PSeq.new(c, PE.newChoice(ecs)))
                else:
                    newes.append(e)
            else:
                newes.append(e)
        return newes[0] if len(newes) == 1 else POre(*newes)
