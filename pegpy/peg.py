#!/usr/local/bin/python
import pegpy.ast as ast
import pegpy.parsefunc as parsefunc
import pegpy.utils as utils

class ParsingExpression(object):
    def __repr__(self):
        return self.__str__()
    def __or__(self,right):
        return Ore(self, pe(right))
    def __and__(self,right):
        return seq(self,pe(right))
    def __xor__(self,right):
        return seq(self,lfold("", pe(right)))
    def __rand__(self,left):
        return seq(pe(left), self)
    def __add__(self,right):
        return seq(Many1(self),pe(right))
    def __mul__(self,right):
        return seq(Many(self),pe(right))
    def __truediv__ (self, right):
        return Ore(self, pe(right))
    def __invert__(self):
        return Not(self)
    def __neq__(self):
        return Not(self)
    def __pos__(self):
        return And(self)
    def setpeg(self, peg):
        if hasattr(self, 'inner'):
            self.inner.setpeg(peg)
        if hasattr(self, 'right'):
            self.left.setpeg(peg)
            self.right.setpeg(peg)
    @classmethod
    def new(cls, e):
        return e

class Empty(ParsingExpression):
    def __str__(self):
        return "''"

EMPTY = Empty()

class Char(ParsingExpression):
    __slots__ = ['a']
    def __init__(self, a):
        self.a = a
    def __str__(self):
        return "'" + quote_str(self.a) + "'"

class Range(ParsingExpression):
    __slots__ = ['chars', 'ranges']
    def __init__(self, *ss):
        chars = []
        ranges = []
        for s in ss :
            if isinstance(s, tuple):
                ranges.append(s)
            elif len(s) == 3 and s[1] is '-':
                ranges.append((s[0], s[2]))
            else:
                for c in s:
                    chars.append(c)
        self.chars = tuple(chars)
        self.ranges = tuple(ranges)
    def __str__(self):
        l = tuple(map(lambda x: quote_str(x[0], ']')+'-'+quote_str(x[1], ']'), self.ranges))
        return "[" + ''.join(l) + quote_str(self.chars, ']') + "]"


class Any(ParsingExpression):
    def __str__(self):
        return '.'
ANY = Any()


class Ref(ParsingExpression, ast.SourcePosition):
    __slots__ = ['peg', 'name', 'pos']
    def __init__(self, name, peg = None):
        self.name = name
        self.peg = peg
    def __str__(self):
        return str(self.name)
    def setpeg(self, peg):
        self.peg = peg
    def isNonTerminal(self):
        return hasattr(self.peg, self.name)
    def deref(self):
        return getattr(self.peg, self.name).inner
    def prop(self):
        return getattr(self.peg, self.name)
    def getmemo(self,prefix):
        return self.peg.getmemo(prefix+self.name)
    def setmemo(self,prefix,value):
        return self.peg.setmemo(prefix+self.name,value)


class Seq(ParsingExpression):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = pe(left)
        self.right = pe(right)
    def __str__(self):
        return grouping(self.left, inSeq) + ' ' + grouping(self.right, inSeq)
    def flatten(self, ls):
        if isinstance(self.left, Seq):
            self.left.flatten(ls)
        else:
            ls.append(self.left)
        if isinstance(self.right, Seq):
            self.right.flatten(ls)
        else:
            ls.append(self.right)
        return ls

class Ore(ParsingExpression):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = pe(left)
        self.right = pe(right)
    def __str__(self):
        if self.right == EMPTY:
            return grouping(self.left, inUnary) + '?'
        return str(self.left) + ' / ' + str(self.right)
    def flatten(self, ls):
        if isinstance(self.left, Ore):
            self.left.flatten(ls)
        else:
            ls.append(self.left)
        if isinstance(self.right, Ore):
            self.right.flatten(ls)
        else:
            ls.append(self.right)
        return ls

class Alt(ParsingExpression):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = pe(left)
        self.right = pe(right)
    def __str__(self):
        return str(self.left) + ' | ' + str(self.right)
    def flatten(self, ls):
        if isinstance(self.left, Alt):
            self.left.flatten(ls)
        else:
            ls.append(self.left)
        if isinstance(self.right, Alt):
            self.right.flatten(ls)
        else:
            ls.append(self.right)
        return ls

