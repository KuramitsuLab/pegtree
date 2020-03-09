# -*- coding: utf-8 -*-
import sys
import os
import errno
import inspect
from pathlib import Path
import pegtree.pasm as pasm
from pegtree.tpeg import TPEGGrammar
# sys.setrecursionlimit(5000)


def DEBUG(*x):
    if 'DEBUG' in os.environ:
        print('DEBUG', *x)

# ParsingExpression


class PExpr(object):
    def __iter__(self): pass
    def __len__(self): return 0

    def cname(self):
        return self.__class__.__name__


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


class PRange(PExpr):
    __slots__ = ['chars', 'ranges']
    ESCTBL = str.maketrans(
        {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\v': '\\v', '\f': '\\f',
         '\\': '\\\\', ']': '\\]', '-': '\\-'})

    def __init__(self, chars, ranges):
        self.chars = chars
        self.ranges = ranges  # newranges(ranges)

    def __repr__(self):
        sb = []
        sb.append('[')
        sb.append(self.chars.translate(PRange.ESCTBL))
        r = self.ranges
        while len(r) > 1:
            sb.append(r[0].translate(PRange.ESCTBL))
            sb.append('-')
            sb.append(r[1].translate(PRange.ESCTBL))
            r = r[2:]
        sb.append(']')
        return ''.join(sb)

    def minLen(self): return 1


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


class PSeq(PTuple):
    @classmethod
    def new(cls, *es):
        if len(es) == 0:
            return EMPTY
        ls = [es[0]]
        for e in es[1:]:
            if e == EMPTY:
                continue
            if isinstance(e, PChar) and isinstance(ls[-1], PChar):
                ls[-1] = PChar(ls[-1].text+e.text)
                continue
            ls.append(e)
        return ls[0] if len(ls) == 1 else PSeq(*ls)

    def __repr__(self):
        return ' '.join(map(ss, self))

    def minLen(self):
        if not hasattr(self, 'minlen'):
            self.minlen = sum(map(lambda e: e.minLen(), self.es))
        return self.minlen


class PAlt(PTuple):
    def __repr__(self):
        return ' | '.join(map(repr, self))


class POre(PTuple):
    @classmethod
    def new(cls, *es):
        choices = []
        for e in es:
            appendChoice(choices, e)
        return choices[0] if len(choices) == 1 else POre(*choices)

    def __repr__(self):
        return ' / '.join(map(repr, self))

    def optimize(self):
        choices = []
        optimizedChoice(choices, self)
        return choices[0] if len(choices) == 1 else POre(*choices)

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


def isSingleChar(e):
    return (isinstance(e, PChar) and len(e.text) == 1) or isinstance(e, PRange)


def mergeRange(e, e2):
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
    return PRange(chars, ranges)


def appendChoice(choices, pe):
    if isinstance(pe, POre):
        for e in pe:
            appendChoice(choices, e)
    elif len(choices) == 0:
        choices.append(pe)
    elif isSingleChar(choices[-1]) and isSingleChar(pe):
        DEBUG('OPTIMIZE', choices[-1], pe, '=>', mergeRange(choices[-1], pe))
        choices[-1] = mergeRange(choices[-1], pe)
    elif choices[-1] != EMPTY:
        choices.append(pe)
    else:
        DEBUG('IGNORED', pe)


def optimizedChoice(choices, pe):
    start = pe
    while isinstance(pe, PRef):
        pe = pe.deref()
    if isinstance(pe, POre):
        if(pe != start):
            DEBUG('INLINE', start, '=>', pe)
        for e in pe:
            optimizedChoice(choices, e)
    elif isinstance(pe, PRange) or isinstance(pe, PChar):
        if(pe != start):
            DEBUG('INLINE', start, '=>', pe)
        appendChoice(choices, pe)
    else:
        appendChoice(choices, start)


