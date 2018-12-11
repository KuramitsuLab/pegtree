from enum import Enum
import pegpy.utils as u

class ParsingExpression(object):
    def __repr__(self):
        return self.__str__()

    def __or__(self,right):
        return Alt(self, ParsingExpression.new(right))

    def __and__(self,right):
        return seq(self, ParsingExpression.new(right))

    def __xor__(self,right):
        return seq(self,lfold("", ParsingExpression.new(right)))

    def __rand__(self,left):
        return seq(ParsingExpression.new(left), self)

    def __add__(self,right):
        return seq(Many1(self),ParsingExpression.new(right))

    def __mul__(self,right):
        return seq(Many(self),ParsingExpression.new(right))

    def __truediv__ (self, right):
        return Ore(self, ParsingExpression.new(right))

    def __invert__(self):
        return Not(self)

    def __neq__(self):
        return Not(self)

    def __pos__(self):
        return And(self)

    def __len__(self):
        if hasattr(self, 'inner'): return 1
        if hasattr(self, 'right'): return 2
        return 0

    def __getitem__(self, item):
        if hasattr(self, 'inner') and item == 0:
            return self.inner
        if hasattr(self, 'right'):
            if item == 0: return self.left
            if item == 1: return self.right
        raise IndexError

    def __iter__(self):
        if hasattr(self, 'inner'):
            yield self.inner
        if hasattr(self, 'right'):
            yield self.left
            yield self.right

    def setpeg(self, peg):
        '''
        if hasattr(self, 'inner'):
            self.inner = self.inner.setpeg(peg)
        if hasattr(self, 'right'):
            self.left = self.left.setpeg(peg)
            self.right = self.right.setpeg(peg)
        '''
        for pe in self:
            pe.setpeg(peg)
        return self

    def deref(self):
        return self.inner

    @classmethod
    def new(cls, e):
        if e == 0: return EMPTY
        if isinstance(e, str):
            if len(e) == 0:
                return EMPTY
            return Char(e)
        return e


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
        return FoldAs(ltag, e.name, ParsingExpression.new(e.inner))
    return e


def grouping(e, f):
    return '(' + str(e) + ')' if f(e) else str(e)


def inSeq(e):
    return isinstance(e, Ore) or isinstance(e, Alt)


def inUnary(e):
    return (isinstance(e, Ore) and e.right != EMPTY) \
           or isinstance(e, Seq) or isinstance(e, Alt) \
           or isinstance(e, LinkAs) or isinstance(e, FoldAs)

# PEG Grammar


class Empty(ParsingExpression):
    def __str__(self):
        return "''"

EMPTY = Empty()

class Char(ParsingExpression):
    __slots__ = ['a']

    def __init__(self, a):
        self.a = a
    def __str__(self):
        return "'" + u.quote_string(self.a) + "'"


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
        self.chars = ''.join(chars)
        self.ranges = tuple(ranges)

    def __str__(self):
        l = tuple(map(lambda x: u.quote_string(x[0], ']') + '-' + u.quote_string(x[1], ']'), self.ranges))
        return "[" + ''.join(l) + u.quote_string(self.chars, ']') + "]"


class Any(ParsingExpression):
    def __str__(self):
        return '.'

ANY = Any()

def flatten(pe, cls, ls):
    if isinstance(pe, cls):
        if isinstance(pe.left, cls):
            flatten(pe.left, cls, ls)
        else:
            ls.append(pe.left)
        if isinstance(pe.right, cls):
            flatten(pe.right, cls,ls)
        else:
            ls.append(pe.right)
        return ls

class Seq(ParsingExpression):
    __slots__ = ['left', 'right']

    def __init__(self, left, right):
        self.left = ParsingExpression.new(left)
        self.right = ParsingExpression.new(right)

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
        self.left = ParsingExpression.new(left)
        self.right = ParsingExpression.new(right)

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
        self.left = ParsingExpression.new(left)
        self.right = ParsingExpression.new(right)
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
        self.inner = ParsingExpression.new(inner)

    def __str__(self):
        return '&' + grouping(self.inner, inUnary)


