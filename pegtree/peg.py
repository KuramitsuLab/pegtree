import os
from .tree import ParseTree  # logging for PRef

##
from logging import getLogger
logger = getLogger(__name__)


def perror(sp: ParseTree, msg: str):
    if sp is not None:
        logger.error(sp.message('(error) ' + msg))


def pwarning(sp: ParseTree, msg: str):
    if sp is not None:
        logger.warning(sp.message('(warning) ' + msg))


# ParsingExpressionGrammar

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


# Parsing Expression

class PExpr(object):

    def __iter__(self):
        pass

    def __len__(self):
        return 0

    def isNullable(self):
        return True

    def hasTreeAnno(self):
        return False

    def match(self, x):
        return None

    def cname(self):  # old interface
        return self.__class__.__name__

    def minLen(self):  # old interface
        return 0 if self.isNullable() else 1


# '.' PAny

class PAny(PExpr):

    def __repr__(self):
        return '.'

    def isNullable(self):
        return False

    def match(self, x):
        return x[1:] if len(x) > 0 else None

# a PChar('a')


class PChar(PExpr):
    text: str
    ESCTBL = str.maketrans(
        {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\v': '\\v', '\f': '\\f',
         '\\': '\\\\', "'": "\\'"})

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "'" + self.text.translate(PChar.ESCTBL) + "'"

    def isNullable(self):
        return len(self.text) == 0

    def match(self, x):
        return x[len(self.text):] if x.startswith(self.text) else None

    @classmethod
    def new(cls, text):
        if len(text) == 0:
            return EMPTY
        return PChar(text)


class PRange(PExpr):
    chars: str
    ranges: str
    neg: bool

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

    def isNullable(self):
        return False

    def match(self, x):
        if len(x) > 0:
            c = x[0]
            if c in self.chars:
                return True
            for i in range(0, len(self.ranges), 2):
                if self.ranges[i] <= c <= self.ranges[i+1]:
                    return True
        return False

    @classmethod
    def new(cls, chars, ranges, neg=False):
        if len(chars) == 0 and len(ranges) == 0:
            return ANY if neg else FAIL
        if len(chars) == 1 and len(ranges) == 0 and neg == False:
            return PChar(chars)
        return PRange(chars, ranges, neg)


# Unary

def repr_unary(e):
    if isinstance(e, POre) or isinstance(e, PSeq) or isinstance(e, PEdge) or isinstance(e, PAlt):
        return '(' + repr(e) + ')'
    return repr(e)


class PUnary(PExpr):
    e: PExpr

    def __init__(self, e):
        self.e = e

    def __iter__(self):
        yield self.e

    def __len__(self):
        return 1

    def isNullable(self):
        return self.e.isNullable()

    def hasTreeAnno(self):
        return self.e.hasTreeAnno()

    def match(self, x):
        return self.e.match(x)


# Parsing Expression

class PNot(PUnary):
    e: PExpr

    def __repr__(self):
        return '!'+repr_unary(self.e)

    def isNullable(self):
        return True

    def isParseTree(self):
        return False

    def match(self, x):
        return x if self.e.match(x) is None else None


class PAnd(PUnary):
    e: PExpr

    def __repr__(self):
        return '&'+repr_unary(self.e)

    def isNullable(self):
        return True

    def match(self, x):
        return None if self.e.match(x) is None else x


class PMany(PUnary):
    e: PExpr

    def __repr__(self):
        return repr_unary(self.e)+'*'

    def isNullable(self):
        return True

    def match(self, x):
        y = self.e.match(x)
        while y is not None and len(y) < len(x):
            x = y
            y = self.e.match(x)
        return x


class POneMany(PUnary):
    e: PExpr

    def __repr__(self):
        return repr_unary(self.e)+'+'

    def isNullable(self):
        return self.e.isNullable()

    def match(self, x):
        y = self.e.match(x)
        if y is not None:
            return PMany.match(self, y)
        return None