class And(ParsingExpression):
    __slots__ = ['inner']
    def __init__(self, inner):
        self.inner = pe(inner)
    def __str__(self):
        return '&' + grouping(self.inner, inUnary)

class Not(ParsingExpression):
    __slots__ = ['inner']
    def __init__(self, inner):
        self.inner = pe(inner)
    def __str__(self):
        return '!' + grouping(self.inner, inUnary)

class Many(ParsingExpression):
    __slots__ = ['inner']
    def __init__(self, inner):
        self.inner = pe(inner)
    def __str__(self):
        return grouping(self.inner, inUnary) + '*'

class Many1(ParsingExpression):
    __slots__ = ['inner']
    def __init__(self, inner):
        self.inner = pe(inner)
    def __str__(self):
        return grouping(self.inner, inUnary) + '+'

def grouping(e, f): return '(' + str(e) + ')' if f(e) else str(e)
def inSeq(e): return isinstance(e, Ore) or isinstance(e, Alt)
def inUnary(e): return (isinstance(e, Ore) and e.right != EMPTY) or isinstance(e, Seq) or isinstance(e, Alt)
def quote_str(e, esc = "'"):
    sb = []
    for c in e:
        if c == '\n' : sb.append(r'\n')
        elif c == '\t' : sb.append(r'\t')
        elif c == '\\' : sb.append(r'\\')
        elif c == '\r' : sb.append(r'\r')
        elif c in esc : sb.append('\\' + c)
        else: sb.append(c)
    return "".join(sb)

def pe(x):
    if x == 0 : return EMPTY
    if isinstance(x, str):
        if len(x) == 0:
            return EMPTY
        return Char(x)
    return x

def ref(name):
    if name.find('/') != -1:
        return lor(list(map(ref, name.split('/'))))
    if name.find(' ') != -1:
        return lseq(list(map(ref, name.split(' '))))
    if name.startswith('$'):
        return LinkAs("", Ref(name[1:]))
    return Ref(name)

def seq(x,y):
    if isinstance(y, Empty): return x
    return Seq(x, y)

def lseq(ls):
    if len(ls) > 1:
        return seq(ls[0], lseq(ls[1:]))
    if len(ls) == 1: return ls[0]
    return EMPTY

def lor(ls):
    if len(ls) > 1:
        return Ore(ls[0], lor(ls[1:]))
    if len(ls) == 1: return ls[0]
    return EMPTY

def lfold(ltag,e):
    if isinstance(e, Many) and isinstance(e.inner, TreeAs):
        return Many(lfold(ltag, e.inner))
    if isinstance(e, Many1) and isinstance(e.inner, TreeAs):
        return Many1(lfold(ltag, e.inner))
    if isinstance(e, Ore):
        return Ore(lfold(ltag, e.left), lfold(ltag, e.right))
    if isinstance(e, TreeAs):
        return FoldAs(ltag, e.name, pe(e.inner))
    return e

## Tree Construction

class TreeAs(ParsingExpression):
    __slots__ = ['name', 'inner']
    def __init__(self, name = '', inner = EMPTY):
        self.name = name
        self.inner = pe(inner)
    def __str__(self):
        return self.name + '{ ' + str(self.inner) + ' }'

class LinkAs(ParsingExpression):
    __slots__ = ['name', 'inner']
    def __init__(self, name = '', inner=None):
        self.name = name
        self.inner = pe(inner)
    def __str__(self):
        if self.name == '':
            return '$' + grouping(self.inner, inUnary)
        return '(' + self.name + '=>' + str(self.inner) + ')'
    def __le__(self, right):
        return LinkAs(self.name, right)
    def __ge__(self, right):
        return LinkAs(self.name, right)
    def __mod__(self, right):
        return ref(right)
    def __xor__(self,right):
        return lfold(self.name, pe(right))

N = LinkAs("")

class FoldAs(ParsingExpression):
    __slots__ = ['left', 'name', 'inner']
    def __init__(self, left = '', name = '', inner = EMPTY):
        self.left = left
        self.name = name
        self.inner = pe(inner)
    def __str__(self):
        return self.left + '^' + self.name + '{ ' + str(self.inner) + ' }'

class Detree(ParsingExpression):
    __slots__ = ['inner']
    def __init__(self, inner):
        self.inner = pe(inner)
    def __str__(self):
        return '@unit(' + str(self.inner) + ')'