class Not(ParsingExpression):
    __slots__ = ['inner']

    def __init__(self, inner):
        self.inner = ParsingExpression.new(inner)

    def __str__(self):
        return '!' + grouping(self.inner, inUnary)

class Many(ParsingExpression):
    __slots__ = ['inner']

    def __init__(self, inner):
        self.inner = ParsingExpression.new(inner)

    def __str__(self):
        return grouping(self.inner, inUnary) + '*'

class Many1(ParsingExpression):
    __slots__ = ['inner']

    def __init__(self, inner):
        self.inner = ParsingExpression.new(inner)

    def __str__(self):
        return grouping(self.inner, inUnary) + '+'

## Tree Construction

class TreeAs(ParsingExpression):
    __slots__ = ['name', 'inner']
    def __init__(self, name = '', inner = EMPTY):
        self.name = name
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        tag = ' #' + self.name if self.name != '' else ''
        return '{ ' + str(self.inner) + tag + ' }'

class LinkAs(ParsingExpression):
    __slots__ = ['name', 'inner']
    def __init__(self, name = '', inner=None):
        self.name = name
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        if self.name == '':
            return '$' + grouping(self.inner, inUnary)
        return self.name + ': ' + str(self.inner)
    def __le__(self, right):
        return LinkAs(self.name, right)
    def __ge__(self, right):
        return LinkAs(self.name, right)
    def __mod__(self, right):
        return ref(right)
    def __xor__(self,right):
        return lfold(self.name, ParsingExpression.new(right))

N = LinkAs("")

class FoldAs(ParsingExpression):
    __slots__ = ['left', 'name', 'inner']
    def __init__(self, left = '', name = '', inner = EMPTY):
        self.left = left
        self.name = name
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        prefix = '^' if self.name == '' else self.left + ':^ '
        tag = ' #' + self.name if self.name != '' else ''
        return prefix + '{ ' + str(self.inner) + tag + ' }'

class Detree(ParsingExpression):
    __slots__ = ['inner']
    def __init__(self, inner):
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        return '@detree(' + str(self.inner) + ')'

## Symbol

class State(ParsingExpression):
    __slots__ = ['func', 'name', 'inner', 'opt']
    def __init__(self, func, inner, opt = None):
        self.func = func
        self.inner = ParsingExpression.new(inner)
        self.name = str(self.inner) if opt is None else opt
        self.opt = opt
    def __str__(self):
        return  self.func + '(' + str(self.inner) + ')'

# @on(flag, e)
class On(ParsingExpression):
    __slots__ = ['name', 'inner']
    def __init__(self, name, inner):
        self.name = name
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        return  '@on(' + str(self.inner) + ')'

# @off(flag, e)
class Off(ParsingExpression):
    __slots__ = ['name', 'inner']
    def __init__(self, name, inner):
        self.name = name
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        return  '@off(' + str(self.inner) + ')'

# @if(flag)
class If(ParsingExpression):
    __slots__ = ['name']
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return  '@if(' + str(self.name) + ')'

## Meta

class Meta(ParsingExpression):
    __slots__ = ['name', 'inner', 'opt']
    def __init__(self, name, inner, opt = None):
        self.name = name
        self.inner = ParsingExpression.new(inner)
        self.opt = opt
    def __str__(self):
        arg = ', ' + repr(self.opt) if self.opt != None else ''
        return self.tag + '(' + str(self.inner) + arg + ')'

# Rule

#class Ref(ParsingExpression, ast.SourcePosition):