class POption(PUnary):
    e: PExpr

    def __repr__(self):
        return repr_unary(self.e)+'?'

    def match(self, x):
        y = self.e.match(x)
        return x if y is None else y


# Binary


def repr_seq(e):
    if isinstance(e, POre) or isinstance(e, PAlt):
        return '(' + repr(e) + ')'
    return repr(e)


class PTuple(PExpr):
    es: tuple

    def __init__(self, *es):
        self.es = tuple(es)

    def __iter__(self):
        return iter(self.es)

    def __len__(self):
        return len(self.es)


class PSeq(PTuple):
    def __repr__(self):
        return ' '.join(map(lambda e: repr_seq(e), self.es))

    def isNullable(self):
        for e in self.es:
            if not e.isNullable():
                return False
        return True

    def hasTreeAnno(self):
        for e in self.es:
            if e.hasTreeAnno:
                return True
        return False

    def match(self, x):
        for e in self.es:
            x = e.match(x)
            if x is None:
                return None
        return x

    @classmethod
    def new(cls, *es):
        if len(es) == 0:
            return EMPTY
        return es[0] if len(es) == 1 else PSeq(*es)


class POre(PTuple):
    def __repr__(self):
        return ' / '.join(map(repr, self))

    def isNullable(self):
        for e in self.es:
            if e.isNullable():
                return True
        return False

    def hasTreeAnno(self):
        for e in self.es:
            if e.hasTreeAnno():
                return True
        return False

    def match(self, x):
        for e in self.es:
            y = e.match(x)
            if x is not None:
                return y
        return None

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
        return es[0] if len(es) == 1 else POre(*es)


class PAlt(POre):
    def __repr__(self):
        return ' | '.join(map(repr, self))


# NonTerminal


def isNullableName(name):
    return name[-1] == '_'


def isCamelStyleName(name):
    upper = 0
    lower = 0
    for c in list(name):
        if c.isupper():
            upper += 1
        elif c.islower():
            lower += 1
    return upper > 0 and lower > 0


# A PRef(A)

class PRef(PExpr):
    peg: Grammar
    name: str

    def __init__(self, peg, name):
        self.peg = peg
        self.name = name

    def __repr__(self):
        return self.name

    def uname(self, peg=None):
        if self.peg == peg:
            return self.name
        return f'{self.peg.ns}{self.name}'

    def deref0(self):
        return self.peg[self.name]

    def deref(self):
        # if self.name not in self.peg:
        #     store_default_parsing_expression(self.peg, self.name, self.tree)
        return self.peg[self.name]

    def isNullable(self):
        return isNullableName(self.name)

    def hasTreeAnno(self):
        return not isCamelStyleName(self.name)

    def match(self, x):
        return self.deref().match(x)


class PName(PUnary):
    e: PRef
    name: str
    tree: ParseTree
    isLeftRec: bool

    def __init__(self, peg: Grammar, name: str, tree: ParseTree = None, isLeftRec=False):
        super().__init__(peg if isinstance(peg, PRef) else peg.newRef(name))
        self.name = name
        self.tree = tree
        self.isLeftRec = isLeftRec

    def __repr__(self):
        return repr(self.e)

    def deref(self):
        if self.name not in self.e.peg:
            store_default_parsing_expression(self.e.peg, self.name, self.tree)
        return self.e.deref()

    def isNullable(self):
        return self.e.isNullable()

    def hasTreeAnno(self):
        return self.e.hasTreeAnno()

    def match(self, x):
        return self.e.match(x)

    def minLen(self):
        return self.e.minLen()


DefaultNonTerminals = {

}