'''
@if(Bool)
@symbol(Indent)
@match(Indent)
@exists(Indent, 'hoge')
'''

class Meta(ParsingExpression):
    __slots__ = ['name', 'inner', 'opt']
    def __init__(self, name, inner, opt = None):
        self.name = name
        self.inner = pe(inner)
        self.opt = opt
    def __str__(self):
        arg = ', ' + repr(self.opt) if self.opt != None else ''
        return self.tag + '(' + str(self.inner) + arg + ')'

'''
class ParserContext:
    __slots__ = ['inputs', 'pos', 'headpos', 'ast']
    def __init__(self, inputs, pos = 0):
        self.inputs = inputs
        self.pos = pos
        self.headpos = pos
        self.ast = None
'''
#

def pegp(peg, name = None, conv = None):
    if not hasattr(Char, 'dasm'):
        def emit(pe): return pe.dasm()

        Empty.dasm = lambda self: parsefunc.true
        Any.dasm = lambda self: parsefunc.any
        Char.dasm = parsefunc.emit_Byte
        Range.dasm = parsefunc.emit_ByteRange

        Seq.dasm = lambda pe: parsefunc.emit_Seq(pe, emit)
        Ore.dasm = lambda pe: parsefunc.emit_Or(pe, emit)
        Not.dasm = lambda pe: parsefunc.emit_Not(pe, emit)
        And.dasm = lambda pe: parsefunc.emit_And(pe, emit)
        Many.dasm = lambda pe: parsefunc.emit_Many(pe, emit)
        Many1.dasm = lambda pe: parsefunc.emit_Many1(pe, emit)

        TreeAs.dasm = lambda pe: parsefunc.emit_TreeAs(pe, emit, ast.ParseTree)
        LinkAs.dasm = lambda pe: parsefunc.emit_LinkAs(pe, emit, ast.TreeLink)
        FoldAs.dasm = lambda pe: parsefunc.emit_FoldAs(pe, emit, ast.ParseTree, ast.TreeLink)
        Detree.dasm = lambda pe: parsefunc.emit_Unit(pe, emit)

        # Ref
        Ref.dasm = lambda pe: parsefunc.emit_Ref(pe.peg, pe.name, "_DAsm_", emit)
        Rule.dasm = lambda pe: parsefunc.emit_Rule(pe, emit)
    # end of dasm

    if isinstance(peg, ParsingExpression):
        f = peg.dasm()
    else:
        if name == None: name = "start"
        f = parsefunc.emit_Ref(peg, name, "_DAsm_", lambda pe: pe.dasm())

    class DAsmContext:
        __slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast']

        def __init__(self, inputs, urn='(unknown)', pos=0):
            s = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
            self.inputs, self.pos = ast.encode_source(s, urn, pos)
            self.length = len(self.inputs)
            self.headpos = self.pos
            self.ast = None

    def parse(s, urn = '(unknown)', pos = 0):
        px = DAsmContext(s, urn, pos)
        pos = px.pos
        ast0 = None
        if not f(px):
            ast0 = ast.ParseTree("err", px.inputs, px.headpos, len(s), None)
        else:
            ast0 = px.ast if px.ast is not None else ast.ParseTree("", px.inputs, pos, px.pos, None)
        return conv(ast0) if conv is not None else ast0

    return parse

# Rule

class Rule(object):
    def __init__(self, name, inner):
        self.name = name
        self.inner = pe(inner)
        self.checked = False
    def __str__(self):
        return str(self.inner)
    def isConsumed(self):
        if not hasattr(self, 'nonnull'):
            self.nonnull = isAlwaysConsumed(self.inner)
        return self.nonnull
    def treeState(self):
        if not hasattr(self, 'ts'):
            self.ts = treeState(self.inner)
        return self.ts
    def checkRule(self):
        if not self.checked:
            s0 = str(self.inner)
            if isRec(self.inner, self.name, {}):
                checkRec(self.inner, self.name, {})
            ts = treeState(self.inner)
            ts = treeCheck(self.inner, ts)
            s1 = str(self.inner)
            if s0 != s1:
                print(self.name, s0, s1)

## Grammar