class Ref(ParsingExpression):
    __slots__ = ['peg', 'name', 'pos3']
    def __init__(self, name, peg = None):
        self.name = name
        self.peg = peg
        self.pos3 = None
    def __str__(self):
        return str(self.name)

    def uname(self):
        return self.name if self.name.find(':') > 0 else self.peg.namespace() + ':' + self.name

    def setpeg(self, peg):
        self.peg = peg
        if self.name[0].islower() and self.name in peg:  # inlining
            # print('@inline', self.name)
            return peg[self.name].inner
        return self

    def isNonTerminal(self):
        return self.name in self.peg

    def deref(self):
        return self.peg[self.name].inner

    def prop(self):
        return getattr(self.peg, self.name)

    def getmemo(self, prefix: str, default = None):
        if self.name in self.peg:
            rule = self.peg[self.name]
            if hasattr(rule, prefix):
                return getattr(rule,prefix)
            return None
        else:
            return default

    def setmemo(self, prefix, value):
        rule = self.peg[self.name]
        setattr(rule, prefix, value)

class Rule(Ref):
    __slots__ = ['peg', 'name', 'inner', 'pos3']
    def __init__(self, peg, name, inner):
        super().__init__(name, peg)
        self.inner = ParsingExpression.new(inner)
        self.checked = False

    def __str__(self):
        return self.name + ' = ' + str(self.inner)

    def deref(self):
        return self.inner


## Properties

def addmethod(*ctags):
    def _match(func):
        name = ctags[-1]
        for ctag in ctags[:-1]:
            setattr(ctag, name, func)
        return func
    return _match

def isAlwaysConsumed(pe: ParsingExpression):
    if not hasattr(Char, 'isAlwaysConsumed'):
        method = 'isAlwaysConsumed'
        @addmethod(Char, Any, Range, method)
        def consumed(pe): return True

        @addmethod(Many, Not, And, Empty, method)
        def consumed(pe): return False

        @addmethod(Many1, LinkAs, TreeAs, FoldAs, Detree, Meta, method)
        def unary(pe):
            return isAlwaysConsumed(pe.inner)

        @addmethod(Seq, method)
        def seq(pe):
            return isAlwaysConsumed(pe.left) or isAlwaysConsumed(pe.right)

        @addmethod(Ore, Alt, method)
        def ore(pe):
            return isAlwaysConsumed(pe.left) and isAlwaysConsumed(pe.right)

        @addmethod(State, method)
        def state(pe):
            if pe.func == '@exists': return False
            return isAlwaysConsumed(pe.inner)

        @addmethod(Ref, method)
        def memo(pe: Ref):
            memoed = pe.getmemo('nonnull', True)
            if memoed == None:
                pe.setmemo('nonnull', True)
                memoed = isAlwaysConsumed(pe.deref())
                pe.setmemo('nonnull', memoed)
            return memoed

    return pe.isAlwaysConsumed()

## TreeState

class T(Enum):
    Unit = 0
    Tree = 1
    Mut = 2
    Fold = 3

def treeState(pe):
    if not hasattr(Char, 'treeState'):
        method = 'treeState'
        @addmethod(Empty, Char, Any, Range, Not, Detree, method)
        def stateUnit(pe):
            return T.Unit

        @addmethod(TreeAs, method)
        def stateTree(pe):
            return T.Tree

        @addmethod(LinkAs, method)
        def stateMut(pe):
            return T.Mut

        @addmethod(FoldAs, method)
        def stateFold(pe):
            return T.Fold

        @addmethod(Seq, method)
        def stateSeq(pe):
            ts0 = treeState(pe.left)
            return ts0 if ts0 != T.Unit else treeState(pe.right)

        @addmethod(Ore, Alt, method)
        def stateAlt(pe):
            ts0 = treeState(pe.left)
            if ts0 != T.Unit: return ts0
            ts1 = treeState(pe.right)
            return T.Mut if ts1 == T.Tree else ts1

        @addmethod(Many, Many1, And, method)
        def stateMany(pe):
            ts0 = treeState(pe.inner)
            return T.Mut if ts0 == T.Tree else ts0

        @addmethod(State, method)
        def state(pe):
            if pe.func == '@exists' or pe.func == '@match': return T.Unit
            return treeState(pe.inner)


        @addmethod(Ref, method)
        def stateRef(pe: Ref):
            memoed = pe.getmemo('ts', T.Unit)
            if memoed == None:
                pe.setmemo('ts', T.Unit)
                memoed = treeState(pe.deref())
                pe.setmemo('ts', memoed)
            return memoed

    return pe.treeState()

