import sys, os, errno, inspect
from collections import namedtuple
from enum import Enum
from pathlib import Path

# Parsing Expression
Empty = namedtuple('Empty', '')
Char = namedtuple('Char', 'text')
Range = namedtuple('Range', 'chars ranges')
Any = namedtuple('Any', '')
Seq = namedtuple('Seq', 'left right')
Ore = namedtuple('Ore', 'left right')
Alt = namedtuple('Alt', 'left right')
And = namedtuple('And', 'inner')
Not = namedtuple('Not', 'inner')
Many = namedtuple('Many', 'inner')
Many1 = namedtuple('Many1', 'inner')
Ref = namedtuple('Ref', 'name peg prop')
# Tree
Node = namedtuple('Node', 'inner node')
Edge = namedtuple('Edge', 'edge inner')
Fold = namedtuple('Fold', 'edge inner node')
Abs = namedtuple('Abs', 'inner')
# Action
Action = namedtuple('Action', 'inner func params')

# CONSTANT
EMPTY = Empty()
ANY = Any()
FAIL = Not(EMPTY)

def char1(x):
    return Char(x) if x != '' else EMPTY

def seq2(x, y):
    if x is None or y is None:
        return None
    if isinstance(y, Empty):
        return x
    if isinstance(x, Empty):
        return y
    if isinstance(x, Char) and isinstance(y, Char):
        return Char(x.a + y.a)
    return Seq(x, y)

def alt2(x, y, c=Alt):
    if isinstance(x, Char) and len(x.text) == 1:
        if isinstance(y, Char) and len(y.text) == 1:
            return Range(x.text + y.text, ())
        if isinstance(y, Range):
            return Range(x.text + y.chars, y.ranges)
    if isinstance(x, Range):
        if isinstance(y, Char) and len(y.text) == 1:
            return Range(x.chars + y.text, y.ranges)
        if isinstance(y, Range):
            return Range(x.chars + y.chars, x.ranges, y.ranges)
    return c(x, y)

def ore2(x, y):
    if x is None or y is None:
        return None
    if x == EMPTY:
        return EMPTY
    return alt2(x, y, Ore)


PEs = [
    Empty, Char, Range, Any, Seq, Ore, Alt, And, Not, Many, Many1, Ref,
    Node, Edge, Fold, Abs, Action,
]

def defmethod(name, f, cs=PEs):
    for c in cs:
        setattr(c, name, f)

defmethod('__and__', lambda x, y: seq2(x, Xe(y)))  # x & y
defmethod('__rand__', lambda x, y: seq2(Xe(x), Xe(y)))  # x & y
defmethod('__or__', lambda x, y: ore2(x, Xe(y)))  # x | y
defmethod('__truediv__', lambda x, y: ore2(x, Xe(y)))  # x / y
defmethod('__invert__', lambda x: Not(x))  # ~x

def piter(p):
    if hasattr(p, 'inner'):
        yield p.inner
    if hasattr(p, 'right'):
        yield p.left
        yield p.right

defmethod('__iter__', lambda p: piter(p))  #

def flaten(p, ps, c=Seq):
    if isinstance(p, c):
        flaten(p.left, ps, c)
        flaten(p.right, ps, c)
    else:
        ps.append(p)

def setmethod(*ctags):
    def _match(func):
        methodname = ctags[0]
        cs = ctags[1:] if len(ctags) > 1 else PEs
        for c in cs:
            setattr(c, methodname, func)
        return func
    return _match


def addmethod(*ctags):
    def _match(func):
        methodname = ctags[0]
        cs = ctags[1:] if len(ctags) > 1 else PEs
        for c in cs:
            if not hasattr(c, methodname):
                setattr(c, methodname, func)
        return func
    return _match