class PEG(object):
    def __init__(self, ns = None):
        self.ns77 = ns
        self.memo77 = {}
        self.example77 = []
    def __getitem__(self, item):
        return getattr(self, item, None)
    def __setattr__(self, key, value):
        if isinstance(value, ParsingExpression):
            value.setpeg(self)
            if not isinstance(value, Rule):
                value = Rule(key, value)
            super().__setattr__(key, value)
            print(key, '=', value)
            if not hasattr(self, "start"):
                setattr(self, "start", value)
        else:
            super().__setattr__(key, value)

    def ns(self): return self.ns77
    def hasmemo(self, key): return key in self.memo77
    def getmemo(self, key): return self.memo77[key] if key in self.memo77 else None
    def setmemo(self, key, value): self.memo77[key] = value

    def example(self, prod, input, output = None):
        for name in prod.split(','):
            self.example77.append((name, input, output))

    def testAll(self, combinator = pegp):
        p = {}
        test = 0
        ok = 0
        for testcase in self.example77:
            name, input, output = testcase
            if not name in p: p[name] = combinator(self, name)
            res = p[name](input)
            t = str(res).replace(" b'", " '")
            if output == None:
                print(name, input, '=>', t)
            else:
                test += 1
                if t == output:
                    print('OK', name, input)
                    ok += 1
                else:
                    print('NG', name, input, output, '!=', t)
        if test > 0:
            print('OK', ok, 'FAIL', test - ok, ok / test * 100.0, '%')

## PEG


## Properties

def match(*ctags):
    def _match(func):
        name = ctags[-1]
        for ctag in ctags[:-1]:
            setattr(ctag, name, func)
        return func
    return _match

def isRec(pe: ParsingExpression, name: str, visited : dict) -> bool:
    if isinstance(pe, Ref):
        if pe.name == name: return True
        if not pe.name in visited:
            visited[pe.name] = True
            return isRec(pe.deref(), name, visited)
    if hasattr(pe, 'inner'):
        return isRec(pe.inner, name, visited)
    if hasattr(pe, 'left'):
        rec = isRec(pe.left, name, visited)
        return rec if rec else isRec(pe.right, name, visited)
    return False

def checkRec(pe: ParsingExpression, name: str, visited : dict) -> bool:
    if hasattr(pe, 'left'):
        if isinstance(pe, Seq):
            return checkRec(pe.left, name, visited) and checkRec(pe.right, name, visited)
        else: #Ore, Alt
            c0 = checkRec(pe.left, name, visited)
            c1 = checkRec(pe.right, name, visited)
            return c0 or c1
    if hasattr(pe, 'inner'):
        rec = checkRec(pe.inner, name, visited)
        return True if isinstance(pe, Not) or isinstance(pe, Many) or isinstance(pe, And) else rec
    if isinstance(pe, Ref):
        if pe.name == name:
            print("TODO left recursion", name)
        if not pe.name in visited:
            visited[pe.name] = True
            checkRec(pe.deref(), name, visited)
        return not pe.prop().isConsumed()
    return isinstance(pe, Empty) # False if (Char,Range,Any)

def isAlwaysConsumed(pe: ParsingExpression):
    if not hasattr(pe, 'cc'):
        @match(Char, Any, Range, 'cc')
        def consumed(pe): return True

        @match(Many, Not, And, Empty, 'cc')
        def consumed(pe): return False

        @match(Many1, LinkAs, TreeAs, FoldAs, Detree, Meta, 'cc')
        def unary(pe):
            return isAlwaysConsumed(pe.inner)

        @match(Seq, 'cc')
        def seq(pe):
            if not isAlwaysConsumed(pe.left): return False
            return isAlwaysConsumed(pe.right)

        @match(Ore, Alt, 'cc')
        def ore(pe):
            return isAlwaysConsumed(pe.left) and isAlwaysConsumed(pe.right)

        @match(Ref, 'cc')
        def memo(pe: Ref):
            if not pe.isNonTerminal():
                return True
            key = 'null' + pe.name
            memoed = pe.getmemo('null')
            if memoed == None:
                pe.setmemo('null', True)
                memoed = isAlwaysConsumed(pe.deref())
                pe.setmemo('null', memoed)
            return memoed
    return pe.cc()

## TreeState
TUnit = 0
TTree = 1
TMut = 2
TFold = 3