class PUnary(PExpr):
    __slot__ = ['e']

    def __init__(self, e):
        self.e = e

    def __iter__(self):
        yield self.e

    def __len__(self):
        return 1

    def minLen(self): return self.e.minLen()


class PAnd(PUnary):
    def __repr__(self):
        return '&'+grouping(self.e, inUnary)

    def minLen(self): return 0


class PNot(PUnary):
    def __repr__(self):
        return '!'+grouping(self.e, inUnary)

    def minLen(self): return 0


class PMany(PUnary):
    def __repr__(self):
        return grouping(self.e, inUnary)+'*'

    def minLen(self): return 0


class PMany1(PUnary):
    def __repr__(self):
        return grouping(self.e, inUnary)+'+'


class POption(PUnary):
    def __repr__(self):
        return grouping(self.e, inUnary)+'?'

    def minLen(self): return 0


class PName(PUnary):
    __slot__ = ['e', 'name', 'position']

    def __init__(self, e, name: str, position):
        super().__init__(e)
        self.name = name
        self.position = position

    def __repr__(self):
        return repr(self.e)

    def minLen(self):
        return self.e.minLen()


class PNode(PUnary):
    __slot__ = ['e', 'tag', 'shift']

    def __init__(self, e, tag='', shift=0):
        self.e = e
        self.tag = tag
        self.shift = shift

    def __repr__(self):
        s = '' if self.shift == 0 else f'/*shift={self.shift}*/'
        tag = '' if self.tag == '' else f' #{self.tag} '
        return '{' + s + ' ' + repr(self.e) + tag + '}'


class PEdge(PUnary):
    __slot__ = ['e', 'edge']

    def __init__(self, edge, e):
        self.e = e
        self.edge = edge

    def __repr__(self):
        return self.edge + ': ' + grouping(self.e, inUnary)


class PFold(PUnary):
    __slot__ = ['e', 'edge', 'tag', 'shift']

    def __init__(self, edge, e, tag='', shift=0):
        self.e = e
        self.edge = edge
        self.tag = tag
        self.shift = shift

    def __repr__(self):
        s = '' if self.shift == 0 else f'/*shift={self.shift}*/'
        edge = '^' if self.edge == '' else f'{self.edge}:^'
        tag = '' if self.tag == '' else f' #{self.tag} '
        return '{ ' + edge + s + ' ' + repr(self.e) + tag + '}'


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


def grouping(e, f):
    return '(' + repr(e) + ')' if f(e) else repr(e)


def inUnary(e):
    return isinstance(e, POre) \
        or isinstance(e, PSeq) or isinstance(e, PAlt) \
        or (isinstance(e, PEdge))


def ss(e):
    return grouping(e, lambda e: isinstance(e, POre) or isinstance(e, PAlt))


# CONSTANT
EMPTY = PChar('')
ANY = PAny()
FAIL = PNot(EMPTY)


# # Grammar


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

######################################################################
# ast.env