def store_default_parsing_expression(peg, name, sp: ParseTree):
    global DefaultNonTerminals
    if len(DefaultNonTerminals) == 0:
        DefaultNonTerminals = {
            '_': PMany(PRange(' \t\u3000', '')),
            '__': PMany(PRange(' \t\r\n\u3000', '')),
            'EOF': PNot(ANY),
            'DIGIT': PRange('', '09'),
            'ALPHA': PRange('', 'AZaz'),
            'W': PRange('_', 'AZaz09'),
        }
    if name.startswith('"') and name.startswith('"'):
        string_literal = PSeq.new(PChar.new(name[1:-1]), PName(peg, '_', sp))
        peg[name] = string_literal
    elif ord(name[0]) > 127:  # utf文字
        peg[name] = PChar.new(name)
    elif name in DefaultNonTerminals:
        peg[name] = DefaultNonTerminals[name]
    else:
        if sp is not None:
            perror(sp, f'undefined name: {name}')
        peg[name] = EMPTY if isNullableName(name) else FAIL

# Tree Construction


def repr_tree_tag(tag):
    return ' ' if tag == '' else f' #{tag} '


def repr_tree_edge(edge, suffix=''):
    return suffix if edge == '' else f'{edge}:{suffix}'


def repr_tree_shift(shift):
    return '' if shift == 0 else f'/*{shift}*/'


class PNode(PUnary):
    e: PExpr
    tag: str
    shift: int

    def __init__(self, e, tag='', shift=0):
        self.e = e
        self.tag = tag
        self.shift = shift

    def __repr__(self):
        shift = '' if self.shift == 0 else f'/*{self.shift}*/'
        tag = '' if self.tag == '' else f' #{self.tag} '
        return '{' + shift + ' ' + repr(self.e) + tag + '}'

    def __repr__2(self):
        shift = repr_tree_shift(self.shift)
        tag = repr_tree_tag(self.tag)
        return '{' + shift + ' ' + repr(self.e) + tag + '}'

    def hasTreeAnno(self):
        return True


class PEdge(PUnary):
    edge: str
    e: PExpr
    shift: int

    def __init__(self, edge, e, shift=0):
        self.e = e
        self.edge = edge
        self.shift = shift

    def __repr__(self):
        shift = '' if self.shift == 0 else f'/*{self.shift}*/'
        return self.edge + shift + ': ' + repr_seq(self.e)

    def __repr__2(self):
        shift = repr_tree_shift(self.shift)
        edge = repr_tree_edge(self.edge)
        return shift + edge + repr_unary(self.e)

    def hasTreeAnno(self):
        return True


class PFold(PUnary):
    edge: str
    e: PExpr
    tag: str
    shift: int

    def __init__(self, edge, e, tag='', shift=0):
        self.e = e
        self.edge = edge
        self.tag = tag
        self.shift = shift

    def __repr__(self):
        shift = '' if self.shift == 0 else f'/*{self.shift}*/'
        edge = '^' if self.edge == '' else f'{self.edge}:^'
        tag = '' if self.tag == '' else f' #{self.tag} '
        return '{ ' + edge + shift + ' ' + repr(self.e) + tag + '}'

    def __repr__2(self):
        shift = repr_tree_shift(self.shift)
        edge = repr_tree_edge(self.edge, suffix='^ ')
        tag = repr_tree_tag(self.tag)
        return '{' + shift + edge + repr(self.e) + tag + '}'

    def hasTreeAnno(self):
        return True


class PAbs(PUnary):
    e: PExpr

    def __init__(self, e):
        self.e = e

    def __repr__(self):
        return f'@abs({self.e})'

    def hasTreeAnno(self):
        return False


# Symbol


class PSymbol(PUnary):
    e: PExpr

    def __init__(self, e):
        self.e = e

    def __repr__(self):
        return f'@symbol({self.e})'


class PMatch(PUnary):
    e: PExpr

    def __init__(self, e):
        self.e = e

    def __repr__(self):
        return f'@match({self.e})'


# class PAny(PUnary):
#     e: PExpr
#     def __init__(self, e):
#         self.e = e
#     def __repr__(self):
#         return f'@any({self.e})'


class PRepeat(PUnary):
    e: PExpr
    name: str

    def __init__(self, e):
        self.e = e

    def __repr__(self):
        return f'@repeat({self.e}, {self.name})'


class PScope(PUnary):
    e: PExpr

    def __init__(self, e):
        self.e = e

    def __repr__(self):
        return f'@scope({self.e})'