def treeState(pe):
    if not hasattr(pe, 'ts'):
        @match(Char, Any, Range, Not, Detree, 'ts')
        def stateUnit(pe):
            return TUnit

        @match(TreeAs, 'ts')
        def stateTree(pe):
            return TTree

        @match(LinkAs, 'ts')
        def stateMut(pe):
            return TMut

        @match(FoldAs, 'ts')
        def stateFold(pe):
            return TFold

        @match(Seq, 'ts')
        def stateSeq(pe):
            ts0 = treeState(pe.left)
            return ts0 if ts0 != TUnit else treeState(pe.right)

        @match(Ore, Alt, 'ts')
        def stateAlt(pe):
            ts0 = treeState(pe.left)
            if ts0 != TUnit: return ts0
            ts1 = treeState(pe.right)
            return TMut if ts1 == TTree else ts1

        @match(Many, Many1, And, 'ts')
        def stateAlt(pe):
            ts0 = treeState(pe.inner)
            return TMut if ts0 == TTree else ts0

        @match(Ref, 'ts')
        def memo(pe: Ref):
            if not pe.isNonTerminal(): return TUnit
            memoed = pe.getmemo('ts')
            if memoed == None:
                pe.setmemo('ts', TUnit)
                memoed = treeState(pe.deref())
                pe.setmemo('ts', memoed)
            return memoed
    return pe.ts()

def treeCheck(pe, ts):
    if not hasattr(pe, 'tc'):
        @match(ParsingExpression, 'tc')
        def checkEmpty(pe, ts): return pe

        @match(TreeAs, 'tc')
        def checkTree(pe, ts):
            if ts == TUnit:
                return treeCheck(pe.inner, TUnit)
            if ts == TTree:
                pe.inner = treeCheck(pe.inner, TMut)
                return pe
            if ts == TMut:
                pe.inner = treeCheck(pe.inner, TMut)
                return LinkAs('', pe)
            if ts == TFold:
                pe.inner = treeCheck(pe.inner, TMut)
                return FoldAs('', pe.tag, pe.inner)

        @match(LinkAs, 'tc')
        def checkLink(pe, ts):
            if ts == TUnit or ts == TFold:
                return treeCheck(pe.inner, TUnit)
            if ts == TTree:
                return treeCheck(pe.inner, TTree)
            if ts == TMut:
                ts0 = treeState(pe.inner)
                if ts0 == TUnit or ts0 == TFold: pe.inner = TreeAs('', treeCheck(pe.inner, TUnit))
                if ts0 == TTree: pe.inner = treeCheck(pe.inner, TTree)
                if ts0 == TMut: pe.inner = TreeAs('', treeCheck(pe.inner, TMut))
                return pe

        @match(FoldAs, 'tc')
        def checkFold(pe, ts):
            if ts == TUnit:
                return treeCheck(pe.inner, TUnit)
            if ts == TTree:
                pe.inner = treeCheck(pe.inner, TMut)
                return TreeAs(pe.tag, pe.inner)
            if ts == TMut:
                pe.inner = treeCheck(pe.inner, TMut)
                return LinkAs(pe.ltag, pe.inner)
            if ts == TFold:
                pe.inner = treeCheck(pe.inner, TMut)
                return pe

        @match(Seq, 'tc')
        def checkSeq(pe, ts):
            if ts == TUnit or ts == TMut or ts == TFold:
                pe.left = treeCheck(pe.left, ts)
                pe.right = treeCheck(pe.right, ts)
                return pe
            ts0 = treeState(pe.left)
            if ts0 == TUnit:
                pe.left = treeCheck(pe.left, TUnit)
                pe.right = treeCheck(pe.right, ts)
                return pe
            if ts0 == TTree:
                pe.left = treeCheck(pe.left, TTree)
                pe.right = treeCheck(pe.right, TFold)
                return pe

        @match(Ore, Alt, 'tc')
        def checkAlt(pe, ts):
            pe.left = treeCheck(pe.left, ts)
            pe.right = treeCheck(pe.right, ts)
            return pe

        @match(Many, Many1, 'tc')
        def checkMany(pe, ts):
            if ts == TUnit:
                pe.inner = treeCheck(pe.inner, TUnit)
                return pe
            if ts == TTree:
                pe.inner = treeCheck(pe.inner, TUnit)
                return TreeAs('', pe)
            if ts == TMut:
                ts0 = treeState(pe.inner)
                if ts0 == TUnit or ts0 == TFold: pe.inner = treeCheck(pe.inner, TUnit)
                if ts0 == TTree or ts0 == TMut: pe.inner = treeCheck(pe.inner, TMut)
                return pe
            if ts == TFold:
                pe.inner = treeCheck(pe.inner, TFold)
                return pe

        @match(Ref, 'tc')
        def checkRef(pe: Ref, ts):
            if not pe.isNonTerminal(): return pe
            ts0 = treeState(pe)
            if ts == ts0: return pe
            if ts == TUnit: Detree(pe)
            if ts == TTree:
                if ts0 == TUnit or ts0 == TMut: return TreeAs('', pe)
                if ts0 == TFold: return seq(TreeAs('', EMPTY), pe)
            if ts == TMut:
                if ts0 == TUnit: return pe
                if ts0 == TTree: return LinkAs('', pe)
                if ts0 == TFold: return LinkAs('', seq(TreeAs('', EMPTY), pe))
            if ts == TFold:
                if ts0 == TUnit: return pe
                if ts0 == TTree: return FoldAs('', '', pe)
                if ts0 == TMut: return FoldAs('', '', TreeAs('', pe))
    return pe.tc(ts)