class Optimizer(object):

    def inline(self, pe: PExpr):
        start = pe
        while isinstance(pe, PRef):
            pe = pe.deref()
        if isinstance(pe, PChar) or isinstance(pe, PRange):
            if(pe != start):
                DEBUG('INLINE', start, '=>', pe)
            return pe
        return start

    def join(self, *es):
        return PSeq.new(*es)

    def fixedExpr(self, e):
        es = [e]
        fixed = []
        size = 0
        while len(es) > 0:
            # print(es, '->')
            lsize, e, es = self.fixedEach(size, es)
            # print('->', lsize, e, es)
            if e is None:
                break
            fixed.append(e)
            size += lsize
        return size, fixed, es

    def fixedEach(self, size, es):
        e = self.inline(es[0])
        if isinstance(e, PChar) and len(e.text) > 0:
            return len(e.text)+size, e, es[1:]
        elif isinstance(e, PRange) or isinstance(e, PAny):
            return 1+size, e, es[1:]
        elif isinstance(e, PAnd) or isinstance(e, PNot):
            return size, e, es[1:]
        elif isinstance(e, PSeq):
            return self.fixedEach(size, e.es+es[1:])
        elif isinstance(e, PMany1):
            lsize, lfixed, les = self.fixedExpr(e.e)
            # print('PMany1', e, '=>', lsize, lfixed, les)
            if len(les) != 0:
                return size, None, es
            return size+lsize, e.e, [PMany(e.e)] + es[1:]
        elif isinstance(e, PNode) and e.shift == 0:
            lsize, lfixed, les = self.fixedExpr(e.e)
            # print('PNode', e, '=>', lsize, lfixed, les)
            if len(lfixed) == 0:
                return size, None, es
            return size+lsize, PSeq.new(*lfixed), [PNode(PSeq.new(*les), e.tag, -lsize)]+es[1:]
        elif isinstance(e, PFold) and e.shift == 0:
            lsize, lfixed, les = self.fixedExpr(e.e)
            if len(lfixed) == 0:
                return size, None, es
            return size+lsize, PSeq.new(*lfixed), [PFold(e.edge, PSeq.new(*les), e.tag, -lsize)]+es[1:]
        return size, None, es

    def sort(self, refs):
        newrefs = []
        unsolved = []
        for ref in refs:
            names = set([])
            self.makerefs(ref.deref(), names)
            if len(names) == 0:
                newrefs.append(ref)
            else:
                unsolved.append((ref, set(names)))
        return self.solve(newrefs, unsolved)

    def makerefs(self, e, names):
        if isinstance(e, PTuple):
            for e2 in e:
                self.makerefs(e2, names)
        elif hasattr(e, 'e'):
            self.makerefs(e.e, names)
        elif isinstance(e, PRef):
            names.add(e.uname())

    def removeSolvedName(self, unsolved, uname):
        removed = False
        for _, names in unsolved:
            if uname in names:
                removed = True
                names.remove(uname)
        return removed

    def solve(self, refs, unsolved):
        removed = False
        # print(refs)
        for ref in refs:
            removed |= self.removeSolvedName(unsolved, ref.uname())
        max = 0
        while max < 10:
            removed = True
            while removed:
                removed = False
                newrefs = []
                stillUnsolved = []
                for ref, names in unsolved:
                    if len(names) <= max:
                        refs.append(ref)
                        newrefs.append(ref)
                    else:
                        stillUnsolved.append((ref, names))
                unsolved = stillUnsolved
                #print(max, newrefs)
                for ref in newrefs:
                    removed |= self.removeSolvedName(unsolved, ref.uname())
                if removed:
                    max = 0
            max += 1
        for ref, _ in unsolved:
            refs.append(ref)
        return refs


