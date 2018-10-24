
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
    def setpeg(self, peg):
        if hasattr(self, 'inner'):
            self.inner.setpeg(peg)
        if hasattr(self, 'right'):
            self.left.setpeg(peg)
            self.right.setpeg(peg)
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

'''def pe(x):
    if x == 0 : return EMPTY
    if isinstance(x, str):
        if len(x) == 0:
            return EMPTY
        return Char(x)
    return x
'''

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

## PEG Grammar

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

#class Ref(ParsingExpression, ast.SourcePosition):
class Ref(ParsingExpression):
    __slots__ = ['peg', 'name', 'pos']
    def __init__(self, name, peg = None):
        self.name = name
        self.peg = peg
        self.pos = None
    def __str__(self):
        return str(self.name)
    def uname(self):
        return self.name if self.name.find(':') > 0 else self.peg.namespace() + ':' + self.name

    def setpeg(self, peg):
        self.peg = peg
    def isNonTerminal(self):
        return self.peg.isDefined(self.name)
    def deref(self):
        return self.peg[self.name].inner

    def prop(self):
        return getattr(self.peg, self.name)
    def getmemo(self,prefix):
        return self.peg.getmemo(prefix+self.name)
    def setmemo(self,prefix,value):
        return self.peg.setmemo(prefix+self.name,value)


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
        return self.name + '{ ' + str(self.inner) + ' }'

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
        prefix = '^' if self.name == '' else self.left + ': ^'
        return prefix + self.name + '{ ' + str(self.inner) + ' }'

class Detree(ParsingExpression):
    __slots__ = ['inner']
    def __init__(self, inner):
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        return '@unit(' + str(self.inner) + ')'

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

    g.Example = TreeAs('Example', 'example' & N%'S _' & (name <= N%'Names') & (inner <= N%'Doc')) & EOS
    g.Names = TreeAs('', N%'$Identifier _' & (Range(',&') & N%'_ $Identifier _')*0)
    Doc1 = TreeAs("Doc", (~(N%'DELIM EOL') & ANY)* 0)
    Doc2 = TreeAs("Doc", (~Range('\r\n') & ANY)* 0)
    g.Doc = N%'DELIM' & (N%'S'*0) & N%'EOL' & Doc1 & N % 'DELIM' | Doc2
    g.DELIM = ParsingExpression.new("'''")

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
    g.NAME = '"' & (ParsingExpression.new(r'\"') | ~Range('\\"\n') & ANY)* 0 & '"' | (~Range(' \t\r\n(,){};<>[|/*+?=^\'`') & ANY)+0

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

