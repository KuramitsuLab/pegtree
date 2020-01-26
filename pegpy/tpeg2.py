import sys
import os
import errno
import inspect
from collections import namedtuple
from enum import Enum
from pathlib import Path

def DEBUG(*x):
    if 'DEBUG' in os.environ:
        print('@DEBUG', *x)

# ParsingExpression

class ParsingExpression(object):
    def __iter__(self): pass
    def __len__(self): return 0

    # operator overloading
    def __and__(self, y): return Seq(self, y)
    def __rand__(self, y): return Seq(self, y)
    def __or__(self, y): return Ore2(self, y)
    def __truediv__(self, y): return Ore2(self, y)
    def __invert__(self): return Not(self)

class Any(ParsingExpression):
    def __repr__(self):
        return '.'

    def minLen(self): return 1


class Char(ParsingExpression):
    __slots__ = ['text']

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "'" + self.text.translate(CharTBL) + "'"

    def minLen(self): return len(self.text)

class Range(ParsingExpression):
    __slots__ = ['chars', 'ranges']

    def __init__(self, chars, ranges):
        self.chars = chars
        self.ranges = ranges

    def __repr__(self):
        return "[" + rs(self.ranges) + self.chars.translate(RangeTBL) + "]"

    def minLen(self): return 1

def unique_range(chars, ranges):
    cs = 0
    for c in chars:
        cs |= 1 << ord(c)
    if isinstance(ranges, str):
        r = []
        while len(ranges) > 1:
            r.append(ranges[0:2])
            ranges = ranges[2:]
        ranges = tuple(r)
    for r in ranges:
        for c in range(ord(r[0]), ord(r[1])+1):
            cs |= 1 << c
    return cs

class Ref(ParsingExpression):
    def __init__(self, name, peg):
        self.name = name
        self.peg = peg

    def __repr__(self):
        return self.name

    def uname(self):
        return self.name if self.name[0].isdigit() else self.peg.gid + self.name

    def deref(self):
        return self.peg[self.name]

    def minLen(self): 
        if not hasattr(self, 'minlen'):
            self.minlen = 0
            self.minlen = self.deref().minLen()
        return self.minlen

    def get(self, key, value):
        return getattr(self, key) if hasattr(self, key) else value

    def set(self, key, value):
        setattr(self, key, value)


class Tuple(ParsingExpression):
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

class Seq(Tuple):
    @classmethod
    def new(cls, *es):
        ls = [es[0]]
        for e in es[1:]:
            if e == EMPTY: continue
            if isinstance(e, Char) and isinstance(ls[-1], Char):
                ls[-1] = Char(ls[-1].text+e.text)
                continue
            ls.append(e)
        return ls[0] if len(ls) == 1 else Seq(*ls)

    def __repr__(self):
        return ' '.join(map(ss, self))

    def minLen(self):
        if not hasattr(self, 'minlen'):
            self.minlen = sum(map(lambda e: e.minLen(), self.es))
        return self.minlen

class Alt(Tuple):
    def __repr__(self):
        return ' | '.join(map(repr, self))

class Ore2(Tuple):
    @classmethod
    def expand(cls, e):
        choice = []
        _expand(e, choice)
        return choice[0] if len(choice)==1 else Ore2(*choice)
    
    def __repr__(self):
        return ' / '.join(map(repr, self))
    
    def listDic(self):
        dic = [e.text for e in self if isinstance(e, Char)]
        dic2 = []
        for s in dic:
            if s == '':break
            dic2.append(s)
        return dic2
    
    def trieDic(self, dic = None):
        if dic is None:
            dic = self.listDic()
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
            d[key] = self.trieDic(d[key])
        return d



def _expand(e, choice=[]):
    s = e
    while isinstance(e, Ref):
        e = e.deref()
    if isinstance(e, Ore2):
        for x in e:
            _expand(x, choice)
    else:
        choice.append(s)


class Unary(ParsingExpression):
    __slot__ = ['e']

    def __init__(self, e):
        self.e = e

    def __iter__(self):
        yield self.e

    def __len__(self):
        return 1

    def minLen(self): return self.e.minLen()



class And(Unary):
    def __repr__(self):
        return '&'+grouping(self.e, inUnary)

    def minLen(self): return 0


class Not(Unary):
    def __repr__(self):
        return '!'+grouping(self.e, inUnary)

    def minLen(self): return 0

class Many(Unary):
    def __repr__(self):
        return grouping(self.e, inUnary)+'*'

    def minLen(self): return 0

class Many1(Unary):
    def __repr__(self):
        return grouping(self.e, inUnary)+'+'

class Option(Unary):
    def __repr__(self):
        return grouping(self.e, inUnary)+'?'


class Node(Unary):
    __slot__ = ['e', 'tag']

    def __init__(self, e, tag=''):
        self.e = e
        self.tag = tag

    def __repr__(self):
        return '{' + repr(self.e) + ' #' + self.tag + '}'


class Edge2(Unary):
    __slot__ = ['e', 'edge']

    def __init__(self, e, edge=''):
        self.e = e
        self.edge = edge

    def __repr__(self):
        return ('$' if self.edge == '' else self.edge + ': ') + grouping(self.e, inUnary)


class Fold2(Unary):
    __slot__ = ['e', 'edge', 'tag']

    def __init__(self, e, edge='', tag=''):
        self.e = e
        self.edge = edge
        self.tag = tag

    def __repr__(self):
        return ('' if self.edge == '' else self.edge + ':') + '^ {' + repr(self.e) + ' #' + self.tag + '}'


class Abs(Unary):
    __slot__ = ['e']

    def __init__(self, e):
        self.e = e

    def __repr__(self):
        return f'@abs({self.e})'

# Action

class Action(Unary):
    __slots__ = ['e', 'func', 'params']
    def __init__(self, e, func, params, pos4=None):
        self.e = e
        self.func = func
        self.params = params

    def __repr__(self):
        return f'@{self.func}{self.params}'


# CONSTANT
EMPTY = Char('')
ANY = Any()
FAIL = Not(EMPTY)

# repr

def grouping(e, f):
    return '(' + repr(e) + ')' if f(e) else repr(e)

def inUnary(e):
    return isinstance(e, Ore2) \
        or isinstance(e, Seq) or isinstance(e, Alt) \
        or (isinstance(e, Edge2))or isinstance(e, Fold2)