def setdup(method):
    f = lambda p, **kw: getattr(p, method)(p, **kw)
    setattr(Empty, method, lambda p, **kw : p)
    setattr(Char, method, lambda p, **kw : p)
    setattr(Range, method, lambda p, **kw : p)
    setattr(Any, method, lambda p, **kw: p)
    setattr(Ref, method, lambda p, **kw: p)
    setattr(And, method, lambda p, **kw: And(f(p[0], **kw)))
    setattr(Not, method, lambda p, **kw: Not(f(p[0], **kw)))
    setattr(Many, method, lambda p, **kw: Many(f(p[0], **kw)))
    setattr(Many1, method, lambda p, **kw: Many1(f(p[0], **kw)))
    setattr(Seq, method, lambda p, **kw: Seq(f(p[0], **kw), f(p[1], **kw)))
    setattr(Ore, method, lambda p, **kw: Ore(f(p[0], **kw), f(p[1], **kw)))
    setattr(Alt, method, lambda p, **kw: Alt(f(p[0], **kw), f(p[1], **kw)))
    setattr(Node, method, lambda p, **kw: Node(f(p[0], **kw), p[1]))
    setattr(Edge, method, lambda p, **kw: Edge(p[0], f(p[1], **kw)))
    setattr(Fold, method, lambda p, **kw: Fold(p[0], f(p[1], **kw), p[2]))
    setattr(Abs, method, lambda p, **kw:  Abs(f(p[0], **kw) ))
    setattr(Action, method, lambda p, **kw: Action(f(p[0], **kw), p[1], p[2]))

# String

