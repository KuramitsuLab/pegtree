'''
`if = if(%s) %s else %s
'''

#https://docs.python.jp/3/library/dis.html#python-bytecode-instructions

'''
assume x,y,z: int
assume x,y,z: double

origami
'''

class TypeSystem(object):
    __slots__ = ['nameMap']
    def __init__(self):
        self.nameMap = {}
        self.nameMap['any'] = AnyType(self)

    def typeName(self, name: str):
        if not name in self.nameMap:
            ty = SimpleType(self, name)
            self.nameMap[name] = ty
        return self.nameMap[name]

class Type(object):
    def __eq__(self, other):
        return id(self) == id(other)

class SimpleType(Type):
    __slots__ = ['name', 'ts']
    def __init__(self, ts: TypeSystem, name: str):
        self.ts = ts
        self.name = name
    def __str__(self):
        return self.name
    def accept(self, ty, subtype = True):
        return self.name == ty.name if isinstance(ty, SimpleType) else False

class AnyType(Type):
    def __init__(self, ts: TypeSystem):
        self.ts = ts
    def __str__(self):
        return 'any'
    def accept(self, ty, subtype = True):
        return True if subtype else self == ty

def matchTypes(ts, ts2):
    if len(ts) == len(ts2):
        for t, at in zip(ts, ts2):
            if not t.accept(at): return False
        return True
    return False

class FuncType(Type):
    __slots__ = ['types', 'ts']
    def __init__(self, ts: TypeSystem, types: tuple):
        self.types = types
        self.ts = ts
    def accept(self, ty):
        return isinstance(ty, FuncType) and matchTypes(ty.types, self.types)

class GenericType(Type):
    __slots__ = ['types', 'ts']
    def __init__(self, ts: TypeSystem, types: tuple):
        self.types = types
        self.ts = ts
    def accept(self, ty):
        if isinstance(ty, FuncType) and len(ty.types) == len(self.types):
            for t, at in zip(self.types, ty.types):
                if not t.accept(at): return False
            return True
        return False

class Rule(object):
    __slots__ = ['prev', 'types', 'fmt', 'req']
    def __init__(self, prev, types, fmt, req):
        self.prev = prev
        self.types = types
        self.fmt = fmt
        self.req = req
    def match(self, e):
        params = e.args()
        m = self
        while m is not None:
            types = m.types
            if types is None: return m.fmt
            if isinstance(types, tuple) and len(types) == len(params):
                return m.fmt
            m = m.prev
        return None

class SyntaxMapper(object):
    __slots__ = ['syntaxMap', 'funcMap', 'ts']
    def __init__(self):
        self.syntaxMap = {}
        self.funcMap = {}
        self.ts = TypeSystem()
        self.syntaxMap['TODO'] = 'TODO(%*)'

    def typeOf(self, t:str):
        if t.endswith("]"):
            types = t[0:-1].replace('[',',').split(',')
        else:
            return self.ts.typeName(t)

    def addSyntax(self, key, fmt):
        self.syntaxMap[key] = fmt

    def addFunc(self, key, types, fmt, req = None):
        rule = self.funcMap[key] if key in self.funcMap else None
        self.funcMap[key] = Rule(rule, types, fmt, req)

    def load(self, path):
        f = open(path, 'r')
        req = ()
        key = None
        fmt = None
        inLines = False
        for line in f.readlines():
            if line.startswith('#'):
                continue

            if inLines:
                if line.startswith("'''"):
                    fmt = fmt.strip()
                    inLines = False
                else:
                    fmt = fmt + line
                    continue
            else:
                loc = line.find(' =')
                if loc == -1:
                    if line.startswith("require"):
                        req = tuple(line[7:].strip().split(','))
                    continue

                fmt = line[loc+2:].strip()
                key = line[0: loc].strip()
                if fmt.endswith("'''"):
                    inLines = True
                    fmt = ""
                    continue

            loc = key.find('::')
            if loc > 0:
                types = self.loadType(key[loc+2:].strip())
                key = key[0: loc].strip()
                self.addFunc(key, types, fmt, req)
            else:
                self.addSyntax(key, fmt)
        f.close()

    def loadType(self, types):
        loc = types.find('->')
        if loc > 0:
            arg = types[:loc].strip()[1:-1].strip()
            ret = types[loc+2:].strip()
            return tuple(self.loadType2(arg) + self.loadType2(ret))

        return tuple(self.loadType2(types) + [self.ts.typeName('void')])

    def loadType2(self, types):
        loc = types.find('(')
        if loc == -1:
            return list(map(lambda str: self.ts.typeName(str.strip()), types.split(',')))
        else:
            tyList = []
            if loc != 0:
                tyList += list(map(lambda str: self.ts.typeName(str.strip()), types[:loc].strip(', ').split(',')))

            nested = 1
            i = loc + 1
            while i < len(types):
                if types[i] == '(':
                    nested += 1
                elif types[i] == ')':
                    nested -= 1
                if nested == 0:
                    break
                i += 1

            tyList += [tuple(self.loadType2(types[loc+1:i].strip()))]#TODO Tuple

            if i + 1 != len(types):
                tyList += self.loadType2(types[i+1:].strip(', '))

            return tyList

        #TODO: List, Data, Dict, Option

    def emit(self, e, ss):
        tag = e.syntaxKey()
        if hasattr(self, tag):
            getattr(self, tag)(e, ss)
            return
        fn = e.funcKey()
        if fn in self.funcMap:
            rule = self.funcMap[fn]
            fmt = rule.match(e)
            if fmt is not None:
                ss.pushFMT(self, fmt, e.args())
                return
        fmt = self.syntaxMap[tag] if tag in self.syntaxMap else self.syntaxMap['TODO']
        ss.pushFMT(self, fmt, e.args())