class Generator(Optimizer):
    def __init__(self):
        self.peg = None
        self.generated = {}
        self.generating_nonterminal = ''
        self.sids = {}
        self.memos = []
        self.Ooox = True
        self.Olex = True

    def getsid(self, name):
        if not name in self.sids:
            self.sids[name] = len(self.sids)
        return self.sids[name]

    def makelist(self, pe, v: dict, ps: list):
        if isinstance(pe, PRef):
            u = pe.uname()
            if u not in self.generated and u not in v:
                v[u] = pe
                self.makelist(pe.deref(), v, ps)
                ps.append(pe)
            return ps
        if isinstance(pe, PUnary) or isinstance(pe, PTuple):
            for e in pe:
                self.makelist(e, v, ps)
        return ps

    def generate(self, peg, **option):
        self.peg = peg
        name = option.get('start', peg.start())
        start = peg.newRef(name)
        # if 'memos' in option and not isinstance(option['memos'], list):
        if 'packrat' in peg:
            memos = peg['packrat']
            if isinstance(memos, POre):
                self.memos = memos.listDict()
            else:
                self.memos = peg.N
            # print(self.memos)
        ps = self.makelist(start, {}, [])
        ps = self.sort(ps)
        for ref in ps:
            assert isinstance(ref, PRef)
            self.generating_nonterminal = ref.uname()
            self.emitRule(ref)
            self.generating_nonterminal = ''

        return self.emitParser(start)

    def emitRule(self, ref):
        A = self.emit(ref.deref(), 0)
        if ref.peg == self.peg and ref.name in self.memos:
            idx = self.memos.index(ref.name)
            if idx != -1:
                A = pasm.pMemo(A, idx, len(self.memos))
                # A = pasm.pMemoDebug(ref.name, A, idx, self.memos)
        self.generated[ref.uname()] = A

    def emitParser(self, start):
        return pasm.generate(self.generated[start.uname()])

    def emit(self, pe: PExpr, step: int):
        pe = self.inline(pe)
        cname = pe.cname()
        if hasattr(self, cname):
            f = getattr(self, cname)
            return f(pe, step)
        print('@TODO(Generator)', cname, pe)
        return self.PChar(EMPTY, step)

    def PAny(self, pe, step):
        return pasm.pAny()

    def PChar(self, pe, step):
        return pasm.pChar(pe.text)

    def PRange(self, pe, step):
        return pasm.pRange(pe.chars, pe.ranges)

    def PAnd(self, pe, step):
        e = self.inline(pe.e)
        if(self.Olex and isinstance(e, PChar)):
            return pasm.pAndChar(e.text)
        if(self.Olex and isinstance(e, PRange)):
            return pasm.pAndRange(e.chars, e.ranges)
        return pasm.pAnd(self.emit(e, step))

    def PNot(self, pe, step):
        e = self.inline(pe.e)
        if(self.Olex and isinstance(e, PChar)):
            return pasm.pNotChar(e.text)
        if(self.Olex and isinstance(e, PRange)):
            return pasm.pNotRange(e.chars, e.ranges)
        return pasm.pNot(self.emit(e, step))

    def PMany(self, pe, step):
        e = self.inline(pe.e)
        if(self.Olex and isinstance(e, PChar)):
            return pasm.pManyChar(e.text)
        if(self.Olex and isinstance(e, PRange)):
            return pasm.pManyRange(e.chars, e.ranges)
        return pasm.pMany(self.emit(e, step))

    def PMany1(self, pe, step):
        e = self.inline(pe.e)
        if(self.Olex and isinstance(e, PChar)):
            return pasm.pMany1Char(e.text)
        if(self.Olex and isinstance(e, PRange)):
            return pasm.pMany1Range(e.chars, e.ranges)
        return pasm.pMany1(self.emit(e, step))

    def POption(self, pe, step):
        e = self.inline(pe.e)
        if(self.Olex and isinstance(e, PChar)):
            return pasm.pOptionChar(e.text)
        if(self.Olex and isinstance(e, PRange)):
            return pasm.pOptionRange(e.chars, e.ranges)
        return pasm.pOption(self.emit(e, step))

    def PSeq(self, pe, step):
        pfs = []
        for e in pe:
            pfs.append(self.emit(e, step))
            step += e.minLen()
        pfs = tuple(pfs)
        if len(pfs) == 2:
            return pasm.pSeq2(pfs[0], pfs[1])
        if len(pe) == 3:
            return pasm.pSeq3(pfs[0], pfs[1], pfs[2])
        if len(pe) == 4:
            return pasm.pSeq4(pfs[0], pfs[1], pfs[2], pfs[3])
        return pasm.pSeq(*pfs)

    # Ore
    def POre(self, pe: POre, step):
        if pe.isDict():
            return pasm.pDict(pe.listDict())
        pfs = tuple(map(lambda e: self.emit(e, step), pe))
        if len(pfs) == 2:
            return pasm.pOre2(pfs[0], pfs[1])
        if len(pe) == 3:
            return pasm.pOre3(pfs[0], pfs[1], pfs[2])
        if len(pe) == 4:
            return pasm.pOre4(pfs[0], pfs[1], pfs[2], pfs[3])
        return pasm.pOre(*pfs)

    def PRef(self, pe, step):
        return pasm.pRef(self.generated, pe.uname())

    def PName(self, pe: PName, step):
        if step == 0 and self.generating_nonterminal == pe.name:
            print(pe.position.message('Left recursion'))
            return self.emit(FAIL, step)
        return self.PRef(pe.e, step)

    # Tree Construction

    def PNode(self, pe, step):
        _, fixed, es = self.fixedEach(0, [pe])
        # print(_, fixed, es)
        if fixed is None or not self.Ooox:
            fs = self.emit(pe.e, step)
            return pasm.pNode(fs, pe.tag, pe.shift)
        else:
            # print('//OOD', self.join(fixed, *es))
            return self.emit(self.join(fixed, *es), step)

    def PEdge(self, pe, step):
        return pasm.pEdge(pe.edge, self.emit(pe.e, step))

    def PFold(self, pe, step):
        _, fixed, es = self.fixedEach(0, [pe])
        # print(_, fixed, es)
        # fixed = None
        if fixed is None or not self.Ooox:
            fs = self.emit(pe.e, step)
            return pasm.pFold(pe.edge, fs, pe.tag, pe.shift)
        else:
            # print('//OOD', self.join(fixed, *es))
            return self.emit(self.join(fixed, *es), step)

    def PAbs(self, pe, step):
        return pasm.pAbs(self.emit(pe.e, step))

    def Skip(self, pe, step):  # @skip()
        return pasm.pSkip()

    def Symbol(self, pe, step):  # @symbol(A)
        params = pe.params
        sid = self.getsid(str(params[0]))
        return pasm.pSymbol(self.emit(pe.e, step), sid)

    def Scope(self, pe, step):
        return pasm.pScope(self.emit(pe.e, step))

    def Exists(self, pe, step):  # @Match(A)
        params = pe.params
        sid = self.getsid(str(params[0]))
        return pasm.pExists(sid)

    def Match(self, pe, step):  # @Match(A)
        params = pe.params
        sid = self.getsid(str(params[0]))
        return pasm.pMatch(sid)

    def Def(self, pe, step):  # @def(A, '名詞')
        params = pe.params
        name = str(params[1]) if len(params) == 2 else str(params[0])
        pf = self.emit(pe.e, step)
        #print('@def', pf, name)
        return pasm.pDef(name, pf)

    def In(self, pe, step):  # @in(A)
        params = pe.params
        name = str(params[0])
        #print('@in', name)
        return pasm.pIn(name)


