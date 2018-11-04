
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
def inUnary(e):
    return (isinstance(e, Ore) and e.right != EMPTY) \
           or isinstance(e, Seq) or isinstance(e, Alt) \
           or isinstance(e, LinkAs) or isinstance(e, FoldAs)

def quote_string(e: str, esc ="'"):
    sb = []
    for c in e:
        if c == '\n' : sb.append(r'\n')
        elif c == '\t' : sb.append(r'\t')
        elif c == '\\' : sb.append(r'\\')
        elif c == '\r' : sb.append(r'\r')
        elif c in esc : sb.append('\\' + str(c))
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
        return "'" + quote_string(self.a) + "'"

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
        l = tuple(map(lambda x: quote_string(x[0], ']') + '-' + quote_string(x[1], ']'), self.ranges))
        return "[" + ''.join(l) + quote_string(self.chars, ']') + "]"

class Any(ParsingExpression):
    def __str__(self):
        return '.'
ANY = Any()

#class Ref(ParsingExpression, ast.SourcePosition):
class Ref(ParsingExpression):
    __slots__ = ['peg', 'name', 'pos3']
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

# @scope(e)
class Scope(ParsingExpression):
    __slots__ = ['inner']
    def __init__(self, inner):
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        return  '@scope(' + str(self.inner) + ')'

# @symbol(A)
class Symbol(ParsingExpression):
    __slots__ = ['name', 'inner']
    def __init__(self, name, inner):
        self.name = str(inner) if name is None else name
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        return  '@symbol(' + str(self.inner) + ')'

# @match(A)
class Match(ParsingExpression):
    __slots__ = ['name', 'inner']
    def __init__(self, name, inner):
        self.name = str(inner) if name is None else name
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        return  '@match(' + str(self.inner) + ')'

# @exists(A)
class Exists(ParsingExpression):
    __slots__ = ['name', 'inner']
    def __init__(self, name, inner):
        self.name = str(inner) if name is None else name
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        return  '@exists(' + str(self.inner) + ')'

# @equals(A)
class Equals(ParsingExpression):
    __slots__ = ['name', 'inner']
    def __init__(self, name, inner):
        self.name = str(inner) if name is None else name
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        return  '@contains(' + str(self.inner) + ')'

# @contains(A)
class Contains(ParsingExpression):
    __slots__ = ['name', 'inner']
    def __init__(self, name, inner):
        self.name = str(inner) if name is None else name
        self.inner = ParsingExpression.new(inner)
    def __str__(self):
        return  '@contains(' + str(self.inner) + ')'

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

    g.Func = TreeAs('Func', N%'$Identifier' & '(' & (N%'$Expression _' & ',' & __)* 0 & N%'$Expression _' & ')')
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

def setup_loader(Grammar, pc):
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
                return Scope(self.conv(a[1]))
            elif name == '@symbol' and len(a) > 1:
                return Symbol(None, self.conv(a[1]))
            elif name == '@match' and len(a) > 1:
                return Match(None, self.conv(a[1]))
            elif name == '@exists' and len(a) > 1:
                return Exists(None, self.conv(a[1]))
            elif name == '@equals' and len(a) > 1:
                return Equals(None, self.conv(a[1]))
            elif name == '@contains' and len(a) > 1:
                return Equals(None, self.conv(a[1]))
            print('@TODO', name)
            return EMPTY

    PEGconv = PEGConv(Ore, Alt, Seq, And, Not, Many, Many1, TreeAs, FoldAs, LinkAs, Ref)
    pegparser = pc(load_tpeg(Grammar('tpeg')))

    def load_grammar(g, path):
        f = open(path)
        data = f.read()
        f.close()
        t = pegparser(data, path)
        if t == 'err':
            er = t.getpos()
            print('SyntaxError ({}:{}:{}+{})'.format(er[0],er[2],er[3],er[1]), '\n', er[4], '\n', er[5])
        # load
        for stmt in t.asArray():
            if stmt == 'Rule':
                name = stmt['name'].asString()
                pexr = stmt['inner']
                pe = PEGconv.conv(pexr)
                #print('@load', name, '\n\t', pexr, '\n\t', pe)
                g.add(name, pe)
            elif stmt == 'Example':
                pexr = stmt['inner']
                doc = stmt['inner'].asString()
                for n in stmt['name'].asArray():
                    g.example(n.asString(), doc)

    Grammar.load = load_grammar

# setup_loader()