def testRules(g: PEG):
    for name in dir(g):
        if not name[0].isupper(): continue
        p = getattr(g, name)
        p.checkRule()


## Loader

def tpeg(g = None):
    if g == None: g = PEG('peg')

    # Preliminary
    __ = N % '__'
    _ = N % '_'
    EOS = N % 'EOS'

    g.Start = N%'__ Source EOF'
    g.EOF = ~ANY
    g.EOL = pe('\n') | pe('\r\n') | N%'EOF'
    g.COMMENT = '/*' & (~pe('*/') & ANY)* 0 & '*/' | '//' & (~(N%'EOL') & ANY)* 0
    g._ = (Range(' \t') | N%'COMMENT')* 0
    g.__ = (Range(' \t\r\n') | N%'COMMENT')* 0
    g.S = Range(' \t')

    g.Source = TreeAs('Source', (N%'$Statement')*0)
    g.EOS = N%'_' & (';' & N%'_' | N%'EOL' & (N%'S' | N%'COMMENT') & N%'_' | N%'EOL')* 0

    left = LinkAs('left')
    right = LinkAs('right')
    name = LinkAs('name')
    inner = LinkAs('inner')

    g.Statement = N%'Example/Rule'

    g.Rule = TreeAs('Rule', (name <= N%'Identifier __') & '=' & __ & (Range('/|') & __ |0) & (inner <= N%'Expression')) & EOS

    g.Example = TreeAs('Example', 'example' & N%'S _' & (name <= N%'Names') & (inner <= N%'Doc')) & EOS
    g.Names = TreeAs('', N%'$Identifier _' & (Range(',&') & N%'_ $Identifier _')*0)
    Doc1 = TreeAs("Doc", (~(N%'DELIM EOL') & ANY)* 0)
    Doc2 = TreeAs("Doc", (~Range('\r\n') & ANY)* 0)
    g.Doc = N%'DELIM' & (N%'S'*0) & N%'EOL' & Doc1 & N % 'DELIM' | Doc2
    g.DELIM = pe("'''")

    g.Expression = N%'Choice' & (left ^ (TreeAs('Alt', __ & '|' & _ & (right <= N%'Expression'))|0))
    g.Choice = N%'Sequence' & (left ^ (TreeAs('Ore', __ & '/' & _ & (right <= N%'Choice'))|0))
    g.SS = N%'S _' & ~(N%'EOL') | (N%'_ EOL')+0 & N%'S _'
    g.Sequence = N%'Predicate' & (left ^ (TreeAs('Seq', (right <= N%'SS Sequence'))|0))

    g.Predicate = TreeAs('Not', '!' & (inner <= N%'Predicate')) \
                  | TreeAs('And', '&' & (inner <= N%'Predicate')) \
                  | TreeAs('Append', '$' & ( inner <= N%'Predicate')) \
                  | N%'Suffix'
    g.Suffix = N%'Term' & ((inner ^ TreeAs('Many', '*')) | (inner ^ TreeAs('Many1', '+')) | (inner ^ TreeAs('Option', '?')) | 0)

    g.Term = N%'Group/Char/Class/Any/Tree/Fold/BindFold/Bind/Func/Ref'
    g.Group = '(' & __ & N%'Expression/Empty' & __ & ')'

    g.Empty = TreeAs('Empty', EMPTY)
    g.Any = TreeAs('Any', '.')
    g.Char = "'" & TreeAs('Char', (r'\\' & ANY | ~Range("'\n") & ANY)*0) & "'"
    g.Class = '[' & TreeAs('Class', (r'\\' & ANY | ~Range("]") & ANY)*0) & ']'
    g.Tree = TreeAs('TreeAs', N%'Tag __' & (inner <= (N%'Expression __' | N%'Empty')) & '}' )
    g.Fold = '^' & _ & TreeAs('Fold', N%'Tag __' & (inner <= (N%'Expression __' | N%'Empty')) & '}' )
    g.Tag = ((name <= N%'Identifier')|0) & '{'
    g.Identifier = TreeAs('Name', Range('A-Z', 'a-z', '@') & Range('A-Z', 'a-z', '0-9', '_.')*0)

    g.Bind = TreeAs('LinkAs', (name <= N%'Var _') & '=>' & (inner <= N%'_ Expression'))
    g.BindFold = TreeAs('Fold', (left <= N%'Var _') & '^' & _ & N%'Tag __' & (inner <= (N%'Expression __' | N%'Empty')) & '}')
    g.Var = TreeAs('Name', Range('a-z', '$') & Range('A-Z', 'a-z', '0-9', '_')*0)

    g.Func = TreeAs('Func', N%'$Identifier' & '(' & (N%'$Expression _' & ',' & __)* 0 & N%'$Expression _' & ')')
    g.Ref = TreeAs('Ref', N%'NAME')
    g.NAME = '"' & (pe(r'\"') | ~Range('\\"\n') & ANY)* 0 & '"' | (~Range(' \t\r\n(,){};<>[|/*+?=^\'`') & ANY)+0

    # Example
    #g.example("Ref", "abc")
    #g.example("Ref", '"abc"')
    g.example("COMMENT", "/*hoge*/hoge", "[# '/*hoge*/']")
    g.example("COMMENT", "//hoge\nhoge", "[# '//hoge']")

    g.example("Ref,Term,Expression", "a", "[#Ref 'a']")

    g.example("Char,Expression", "''", "[#Char '']")
    g.example("Char,Expression", "'a'", "[#Char 'a']")
    g.example("Ref,Expression", "\"a\"", "[#Ref '\"a\"']")
    g.example("Class,Expression", "[a]", "[#Class 'a']")
    g.example("Func", "f(a)", "[#Func [#Name 'f'] [#Ref 'a']]")
    g.example("Func", "f(a,b)", "[#Func [#Name 'f'] [#Ref 'a'] [#Ref 'b']]")
    g.example("Predicate,Expression", "&a", "[#And inner=[#Ref 'a']]")
    g.example("Predicate,Expression", "!a", "[#Not inner=[#Ref 'a']]")
    g.example("Suffix,Expression", "a?", "[#Option inner=[#Ref 'a']]")
    g.example("Suffix,Expression", "a*", "[#Many inner=[#Ref 'a']]")
    g.example("Suffix,Expression", "a+", "[#Many1 inner=[#Ref 'a']]")
    g.example("Expression", "{}", "[#TreeAs inner=[#Empty '']]")
    g.example("Expression", "{ a }", "[#TreeAs inner=[#Ref 'a']]")
    g.example("Expression", "{ }", "[#TreeAs inner=[#Empty '']]")
    g.example("Expression", "()", "[#Empty '']")
    g.example("Expression", "&'a'", "[#And inner=[#Char 'a']]")

    g.example("Expression", "{a}", "[#TreeAs inner=[#Ref 'a']]")
    g.example("Expression", "Int{a}", "[#TreeAs name=[#Name 'Int'] inner=[#Ref 'a']]")
    g.example("Expression", "^{a}", "[#Fold inner=[#Ref 'a']]")
    g.example("Expression", "^Int{a}", "[#Fold name=[#Name 'Int'] inner=[#Ref 'a']]")
    g.example("Expression", "name^{a}", "[#Fold left=[#Name 'name'] inner=[#Ref 'a']]")
    g.example("Expression", "name^Int{a}", "[#Fold left=[#Name 'name'] name=[#Name 'Int'] inner=[#Ref 'a']]")
    g.example("Expression", "$a", "[#Append inner=[#Ref 'a']]")
    g.example("Expression", "name=>a", "[#LinkAs name=[#Name 'name'] inner=[#Ref 'a']]")
    g.example("Expression", "name => a", "[#LinkAs name=[#Name 'name'] inner=[#Ref 'a']]")

    g.example("Expression", "a a", "[#Seq left=[#Ref 'a'] right=[#Ref 'a']]")
    g.example("Expression", "a b c", "[#Seq left=[#Ref 'a'] right=[#Seq left=[#Ref 'b'] right=[#Ref 'c']]]")
    g.example("Expression", "a/b / c", "[#Ore left=[#Ref 'a'] right=[#Ore left=[#Ref 'b'] right=[#Ref 'c']]]")
    g.example("Expression", "a|b | c", "[#Alt left=[#Ref 'a'] right=[#Alt left=[#Ref 'b'] right=[#Ref 'c']]]")
    g.example("Statement", "A=a", "[#Rule name=[#Name 'A'] inner=[#Ref 'a']]")
    g.example("Statement", "example A,B abc \n", "[#Example name=[# [#Name 'A'] [#Name 'B']] inner=[#Doc 'abc ']]")
    g.example("Statement", "A = a\n  b", "[#Rule name=[#Name 'A'] inner=[#Seq left=[#Ref 'a'] right=[#Ref 'b']]]")
    g.example("Start", "A = a; B = b;;",
              "[#Source [#Rule name=[#Name 'A'] inner=[#Ref 'a']] [#Rule name=[#Name 'B'] inner=[#Ref 'b']]]")
    g.example("Start", "A = a\nB = b",
              "[#Source [#Rule name=[#Name 'A'] inner=[#Ref 'a']] [#Rule name=[#Name 'B'] inner=[#Ref 'b']]]")
    g.example("Start", "A = a //hoge\nB = b",
              "[#Source [#Rule name=[#Name 'A'] inner=[#Ref 'a']] [#Rule name=[#Name 'B'] inner=[#Ref 'b']]]")

    return g