def checkTree(pe, inside):
    if not hasattr(LinkAs, 'checkTree'):
        method = 'checkTree'

        @addmethod(Empty, Char, Any, Range, method)
        def term(pe, inside):
            return pe

        @addmethod(And, Not, Many, Many1, Rule, method)
        def unary(pe, inside):
            pe.inner = checkTree(pe.inner, inside)
            return pe

        @addmethod(Seq, Ore, Alt, method)
        def binary(pe, inside):
            pe.left = checkTree(pe.left, inside)
            pe.right = checkTree(pe.right, inside)
            return pe

        @addmethod(TreeAs, method)
        def tree(pe, inside):
            pe.inner = checkTree(pe.inner, TreeAs)
            return LinkAs('', pe) if inside == TreeAs else pe

        @addmethod(FoldAs, method)
        def tree(pe, inside):
            pe.inner = checkTree(pe.inner, TreeAs)
            return pe

        @addmethod(LinkAs, method)
        def fold(pe, inside):
            ts = treeState(pe.inner)
            if ts != T.Tree:
                pe.inner = TreeAs('', pe.inner)
            checkTree(pe.inner, LinkAs)
            return pe

        @addmethod(State, method)
        def state(pe, inside):
            pe.inner = checkTree(pe.inner, inside)
            return pe

        @addmethod(Ref, method)
        def ref(pe, inside):
            ts = treeState(pe)
            if ts == T.Tree and inside == TreeAs:
                return LinkAs('', pe)
            return pe

    return pe.checkTree(inside)

## Setup