generator = Generator()


def generate(peg, **options):
    return generator.generate(peg, **options)


# ParseTree


def logger(type, pos, msg):
    print(pos.message(msg))


class TPEGLoader(object):
    def __init__(self, peg):
        self.names = {}
        self.peg = peg

    def load(self, t):
        for stmt in t:
            if stmt == 'Rule':
                name = str(stmt.name)
                if name in self.names:
                    # pos4 = stmt['name'].getpos4()
                    logger('error', stmt.name, f'redefined name {name}')
                    continue
                self.names[name] = stmt.e
            elif stmt == 'Example':
                doc = stmt.doc
                for n in stmt.names:
                    self.example(str(n), doc)
            # elif stmt == 'Import':
            #     urn = str(stmt.name)
            #     apeg = grammar(urn, **options)
            #     for n in stmt.names:
            #         lname = str(n)  # ns.Expression
            #         name = lname
            #         if lname.find('.') != -1:
            #             name = lname.split('.')[-1]
            #         pos4 = n.getpos4()
            #         if not name in apeg:
            #             logger('perror', pos4, f'undefined name {name}')
            #             continue
            #         g.add(lname, Action(apeg.newRef(name),
            #                             'import', (name, urn), pos4))
        for name in self.names:
            t = self.names[name]
            self.peg[name] = self.conv(t, 0)

    def example(self, name, doc):
        self.peg['@@example'].append((name, doc))

    def conv(self, t, step):
        tag = t.gettag()
        if hasattr(self, tag):
            f = getattr(self, tag)
            return f(t, step)
        return t

    @classmethod
    def unquote(cls, s):
        if s.startswith('\\'):
            if s.startswith('\\n'):
                return '\n', s[2:]
            if s.startswith('\\t'):
                return '\t', s[2:]
            if s.startswith('\\r'):
                return '\r', s[2:]
            if s.startswith('\\v'):
                return '\v', s[2:]
            if s.startswith('\\f'):
                return '\f', s[2:]
            if s.startswith('\\b'):
                return '\b', s[2:]
            if (s.startswith('\\x') or s.startswith('\\X')) and len(s) >= 4:
                c = int(s[2:4], 16)
                return chr(c), s[4:]
            if (s.startswith('\\u') or s.startswith('\\U')) and len(s) >= 6:
                c = chr(int(s[2:6], 16))
                if len(c) != 1:
                    c = ''  # remove unsupported unicode
                return c, s[6:]
            else:
                return s[1], s[2:]
        else:
            return s[0], s[1:]

    def Empty(self, t, step):
        return EMPTY

    def Any(self, t, step):
        return ANY

    def Char(self, t, step):
        s = str(t)
        sb = []
        while len(s) > 0:
            c, s = TPEGLoader.unquote(s)
            sb.append(c)
        return PChar(''.join(sb))

    def Class(self, t, step):
        s = str(t)
        chars = []
        ranges = []
        while len(s) > 0:
            c, s = TPEGLoader.unquote(s)
            if s.startswith('-') and len(s) > 1:
                c2, s = TPEGLoader.unquote(s[1:])
                ranges.append(c + c2)
            else:
                chars.append(c)
        if len(chars) == 0 and len(ranges) == 0:
            return EMPTY
        if len(chars) == 1 and len(ranges) == 0:
            return PChar(chars[0])
        return PRange(''.join(chars), ''.join(ranges))

    def Name(self, t, step):
        name = str(t)
        if name in self.names:
            ref = self.peg.newRef(name)
            return PName(ref, ref.uname(), t)
        if name[0].isupper() or name.startswith('_'):  # or name[0].islower() :
            logger('warning', t, f'undefined nonterminal {name}')
            self.peg[name] = EMPTY
            return self.peg.newRef(name)
        return PChar(name)

    def Quoted(self, t, step):
        name = str(t)
        if name in self.names:
            ref = self.peg.newRef(name)
            return PName(ref, ref.uname(), t)
        return PChar(name[1:-1])

    def Many(self, t, step):
        return PMany(self.conv(t.e, step))

    def Many1(self, t, step):
        return PMany1(self.conv(t.e, step))

    def Option(self, t, step):
        return POption(self.conv(t.e, step))

    def And(self, t, step):
        return PAnd(self.conv(t.e, step))

    def Not(self, t, step):
        return PNot(self.conv(t.e, step))

    def Seq(self, t, step):
        es = []
        for p in t:
            e = self.conv(p, step)
            # step += e.minLen()
            es.append(e)
        return PSeq.new(*es)

    def Ore(self, t, step):
        return POre.new(*tuple(map(lambda p: self.conv(p, step), t)))

    def Alt(self, t, step):
        return POre.new(*tuple(map(lambda p: self.conv(p, step), t)))

    def Node(self, t, step):
        tag = str(t.tag) if hasattr(t, 'tag') else ''
        e = self.conv(t.e, step)
        return PNode(e, tag, 0)

    def Edge(self, t, step):
        edge = str(t.edge) if hasattr(t, 'edge') else ''
        e = self.conv(t.e, step)
        return PEdge(edge, e)

    def Fold(self, t, step):
        edge = str(t.edge) if hasattr(t, 'edge') else ''
        tag = str(t.tag) if hasattr(t, 'tag') else ''
        e = self.conv(t.e, step)
        return PFold(edge, e, tag, 0)

    FIRST = {'lazy', 'scope', 'symbol', 'def',
             'match', 'equals', 'contains', 'cat'}

    def Func(self, t, step):
        funcname = str(t[0])
        ps = [self.conv(p, step) for p in t[1:]]
        if funcname.startswith('choice'):
            n = funcname[6:]
            if n.isdigit():
                return TPEGLoader.choiceN(t.urn_, int(n), ps)
            return TPEGLoader.choice(t.urn_, ps)
        if funcname in TPEGLoader.FIRST:
            return PAction(ps[0], funcname, tuple(ps), t)
        return PAction(EMPTY, funcname, tuple(ps), t)

    @classmethod
    def fileName(cls, e):
        s = str(e)
        return s[1:-1]  # if s.startswith('"') else s

    @classmethod
    def choice(cls, urn, es):
        ds = set()
        for e in es:
            file = TPEGLoader.fileName(e)
            file = Path(urn).parent / file
            with file.open(encoding='utf-8_sig') as f:
                ss = [x.strip('\r\n') for x in f.readlines()]
                ds |= {x for x in ss if len(x) > 0 and not x.startswith('#')}
        choice = [PChar(x) for x in sorted(ds, key=lambda x: len(x))[::-1]]
        return POre(*choice)

    @classmethod
    def choiceN(cls, urn, n, es):
        ds = set()
        for e in es:
            file = TPEGLoader.fileName(e)
            file = Path(urn).parent / file
            with file.open(encoding='utf-8_sig') as f:
                ss = [x.strip('\r\n') for x in f.readlines()]
                if n == 0:
                    ds |= {x for x in ss if len(
                        x) > 9 and not x.startswith('#')}
                else:
                    ds |= {x for x in ss if len(
                        x) == n and not x.startswith('#')}
        choice = [PChar(x) for x in ds]
        return POre(*choice)