def setup_loader():
    class PEGConv(ast.TreeConv):
        def __init__(self, *args):
            super(PEGConv, self).__init__(*args)

        def Empty(self, t):
            return EMPTY

        def Any(self, t):
            return ANY

        def Char(self, t):
            s = t.asString()
            if s.find(r'\x') >= 0:
                sb = []
                s = s.encode('utf-8')
                while len(s) > 0:
                    c, s = utils.unquote(bytes(s, 'ascii'))
                    sb.append(c)
                return pe(b''.join(sb))
            else:
                sb = []
                while len(s) > 0:
                    c, s = utils.unquote(s)
                    sb.append(c)
                return pe(''.join(sb))

        def Class(self, t):
            s = t.asString()
            sb = []
            while len(s) > 0:
                c, s = utils.unquote(s)
                if s.startswith('-') and len(s) > 2:
                    c2, s = utils.unquote(s[1:])
                    sb.append((c, c2))
                else:
                    sb.append(c)
            return Range(sb)

        def Fold(self, t):
            left = t['left'].asString() if t.has('left') else ''
            name = t['name'].asString() if t.has('name') else ''
            inner = self.conv(t['inner'])
            return FoldAs(left, name, inner)

    PEGconv = PEGConv(Ore, Alt, Seq, And, Not, Many, Many1, TreeAs, FoldAs, LinkAs, Ref)
    pegparser = pegp(tpeg())

    def load(self, path):
        f = open(path)
        data = f.read()
        f.close()
        # print('@@', data)
        t = pegparser(data, path)
        # print('@@', pegparser(data))
        # load
        for stmt in t.asArray():
            if stmt == 'Rule':
                name = stmt['name'].asString()
                pexr = stmt['inner']
                # print(name, '\n\t', pexr, '\n\t', pexr.asJSON())
                print(name, PEGconv.conv(pexr))
    PEG.load = load

setup_loader()