def load_tpeg(g):
    # Preliminary
    __ = N % '__'
    _ = N % '_'
    EOS = N % 'EOS'

    g.Start = N%'__ Source EOF'
    g.EOF = ~ANY
    g.EOL = ParsingExpression.new('\n') | ParsingExpression.new('\r\n') | N%'EOF'
    g.COMMENT = '/*' & (~ParsingExpression.new('*/') & ANY)* 0 & '*/' | '//' & (~(N%'EOL') & ANY)* 0
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
    g.Identifier = TreeAs('Name', (Range('A-Z', 'a-z', '@_') & Range('A-Z', 'a-z', '0-9', '_.')*0
                                   | '"' & (ParsingExpression.new(r'\"') | ~Range('\\"\n') & ANY)* 0 & '"'))

    g.Example = TreeAs('Example', 'example' & N%'S _' & (name <= N%'Names') & (inner <= N%'Doc')) & EOS
    g.Names = TreeAs('', N%'$Identifier _' & (Range(',&') & N%'_ $Identifier _')*0)
    Doc1 = TreeAs("Doc", (~(N%'DELIM EOL') & ANY)* 0)
    Doc2 = TreeAs("Doc", (~Range('\r\n') & ANY)* 0)
    g.Doc = N%'DELIM' & (N%'S'*0) & N%'EOL' & Doc1 & N % 'DELIM' | Doc2
    g.DELIM = ParsingExpression.new("'''")

    #g.Expression = N%'Choice' & (left ^ (TreeAs('Alt', __ & '|' & _ & (right <= N%'Expression'))|0))
    g.Expression = N%'Choice' & (left ^ TreeAs('Alt', __ & '|' & _ & (right <= N%'Expression'))|0)
    g.Choice = N%'Sequence' & (left ^ TreeAs('Ore', __ & '/' & _ & (right <= N%'Choice'))|0)
    g.SS = N%'S _' & ~(N%'EOL') | (N%'_ EOL')+0 & N%'S _'
    g.Sequence = N%'Predicate' &  (left ^ TreeAs('Seq', (right <= N%'SS Sequence'))|0)

    g.Predicate = TreeAs('Not', '!' & (inner <= N%'Predicate')) \
                  | TreeAs('And', '&' & (inner <= N%'Predicate')) \
                  | TreeAs('Append', '$' & ( inner <= N%'Predicate')) \
                  | N%'Suffix'
    g.Suffix = N%'Term' & ((inner ^ TreeAs('Many', '*')) | (inner ^ TreeAs('Many1', '+')) | (inner ^ TreeAs('Option', '?')) | 0)

    g.Term = N%'Group/Char/Class/Any/Tree/Fold/BindFold/Bind/Func/Ref'
    g.Group = '(' & __ & N%'Expression/Empty' & __ & ')'

    g.Empty = TreeAs('Empty', EMPTY)
    g.Any = TreeAs('Any', '.')
    g.Char = "'" & TreeAs('Char', ('\\' & ANY | ~Range("'\n") & ANY)*0) & "'"
    g.Class = '[' & TreeAs('Class', ('\\' & ANY | ~Range("]") & ANY)*0) & ']'

    g.Tag = '{' & __ & (('#' & (name <= N%'Identifier')) | 0) & __
    g.ETag = ('#' & (name <= N%'Identifier') | 0) & __ & '}'

    g.Tree = TreeAs('TreeAs', N%'Tag' & (inner <= (N%'Expression __' | N%'Empty')) & N%'ETag' )
    g.Fold = '^' & _ & TreeAs('Fold', N%'Tag' & (inner <= (N%'Expression __' | N%'Empty')) & N%'ETag' )
    g.Bind = TreeAs('LinkAs', (name <= N%'Var' & ':') & _ & (inner <= N%'_ Term'))
    g.BindFold = TreeAs('Fold', (left <= N%'Var' & ':^') & _ & N%'Tag' & (inner <= (N%'Expression __' | N%'Empty')) & N%'ETag')
    g.Var = TreeAs('Name', Range('a-z', '$') & Range('A-Z', 'a-z', '0-9', '_')*0)

    g.Func = TreeAs('Func', N%'$Identifier' & '(' & __ & (N%'$Expression _' & ',' & __)* 0 & N%'$Expression __' & ')')
    g.Ref = TreeAs('Ref', N%'NAME')
    g.NAME = '"' & (ParsingExpression.new(r'\"') | ~Range('\\"\n') & ANY)* 0 & '"' | (~Range(' \t\r\n(,){};<>[|/*+?=^\'`#') & ANY)+0

    # Example
    #g.example("Ref", "abc")
    #g.example("Ref", '"abc"')
    g.example("COMMENT", "/*hoge*/hoge", "[# '/*hoge*/']")
    g.example("COMMENT", "//hoge\nhoge", "[# '//hoge']")

    g.example("Ref,Term,Expression", "a", "[#Ref 'a']")

    g.example("Char,Expression", "''", "[#Char '']")
    g.example("Char,Expression", "'a'", "[#Char 'a']")
    g.example("Char,Expression", "'ab'", "[#Char 'ab']")
    #g.example("Char,Expression", "'\\''", "[#Char \"'\"]")
    g.example("Char,Expression", "'\\\\a'", "[#Char '\\\\\\\\a']")
    g.example("Ref,Expression", "\"a\"", "[#Ref '\"a\"']")
    g.example("Class,Expression", "[a]", "[#Class 'a']")
    g.example("Func,Expression", "f(a)", "[#Func [#Name 'f'] [#Ref 'a']]")
    g.example("Func,Expression", "f(a,b)", "[#Func [#Name 'f'] [#Ref 'a'] [#Ref 'b']]")
    g.example("Func,Expression", "@symbol(a)", "[#Func [#Name '@symbol'] [#Ref 'a']]")
    g.example("Func,Expression", "@exists(a,'b')", "[#Func [#Name '@exists'] [#Ref 'a'] [#Char 'b']]")
    #g.example("Func,Expression", "$name(a)", "[#Func [#Name '$name'] [#Ref 'a']]")

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
    g.example("Expression", "{a #Int}", "[#TreeAs inner=[#Ref 'a'] name=[#Name 'Int']]")
    g.example("Expression", "{#Int a}", "[#TreeAs name=[#Name 'Int'] inner=[#Ref 'a']]")
    g.example("Expression", "^{a}", "[#Fold inner=[#Ref 'a']]")
    g.example("Expression", "^{ #Int a }", "[#Fold name=[#Name 'Int'] inner=[#Ref 'a']]")
    g.example("Expression", "name:^ {a}", "[#Fold left=[#Name 'name'] inner=[#Ref 'a']]")
    g.example("Expression", "name:^ {#Int a}", "[#Fold left=[#Name 'name'] name=[#Name 'Int'] inner=[#Ref 'a']]")
    g.example("Expression", "$a", "[#Append inner=[#Ref 'a']]")
    g.example("Expression", "$(a)", "[#Append inner=[#Ref 'a']]")
    g.example("Expression", "name: a", "[#LinkAs name=[#Name 'name'] inner=[#Ref 'a']]")
    g.example("Expression", "name: a a", "[#Seq left=[#LinkAs name=[#Name 'name'] inner=[#Ref 'a']] right=[#Ref 'a']]")
    #g.example("Expression", "name: a", "[#LinkAs name=[#Name 'name'] inner=[#Ref 'a']]")

    g.example("Expression", "a b", "[#Seq left=[#Ref 'a'] right=[#Ref 'b']]")
    g.example("Expression", "a b c", "[#Seq left=[#Ref 'a'] right=[#Seq left=[#Ref 'b'] right=[#Ref 'c']]]")
    g.example("Expression", "a/b / c", "[#Ore left=[#Ref 'a'] right=[#Ore left=[#Ref 'b'] right=[#Ref 'c']]]")
    g.example("Expression", "a|b | c", "[#Alt left=[#Ref 'a'] right=[#Alt left=[#Ref 'b'] right=[#Ref 'c']]]")
    g.example("Statement", "A=a", "[#Rule name=[#Name 'A'] inner=[#Ref 'a']]")

    g.example("Statement", '"A"=a', "[#Rule name=[#Name '\"A\"'] inner=[#Ref 'a']]")

    g.example("Statement", "example A,B abc \n", "[#Example name=[# [#Name 'A'] [#Name 'B']] inner=[#Doc 'abc ']]")
    g.example("Statement", "A = a\n  b", "[#Rule name=[#Name 'A'] inner=[#Seq left=[#Ref 'a'] right=[#Ref 'b']]]")
    g.example("Start", "A = a; B = b;;",
              "[#Source [#Rule name=[#Name 'A'] inner=[#Ref 'a']] [#Rule name=[#Name 'B'] inner=[#Ref 'b']]]")
    g.example("Start", "A = a\nB = b",
              "[#Source [#Rule name=[#Name 'A'] inner=[#Ref 'a']] [#Rule name=[#Name 'B'] inner=[#Ref 'b']]]")
    g.example("Start", "A = a //hoge\nB = b",
              "[#Source [#Rule name=[#Name 'A'] inner=[#Ref 'a']] [#Rule name=[#Name 'B'] inner=[#Ref 'b']]]")
    return g