def setup_repr():
    def grouping(e, f):
        return '(' + repr(e) + ')' if f(e) else repr(e)

    def inSeq(e):
        return (isinstance(e, Ore) and e.right != EMPTY) or isinstance(e, Alt)

    def inUnary(e):
        return (isinstance(e, Ore) and e.right != EMPTY) \
            or isinstance(e, Seq) or isinstance(e, Alt) \
            or (isinstance(e, Edge))or isinstance(e, Fold)
    CharTBL = str.maketrans(
        {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\\': '\\\\', "'": "\\'"})
    RangeTBL = str.maketrans(
        {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\\': '\\\\', ']': '\\]', '-': '\\-'})

    def rs(ranges):
        ss = tuple(map(lambda x: x[0].translate(
            RangeTBL) + '-' + x[1].translate(RangeTBL), ranges))
        return ''.join(ss)
    Empty.__repr__ = lambda p: "''"
    Char.__repr__ = lambda p: "'" + p.text.translate(CharTBL) + "'"
    Range.__repr__ = lambda p: "[" + \
        rs(p.ranges) + p.chars.translate(RangeTBL) + "]"
    Any.__repr__ = lambda p: '.'
    Seq.__repr__ = lambda p: grouping(
        p.left, inSeq) + ' ' + grouping(p.right, inSeq)
    Ore.__repr__ = lambda p: grouping(
        p.left, inUnary) + '?' if p.right == EMPTY else repr(p.left) + ' / ' + repr(p.right)
    Alt.__repr__ = lambda p: repr(p.left) + ' | ' + repr(p.right)
    And.__repr__ = lambda p: '&'+grouping(p.inner, inUnary)
    Not.__repr__ = lambda p: '!'+grouping(p.inner, inUnary)
    Many.__repr__ = lambda p: grouping(p.inner, inUnary)+'*'
    Many1.__repr__ = lambda p: grouping(p.inner, inUnary)+'+'
    Ref.__repr__ = lambda p: p.name
    Node.__repr__ = lambda p: '{' + str(p.inner) + ' #' + p.node + '}'
    Edge.__repr__ = lambda p: ('$' if p.edge == '' else p.edge + ': ') + grouping(p.inner, inUnary)
    Fold.__repr__ = lambda p: ('' if p.edge == '' else p.edge + ':') + '^ {' + str(p.inner) + ' #' + p.node + '}'
    Abs.__repr__ = lambda p: f'@abs({p.inner})'
    Action.__repr__ = lambda p: f'@{p.func}{p.params}'

setup_repr()

Ref.uname = lambda p : p.name[0] if p.name[0].isdigit() else (p.peg.gid + p.name)
Ref.deref = lambda p: p.peg[p.name]

GrammarId = 0

class Grammar(dict):
    def __init__(self):
        global GrammarId
        self.gid = str(GrammarId)
        GrammarId += 1
        self.N = []

    def __setitem__(self, key, item):
        super().__setitem__(key, item)
        self.N.append(key)

    def __repr__(self):
        ss = []
        for rule in self.N:
            ss.append(rule)
            ss.append('=')
            ss.append(repr(self[rule]))
            ss.append('\n')
        return ''.join(ss)
    
    def newRef(self, name):
        key = '@' + name
        if not key in self:
            super().__setitem__(key, Ref(name, self, {}))
        return self[key]

    def start(self):
        if len(self.N) == 0: 
            self['EMPTY'] = EMPTY
        return self.N[0]

# TPEG Setting

def Xe(p):
    if isinstance(p, str):
        return char1(p)
    if isinstance(p, dict):
        for key in p:
            return Edge(key, Xe(p[key]))
        return EMPTY
    return p


def crange(*ps):
    chars = []
    ranges = []
    for x in ps:
        if isinstance(x, str):
            chars.append(x)
        else:
            ranges.append(tuple(x))
    return Range(''.join(chars), ranges)


def seq(*ps):
    if len(ps) == 0:
        return EMPTY
    if len(ps) == 1:
        return Xe(ps[0])
    return Seq(Xe(ps[0]), seq(*ps[1:]))


def many(*ps): return Many(seq(*ps))
def many1(*ps): return Many1(seq(*ps))
def option(*ps): return Ore(seq(*ps), EMPTY)
def TreeAs(node, *ps): return Node(seq(*ps), node)
def ListAs(*ps): return Node(seq(*ps), '')
def FoldAs(edge, node, *ps): return Fold(edge, seq(*ps), node)

def TPEG(g):
    c = crange
    e = seq
    def ref(p): return g.newRef(p)

    __ = ref('__')
    _ = ref('__')
    EOS = ref('EOS')
    EOL = ref('EOL')
    S = ref('S')
    COMMENT = ref('COMMENT')
    Expression = ref('Expression')
    Identifier = ref('Identifier')
    Empty = ref('Empty')

    g['Start'] = e(__, ref('Source'), ref('EOF'))

    g['__'] = many(c(' \t\r\n') | COMMENT)
    g['_'] = many(c(' \t') | COMMENT)
    g['EOF'] = ~ANY
    g['COMMENT'] = e('/*', many(~e('*/'), ANY),
                     '*/') | e('//', many(~EOL, ANY))
    g['EOL'] = e('\n') | e('\r\n') | ref('EOF')
    g['S'] = c(' \t')

    g['Source'] = TreeAs('Source', many({'': ref('Statement')}))
    g['EOS'] = _ & many(e(';', _) | EOL & (S | COMMENT) & _ | EOL)

    g['Statement'] = ref('Import') | ref('Example') | ref('Rule')

    g['Rule'] = TreeAs('Rule', {'name': Identifier}, __, '=', __, option(
        c('/|'), __), {'inner': Expression}, EOS)

    NAME = c(('A', 'Z'), ('a', 'z'), '@_') & many(
        c(('A', 'Z'), ('a', 'z'), ('0', '9'), '_.'))
    g['Identifier'] = TreeAs('Name', NAME | e(
        '"', many(e(r'\"') | ~c('\\"\n') & ANY), '"'))

    # import
    FROM = option(_, 'import', S, _, {'names': ref('Names')})
    g['Import'] = TreeAs('Import', 'from', S, _, {'name': Identifier / ref('Char')}, FROM) & EOS

    g['Example'] = TreeAs('Example', 'example', S, _, {
                          'names': ref('Names')}, {'doc': ref('Doc')}) & EOS
    g['Names'] = ListAs({'': Identifier}, _, many(
        c(',&'), _, {'': Identifier}, _))
    DELIM = Xe("'''")
    DOC1 = TreeAs("Doc", many(~e(DELIM, EOL), ANY))
    DOC2 = TreeAs("Doc", many(~c('\r\n'), ANY))
    g['Doc'] = e(DELIM, many(S), EOL, DOC1, DELIM) | DOC2

    g['Expression'] = ref('Choice') & option(
        FoldAs('left', 'Alt', __, '|', _, {'right': Expression}))
    g['Choice'] = ref('Sequence') & option(
        FoldAs('left', 'Ore', __, '/', _, {'right': ref('Choice')}))
    SS = e(S, _, ~EOL) | many1(_, EOL) & S & _
    g['Sequence'] = ref('Predicate') & option(
        FoldAs('left', 'Seq', SS, {'right': ref('Sequence')}))

    g['Predicate'] = ref('Not') | ref('And') | ref('Append') | ref('Suffix')
    g['Not'] = TreeAs('Not', '!', {'inner': ref('Predicate')})
    g['And'] = TreeAs('And', '&', {'inner': ref('Predicate')})
    g['Append'] = TreeAs('Append', '$', {'inner': ref('Term')})

    g['Suffix'] = ref('Term') & option(FoldAs('inner', 'Many', '*') |
                                       FoldAs('inner', 'Many1', '+') | FoldAs('inner', 'Option', '?'))

    g['Term'] = ref('Group') / ref('Char') / ref('Class') / ref('Any') / ref('Node') / \
        ref('Fold') / ref('EdgeFold') / ref('Edge') / ref('Func') / ref('Ref')
    g['Group'] = e('(', __, (Expression/Empty), __, ')')

    g['Empty'] = TreeAs('Empty', EMPTY)
    g['Any'] = TreeAs('Any', '.')
    g['Char'] = e("'", TreeAs('Char', many(
        e('\\', ANY) | ~c("'\n") & ANY)), "'")
    g['Class'] = e(
        '[', TreeAs('Class', many(e('\\', ANY) | ~e("]") & ANY)), ']')

    Tag = e('{', __, option('#', {'node': ref('Identifier')}), __)
    ETag = e(option('#', {'node': ref('Identifier')}), __, '}')

    g['Node'] = TreeAs('Node', Tag, {'inner': Expression | Empty}, __, ETag)
    g['Fold'] = e('^', _, TreeAs('Fold', Tag, {'inner': Expression | Empty}, __, ETag))
    g['Edge'] = TreeAs('Edge', {'edge': ref('EdgeName')}, ':', _, {
                       'inner': ref('Term')})
    g['EdgeFold'] = TreeAs('Fold', {'edge': ref('EdgeName')}, ':^', _, Tag, {
                           'inner': Expression / Empty}, __, ETag)
    g['EdgeName'] = TreeAs('', c(('a', 'z'), '$'), many(c(('A', 'Z'), ('a', 'z'), ('0', '9'), '_')))
    g['Func'] = TreeAs('Func', '@', {'name': Identifier}, '(', __, {'params': ref('Params')}, ')')
    g['Params'] = ListAs({'': Expression}, many(_, ',', __, {'': Expression}), __)
    g['Ref'] = TreeAs('Ref', ref('REF'))
    g['REF'] = e('"', many(Xe('\\"') | e(~c('\\"\n'), ANY)), '"') | many1(~c(' \t\r\n(,){};<>[|/*+?=^\'`#') & ANY)
    return g

TPEGGrammar = TPEG(Grammar())
print(TPEGGrammar)


######################################################################
# ast.env

Pos4 = namedtuple('Pos4', 'urn inputs spos epos')

def bytestr(b):
    return b.decode('utf-8') if isinstance(b, bytes) else b

def decpos4(pos4):
    urn, inputs, spos, epos = pos4
    #urn, inputs, pos, length = decsrc(s)
    lines = inputs.split(b'\n' if isinstance(inputs, bytes) else '\n')
    linenum = 0
    cols = spos
    for line in lines:
        len0 = len(line) + 1
        linenum += 1
        if cols < len0:
            break
        cols -= len0
    epos = cols + (epos - spos)
    length = len(line) - cols if len(line) < epos else epos - cols
    if length <= 0:
        length = 1
    mark = (' ' * cols) + ('^' * length)
    return (urn, spos, linenum, cols, bytestr(line), mark)

def serror4(pos4, msg='SyntaxError'):
    if pos4 is not None:
        urn, pos, linenum, cols, line, mark = decpos4(pos4)
        return '{} ({}:{}:{}+{})\n{}\n{}'.format(msg, urn, linenum, cols, pos, line, mark)
    return '{} (unknown source)'.format(msg)


class Logger(object):
    __slots__ = ['file', 'istty', 'isVerbose']

    def __init__(self, file=None, isVerbose=True):
        if file is None:
            self.file = sys.stdout
            self.istty = True
        else:
            self.file = open(file, 'w+')
            self.istty = False
        self.isVerbose = isVerbose

    def print(self, *args):
        file = self.file
        if len(args) > 0:
            file.write(str(args[0]))
            for a in args[1:]:
                file.write(' ')
                file.write(str(a))

    def println(self, *args):
        self.print(*args)
        self.file.write(os.linesep)
        self.file.flush()

    def dump(self, o, indent=''):
        if hasattr(o, 'dump'):
            o.dump(self, indent)
        else:
            self.println(o)

    def verbose(self, *args):
        if self.isVerbose:
            ss = map(lambda s: self.c('Blue', s), args)
            self.println(*ss)

    def bold(self, s):
        return '\033[1m' + str(s) + '\033[0m' if self.istty else str(s)

    COLOR = {
        "Black": '0;30', "DarkGray": '1;30',
        "Red": '0;31', "LightRed": '1;31',
        "Green": '0;32', "LightGreen": '1;32',
        "Orange": '0;33', "Yellow": '1;33',
        "Blue": '0;34', "LightBlue": '1;34',
        "Purple": '0;35', "LightPurple": '1;35',
        "Cyan": '0;36', "LightCyan": '1;36',
        "LightGray": '0;37', "White": '1;37',
    }

    def c(self, color, s):
        return '\033[{}m{}\033[0m'.format(Logger.COLOR[color], str(s)) + '' if self.istty else str(s)

    def perror(self, pos4, msg='Syntax Error'):
        self.println(serror4(pos4, self.c('Red', '[error] ' + str(msg))))

    def warning(self, pos4, msg):
        self.println(serror4(pos4, self.c('Orange', '[warning] ' + str(msg))))

    def notice(self, pos4, msg):
        self.println(serror4(pos4, self.c('Cyan', '[notice] ' + str(msg))))

STDLOG = Logger()

#####################################

def Merge(prev, edge, child): 
  return (prev, edge, child)

class ParseTree(object):
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

    def __len__(self):
        c = 0
        cur = self.child
        while(cur is not None):
            c += 1
            cur = cur.prev
        return c

    def __contains__(self, label):
        cur = self.child
        while(cur is not None):
            cur, edge, child = cur
            if label == edge: return True
        return False

    def __getitem__(self, label):
        cur = self.child
        while(cur is not None):
            cur, edge, child = cur
            if label == edge: return child
        return None
    
    def get(self, label: str, default=None, conv=lambda x: x):
        cur = self.child
        while(cur is not None):
            cur, edge, child = cur
            if label == edge: return conv(child)
        return default

    def getString(self, label: str, default=None):
        return self.get(label, default, lambda t: t.asString())

    def __iter__(self):
        return TreeLinkIter(self.child)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        sb = []
        self.strOut(sb)
        return "".join(sb)

    def strOut(self, sb):
        sb.append("[#")
        sb.append(self.tag)
        c = len(sb)
        for tag, child in self:
            sb.append(' ' if tag is '' else ' ' + tag + '=')
            child.strOut(sb)
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

    def getpos4(self):
        return Pos4(self.urn, self.inputs, self.spos, self.epos)

    def asString(self):
        s = self.inputs[self.spos:self.epos]
        return s.decode('utf-8') if isinstance(s, bytes) else s

    '''
    def dump(self, w, indent=''):
        if self.child is None:
            s = self.inputs[self.spos:self.epos]
            w.println(w.bold("[#" + self.tag), repr(s) + w.bold("]"))
            return
        w.println(w.bold("[#" + self.tag))
        indent2 = '  ' + indent
        for tag, child in self:
            w.print(indent2 if tag is '' else indent2 + tag + '=')
            child.dump(w, indent2)
        w.println(indent + w.bold("]"))

    def isString(self):
        return self.child is None

    def isArray(self):
        cur = self.child
        while cur is not None:
            if cur.tag is not None and len(cur.tag) > 0:
                return False
            cur = cur.prev
        return True

    def asArray(self):
        a = []
        cur = self.child
        while cur is not None:
            if cur.child is not None:
                a.append(cur.child)
            cur = cur.prev
        a.reverse()
        return a

    def asJSON(self, tag='__class__', hook=None):
        listCount = 0
        cur = self.child
        while cur is not None:
            if cur.tag is not None and len(cur.tag) > 0:
                listCount = -1
                break
            listCount += 1
            cur = cur.prev
        if listCount == 0:
            return self.asString() if hook is None else hook(self)
        if listCount == -1:
            d = {}
            if self.tag is not None and len(self.tag) > 0:
                d[tag] = self.tag
            cur = self.child
            while cur is not None:
                if not cur.tag in d:
                    d[cur.tag] = cur.child.asJSON(tag, hook)
                cur = cur.prev
            return d
        else:
            return self.asArray()

    def pos3(self):
        return (self.inputs, self.spos, self.epos)
    '''

class TreeLinkIter(object):
    __slots__ = ['stack']

    def __init__(self, cur):
        self.stack = []
        while cur is not None:
            prev, edge, child = cur
            if child is not None:
                self.stack.append((edge, child))
            cur = prev

    def __next__(self):
        if len(self.stack) == 0:
            raise StopIteration()
        return self.stack.pop()


## TreeConv

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

######################################################################

class ParserContext:
    __slots__ = ['urn', 'inputs', 'pos', 'epos',
                 'headpos', 'ast', 'state', 'dict', 'memo']

    def __init__(self, urn, inputs, spos, epos):
        self.urn = urn
        self.inputs = inputs
        self.pos = spos
        self.epos = epos
        self.headpos = spos
        self.ast = None
        self.state = None
        self.dict = {}
        self.memo = {}

# setup parser

def gen_Pexp(pe, **option):
    try:
        return pe.gen(**option)
    except AttributeError:
        print('@@', pe)
        return pe.gen(**option)


def gen_Empty(pe, **option):
    def empty(px): return True
    return empty


def gen_Char(pe, **option):
    chars = pe.text
    clen = len(pe.text)

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

def gen_Range(pe, **option):
    #offset = pe.min()
    bitset = first_range(pe) ## >> offset

    def bitmatch(px):
        if px.pos < px.epos:
            shift = ord(px.inputs[px.pos]) ## - offset
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
    pf = gen_Pexp(pe.inner, **option)

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
    pf = gen_Pexp(pe.inner, **option)

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
    pf = gen_Pexp(pe.inner, **option)

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
    pf = gen_Pexp(pe.inner, **option)

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

# Seq


def gen_Seq(pe, **option):
    pf1 = gen_Pexp(pe.left, **option)
    pf2 = gen_Pexp(pe.right, **option)
    return lambda px: pf1(px) and pf2(px)

# Ore


def gen_Ore(pe, **option):
    pf1 = gen_Pexp(pe.left, **option)
    pf2 = gen_Pexp(pe.right, **option)

    def match_ore(px):
        pos = px.pos
        ast = px.ast
        if not pf1(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return pf2(px)
        return True

    return match_ore

# Ref

def gen_Ref(ref, **option):
    key = ref.uname()
    generated = option['generated']
    if not key in generated:
        generated[key] = lambda px: generated[key](px)
        generated[key] = gen_Pexp(ref.deref(), **option)
        #memo[key] = emit_trace(ref, emit(ref.deref()))
    return generated[key]

# Tree Construction


def gen_Node(pe, **option):
    node = pe.node
    pf = gen_Pexp(pe.inner, **option)
    mtree = option.get('tree', ParseTree)

    def tree(px):
        pos = px.pos
        px.ast = None
        if pf(px):
            px.ast = mtree(node, px.urn, px.inputs, pos, px.pos, px.ast)
            return True
        return False

    return tree


def gen_Edge(pe, **option):
    edge = pe.edge
    pf = gen_Pexp(pe.inner, **option)
    merge = option.get('merge', Merge)

    def link(px):
        prev = px.ast
        if pf(px):
            px.ast = merge(prev, edge, px.ast)
            return True
        return False

    return link


def gen_Fold(pe, **option):
    edge = pe.edge
    node = pe.node
    pf = gen_Pexp(pe.inner, **option)
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
    pf = gen_Pexp(pe.inner, **option)

    def unit(px):
        ast = px.ast
        if pf(px):
            px.ast = ast
            return True
        return False

    return unit

# SymbolTable

def gen_Action(pe, **option):
    return gen_Pexp(pe.inner, **option)

Empty.gen = gen_Empty
Char.gen = gen_Char
Range.gen = gen_Range
Any.gen = gen_Any

And.gen = gen_And
Not.gen = gen_Not
Many.gen = gen_Many
Many1.gen = gen_Many1

Seq.gen = gen_Seq
Ore.gen = gen_Ore
Alt.gen = gen_Ore
Ref.gen = gen_Ref

Node.gen = gen_Node
Edge.gen = gen_Edge
Fold.gen = gen_Fold
Abs.gen = gen_Abs

Action.gen = gen_Action

def generate(peg, **option):
    name = option.get('start', peg.start())
    p = peg.newRef(name)
    option['peg'] = peg
    option['generated'] = {}

    pf = gen_Pexp(p, **option)
    mtree = option.get('tree', ParseTree)
    conv = option.get('conv', lambda x: x)

    def parse(inputs, urn='(unknown)', pos=0, epos=None):
        if epos is None: epos = len(inputs)
        px = ParserContext(urn, inputs, pos, epos)
        pos = px.pos
        result = None
        if not pf(px):
            result = mtree("err", urn, inputs, px.headpos, epos, None)
        else:
            result = px.ast if px.ast is not None else mtree("", urn, inputs, pos, px.pos, None)
        return conv(result)
    
    return parse

######################################################################

# isAlwaysConsumed


defmethod('isAlwaysConsumed', lambda p: True, [Char, Any, Range])
defmethod('isAlwaysConsumed', lambda p: False, [Many, Not, And, Empty])
defmethod('isAlwaysConsumed',
          lambda p: p.inner.isAlwaysConsumed(),
          [Many1, Edge, Node, Fold, Abs, Action])
defmethod('isAlwaysConsumed',
          lambda p: p.left.isAlwaysConsumed() or p.right.isAlwaysConsumed(), [Seq])
defmethod('isAlwaysConsumed',
          lambda p: p.left.isAlwaysConsumed() and p.right.isAlwaysConsumed(), [Ore, Alt])


def isAlwaysConsumed(p):
    if isinstance(p, Ref):
        memoed = p.prop.get('isAlwaysConsumed', None)
        if memoed == None:
            p.prop['isAlwaysConsumed'] = True
            memoed = isAlwaysConsumed(p.deref())
            p.prop['isAlwaysConsumed'] = memoed
        return memoed
    else:
        return p.isAlwaysConsumed()

defmethod('isAlwaysConsumed', isAlwaysConsumed, [Ref])

'''
def checkRef(pe, consumed: bool, name: str, visited: dict, logger):
    if isinstance(pe, Seq):
        pe.left = checkRef(pe.left, consumed, name, visited, logger)
        if not consumed:
            consumed = isAlwaysConsumed(pe.left)
        pe.right = checkRef(pe.right, consumed, name, visited, logger)
        return pe
    if isinstance(pe, Ore) or isinstance(pe, Alt):
        pe.left = checkRef(pe.left, consumed, name, visited, logger)
        pe.right = checkRef(pe.right, consumed, name, visited, logger)
        return pe
    if hasattr(pe, 'inner'):
        pe.inner = checkRef(pe.inner, consumed, name, visited, logger)
        return pe
    if isinstance(pe, Ref):
        if not consumed and pe.name == name:
            out.perror(pe.pos3, msg='left recursion: ' + str(pe.name))
            return pe
        if not pe.isNonTerminal():
            if pe.name[0] == '"':
                return Char(pe.name[1:-2])
            if not pe.name[0].isupper():
                return Char(pe.name)
            out.perror(pe.pos3, msg='undefined name: ' + str(pe.name))
            return FAIL if Rule.isUnitName(pe.name) else TreeAs('', FAIL)
        if Rule.isInlineName(pe.name):
            out.notice(pe.pos3, msg='inlining: ' +
                        str(pe.name) + ' => ' + str(pe.deref()))
            return pe.deref()
        if not pe.name in visited:
            visited[pe.name] = True
            checkRef(pe.deref(), consumed, name, visited, logger)
    return pe
'''

def grammar_factory():
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

    class PEGConv(ParseTreeConv):
        def __init__(self, peg, N):
            self.peg = peg
            self.N = N

        def Empty(self, t, logger):
            return EMPTY

        def Any(self, t, logger):
            return ANY

        def Char(self, t, logger):
            s = t.asString()
            sb = []
            while len(s) > 0:
                c, s = unquote(s)
                sb.append(c)
            return char1(''.join(sb))

        def Class(self, t, logger):
            s = t.asString()
            chars = []
            ranges = []
            while len(s) > 0:
                c, s = unquote(s)
                if s.startswith('-') and len(s) > 1:
                    c2, s = unquote(s[1:])
                    ranges.append((c, c2))
                else:
                    chars.append(c)
            return Range(''.join(chars), ranges)

        def Ref(self, t, logger):
            name = t.asString()
            if name[0].isupper() or name[0].islower():
                return self.peg.newRef(name)
            if name in self.N:
                return self.peg.newRef(name)
            p = char1(name[1:-1]) if name.startswith('"') else char1(name)
            return p

        def Many(self, t, logger):
            return Many(self.conv(t['inner'], logger))

        def Many1(self, t, logger):
            return Many1(self.conv(t['inner'], logger))

        def Option(self, t, logger):
            return Ore(self.conv(t['inner'], logger), EMPTY)

        def And(self, t, logger):
            return And(self.conv(t['inner'], logger))

        def Not(self, t, logger):
            return Not(self.conv(t['inner'], logger))

        def Seq(self, t, logger):
            return seq2(self.conv(t['left'], logger), self.conv(t['right'], logger))

        def Ore(self, t, logger):
            return ore2(self.conv(t['left'], logger), self.conv(t['right'], logger))

        def Alt(self, t, logger):
            return Alt(self.conv(t['left'], logger), self.conv(t['right'], logger))

        def Node(self, t, logger):
            node = t.getString('node', '')
            inner = self.conv(t['inner'], logger)
            return Node(inner, node)

        def Edge(self, t, logger):
            edge = t.getString('edge', '')
            inner = self.conv(t['inner'], logger)
            return Edge(edge, inner)

        def Fold(self, t, logger):
            edge = t.getString('edge', '')
            node = t.getString('node', '')
            inner = self.conv(t['inner'], logger)
            return Fold(edge, inner, node)
        
        def Append(self, t, logger):
            name = ''
            tsub = t['inner']
            if tsub == 'Func':
                a = tsub.asArray()
                name = a[0].asString()
                inner = self.conv(a[1], logger)
            else:
                inner = self.conv(tsub, logger)
            return Edge(name, inner)

        FIRST = {'lazy', 'scope', 'symbol', 'match', 'equals', 'contains'}

        def Func(self, t, logger):
            funcname = t.getString('name', '')
            ps = []
            for l, p in t['params']:
                ps.append(self.conv(p, logger))
            if funcname in PEGConv.FIRST:
                return Action(ps[0], funcname, tuple(ps))
            return Action(EMPTY, funcname, tuple(ps))

    def example(peg, name, doc):
        peg['@@example'].append((name,doc))

    tpeg = TPEG(Grammar())
    pegparser = generate(tpeg)

    def load_grammar(g, file, logger=STDLOG):
        if isinstance(file, Path):
            f = file.open()
            data = f.read()
            f.close()
            t = pegparser(data, file)
            basepath = str(file)
        else:
            basepath = inspect.currentframe().f_back.f_code.co_filename
            t = pegparser(data, basepath)
            basepath = (str(Path(basepath).resolve().parent))
        if t == 'err':
            logger.perror(t.getpos4())
            return
        # load
        N = {}
        for _, stmt in t:
            if stmt == 'Rule':
                N[stmt['name'].asString()] = True
        pconv = PEGConv(g, N)
        g['@@example'] = []
        for _, stmt in t:
            if stmt == 'Rule':
                name = stmt['name'].asString()
                if name in g:
                    logger.perror(stmt['name'].getpos4(), f'redefined name {name}')
                    continue
                pe = pconv.conv(stmt['inner'], logger)
                g[name] = pe
                #g.add(name, pe, stmt['name'].pos3())
            elif stmt == 'Example':
                doc = stmt['doc']
                for _, n in stmt['names']:
                    example(g, n.asString(), doc.getpos4())
            elif stmt == 'Import':
                urn = stmt['name'].asString()
                lg = grammar(urn, basepath)
                for _, n in stmt['names']:
                    lname = n.asString()  # ns.Expression
                    name = lname
                    if lname.find('.') != -1:
                        name = lname.split('.')[-1]
                    if not name in lg:
                        logger.perror(n.getpos4(), f'undefined name {name}')
                    g[lname] = lg.newRef(name)
        '''
        g.forEachRule(lambda rule: checkRef(
            rule.inner, False, rule.name, {}, logger))

        def treeRule(rule):
            pe = checkTree(rule.inner, None)
            if not Rule.isInlineName(rule.name):
                ts = treeState(rule.inner)
                if ts == T.Unit and not Rule.isUnitName(rule.name):
                    out.warning(rule.pos3, 'illegal naming: use {}'.format(
                        rule.name.upper()))
                elif ts == T.Tree and not Rule.isTreeName(rule.name):
                    out.warning(rule.pos3, 'illegal naming: use camel case')
                elif ts == T.Mut or ts == T.Fold:
                    out.warning(
                        rule.pos3, 'illegal naming: allowed only inline')
            return pe
        g.forEachRule(treeRule)

        def dummy(pe):
            print('@first', first(pe.inner, g.max))
            return pe.inner
        '''
        # g.forEachRule(dummy)

    def findpath(paths, file):
        for p in paths:
            path = Path(p) / file
            print('@', path)
            if path.exists():
                return path.resolve()
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)

    GrammarDB = {}

    def grammar(urn, basepath=''):
        paths = []
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
            return GrammarDB
        peg = Grammar()
        load_grammar(peg, path)
        GrammarDB[key] = peg
        return peg
    
    return grammar

grammar = grammar_factory()

## grammar loader

peg = grammar('testcase.tpeg')
print(peg)