# Action


class PAction(PUnary):
    __slots__ = ['e', 'func', 'params', 'ptree']

    def __init__(self, e, func, params, ptree=None):
        self.e = e
        self.func = func
        self.params = params
        self.ptree = ptree

    def __repr__(self):
        return f'@{self.func}{self.params}'

    def cname(self):
        return self.func.capitalize()

# Visitor


class PExprVisitor(object):

    def visit(self, pe: PExpr):
        key = f'accept{pe.__class__.__name__}'
        if hasattr(self, key):
            acceptMethod = getattr(self, key)
            return acceptMethod(pe)
        return self.visitUndefined(pe)

    def visitUndefined(self, pe):
        logger.warning(
            f'(TODO) define accept{pe.__class__.__name__} in {self.__class__.__name__}')
        return None


# CONSTANT
EMPTY = PChar('')
ANY = PAny()
FAIL = PNot(EMPTY)


def isEmpty(pe):
    return pe == EMPTY or isinstance(pe, PChar) and len(pe.text) == 0


def isAny(pe):
    return pe == ANY or isinstance(pe, PAny)


def isSingleCharacter(pe):
    return (isinstance(pe, PChar) and len(pe.text) == 1) or isinstance(pe, PRange) or isinstance(pe, PAny)


def checkLeftRec(peg, name, e=None, visited=None):
    if e == None:
        visited = set()
        e = peg[name]
    if isinstance(e, PName):
        if name == e.name:
            e.isLeftRec = True
            return
        if e.name not in visited:
            visited.add(e.name)
            checkLeftRec(peg, name, e.deref(), visited)
    elif isinstance(e, PSeq):
        for ei in e.es:
            checkLeftRec(peg, name, ei, visited)
            if not ei.isNullable():
                return
    elif len(e) != 0:
        for ei in e:
            checkLeftRec(peg, name, ei, visited)


#
# PExprVisitor
#

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


defaultNullableChecker = Nullable()


def isAlwaysConsumed(pe):
    return defaultNullableChecker.visit(pe)


# class First(PVisitor):

#     def __init__(self):
#         self.memos = {}

#     def PChar(self, pe):
#         if len(pe.text) == 0:
#             return (0, 0)
#         return (1 << ord(pe.text[0]), 0)

#     def PAny(self, pe):
#         return (-1, 0)

#     def PRange(self, pe):
#         if(pe.neg):
#             return (-1, unique_range(pe.chars, pe.ranges))
#         return (unique_range(pe.chars, pe.ranges), 0)

#     def PRef(self, pe):
#         uname = pe.uname()
#         if(uname not in self.memos):
#             self.memos[uname] = (-1, 0)
#             self.memos[uname] = self.visit(pe.deref())
#         return self.memos[uname]

#     def PNot(self, pe):
#         if isSingleCharacter(pe.e):
#             pos, neg = self.visit(pe.e)
#             return (neg, pos)
#         return LeftRef.EMPTYSET

#     def PAnd(self, pe): return self.visit(pe.e)
#     def PMany(self, pe): return self.visit(pe.e)
#     def POneMany(self, pe): return self.visit(pe.e)
#     def POption(self, pe): return self.visit(pe.e)

#     def PSeq(self, pe):
#         pos, neg = 0, 0
#         for e in pe:
#             pos1, neg1 = self.visit(e)
#             pos |= pos1
#             neg |= neg1
#             if isAlwaysConsumed(e):
#                 break
#         return (pos, neg)

#     def POre(self, pe):
#         pos, neg = 0, 0
#         for e in pe:
#             pos1, neg1 = self.visit(e)
#             pos |= pos1
#             neg |= neg1
#         return (pos, neg)

#     def PNode(self, pe): return self.visit(pe.e)
#     def PFold(self, pe): return self.visit(pe.e)
#     def PEdge(self, pe): return self.visit(pe.e)
#     def PAbs(self, pe): return self.visit(pe.e)

#     def PAction(self, pe): return self.visit(pe.e)