CharTBL = str.maketrans(
    {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\\': '\\\\', "'": "\\'"})

RangeTBL = str.maketrans(
    {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\\': '\\\\', ']': '\\]', '-': '\\-'})

def rs(ranges):
    ss = tuple(map(lambda x: x[0].translate(
        RangeTBL) + '-' + x[1].translate(RangeTBL), ranges))
    return ''.join(ss)

def ss(e): 
    return grouping(e, lambda e: isinstance(e, Ore2) or isinstance(e, Alt))


def setup():
    def grouping(e, f):
        return '(' + repr(e) + ')' if f(e) else repr(e)

    def inUnary(e):
        return isinstance(e, Ore2) \
            or isinstance(e, Seq) or isinstance(e, Alt) \
            or (isinstance(e, Edge2))or isinstance(e, Fold2)

    CharTBL = str.maketrans(
        {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\\': '\\\\', "'": "\\'"})

    RangeTBL = str.maketrans(
        {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\\': '\\\\', ']': '\\]', '-': '\\-'})

    def rs(ranges):
        ss = tuple(map(lambda x: x[0].translate(
            RangeTBL) + '-' + x[1].translate(RangeTBL), ranges))
        return ''.join(ss)
    Char.__repr__ = lambda p: "'" + p.text.translate(CharTBL) + "'"
    Range.__repr__ = lambda p: "[" + \
        rs(p.ranges) + p.chars.translate(RangeTBL) + "]"
    Any.__repr__ = lambda p: '.'

    def ss(e): return grouping(e, lambda e: isinstance(
        e, Ore2)  or isinstance(e, Alt))

    Seq.__repr__ = lambda p: ' '.join(map(ss, p))
    Ore2.__repr__ = lambda p: ' / '.join(map(repr, p))
    # grouping(
    #     p.left, inUnary) + '?' if p.right == EMPTY else repr(p.left) + ' / ' + repr(p.right)
    Alt.__repr__ = lambda p: ' | '.join(map(repr, p))
    #repr(p.left) + ' | ' + repr(p.right)

    And.__repr__ = lambda p: '&'+grouping(p.e, inUnary)
    Not.__repr__ = lambda p: '!'+grouping(p.e, inUnary)
    Many.__repr__ = lambda p: grouping(p.e, inUnary)+'*'
    Many1.__repr__ = lambda p: grouping(p.e, inUnary)+'+'
    Option.__repr__ = lambda p: grouping(p.e, inUnary)+'?'
    Ref.__repr__ = lambda p: p.name
    Node.__repr__ = lambda p: '{' + str(p.e) + ' #' + p.tag + '}'
    Edge2.__repr__ = lambda p: (
        '$' if p.edge == '' else p.edge + ': ') + grouping(p.e, inUnary)
    Fold2.__repr__ = lambda p: (
        '' if p.edge == '' else p.edge + ':') + '^ {' + str(p.e) + ' #' + p.tag + '}'
    Abs.__repr__ = lambda p: f'@abs({p.e})'
    Action.__repr__ = lambda p: f'@{p.func}{p.params}'

#setup()

# # Grammar

GrammarId = 0

class Grammar(dict):
    def __init__(self):
        global GrammarId
        self.gid = str(GrammarId)
        self.N = []
        GrammarId += 1

    def __repr__(self):
        ss = []
        for rule in self.N:
            ss.append(rule)
            ss.append('=')
            ss.append(repr(self[rule]))
            ss.append('\n')
        return ''.join(ss)

    def add(self, key, item):
        if not key in self:
            self.N.append(key)
        self[key] = item

    def newRef(self, name):
        key = '@' + name
        if not key in self:
            super().__setitem__(key, Ref(name, self))
        return self[key]

    def start(self):
        if len(self.N) == 0:
            self['EMPTY'] = EMPTY
        return self.N[0]

##

def TPEG(g):
    def Xe(p):
        if isinstance(p, str):
            return Char(p)
        if isinstance(p, dict):
            for key in p:
                return Edge2(Xe(p[key]), key)
            return EMPTY
        return p

    def seq(*ps):
        if len(ps) == 0: return EMPTY
        if len(ps) == 1: return Xe(ps[0])
        return Seq(*list(map(Xe, ps)))
    e = seq

    def choice(*ps):
        return Ore2(*list(map(Xe, ps)))

    def many(*ps): return Many(seq(*ps))
    def many1(*ps): return Many1(seq(*ps))
    def option(*ps): return Option(seq(*ps))
    def TreeAs(node, *ps): return Node(seq(*ps), node)
    def ListAs(*ps): return Node(seq(*ps), '')
    def FoldAs(edge, node, *ps): return Fold2(seq(*ps), edge, node)

    def c(*ps):
        chars = []
        ranges = []
        for x in ps:
            if isinstance(x, str):
                chars.append(x)
            else:
                ranges.append(tuple(x))
        return Range(''.join(chars), ranges)
    #
    def ref(p): return g.newRef(p)
    def rule(g, name, *ps): g.add(name,seq(*ps))

    __ = ref('__')
    _ = ref('_')
    EOS = ref('EOS')
    EOL = ref('EOL')
    S = ref('S')
    COMMENT = ref('COMMENT')
    Expression = ref('Expression')
    Identifier = ref('Identifier')
    Empty = ref('Empty')

    rule(g, 'Start', __, ref('Source'), ref('EOF'))

    rule(g, '__', many(choice(c(' \t\r\n'),COMMENT)))
    rule(g, '_', many(choice(c(' \t'),COMMENT)))

    rule(g, 'EOF', Not(ANY))
    rule(g, 'COMMENT', choice(
        e('/*', many(Not(e('*/')), ANY),'*/'), 
        e('//', many(Not(EOL), ANY))))
    rule(g, 'EOL', choice('\n', '\r\n', ref('EOF')))
    rule(g, 'S', c(' \t'))

    rule(g, 'Source', TreeAs('Source', many({'': ref('Statement')})))
    rule(g, 'EOS', _, many(choice(e(';', _), e(EOL,choice(S,COMMENT),_), EOL)))

    rule(g, 'Statement', choice(ref('Import'),ref('Example'),ref('Rule')))

    rule(g, 'Rule', TreeAs('Rule', {'name': Identifier}, __, '=', __, option(
        c('/|'), __), {'inner': Expression}, EOS))

    NAME = c(('A', 'Z'), ('a', 'z'), '@_') & many(
        c(('A', 'Z'), ('a', 'z'), ('0', '9'), '_.'))
    
    rule(g, 'Identifier', TreeAs('Name', NAME | e(
        '"', many(e(r'\"') | Not(c('\\"\n')) & ANY), '"')))

    # import
    FROM = option(_, 'import', S, _, {'names': ref('Names')})
    rule(g, 'Import', TreeAs('Import', 'from', S, _, {
                         'name': Identifier / ref('Char')}, FROM) & EOS)

    rule(g,'Example', TreeAs('Example', 'example', S, _, {
                          'names': ref('Names')}, {'doc': ref('Doc')}) & EOS)
    rule(g, 'Names', ListAs({'': Identifier}, _, many(
        c(',&'), _, {'': Identifier}, _)))
    
    DELIM = Xe("'''")
    DOC1 = TreeAs("Doc", many(Not(e(DELIM, EOL)), ANY))
    DOC2 = TreeAs("Doc", many(Not(c('\r\n')), ANY))
    rule(g,'Doc', e(DELIM, many(S), EOL, DOC1, DELIM) | DOC2)

    rule(g, 'Expression', ref('Choice'), option(
        FoldAs('left', 'Alt', many1(__, '|', _, {'right': ref('Choice')}))))

    rule(g, 'Choice', ref('Sequence'), option(
        FoldAs('left', 'Ore', many1(__, '/', _, {'right': ref('Sequence')}))))

    SS = choice(e(S, _, ~EOL), e(many1(_, EOL), S, _))
    rule(g, 'Sequence', ref('Predicate'), option(
        FoldAs('left', 'Seq', many1(SS, {'right': ref('Predicate')}))   ))

    rule(g, 'Predicate', choice(ref('Not'),ref('And'),ref('Suffix')))

    rule(g, 'Not', TreeAs('Not', '!', {'inner': ref('Predicate')}))
    rule(g,'And', TreeAs('And', '&', {'inner': ref('Predicate')}))
    #g['Append'] = TreeAs('Append', '$', {'inner': ref('Term')})

    rule(g, 'Suffix', ref('Term'), choice(
        FoldAs('inner', 'Many', '*'),
        FoldAs('inner', 'Many1', '+'),
        FoldAs('inner', 'Option', '?'), EMPTY))

    rule(g, 'Term', choice(ref('Group'),ref('Char'),ref('Class'),ref('Any'),ref('Node'),
        ref('Fold'),ref('EdgeFold'),ref('Edge'),ref('Func'),ref('Identifier')))
    rule(g, 'Group', '(', __, choice(Expression,Empty), __, ')')

    rule(g, 'Empty', TreeAs('Empty', EMPTY))
    rule(g, 'Any', TreeAs('Any', '.'))
    rule(g, 'Char', "'", TreeAs('Char', many(
        e('\\', ANY) | Not(c("'\n")) & ANY)), "'")
    rule(g, 'Class', 
        '[', TreeAs('Class', many(e('\\', ANY) | e(Not(e("]")),ANY))), ']')

    Tag = e('{', __, option('#', {'node': ref('Identifier')}), __)
    ETag = e(option('#', {'node': ref('Identifier')}), __, '}')

    rule(g, 'Node', TreeAs('Node', Tag, {'inner': choice(Expression,Empty)}, __, ETag))
    rule(g, 'Fold', '^', _, TreeAs(
        'Fold', Tag, {'inner': choice(Expression,Empty)}, __, ETag))
    rule(g, 'Edge', TreeAs('Edge', {'edge': ref('EdgeName')}, ':', _, {
                       'inner': ref('Term')}))
    rule(g, 'EdgeFold', TreeAs('Fold', {'edge': ref('EdgeName')}, ':', _, '^', _, Tag, {
                           'inner': choice(Expression,Empty)}, __, ETag))
    rule(g, 'EdgeName', TreeAs('', c(('a', 'z'), '$'), many(
        c(('A', 'Z'), ('a', 'z'), ('0', '9'), '_'))))
    rule(g, 'Func', TreeAs('Func', '@', {'name': Identifier}, '(', __, {
                       'params': ref('Params')}, ')'))
    rule(g, 'Params', ListAs({'': Expression}, many(
        _, ',', __, {'': Expression}), __))
    # rule(g, 'Ref', TreeAs('Ref', ref('REF')))
    # rule(g, 'REF', e('"', many(Xe('\\"') | e(Not(c('\\"\n')), ANY)), '"') | many1(
    #     Not(c(' \t\r\n(,){};<>[|/*+?=^\'`#')) & ANY))
    #g.N = ['Start', 'Sequence']
    return g


TPEGGrammar = TPEG(Grammar())
#print(TPEGGrammar)

######################################################################
# ast.env

def bytestr(b):
    return b.decode('utf-8') if isinstance(b, bytes) else b

#####################################

class PTree(object):
    __slots__ = ['prev', 'tag', 'spos', 'epos', 'child']

    def __init__(self, prev, label, spos, epos, child):
        self.prev = prev
        self.tag = tag
        self.spos = spos
        self.epos = epos
        self.child = child

    def isEdge(self):
        return self.epos < 0            

class AST(object):
    def __init__(self):
        pass


# ParserContext

State = namedtuple('State', 'sid val prev')


class Memo(object):
    __slots__ = ['key', 'pos', 'ast', 'result']

    def __init__(self):
        self.key = -1
        self.pos = 0
        self.ast = None
        self.result = False


class ParserContext:
    __slots__ = ['urn', 'inputs', 'pos', 'epos',
                 'headpos', 'ast', 'state', 'memo']

    def __init__(self, urn, inputs, spos, epos):
        self.urn = urn
        self.inputs = inputs
        self.pos = spos
        self.epos = epos
        self.headpos = spos
        self.ast = None
        self.state = None
        self.memo = [Memo() for x in range(1789)]

    def getstate(self, state, sid):
        while state is not None:
            if state.sid == sid:
                return state
            state = state.prev
        return None


# Generator


def match_empty(px): return True


def match_any(px):
    if px.pos < px.epos:
        px.pos += 1
        return True
    return False


class Generator(object):
    def __init__(self):
        self.peg = None
        self.generated = {}
        self.generating_nonterminal = ''
        self.pcache = {'': match_empty}
        self.sids = {}

    def getsid(self, name):
        if not name in self.sids:
            self.sids[name] = len(self.sids)
        return self.sids[name]

    def makelist(self, pe, v: dict, ps: list):
        if isinstance(pe, Ref):
            u = pe.uname()
            if u not in self.generated and u not in v:
                v[u] = pe
                self.makelist(pe.deref(), v, ps)
                ps.append(pe)
            return ps
        if isinstance(pe, Unary) or isinstance(pe, Tuple):
            for e in pe:
                self.makelist(e, v, ps)
        return ps

    def generate(self, peg, **option):
        self.peg = peg
        name = option.get('start', peg.start())
        start = peg.newRef(name)
        # if 'memos' in option and not isinstance(option['memos'], list):
        memos = option.get('memos', peg.N)
        ps = self.makelist(start, {}, [])

        for ref in ps:
            assert isinstance(ref, Ref)
            uname = ref.uname()
            self.generating_nonterminal = uname
            A = self.emit(ref.deref())
            self.generating_nonterminal = ''
            idx = memos.index(ref.name)
            if idx != -1 and ref.peg == peg:
                A = self.memoize(idx, len(memos), A)
            self.generated[uname] = A

        pf = self.generated[start.uname()]
        conv = option.get('conv', lambda x: x)

        def parse(inputs, urn='(unknown source)', pos=0, epos=None):
            if epos is None:
                epos = len(inputs)
            px = ParserContext(inputs, pos, epos)
            pos = px.pos
            result = None
            if not pf(px):
                result = PTree(None, "err", px.headpos, px.headpos, None)
            else:
                result = px.ast if px.ast is not None else PTree(None, 
                    "", pos, px.pos, None)
            return conv(result)
        return parse

    def emit(self, pe: ParsingExpression, step: int):
        if isinstance(pe, Action):
            cname = pe.func
        else:
            cname = pe.__class__.__name__
        if hasattr(self, cname):
            f = getattr(self, cname, step)
            return f(pe)
        print('@TODO(Generator)', cname, pe)
        return match_empty

    def memoize(self, mp, msize, A):
        def match_memo(px):
            key = (msize * px.pos) + mp
            m = px.memo[key % 1789]
            if m.key == key:
                px.pos = m.pos
                if m.ast != False:
                    px.ast = m.ast
                return m.result
            prev = px.ast
            m.result = A(px)
            m.pos = px.pos
            m.ast = px.ast if prev != px.ast else False
            m.key = key
            return m.result
        return match_memo

    def Any(self, pe, step):
        return match_any

    def Char(self, pe, step):
        if pe.text in self.cache:
            return self.cache[pe.text]
        chars = pe.text
        clen = len(pe.text)
        #
        def match_char(px):
            if px.inputs.startswith(chars, px.pos):
                px.pos += clen
                return True
            return False
        self.cache[pe.text] = match_char
        return match_char

    def Range(self, pe, step):
        bitset = unique_range(pe)  # >> offset

        def match_bitset(px):
            if px.pos < px.epos:
                shift = ord(px.inputs[px.pos])  # - offset
                if shift >= 0 and (bitset & (1 << shift)) != 0:
                    px.pos += 1
                    return True
            return False

        return match_bitset

    def And(self, pe, step):
        pf = self.emit(pe.e, step)

        def match_and(px):
            pos = px.pos
            if pf(px):
                # backtracking
                px.headpos = max(px.pos, px.headpos)
                px.pos = pos
                return True
            return False

        return match_and

    def Not(self, pe, step):
        pf = self.emit(pe.e, step)

        def match_not(px):
            pos = px.pos
            ast = px.ast
            if not pf(px):
                # backtracking
                px.headpos = max(px.pos, px.headpos)
                px.pos = pos
                px.ast = ast
                return True
            return False

        return match_not

    def Many(self, pe, step):
        pf = self.emit(pe.e, step)

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

    def Many1(self, pe, step):
        pf = self.emit(pe.e, step)

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

    def Option(self, pe, step):
        pf = self.emit(pe.e, step)

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

    def Seq(self, pe, step):
        if len(pe) == 2:
            return self.Seq(pe)
        if len(pe) == 3:
            return self.Seq3(pe)
        #
        pfs = tuple(map(lambda e: self.emit(e), pe))

        def match_seq(px):
            for pf in pfs:
                if not pf(px):
                    return False
            return True
        return match_seq

    # Ore

    def Ore(pe, **option):
        pfs = tuple(map(lambda e: e.gen(**option), pe))

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


    def OreDic(self, dic: list):
        d = trie(dic)

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

    def gen_Ore(pe, **option):
        pe2 = Ore2.expand(pe)
        if not isinstance(pe2, Ore2):
            return self.emit(pe2)
        pe = pe2
        dic = [e.text for e in pe if isinstance(e, Char)]
        #print('@choice', len(pe), len(dic))
        if len(dic) == len(pe):
            d = trie(dic)
            return lambda px: match_trie(px, d)
        #print('@choice', len(pe))
        return gen_Ore(pe, **option)

    def Ref(self, pe, step):
        uname = ref.uname()
        generated = self.generated
        if uname not in generated:
            generated[uname] = lambda px: generated[uname](px)
        return generated[uname]

    # Tree Construction

    def Node(self, pe, step):
        pf = self.emit(pe.e, step)
        node = pe.tag

        def make_tree(px):
            pos = px.pos
            prev = px.ast
            px.ast = None
            if pf(px):
                px.ast = PTree(prev, node, pos, px.pos, px.ast)
                return True
            return False

        return make_tree

    def Edge(self, pe, step):
        pf = self.emit(pe.e, step)
        node = pe.tag
        edge = pe.edge

        def match_edge(px):
            prev = px.ast
            if pf(px):
                px.ast = PTree(prev, edge, -1, -1, px.ast)
                return True
            return False
        return match_edge

    def Fold(self, pe, step):
        pf = self.emit(pe.e)
        node = pe.tag
        edge = pe.edge

        def match_fold(px):
            pos = px.pos
            px.ast = PTree(None, edge, -1, -1, px.ast)
            if pf(px):
                px.ast = PTree(prev, node, pos, px.pos, px.ast)
                return True
            return False
        return match_fold

    def Abs(self, pe, step):
        pf = self.emit(pe.e, step)

        def match_abs(px):
            ast = px.ast
            if pf(px):
                px.ast = ast
                return True
            return False
        return match_abs

    # StateTable

    # def adddict(px, s):
    #     if len(s) == 0:
    #         return
    #     key = s[0]
    #     if key in px.memo:
    #         l = px.memo[key]
    #         slen = len(s)
    #         for i in range(len(l)):
    #             if slen > len(l[i]):
    #                 l.insert(i, s)
    #                 return
    #         l.append(s)
    #     else:
    #         px.memo[key] = [s]

    def Lazy(self, pe, step):  # @lazy(A)
        name = pe.e.name
        peg = self.peg
        return peg.newRef(name).gen(**option) if name in peg else pe.e.gen(**option)

    def Skip(self, pe, step): # @skip()
        def skip(px):
            px.pos = min(px.headpos, px.epos)
            return True
        return skip
    
    def Symbol(self, pe, step): # @symbol(A)
        params = pe.params
        sid = self.getsid(str(params[0]))
        pf = self.emit(pe.e, step)

        def match_symbol(px):
            pos = px.pos
            if pf(px):
                px.state = State(sid, px.inputs[pos:px.pos], px.state)
                return True
            return False
        return match_symbol

    def Scope(self, pe, step):
        pf = self.emit(pe.e, step)

        def scope(px):
            state = px.state
            res = pf(px)
            px.state = state
            return res
        return scope

    def Exists(self, pe, step):  # @Match(A)
        params = pe.params
        sid = self.getsid(str(params[0]))
        return lambda px: px.getstate(px.state, sid) != None

    def Match(self, pe, step):  # @Match(A)
        params = pe.params
        sid = self.getsid(str(params[0]))
        pf = self.emit(pe.e)

        def match(px):
            state = px.getstate(px.state, sid)
            if state is not None and px.inputs.startswith(state.val, px.pos):
                px.pos += len(state.val)
                return True
            return False
        return match

    def Def(self, pe, step):
        params = pe.params
        name = str(params[0])
        pf = self.emit(pe.e, step)

        def define_dict(px):
            pos = px.pos
            if pf(px):
                s = px.inputs[pos:px.pos]
                if len(s) == 0:
                    return True
                if name in px.memo:
                    d = px.memo[name]
                else:
                    d = {}
                    px.memo[name] = d
                key = s[0]
                if not key in d:
                    d[key] = [s]
                    return True
                l = d[key]
                slen = len(s)
                for i in range(len(l)):
                    if slen > len(l[i]):
                        l.insert(i, s)
                        break
                return True
            return False
        return define_dict

    def In(self, pe, step): # @in(NAME)
        name = str(params[0])

        def refdict(px):
            if name in px.memo and px.pos < px.epos:
                d = px.memo[name]
                key = px.inputs[px.pos]
                if key in d:
                    for s in d[key]:
                        if px.inputs.startswith(s, px.pos):
                            px.pos += len(s)
                            return True
            return False
        return refdict

    '''
            if fname == 'on':  # @on(!A, e)
            name = str(params[0])
            pf = pe.e.gen(**option)
            if name.startswith('!'):
                sid = getsid(name[1:])

                def off(px):
                    state = px.state
                    px.state = State(sid, False, px.state)
                    res = pf(px)
                    px.state = state
                    return res
                return off

            else:
                sid = getsid(name[1:])

                def on(px):
                    state = px.state
                    px.state = State(sid, False, px.state)
                    res = pf(px)
                    px.state = state
                    return res
                return on

        if fname == 'if':  # @if(A)
            sid = getsid(str(params[0]))

            def cond(px):
                state = getstate(px.state, sid)
                return state != None and state.val
            return cond
    '''

#####################################

class ParseRange(object):
    __slots__ = ['urn', 'inputs', 'spos', 'epos']
    def __init__(self, urn, inputs, spos, epos):
        self.urn = urn
        self.inputs = inputs
        self.spos = spos
        self.epos = epos

    @classmethod
    def expand(cls, urn, inputs, spos):
        inputs = inputs[:spos + (1 if len(inputs) > spos else 0)]
        rows = inputs.split(b'\n' if isinstance(inputs, bytes) else '\n')
        return urn, spos, len(rows), len(rows[-1])-1

    def start(self):
        return ParseRange.expand(self.urn, self.inputs, self.spos)

    def end(self):
        return ParseRange.expand(self.urn, self.inputs, self.epos)

    def decode(self):
        inputs, spos, epos = self.inputs, self.spos, self.epos
        LF = b'\n' if isinstance(inputs, bytes) else '\n'
        rows = inputs[:spos + (1 if len(inputs) > spos else 0)]
        rows = rows.split(LF)
        linenum, column = len(rows), len(rows[-1])-1
        begin = inputs.rfind(LF, 0, spos) + 1
        #print('@', spos, begin, inputs)
        end = inputs.find(LF, spos)
        #print('@', spos, begin, inputs)
        if end == -1 : end = len(inputs)
        #print('@[', begin, spos, end, ']', epos)
        line = inputs[begin:end] #.replace('\t', '   ')
        mark = []
        endcolumn = column + (epos - spos)
        for i, c in enumerate(line):
            if column <= i and i <= endcolumn:
                mark.append('^' if ord(c) < 256 else '^^')
            else:
                mark.append(' ' if ord(c) < 256 else '  ')
        mark = ''.join(mark)
        return (self.urn, spos, linenum, column, bytestr(line), mark)

    def showing(self, msg='Syntax Error'):
        urn, pos, linenum, cols, line, mark = self.decode()
        return '{} ({}:{}:{}+{})\n{}\n{}'.format(msg, urn, linenum, cols, pos, line, mark)


class ParseTree(ParseRange):
    __slots__ = ['tag', 'urn', 'inputs', 'spos', 'epos', 'child']

    def __init__(self, tag, urn, inputs, spos, epos, child):
        self.tag = tag
        self.urn = urn
        self.inputs = inputs
        self.spos = spos
        self.epos = epos
        self.child = child

    def __eq__(self, tag):
        return self.tag == tag

    def isError(self):
        return self.tag == 'err'

    def subs(self):
        if not isinstance(self.child, list):
            stack = []
            cur = self.child
            while cur is not None:
                prev, edge, child = cur
                if child is not None:
                    stack.append((edge, child))
                cur = prev
            self.child = list(stack[::-1])
        return self.child

    def __len__(self):
        return len(self.subs())

    def __contains__(self, label):
        for edge, _ in self.subs():
            if label == edge: return True
        return False

    def __getitem__(self, label):
        if isinstance(label, int):
            return self.subs()[label][1]
        for edge, child in self.subs():
            if label == edge:
                return child
        return None

    def get(self, label: str, default=None, conv=lambda x: x):
        for edge, child in self.subs():
            if label == edge:
                return conv(child)
        return default
    
    def __getattr__(self, label: str):
        for edge, child in self.subs():
            if label == edge: return child
        raise AttributeError()

    def getString(self, label: str, default=None):
        return self.get(label, default, str)

    def keys(self):
        ks = []
        for edge, _ in self.subs():
            if edge != '': ks.append(edge)
        return ks

    def __iter__(self):
        return map(lambda x: x[1], self.subs())

    def __str__(self):
        s = self.inputs[self.spos:self.epos]
        return s.decode('utf-8') if isinstance(s, bytes) else s

    def __repr__(self):
        if self.isError():
            return self.showing('Syntax Error')
        sb = []
        self.strOut(sb)
        return "".join(sb)

    def strOut(self, sb):
        sb.append("[#")
        sb.append(self.tag)
        c = len(sb)
        for tag, child in self.subs():
            sb.append(' ' if tag == '' else ' ' + tag + '=')
            if hasattr(child, 'strOut'):
                child.strOut(sb)
            else:
                sb.append(f'@FIXME({repr(child)})')
        if c == len(sb):
            s = self.inputs[self.spos:self.epos]
            if isinstance(s, str):
                sb.append(" '")
                sb.append(s)
                sb.append("'")
            elif isinstance(s, bytes):
                sb.append(" '")
                sb.append(s.decode('utf-8'))
                sb.append("'")
            else:
                sb.append(" ")
                sb.append(str(s))
        sb.append("]")

    def pos(self):
        return self.start()

    def getpos4(self):
        return ParseRange(self.urn, self.inputs, self.spos, self.epos)

    def dump(self, indent='', edge='', bold=lambda x: x, println= lambda *x: print(*x)):
        if self.child is None:
            s = self.inputs[self.spos : self.epos]
            println(indent + edge + bold("[#" + self.tag), repr(s) + bold("]"))
            return
        println(indent + edge + bold("[#" + self.tag))
        indent2 = '  ' + indent
        for tag, child in self.subs():
            if tag != '': tag = tag+'='
            child.dump(indent2, tag, bold, println)
        println(indent + bold("]"))

# TreeConv

class ParseTreeConv(object):
    def settree(self, s, t):
        if hasattr(s, 'pos3'):
            s.pos3 = t.pos3()
        return s

    def conv(self, t: ParseTree, logger):
        tag = t.tag
        if hasattr(self, tag):
            f = getattr(self, tag)
            return self.settree(f(t, logger), t)
        return t

class ParseError(IOError):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return self.pos.showing()


######################################################################

def setup_generate():

    def gen_Char(pe, **option):
        chars = pe.text
        clen = len(pe.text)
        if clen == 0:
            return lambda px: True

        def match_char(px):
            if px.inputs.startswith(chars, px.pos):
                px.pos += clen
                return True
            return False

        return match_char

    # Range

    def first_range(pe):
        cs = 0
        for c in pe.chars:
            cs |= 1 << ord(c)
        for r in pe.ranges:
            for c in range(ord(r[0]), ord(r[1])+1):
                cs |= 1 << c
        return cs
    Range.bits = first_range

    def gen_Range(pe, **option):
        #offset = pe.min()
        bitset = first_range(pe)  # >> offset

        def bitmatch(px):
            if px.pos < px.epos:
                shift = ord(px.inputs[px.pos])  # - offset
                if shift >= 0 and (bitset & (1 << shift)) != 0:
                    px.pos += 1
                    return True
            return False

        return bitmatch

    # Any

    def gen_Any(pe, **option):
        def match_any(px):
            if px.pos < px.epos:
                px.pos += 1
                return True
            return False

        return match_any

    # And

    def gen_And(pe, **option):
        pf = pe.e.gen(**option)

        def match_and(px):
            pos = px.pos
            if pf(px):
                # backtracking
                px.headpos = max(px.pos, px.headpos)
                px.pos = pos
                return True
            return False

        return match_and

    # Not

    def gen_Not(pe, **option):
        pf = pe.e.gen(**option)

        def match_not(px):
            pos = px.pos
            ast = px.ast
            if not pf(px):
                # backtracking
                px.headpos = max(px.pos, px.headpos)
                px.pos = pos
                px.ast = ast
                return True
            return False

        return match_not

    # Many

    def gen_Many(pe, **option):
        pf = pe.e.gen(**option)

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

    def gen_Many1(pe, **option):
        pf = pe.e.gen(**option)

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

    def gen_Option(pe, **option):
        pf = pe.e.gen(**option)

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

    def gen_Seq(pe, **option):
        if len(pe) == 2:
            pf0 = pe.es[0].gen(**option)
            pf1 = pe.es[1].gen(**option)
            return lambda px: pf0(px) and pf1(px)
        pfs = tuple(map(lambda e: e.gen(**option), pe))
        #print('@seq', len(pe))
        def match_seq(px):
            for pf in pfs:
                if not pf(px):
                    return False
            return True
        return match_seq

    # Ore

    def gen_Ore(pe, **option):
        pfs = tuple(map(lambda e: e.gen(**option), pe))

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

    def trie(dic):
        if '' in dic or len(dic) < 10:
            return dic
        d = {}
        for s in dic:
            s0, s = s[0], s[1:]
            if s0 in d:
                ss = d[s0]
                if not s in ss: ss.append(s)
            else:
                d[s0] = [s]
        for key in d:
            d[key] = trie(d[key])
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


    def gen_Ore2(pe, **option):
        pe2 = Ore2.expand(pe)
        if not isinstance(pe2, Ore2):
            #print('@not choice', pe, pe2)
            return pe2.gen(**option)
        pe = pe2
        dic = [e.text for e in pe if isinstance(e, Char)]
        #print('@choice', len(pe), len(dic))
        if len(dic) == len(pe):
            d = trie(dic)
            return lambda px: match_trie(px, d)
        #print('@choice', len(pe))
        return gen_Ore(pe, **option)

    # Ref
    '''
    def gen_Ref0(ref, **option):
        f = ref.get('tpegfunc', None)
        if f is None:
            try:
                ref.tpegfunc = lambda px: ref.tpegfunc(px)
                ref.tpegfunc = gen_Pexp(ref.deref(), **option)
                return ref.tpegfunc
            except RecursionError:
                option['lazyfuncs'].append(ref)
                return lambda px: ref.tpegfunc(px)
        return f
    '''

    def gen_Memo(mp, msize, A):
        def memoMatch(px):
            key = (msize * px.pos) + mp
            m = px.memo[key % 1789]
            if m.key == key:
                px.pos = m.pos
                return m.result
            m.result = A(px)
            m.pos = px.pos
            m.key = key
            return m.result
        return memoMatch

    def gen_Tree(mp, msize, A):
        def memoTree(px):
            key = (msize * px.pos) + mp
            m = px.memo[key % 1789]
            if m.key == key:
                px.pos = m.pos
                px.ast = m.ast
                return m.result
            m.result = A(px)
            m.pos = px.pos
            m.ast = px.ast
            m.key = key
            return m.result
        return memoTree

    def gen_Ref(ref, **option):
        if not hasattr(ref, 'parsefunc'):
            return gen_dummy(ref)
        return ref.parsefunc

    # Tree Construction

    def gen_Node(pe, **option):
        node = pe.tag
        pf = pe.e.gen(**option)
        mtree = option.get('tree', ParseTree)

        def tree(px):
            pos = px.pos
            px.ast = None
            if pf(px):
                px.ast = mtree(node, px.urn, px.inputs, pos, px.pos, px.ast)
                return True
            return False

        return tree


    def Merge(prev, edge, child):
        return (prev, edge, child)


    def gen_Edge(pe, **option):
        edge = pe.edge
        pf = pe.e.gen(**option)
        merge = option.get('merge', Merge)

        def fedge(px):
            prev = px.ast
            if pf(px):
                px.ast = merge(prev, edge, px.ast)
                return True
            return False
        return fedge

    def gen_Fold(pe, **option):
        edge = pe.edge
        node = pe.tag
        pf = pe.e.gen(**option)
        mtree = option.get('tree', ParseTree)
        merge = option.get('merge', Merge)

        def fold(px):
            pos = px.pos
            px.ast = merge(None, edge, px.ast)
            if pf(px):
                px.ast = mtree(node, px.urn, px.inputs, pos, px.pos, px.ast)
                return True
            return False

        return fold

    def gen_Abs(pe, **option):
        pf = pe.e.gen(**option)

        def unit(px):
            ast = px.ast
            if pf(px):
                px.ast = ast
                return True
            return False

        return unit

    # StateTable

    State = namedtuple('State', 'sid val prev')

    SIDs = {}

    def getsid(name):
        if not name in SIDs:
            SIDs[name] = len(SIDs)
        return SIDs[name]

    def getstate(state, sid):
        while state is not None:
            if state.sid == sid:
                return state
            state = state.prev
        return None
    
    # def adddict(px, s):
    #     if len(s) == 0:
    #         return
    #     key = s[0]
    #     if key in px.memo:
    #         l = px.memo[key]
    #         slen = len(s)
    #         for i in range(len(l)):
    #             if slen > len(l[i]):
    #                 l.insert(i, s)
    #                 return
    #         l.append(s)
    #     else:
    #         px.memo[key] = [s]

    def gen_Action(pe, **option):
        fname = pe.func
        params = pe.params

        if fname == 'lazy':  # @lazy(A)
            name = pe.e.name
            peg = option.get('peg')
            return peg.newRef(name).gen(**option) if name in peg else pe.e.gen(**option)

        if fname == 'skip':  # @recovery({..})
            def skip(px):
                px.pos = min(px.headpos, px.epos)
                return True
            return skip

        # SPEG
        if fname == 'symbol':   # @symbol(A)
            sid = getsid(str(params[0]))
            pf = pe.e.gen(**option)

            def symbol(px):
                pos = px.pos
                if pf(px):
                    px.state = State(sid, px.inputs[pos:px.pos], px.state)
                    return True
                return False
            return symbol

        if fname == 'exists':   # @exists(A)
            sid = getsid(str(params[0]))
            return lambda px: getstate(px.state, sid) != None

        if fname == 'match':   # @match(A)
            sid = getsid(str(params[0]))

            def match(px):
                state = getstate(px.state, sid)
                if state is not None and px.inputs.startswith(state.val, px.pos):
                    px.pos += len(state.val)
                    return True
                return False
            return match

        if fname == 'scope':  # @scope(e)
            pf = pe.e.gen(**option)

            def scope(px):
                state = px.state
                res = pf(px)
                px.state = state
                return res
            return scope

        if fname == 'on':  # @on(!A, e)
            name = str(params[0])
            pf = pe.e.gen(**option)
            if name.startswith('!'):
                sid = getsid(name[1:])

                def off(px):
                    state = px.state
                    px.state = State(sid, False, px.state)
                    res = pf(px)
                    px.state = state
                    return res
                return off

            else:
                sid = getsid(name[1:])

                def on(px):
                    state = px.state
                    px.state = State(sid, False, px.state)
                    res = pf(px)
                    px.state = state
                    return res
                return on

        if fname == 'if':  # @if(A)
            sid = getsid(str(params[0]))

            def cond(px):
                state = getstate(px.state, sid)
                return state != None and state.val
            return cond

        if fname == 'def':  # @def(NAME)
            name = str(params[0])
            pf = pe.e.gen(**option)

            def defdict(px):
                pos = px.pos
                if pf(px):
                    s = px.inputs[pos:px.pos]
                    if len(s) == 0:
                        return True
                    if name in px.memo:
                        d = px.memo[name]
                    else:
                        d = {}
                        px.memo[name] = d
                    key = s[0]
                    if not key in d:
                        d[key] = [s]
                        return True
                    l = d[key]
                    slen = len(s)
                    for i in range(len(l)):
                        if slen > len(l[i]):
                            l.insert(i, s)
                            break
                    return True
                return False
            return defdict

        if fname == 'in':  # @in(NAME)
            name = str(params[0])

            def refdict(px):
                if name in px.memo and px.pos < px.epos:
                    d = px.memo[name]
                    key = px.inputs[px.pos]
                    if key in d:
                        for s in d[key]:
                            if px.inputs.startswith(s, px.pos):
                                px.pos += len(s)
                                return True
                return False
            return refdict

        print('@TODO: gen_Action', pe.func)
        return pe.e.gen(**option)

    #Empty.gen = gen_Empty
    Char.gen = gen_Char
    Range.gen = gen_Range
    Any.gen = gen_Any

    And.gen = gen_And
    Not.gen = gen_Not
    Many.gen = gen_Many
    Many1.gen = gen_Many1
    Option.gen = gen_Option

    Seq.gen = gen_Seq
    #Ore2.gen = gen_Ore
    Ore2.gen = gen_Ore2
    Alt.gen = gen_Ore2
    Ref.gen = gen_Ref

    Node.gen = gen_Node
    Edge2.gen = gen_Edge
    Fold2.gen = gen_Fold
    Abs.gen = gen_Abs

    Action.gen = gen_Action

    def makelist(pe, v: dict, ps: list):
        if isinstance(pe, Ref):
            u = pe.uname();
            if u not in v and not hasattr(pe, 'parsefunc'): 
                v[u] = pe
                makelist(pe.deref(), v, ps)
                ps.append(pe)
            return ps
        if isinstance(pe, Unary) or isinstance(pe, Tuple):
            for e in pe:
                makelist(e, v, ps)
        return ps

    def gen_dummy(ref):
        return lambda px : ref.parsefunc(px)

    def generate(peg, **option):
        name = option.get('start', peg.start())
        p = peg.newRef(name)
        option['peg'] = peg
        # if 'memos' in option and not isinstance(option['memos'], list):
        option['memos'] = peg.N

        ps = makelist(p, {}, [])
        for ref in ps:
            assert isinstance(ref, Ref)
            ref.parsefunc = gen_dummy(ref)
            A = ref.deref().gen(**option)
            if 'memos' in option:
                memos = option['memos']
                idx = memos.index(ref.name)
                if idx != -1: 
                    ts = ref.deref().treeState()
                    if ts == T.Unit:
                        A = gen_Memo(idx, len(memos), A)
                    if ts == T.Tree:
                        A = gen_Tree(idx, len(memos), A)
            ref.parsefunc = A
        
        pf = p.parsefunc
        mtree = option.get('tree', ParseTree)
        conv = option.get('conv', lambda x: x)

        def parse(inputs, urn='(unknown source)', pos=0, epos=None):
            if epos is None:
                epos = len(inputs)
            px = ParserContext(urn, inputs, pos, epos)
            pos = px.pos
            result = None
            if not pf(px):
                result = mtree("err", urn, inputs,
                               px.headpos, px.headpos, None)
            else:
                result = px.ast if px.ast is not None else mtree(
                    "", urn, inputs, pos, px.pos, None)
            return conv(result)

        return parse
    return generate

generate = setup_generate()

# ######################################################################

## TreeState

class T(Enum):
    Unit = 0
    Tree = 1
    Mut = 2
    Fold = 3

def nameTreeState(n):
    loc = n.rfind('.')
    n = n[loc+1:] if loc > 0 else n
    c = n[0]
    if c.islower():
        if n.replace('_','').islower() : return T.Mut
    if c.isupper():
        for c in n:
            if c.islower():
                return T.Tree
    return T.Unit

# isAlwaysConsumed
def setup2():

    def defmethod(name, f, cs=[
        Char, Range, Any, Seq, Ore2, Alt, And, Not, Many, Many1, Ref,
        Node, Edge2, Fold2, Abs, Action]):
        for c in cs: setattr(c, name, f)

    defmethod('isAlwaysConsumed', lambda p: len(p.text) > 0, [Char])
    defmethod('isAlwaysConsumed', lambda p: True, [Any, Range])
    defmethod('isAlwaysConsumed', lambda p: False, [Many, Not, And, Option])
    defmethod('isAlwaysConsumed',
            lambda p: p.e.isAlwaysConsumed(),
            [Many1, Edge2, Node, Fold2, Abs, Action])

    def checkSeq(p):
        for e in p:
            if e.isAlwaysConsumed(): return True
        return False
    Seq.isAlwaysConsumed = checkSeq

    def checkOre(p):
        for e in p:
            if not e.isAlwaysConsumed():
                return False
        return True
    Ore2.isAlwaysConsumed = checkOre
    Alt.isAlwaysConsumed = checkOre

    def checkRef(p):
        memoed = p.get('isAlwaysConsumed', None)
        if memoed == None:
            p.isAlwaysConsumed= True
            memoed = (p.deref()).isAlwaysConsumed()
            p.isAlwaysConsumed = memoed
        return memoed
    Ref.isAlwaysConsumed = checkRef

    # treeState
    def treeState(e):
        return e.treeState()

    defmethod('treeState', lambda p: T.Unit, [Char, Any, Range, Not, Abs])
    defmethod('treeState', lambda p: T.Tree, [Node] )
    defmethod('treeState', lambda p: T.Mut,  [Edge2] )
    defmethod('treeState', lambda p: T.Fold, [Fold2] )

    def mutTree(ts): return T.Mut if ts == T.Tree else ts
    defmethod('treeState', lambda p: mutTree(treeState(p.e)), [Many, Many1, Option, And])
    defmethod('treeState', lambda p: treeState(p.e), [Action])

    # def treeRef(pe):
    #     ts = pe.get('ts', None)
    #     if ts is None:
    #         pe.ts = T.Unit
    #         pe.ts = pe.deref().treeState()
    #         return pe.ts
    #     return ts
    Ref.treeState = lambda p : nameTreeState(p.name)

    def treeSeq(pe):
        ts = T.Unit
        for se in pe:
            ts = se.treeState()
            if ts != T.Unit: return ts
        return ts
    Seq.treeState = treeSeq

    def treeAlt(pe):
        ts = list(map(treeState, pe))
        if T.Tree in ts:
            return T.Tree if ts.count(T.Tree) == len(ts) else T.Mut
        if T.Fold in ts:
            return T.Fold
        return T.Mut if T.Mut in ts else T.Unit
    Alt.treeState = treeAlt
    Ore2.treeState = treeAlt

    def formTree(e, state):
        e, _ = e.formTree(state)
        return e

    def formTree2(e, state):
        return e.formTree(state)
    
    def formNode(pe: Node, state):
        if state == T.Unit:  # {e #T} => e
            return formTree(pe.e, state), T.Unit
        if state == T.Fold:  # {e #T} => ^{e #T}
            return Fold2(formTree(pe.e, T.Mut), '', pe.tag), T.Fold
        pe = Node(formTree(pe.e, T.Mut), pe.tag)
        if state == T.Mut:  # {e #T} => : {e #T}
            return Edge2(pe, ''), state
        return pe, T.Fold   # state == T.Tree
    Node.formTree = formNode

    def formEdge(pe: Edge2, state):
        if state == T.Unit:  # L: e  => e
            return formTree(pe.e, state), T.Unit
        if state == T.Fold: # L: e => L:^ {e}
            return Fold2(formTree(pe.e, T.Mut), pe.edge, ''), T.Fold
        sub, ts2 = formTree2(pe.e, T.Tree)
        if ts2 != T.Fold:  
            sub = Node(sub, '')  # L:e => L: {e}
        pe = Edge2(sub, pe.edge)
        return (Node(pe, ''), T.Fold)  if state == T.Tree else (pe, T.Mut)
    Edge2.formTree = formEdge

    def formFold(pe: Fold2, state):
        if state == T.Unit:  # ^{e #T} => e
            return formTree(pe.e, state), T.Unit
        if state == T.Mut: # L:^ {e #T} => L:{ e #T}
            return Edge2(Node(formTree(pe.e, T.Mut), pe.tag), pe.edge), T.Mut
        if state == T.Tree: # L:^ {e #T} => {e #T}
            return Node(formTree(pe.e, T.Mut), pe.tag), T.Fold
        return Fold2(formTree(pe.e, T.Mut), pe.edge, pe.tag), T.Fold
    Fold2.formTree = formFold

    def formRef(pe, state):
        refstate = pe.treeState()
        if state == T.Unit:
            if refstate == T.Unit: # original
                return pe, T.Unit
            else:
                return Abs(pe), T.Unit
        if state == T.Tree:
            if refstate == T.Tree: # original
                return pe, T.Fold
            if refstate == T.Mut:  # mut => { mut }
                return Node(pe, ''), T.Fold
            return pe, state  # no change
        if state == T.Mut:
            if refstate == T.Unit or refstate == T.Mut:
                return pe, T.Mut
            assert refstate == T.Tree  # Expr => L: Expr
            return Edge2(pe, ''), T.Mut
        if state == T.Fold:
            if refstate == T.Unit:
                return pe, T.Fold
            if refstate == T.Tree:  # Expr => ^{ Expr }
                return Fold2(Edge2(pe, ''), '', ''), T.Fold
            if refstate == T.Mut:  # expr => ^{ expr }
                return Fold2(pe, '', ''), T.Fold
        assert(pe == None)  # Never happen
    Ref.formTree = formRef

    def formSeq(pe, state):
        for i, e in enumerate(pe):
            pe.es[i], state = formTree2(e, state)
        return pe, state
    Seq.formTree = formSeq

    def formAlt(pe, state):
        for i, e in enumerate(pe):
            pe.es[i],nextstate = formTree2(e, state)
        return pe, nextstate
    Alt.formTree = formAlt
    Ore2.formTree = formAlt

    def formUnary(pe, state):
        pe.e, state = formTree2(pe.e, state)
        return pe, state
    Unary.formTree = formUnary

    def formAction(pe: Action, state):
        if pe.func == 'cat':
            e = Ore2.expand(pe.e)
            if isinstance(e, Ore2):
                y = pe.params[1:]
                e.es = [Seq.new(*((x,) + y)) for x in e.es]
                DEBUG(e)
                return formAlt(e, state)
            return formSeq(Seq(*pe.params), state)
        else:
            pe.e, state = formTree2(pe.e, state)
            return pe, state
    Action.formTree = formAction

    def formTerm(pe, state):
        return pe, state
    ParsingExpression.formTree = formTerm

setup2()

def grammar_factory():
    def char1(x):
        return Char(x) if x != '' else EMPTY

    def unquote(s):
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
            if (s.startswith('\\x') or s.startswith('\\X')) and len(s) > 4:
                c = int(s[2:4], 16)
                return chr(c), s[4:]
            if (s.startswith('\\u') or s.startswith('\\U')) and len(s) > 6:
                c = int(s[2:6], 16)
                return chr(c), s[6:]
            else:
                return s[1], s[2:]
        else:
            return s[0], s[1:]
    
    def choice(t: ParseTree, file):
        urn, _, _, _ = t.pos()
        file = str(file)[1:-1]
        file = Path(urn).parent / file
        with file.open(encoding='utf-8_sig') as f:
            ss = [x.strip('\r\n') for x in f.readlines()]
            ss = [x for x in ss if len(x) > 0 and not x.startswith('#')]
            ss = sorted(ss, key= lambda x: len(x))[::-1]
            choice = [Char(x) for x in ss]
            e = Ore2(*choice)
            DEBUG(file, e)
            return e
        return EMPTY

    def log(type, pos, msg):
        print(pos.showing(msg))

    class PEGConv(ParseTreeConv):
        def __init__(self, peg):
            self.peg = peg

        def Empty(self, t, logger):
            return EMPTY

        def Any(self, t, logger):
            return ANY

        def Char(self, t, logger):
            s = str(t)
            sb = []
            while len(s) > 0:
                c, s = unquote(s)
                sb.append(c)
            return char1(''.join(sb))

        def Class(self, t, logger):
            s = str(t)
            chars = []
            ranges = []
            while len(s) > 0:
                c, s = unquote(s)
                if s.startswith('-') and len(s) > 1:
                    c2, s = unquote(s[1:])
                    ranges.append((c, c2))
                else:
                    chars.append(c)
            if len(chars) == 1 and len(ranges) == 0:
                return char1(chars[0])
            return Range(''.join(chars), ranges)

        def Ref(self, t, logger):
            name = str(t)
            if name in self.peg:
                return Action(self.peg.newRef(name), 'NT', (name,), t.getpos4())
            if name[0].isupper() or name[0].islower() or name.startswith('_'):
                logger('warning', t, f'undefined nonterminal {name}')
                self.peg.add(name, EMPTY)
                return self.peg.newRef(name)
            return char1(name[1:-1]) if name.startswith('"') else char1(name)

        def Many(self, t, logger):
            return Many(self.conv(t['inner'], logger))

        def Many1(self, t, logger):
            return Many1(self.conv(t['inner'], logger))

        def Option(self, t, logger):
            return Option(self.conv(t['inner'], logger))

        def And(self, t, logger):
            return And(self.conv(t['inner'], logger))

        def Not(self, t, logger):
            return Not(self.conv(t['inner'], logger))

        def Seq(self, t, logger):
            return Seq(*tuple(map(lambda p: self.conv(p, logger), t)))
            # return self.conv(t['left'], logger) & self.conv(t['right'], logger)

        def Ore(self, t, logger):
            return Ore2(*tuple(map(lambda p: self.conv(p, logger), t)))
            # return self.conv(t['left'], logger) / self.conv(t['right'], logger)

        def Alt(self, t, logger):
            return Alt(*tuple(map(lambda p: self.conv(p, logger), t)))
            # return self.conv(t['left'], logger) // self.conv(t['right'], logger)

        def Node(self, t, logger):
            node = t.getString('node', '')
            inner = self.conv(t['inner'], logger)
            return Node(inner, node)

        def Edge(self, t, logger):
            edge = t.getString('edge', '')
            inner = self.conv(t['inner'], logger)
            return Edge2(inner, edge)

        def Fold(self, t, logger):
            edge = t.getString('edge', '')
            node = t.getString('node', '')
            inner = self.conv(t['inner'], logger)
            return Fold2(inner, edge, node)

        def Append(self, t, logger):
            name = ''
            tsub = t['inner']
            if tsub == 'Func':
                a = tsub.asArray()
                name = str(a[0])
                inner = self.conv(a[1], logger)
            else:
                inner = self.conv(tsub, logger)
            return Edge2(inner, name)

        FIRST = {'lazy', 'scope', 'symbol', 'match', 'equals', 'contains', 'cat'}

        def Func(self, t, logger):
            funcname = t.getString('name', '')
            ps = []
            for p in t['params']:
                ps.append(self.conv(p, logger))
            if funcname == 'choice' and len(ps)>0:
                return choice(t, ps[0])
            if funcname in PEGConv.FIRST:
                return Action(ps[0], funcname, tuple(ps), t['name'].getpos4())
            return Action(EMPTY, funcname, tuple(ps), t['name'].getpos4())

    def example(peg, name, doc):
        peg['@@example'].append((name, doc))

    def checkRec(pe, consumed, peg, name, visited, logger):
        if isinstance(pe, ParseTree):
            nt = str(pe)
            if nt == name and not consumed:
                logger('warning', pe, f'left recursion {nt}')
                return FAIL
            if nt not in peg:
                logger('warning', pe, f'undefined nonterminal {nt}')
                return char1(nt[1:-1]) if nt.startswith('"') else char1(nt)
            pe = peg.newRef(nt)
        if isinstance(pe, Ref):
            if peg == pe.peg and pe.name not in visited:
                visited[pe.name] = True
                checkRec(peg[pe.name], consumed, peg, name, visited, logger)
            return pe
        if isinstance(pe, Action):
            pe.e = checkRec(pe.e, consumed, peg, name, visited, logger)
            pe.params = tuple([checkRec(x, consumed, peg, name,
                                  visited, logger) for x in pe.params])
            return pe
        if isinstance(pe, Unary):
            pe.e = checkRec(pe.e, consumed, peg, name, visited, logger)
            return pe
        if isinstance(pe, Seq):
            for i, e in enumerate(pe):
                pe.es[i] = checkRec(e, consumed, peg, name, visited, logger)
                consumed = (pe.es[i]).isAlwaysConsumed()
            return pe
        if isinstance(pe, Tuple):
            for i, e in enumerate(pe):
                pe.es[i] = checkRec(e, consumed, peg, name, visited, logger)
            return pe
        return pe
    
    #pegparser = generate(TPEGGrammar)

    def load_grammar(g, file, **options):
        g['@@example'] = []
        logger = options.get('logger', log)
        pegparser = generate(options.get('peg', TPEGGrammar))
        if isinstance(file, Path):
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
        # load
        for stmt in t:
            if stmt == 'Rule':
                name = str(stmt['name'])
                pos4 = stmt['name'].getpos4()
                if name in g:
                    logger('error', stmt['name'], f'redefined name {name}')
                    continue
                g.add(name, stmt['inner'])
                g.newRef(name).pos = pos4
            elif stmt == 'Example':
                doc = stmt['doc']
                for n in stmt['names']:
                    example(g, str(n), doc.getpos4())
            elif stmt == 'Import':
                urn = str(stmt['name'])
                lg = grammar(urn, **options)
                for n in stmt['names']:
                    lname = str(n)  # ns.Expression
                    name = lname
                    if lname.find('.') != -1:
                        name = lname.split('.')[-1]
                    pos4 = n.getpos4()
                    if not name in lg:
                        logger('perror', pos4, f'undefined name {name}')
                        continue
                    g.add(lname, Action(lg.newRef(name),
                                        'import', (name, urn), pos4))
        pconv = PEGConv(g)
        for name in g.N[:]:
            t = g[name]
            if isinstance(t, ParseTree):
                g[name] = pconv.conv(t, logger)
        for name in g.N: # FIXME
            g[name] = checkRec(g[name], False, g, name, {}, logger)
        for name in g.N: 
            pe = g[name]
            ts = pe.treeState()
            ts2 = nameTreeState(name)
            if ts != ts2:
                DEBUG('(@NAME)', name, ts, ts2)
            pe2,_ = pe.formTree(ts)
            if str(pe) != str(pe2):
                DEBUG('(@OLD)', ts, name, '=', pe)
                DEBUG('(@NEW)', ts, name, '=', pe2)
            g[name] = pe2
        #end of load_grammar()

    def findpath(paths, file):
        if file.find('=') > 0:
            return file
        for p in paths:
            path = Path(p) / file
            #print('@', path)
            if path.exists():
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
    peg = grammar('math.tpeg')
    print(peg)