class SourceSection(object):
    __slots__ = ['sb', 'indent', 'tab', 'lf']
    def __init__(self, indent = 0, tab = '   ', lf = '\n'):
        self.sb = []
        self.indent = indent
        self.tab = tab
        self.lf = lf

    def __str__(self):
        return ''.join(self.sb)

    def incIndent(self):
        self.indent += 1

    def decIndent(self):
        self.indent -= 1

    def pushLF(self):
        if len(self.lf) > 0: self.sb.append(self.lf)

    def pushTAB(self):
        if self.indent > 0 and len(self.tab) > 0:
            self.sb.append(self.tab * self.indent)

    def pushSTR(self, s):
        if len(s) > 0: self.sb.append(s)

    def pushLINE(self, s):
        self.pushSTR(s)
        self.pushLF()

    def pushINDENT(self, s=''):
        self.pushTAB()
        self.pushSTR(s)

    def pushEXPR(self, syn: SyntaxMapper, e):
        if isinstance(e, SyntaxTree):
            syn.emit(e, self)
        else:
            self.pushSTR(str(e))

    def pushFMT(self, syn: SyntaxMapper, fmt: str, args: list):
        index = 0
        start = 0
        i = 0
        while i < len(fmt):
            c = fmt[i]
            i += 1
            if c == '\t' :
                self.pushSTR(fmt[start: i - 1])
                start = i
                self.pushTAB()
                continue
            if c == '\f' :
                self.pushSTR(fmt[start: i - 1])
                start = i
                self.incIndent()
                continue
            if c == '\b' :
                self.pushSTR(fmt[start: i - 1])
                start = i
                self.incIndent()
                continue
            if c == '\n':
                self.pushSTR(fmt[start: i - 1])
                start = i
                self.pushLF()
                continue
            if c == '%':
                c = fmt[i] if i < len(fmt) else '%'
                i += 1
                if c == '%':
                    self.pushSTR(fmt[start: i - 1])
                    start = i
                    continue
                self.pushSTR(fmt[start: i - 2])
                start = i
                if '0' <= c and c <= '9':
                    index = int(c)
                    self.pushEXPR(syn, args[index])
                    index +=1
                    continue
                if c == 's':
                    self.pushEXPR(syn, args[index])
                    index += 1
                    continue
                if c == '*' or c == ',' or c == ';':
                    cnt = 0
                    delim = c.replace('*', ' ')
                    for a in args[index:]:
                        if cnt > 0 : self.pushSTR(delim)
                        self.pushEXPR(syn, a)
                        cnt += 1
                    continue
                if c == '+':
                    cnt = 0
                    for a in args[index:]:
                        if cnt > 0:
                            self.pushLF()
                            self.pushINDENT()
                        self.pushEXPR(syn, a)
                        cnt += 1
                    continue
        #end while
        self.pushSTR(fmt[start:])

### Envrionment

class Env(object):
    def __init__(self, parent = None):
        self.parent = parent
        self.vars = {}
    def __getitem__(self, name):
        if name in self.vars: return self.vars[name]
        return self.parent[name] if self.parent is not None else None
    def pop(self):
        return self.parent


### SyntaxTree

class SyntaxTree(object):
    def syntaxKey(self):
        return self.__class__.__name__
    def funcKey(self):
        return self.syntaxKey().lower()
    def args(self):
        return ()

class Expression(SyntaxTree):
    def type(self): return None
    def exprs(self): return None

class Val(Expression):
    __slots__ = ['value', 'ty']
    def __init__(self, value):
        self.value = value
        self.ty = None
    def args(self):
        return tuple([self.value])
    def eval(self, env):
        return self.value

class Var(Expression):
    __slots__ = ['name', 'ty']
    def __init__(self, name):
        self.name = name
        self.ty = None
    def funcKey(self):
        return self.name
    def args(self):
        return tuple([self.name])
    def eval(self, env):
        return env[self.name]

class FuncCall(Expression):
    __slots__ = ['exprs', 'ty']
    def __init__(self, fname, *args):
        self.exprs = tuple([fname] + args)
    def funcKey(self):
        return self.exprs[0]
    def args(self):
        return self.exprs

class Infix(Expression):
    __slots__ = ['exprs', 'ty']
    def __init__(self, left, op, right):
        self.exprs = (op, left, right)
    def funcKey(self):
        return self.exprs[0]
    def args(self):
        return self.exprs
    def eval(self, env):
        fs = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x // y,
            '%': lambda x, y: x % y,
        }
        return fs[self.exprs[0]](self.exprs[1].eval(env),self.exprs[2].eval(env))


'''
require math.h
+ :: any <- any, any = %1 + %2
'''

sm = SyntaxMapper()
sm.addSyntax('IfExpr', '%2 if %1 else %3')
sm.addSyntax('Val', '%0')
any = sm.typeOf('any')
sm.addFunc('+', (any, any, any), '%1 + %2')

ss = SourceSection()
e = Infix(Val(1), '+', Val(123))
sm.emit(e, ss)
print('SS', str(ss))
