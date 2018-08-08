from pegpy.peg import *

def math(peg = None):
    '''
    Expression = Product left ^ Infix{ name => { [+\-] } right => Product }
    Product = Value left ^ Infix{ name => { [*%] } right => Value }
    Value = Int / '(' Expression ')'
    Int = Int{ [0-9]+ }
    '''
    if peg == None: peg = PEG('math')
    left = LinkAs('left')
    right = LinkAs('right')
    op = LinkAs('name')
    peg.Expression = N % 'Product' & (left ^ TreeAs('Infix', (op <= N % 'AddSub') & (right <= N % 'Product'))) * 0
    peg.Product = N % 'Value' & (left ^ TreeAs('Infix', (op <= N % 'MulDiv') & (right <= N % 'Value')) * 0)
    peg.Value = N % 'Int' | '(' & N % 'Expression' & ')'
    peg.Int = TreeAs('Int', Range('0-9')+ 0)
    peg.AddSub = TreeAs('', Range('+-'))
    peg.MulDiv = TreeAs('', Range('*/%'))
    peg.example('Expression,Int', '123', "[#Int '123']")
    peg.example('Expression', '1+2*3')
    return peg


def peg(g = None):
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

    g.Name = TreeAs('Name', N%'NAME')
    g.NAME = '"' & (pe(r'\"') | ~Range('\\"\n') & ANY)* 0 & '"' | (~Range(' \t\r\n(,){};<>[|/*+?=^\'`') & ANY)+0

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
    g.Suffix = N%'Term' & ((inner ^ TreeAs('Many', '*')) | (inner ^ TreeAs('OneMore', '+')) | (inner ^ TreeAs('Option', '?')) | 0)

    g.Term = N%'Group/Char/Class/Any/Tree/Fold/BindFold/Bind/Func/Ref'
    g.Group = '(' & __ & N%'Expression/Empty' & __ & ')'

    g.Empty = TreeAs('Empty', EMPTY)
    g.Any = TreeAs('Any', '.')
    g.Char = "'" & TreeAs('Char', (r'\\' & ANY | ~Range("'\n") & ANY)*0) & "'"
    g.Class = '[' & TreeAs('Class', (r'\\' & ANY | ~Range("]") & ANY)*0) & ']'
    g.Tree = TreeAs('Tree', N%'Tag __' & (inner <= (N%'Expression __' | N%'Empty')) & '}' )
    g.Fold = '^' & _ & TreeAs('Fold', N%'Tag __' & (inner <= (N%'Expression __' | N%'Empty')) & '}' )
    g.Tag = ((name <= N%'Identifier')|0) & '{'
    g.Identifier = TreeAs('Name', Range('A-Z', 'a-z', '@') & Range('A-Z', 'a-z', '0-9', '_.')*0)

    g.Bind = TreeAs('Bind', (name <= N%'Var _') & '=>' & (inner <= N%'_ Expression'))
    g.BindFold = TreeAs('Fold', (left <= N%'Var _') & '^' & _ & N%'Tag __' & (inner <= (N%'Expression __' | N%'Empty')) & '}')
    g.Var = TreeAs('Name', Range('a-z', '$') & Range('A-Z', 'a-z', '0-9', '_')*0)

    g.Func = TreeAs('Func', N%'$Identifier' & '(' & (N%'$Expression _' & ',' & __)* 0 & N%'$Expression _' & ')')
    g.Ref = N%'Name'

    # Example
    g.example("Name", "abc")
    g.example("Name", '"abc"')
    g.example("COMMENT", "/*hoge*/hoge", "[# '/*hoge*/']")
    g.example("COMMENT", "//hoge\nhoge", "[# '//hoge']")

    g.example("Ref,Term,Expression", "a", "[#Name 'a']")

    g.example("Char,Expression", "''", "[#Char '']")
    g.example("Char,Expression", "'a'", "[#Char 'a']")
    g.example("Name,Expression", "\"a\"", "[#Name '\"a\"']")
    g.example("Class,Expression", "[a]", "[#Class 'a']")
    g.example("Func", "f(a)", "[#Func [#Name 'f'] [#Name 'a']]")
    g.example("Func", "f(a,b)", "[#Func [#Name 'f'] [#Name 'a'] [#Name 'b']]")
    g.example("Predicate,Expression", "&a", "[#And inner=[#Name 'a']]")
    g.example("Predicate,Expression", "!a", "[#Not inner=[#Name 'a']]")
    g.example("Suffix,Expression", "a?", "[#Option inner=[#Name 'a']]")
    g.example("Suffix,Expression", "a*", "[#Many inner=[#Name 'a']]")
    g.example("Suffix,Expression", "a+", "[#OneMore inner=[#Name 'a']]")
    g.example("Expression", "{}", "[#Tree inner=[#Empty '']]")
    g.example("Expression", "{ a }", "[#Tree inner=[#Name 'a']]")
    g.example("Expression", "{ }", "[#Tree inner=[#Empty '']]")
    g.example("Expression", "()", "[#Empty '']")
    g.example("Expression", "&'a'", "[#And inner=[#Char 'a']]")

    g.example("Expression", "{a}", "[#Tree inner=[#Name 'a']]")
    g.example("Expression", "Int{a}", "[#Tree name=[#Name 'Int'] inner=[#Name 'a']]")
    g.example("Expression", "^{a}", "[#Fold inner=[#Name 'a']]")
    g.example("Expression", "^Int{a}", "[#Fold name=[#Name 'Int'] inner=[#Name 'a']]")
    g.example("Expression", "name^{a}", "[#Fold left=[#Name 'name'] inner=[#Name 'a']]")
    g.example("Expression", "name^Int{a}", "[#Fold left=[#Name 'name'] name=[#Name 'Int'] inner=[#Name 'a']]")
    g.example("Expression", "$a", "[#Append inner=[#Name 'a']]")
    g.example("Expression", "name=>a", "[#Bind name=[#Name 'name'] inner=[#Name 'a']]")
    g.example("Expression", "name => a", "[#Bind name=[#Name 'name'] inner=[#Name 'a']]")

    g.example("Expression", "a a", "[#Seq left=[#Name 'a'] right=[#Name 'a']]")
    g.example("Expression", "a b c", "[#Seq left=[#Name 'a'] right=[#Seq left=[#Name 'b'] right=[#Name 'c']]]")
    g.example("Expression", "a/b / c", "[#Ore left=[#Name 'a'] right=[#Ore left=[#Name 'b'] right=[#Name 'c']]]")
    g.example("Expression", "a|b | c", "[#Alt left=[#Name 'a'] right=[#Alt left=[#Name 'b'] right=[#Name 'c']]]")
    g.example("Statement", "A=a", "[#Rule name=[#Name 'A'] inner=[#Name 'a']]")
    g.example("Statement", "example A,B abc \n", "[#Example name=[# [#Name 'A'] [#Name 'B']] inner=[#Doc 'abc ']]")
    g.example("Statement", "A = a\n  b", "[#Rule name=[#Name 'A'] inner=[#Seq left=[#Name 'a'] right=[#Name 'b']]]")
    g.example("Start", "A = a; B = b;;",
              "[#Source [#Rule name=[#Name 'A'] inner=[#Name 'a']] [#Rule name=[#Name 'B'] inner=[#Name 'b']]]")
    g.example("Start", "A = a\nB = b",
              "[#Source [#Rule name=[#Name 'A'] inner=[#Name 'a']] [#Rule name=[#Name 'B'] inner=[#Name 'b']]]")
    g.example("Start", "A = a //hoge\nB = b",
              "[#Source [#Rule name=[#Name 'A'] inner=[#Name 'a']] [#Rule name=[#Name 'B'] inner=[#Name 'b']]]")

    return g