# Expression loader

def setup_loader(Grammar, pgen):
    import pegpy.utils as u
    from pegpy.ast import ParseTreeConv
    class PEGConv(ParseTreeConv):
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
                    c, s = u.unquote(bytes(s, 'ascii'))
                    sb.append(c)
                return ParsingExpression.new(b''.join(sb))
            else:
                sb = []
                while len(s) > 0:
                    c, s = u.unquote(s)
                    sb.append(c)
                return ParsingExpression.new(''.join(sb))

        def Class(self, t):
            s = t.asString()
            sb = []
            while len(s) > 0:
                c, s = u.unquote(s)
                if s.startswith('-') and len(s) > 1:
                    c2, s = u.unquote(s[1:])
                    sb.append((c, c2))
                else:
                    sb.append(c)
            return Range(*sb)

        def Option(self, t):
            inner = self.conv(t['inner'])
            return Ore(inner, EMPTY)

        def TreeAs(self, t):
            name = t['name'].asString() if 'name' in t else ''
            inner = self.conv(t['inner'])
            return TreeAs(name, inner)

        def LinkAs(self, t):
            name = t['name'].asString() if 'name' in t else ''
            inner = self.conv(t['inner'])
            #print('@LinkAs', LinkAs(name, inner))
            return LinkAs(name, inner)

        def Append(self, t):
            name = ''
            tsub = t['inner']
            if tsub == 'Func':
                a = tsub.asArray()
                name = a[0].asString()
                inner = self.conv(a[1])
            else:
                inner = self.conv(tsub)
            #print('@Append', LinkAs(name, inner))
            return LinkAs(name, inner)

        def Fold(self, t):
            left = t['left'].asString() if 'left' in t else ''
            name = t['name'].asString() if 'name' in t else ''
            inner = self.conv(t['inner'])
            return FoldAs(left, name, inner)

        def Func(self, t):
            a = t.asArray()
            name = a[0].asString()
            if name == '@if' and len(a) > 1:
                return If(a[1].asString())
            elif name == '@on' and len(a) > 2:
                return On(a[1].asString(), self.conv(a[2]))
            elif name == '@off' and len(a) > 2:
                return Off(a[1].asString(), self.conv(a[2]))
            elif name == '@scope' and len(a) > 1:
                return State(name, self.conv(a[1]))
            elif name == '@symbol' and len(a) > 1:
                return State(name, self.conv(a[1]))
            elif name == '@match' and len(a) > 1:
                return State(name, self.conv(a[1]))
            elif name == '@exists' and len(a) > 1:
                return State(name, self.conv(a[1]))
            elif name == '@equals' and len(a) > 1:
                return State(name, self.conv(a[1]))
            elif name == '@contains' and len(a) > 1:
                return State(name, self.conv(a[1]))
            print('@TODO', name)
            return EMPTY

    def checkRef(pe, consumed: bool, name: str, visited: dict):
        if isinstance(pe, Seq):
            pe.left = checkRef(pe.left, consumed, name, visited)
            if not consumed:
                consumed = isAlwaysConsumed(pe.left)
            pe.right = checkRef(pe.right, consumed, name, visited)
            return pe
        if isinstance(pe, Ore) or isinstance(pe, Alt):
            pe.left = checkRef(pe.left, consumed, name, visited)
            pe.right = checkRef(pe.right, consumed, name, visited)
            return pe
        if hasattr(pe, 'inner'):
            pe.inner = checkRef(pe.inner, consumed, name, visited)
            return pe
        if isinstance(pe, Ref):
            if not consumed and pe.name == name:
                u.perror(pe.pos3, msg='Left Recursion')
                return pe
            if not pe.isNonTerminal():
                u.perror(pe.pos3, msg='Undefined Name')
                return Char(pe.name)
            if pe.name[0].islower(): # inlining
                return pe.deref()
            if not pe.name in visited:
                visited[pe.name] = True
                checkRef(pe.deref(), consumed, name, visited)
        return pe

    def checkRule(rule):
        rule.inner = checkRef(rule.inner, False, rule.name, {})

    PEGconv = PEGConv(Ore, Alt, Seq, And, Not, Many, Many1, TreeAs, FoldAs, LinkAs, Ref)
    pegparser = pgen(load_tpeg(Grammar('tpeg')))

    def load_grammar(g, path):
        f = u.find_path(path).open()
        data = f.read()
        f.close()
        t = pegparser(data, path)
        if t == 'err':
            u.perror(t.pos3())
        # load
        for stmt in t.asArray():
            if stmt == 'Rule':
                name = stmt['name'].asString()
                pexr = stmt['inner']
                pe = PEGconv.conv(pexr)
                g.add(name, pe)
            elif stmt == 'Example':
                pexr = stmt['inner']
                doc = stmt['inner'].asString()
                for n in stmt['name'].asArray():
                    g.example(n.asString(), doc)
        g.foreach(checkRule)
        g.map(lambda pe: checkTree(pe, None))

    Grammar.load = load_grammar

# setup_loader()