def grammar_factory():

    def load_grammar(g, file, **options):
        # logger = options.get('logger', logger)
        # pegparser = pasm.generate(options.get('peg', TPEGGrammar))
        pegparser = pasm.generate(TPEGGrammar['Start'])
        if isinstance(file, Path) and file.is_file():
            f = file.open(encoding=options.get('encoding', 'utf-8_sig'))
            data = f.read()
            f.close()
            t = pegparser(data, file)
            basepath = str(file)
        else:
            if 'basepath' in options:
                basepath = options['basepath']
            else:
                basepath = inspect.currentframe().f_back.f_code.co_filename
            t = pegparser(file, basepath)
            basepath = (str(Path(basepath).resolve().parent))
        options['basepath'] = basepath
        if t == 'err':
            logger('error', t, 'Syntax Error')
            return
        pconv = TPEGLoader(g)
        pconv.load(t)

    def findpath(paths, file):
        if file.find('=') > 0 or file.find('<-') > 0:
            return file
        for p in paths:
            path = Path(p) / file
            if path.is_file():
                return path.resolve()
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)

    GrammarDB = {}

    def grammar(urn, **options):
        paths = []
        basepath = options.get('basepath', '')
        if basepath == '':
            paths.append('')
        else:
            paths.append(str(Path(basepath).resolve().parent))
        framepath = inspect.currentframe().f_back.f_code.co_filename
        paths.append(str(Path(framepath).resolve().parent))
        paths.append(str(Path(__file__).resolve().parent / 'grammar'))
        paths += os.environ.get('GRAMMAR', '').split(':')
        path = findpath(paths, urn)
        key = str(path)
        if key in GrammarDB:
            return GrammarDB[key]
        peg = Grammar()
        load_grammar(peg, path, **options)
        GrammarDB[key] = peg
        return peg

    return grammar


grammar = grammar_factory()


if __name__ == '__main__':
    peg = grammar('es.tpeg')
