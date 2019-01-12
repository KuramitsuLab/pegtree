from functools import lru_cache
from pegpy.peg import Grammar, nez
from pegpy.origami.sexpr import SExpr, ListExpr, AtomExpr, TypeExpr
import pegpy.utils as u
from pegpy.origami.desugar import desugar

g = Grammar('konoha6')
g.load('konoha6.tpeg')
origami_parser = nez(g['OrigamiFile'])

class Def(object):
    __slots__ = ['ty', 'libs', 'code', 'delim']

    def __init__(self, ty, libs, code, delim = None):
        self.libs = libs
        self.ty = ty
        self.code = code
        self.delim = delim

    def __str__(self):
        return str(self.code)

    def __repr__(self):
        return repr(self.code)

    def getcode(self):
        return None if self.code is None else compile_code(self.code, self.delim)

    @classmethod
    def getkeys(cls, stmt, ty):
        iname = stmt['name'].asString()
        name = iname.split('@')[0] if '@' in iname else iname
        keys = []
        if ty is not None and ty.isFuncType():
            iname = name + '@' + str(len(ty))
            keys.append(iname + '@' + str(ty[0]))
        keys.append(iname)
        if iname != name:
            keys.append(name)
        return keys

class Env(object):
    __slots__ = ['parent', 'nameMap']

    def __init__(self, parent = None):
        self.parent = parent
        self.nameMap = {}

    def newLocal(self):
        return Env(self)

    def __contains__(self, item):
        if item in self.nameMap:
            return True
        if self.parent is not None:
            return item in self.parent
        return False

    def __getitem__(self, item):
        if item in self.nameMap:
            return self.nameMap[item]
        if self.parent is not None:
            return self.parent[item]
        return None

    def __setitem__(self, item, value):
        self.nameMap[item] = value

    def load(self, path, out):
        path = u.find_path(path, 'origami')
        f = path.open()
        data = f.read()
        f.close()
        t = origami_parser(data, path)
        if t == 'err':
            out.verbose(u.serror(t.pos3()))
            return
        libs = None
        for _, stmt in t:
            #print(stmt)
            if stmt == 'CodeMap':
                ty = stmt.get('type', None, lambda t: SExpr.of(t))
                keys = Def.getkeys(stmt, ty)
                code = u.unquote_string(stmt['expr'].asString()) if 'expr' in stmt else None
                delim = u.unquote_string(stmt['delim'].asString()) if 'delim' in stmt else None
                d = Def(ty, libs, code, delim)
                self.add(keys, d)
            elif stmt == 'Include':
                file = stmt['file'].asString()
                file = u.find_importPath(path.absolute(), file)
                # out.verbose('loading...', file)
                self.load(file, out)
        #print('DEBUG', self.nameMap)

    def add(self, keys, defined):
        if isinstance(keys, str):
            self[keys] = defined
        else:
            self[keys[0]] = defined
            for key in keys[1:]:
                if not key in self:
                    self[key] = defined

    def addName(self, name, ty):
        self[name] = Def(ty, None, None)

    def inferName(self, name):
        if name[-1] in "0123456789'_": name = name[:-1]
        if name in self:
            ty = self[name].ty
            if ty is not None: return ty
        if len(name) >= 2:
            return self.inferName(name[1:])
        return None

## Typing

class Typer(object):
    __slot__ = ['methodMap']
    def __init__(self):
        self.methodMap = {}

    def lookupMethod(self, key):
        if key in self.methodMap:
            return self.methodMap[key]
        if key.startswith('#'):
            name = key.replace('#', '')
            if hasattr(self, name):
                self.methodMap[key] = getattr(self, name)
                return self.methodMap[key]
        if key.endswith('Expr'):
            name = key.replace('Expr', '')
            if hasattr(self, name):
                self.methodMap[key] = getattr(self, name)
                return self.methodMap[key]
        return self.undefined

    def undefined(self, env, expr, ty):
        if isinstance(expr, AtomExpr):
            return self.Var(env, expr, ty)
        else:
            return self.Apply(env, expr, ty)

    VoidType = SExpr.ofType('Void')
    BoolType = SExpr.ofType('Bool')

    def asType(self, env, expr, ty):
        if expr.isUntyped():
            desugar(env, expr)
            expr = self.tryType(env, expr, ty)
        if ty is None or expr.ty is None or expr.ty is ty:
            return expr
        for key in SExpr.makekeys(str(ty), 1, expr.ty):
            defined = env[key]
            if defined is None: continue
            expr = SExpr.new('#Cast', expr, ty)
            expr.setCode(defined.getcode())
            return expr.setType(ty)
        return expr.err('Type Error: Expected={} Given={}'.format(ty, expr.ty))

    def tryType(self, env, expr, ty):
        method = self.lookupMethod(expr.asSymbol())
        return method(env, expr, ty)

    def typeAt(self, env, expr, n, ty):
        expr.data[n] = self.asType(env, expr.data[n],ty)

    def CastExpr(self, env, expr, ty):
        self.typeAt(env, expr, 1, None)
        ty = expr[2]
        for key in SExpr.makekeys(str(ty), 1, expr[1].ty):
            defined = env[key]
            if defined is None: continue
            expr.setCode(defined.getcode())
            return expr.setType(ty)
        if expr[1].ty is not None:
            expr = expr.err('Undefined Cast {}=>{}'.format(expr[1].ty, ty), expr[2].getpos())
        return expr.setType(ty)

    def Scope(self, env, expr, ty):
        lenv = env.newLocal()
        if len(expr) == 1: return expr.setType(ty)
        for n in range(1, len(expr)-1):
            self.typeAt(lenv, expr, n, Typer.VoidType)
        self.typeAt(lenv, expr, -1, ty)
        return expr.setType(expr[-1].ty)

    def Block(self, env, expr, ty):
        if len(expr) == 1: return expr.setType(ty)
        for n in range(1, len(expr)-1):
            self.typeAt(env, expr, n, Typer.VoidType)
        self.typeAt(env, expr, -1, ty)
        return expr.setType(expr[-1].ty)

    def AssumeDecl(self, env, expr, ty):
        ty = expr[-1]
        for name in expr[1:-1]:
            env.addName(str(name), ty)
        return expr.done()

    def FuncDecl(self, env, expr, ty):
        lenv = env.newLocal()
        for n in range(2, len(expr)):
            self.typeAt(lenv, expr, n, None)
        if isinstance(expr[-2], TypeExpr):
            expr[1].ty = expr[-2]
            del expr.data[-2]
        else:
            expr[1].ty = expr[-1].ty
        types = list(map(lambda e: e.ty, expr[2:]))
        if None not in types:
            ty = SExpr.ofFuncType(*types)
            keys = SExpr.makekeys(str(expr[1]), len(types)-1, ty[0])
            env.add(keys, Def(ty, None, None))
        return expr.setType('Void')

    def FuncMatchDecl(self, env, expr, ty):
        lenv = env.newLocal()
        for n in range(2, len(expr)):
            self.typeAt(lenv, expr, n, None)
        if isinstance(expr[-2], TypeExpr):
            expr[1].ty = expr[-2]
            del expr.data[-2]
        else:
            expr[1].ty = expr[-1].ty
        types = list(map(lambda e: e.ty, expr[2:]))
        if None not in types:
            ty = SExpr.ofFuncType(*types)
            keys = SExpr.makekeys(str(expr[1]), len(types)-1, ty[0])
            env.add(keys, Def(ty, None, None))
        return expr.setType('Void')

    def FuncMatch(self, env, expr, ty):
        self.typeAt(env, expr, 1, None)
        for n in range(2, len(expr)):
            self.typeAt(env, expr, n, expr[1].ty)
        return expr.setType(expr[1].ty)

    def FuncCase(self, env, expr, ty):
        self.typeAt(env, expr, 1, ty)
        if len(expr) == 3:
            self.typeAt(env, expr, 2, Typer.BoolType)
        return expr.setType(expr[1].ty)

    def Param(self, env, expr, ty):
        name = str(expr[1])
        if len(expr) == 2:
            ty = env.inferName(name)
        else:
            ty = expr[2]
        env[name] = Def(ty, None, name)
        if ty is None:
            return expr.err('Untyped ' + name)
        expr[1].setType(ty)
        expr.data.append(ty)
        return expr.setType('Void')

    def Return(self, env, expr, ty):
        if len(expr) == 2:
            self.typeAt(env, expr, 1, None)
            return expr.setType(expr[1].ty)
        else:
            return expr.setType('Void')

    def FuncExpr(self, env, expr, ty):
        lenv = env.newLocal()
        for n in range(1, len(expr)):
            self.typeAt(lenv, expr, n, None)
        types = list(map(lambda e: e.ty, expr[1:]))
        if None not in types:
            ty = SExpr.ofFuncType(*types)
            return expr.setType(ty)
        return expr

    def LetDecl(self, env, expr, ty):
        if len(expr) == 3:
            self.typeAt(env, expr, 2, None)
            ty = expr[2].ty
        else:
            ty = expr[2]
            self.typeAt(env, expr, 3, ty)
        if ty is not None:
            name = str(expr[1])
            env[name] = Def(ty, None, name)
        return expr.setType('Void')

    def VarDecl(self, env, expr, ty):
        if len(expr) == 3:
            self.typeAt(env, expr, 2, None)
            ty = expr[2].ty
        else:
            ty = expr[2]
            self.typeAt(env, expr, 3, ty)
        if ty is not None:
            name = str(expr[1])
            env[name] = Def(ty, None, name)
        return expr.setType('Void')

    def Assign(self, env, expr, ty):
        left = expr[1]
        if left == '#GetExpr':
            setter = ListExpr([left[2], left[1], expr[2]])
            setter = self.Apply(env, setter, ty)
            if not setter.isUncode(): return setter
        elif left == '#IndexExpr':
            pass
        self.typeAt(env, expr, 1, None)
        ty = expr[2].ty
        self.typeAt(env, expr, 2, ty)
        return expr.setType('Void')

    def Var(self, env, expr, ty):
        key = expr.asSymbol()
        defined = env[key]
        if defined is not None:
            expr.setCode(defined.getcode())
            return expr.setType(defined.ty)
        return expr.err('Undefined Name: ' + key)

    def IfExpr(self, env, expr, ty):
        self.typeAt(env, expr, 1, Typer.BoolType)
        if len(expr) == 4:
            self.typeAt(env, expr, 2, ty)
            self.typeAt(env, expr, 3, expr[2].ty)
            return expr.setType(expr[3].ty)
        else:
            self.typeAt(env, expr, 2, Typer.VoidType)
            return expr.setType(Typer.VoidType)

    def Group(self, env, expr, ty):
        self.typeAt(env, expr, 1, ty)
        return expr.setType(expr[1].ty)

    def Unary(self, env, expr, ty):
        op = ListExpr([expr[1], expr[2]])
        op = self.Apply(env, op, ty)
        if op.isUncode():
            expr.ty = op.ty
            expr[1] = op[0]
            expr[2] = op[1]
            return expr
        return op

    def GetExpr(self, env, expr, ty):
        getter = ListExpr([expr[2], expr[1]])
        getter = self.Apply(env, getter, ty)
        if getter.isUncode():
            expr.ty = getter.ty
            expr[2] = getter[0]
            expr[1] = getter[1]
            if expr[1].ty is not None and expr[1].ty.isDataType():
                name = expr[2].asSymbol()
                dataty = expr[1].ty
                if not name in dataty:
                    return expr.err('undefined name: {} in {}'.format(name, dataty))
                return expr.setType(env.inferName(name))
            return expr
        return getter

    def Infix(self, env, expr, ty):
        binary = ListExpr([expr[2], expr[1], expr[3]])
        binary = self.Apply(env, binary, ty)
        if binary.isUncode():
            expr.ty = binary.ty
            expr[2] = binary[0]
            expr[1] = binary[1]
            expr[3] = binary[2]
            return expr
        return binary

    def ApplyExpr(self, env, expr, ty):
        app = ListExpr(expr.data[1:])
        app = self.Apply(env, app, ty)
        if app.isUncode():
            expr.ty = app.ty
            for i in range(0, len(app)):
                expr.data[i+1] = app[i]
            return expr
        return app

    def MethodExpr(self, env, expr, ty):
        app = ListExpr(expr.data[1:])
        print('@befor', app)
        app[0], app[1] = app[1], app[0]  # swap callee, funcname
        print('@after', app)
        app = self.Apply(env, app, ty)
        if app.isUncode():
            expr.ty = app.ty
            print('@befor', app)
            app[0], app[1] = app[1], app[0] # swap callee, funcname
            print('@after', app)
            for i in range(0, len(app)):
                expr.data[i+1] = app[i]
            return expr
        return app

    def Apply(self, env, expr, ty):
        for n in range(1, len(expr)):
            self.typeAt(env, expr, n, None)
        #print('@keys', expr.keys())
        for key in expr.keys():
            defined = env[key]
            #print(key, defined)
            if defined is None: continue
            expr.setCode(defined.getcode())
            if expr.isUntyped() and defined.ty is not None:
                expr.setType(defined.ty.ret())
                for n in range(1, len(expr)):
                    self.typeAt(env, expr, n, defined.ty[n-1])
            if not expr.isUntyped() and not expr.isUncode():
                break
        return expr

    def TupleExpr(self, env, expr, ty):
        if len(expr) == 2:
            expr.data[0].data = '#Group'
            return self.Group(env, expr, ty)
        for n in range(1, len(expr)):
            self.typeAt(env, expr, n, None)
        types = list(map(lambda e: e.ty, expr[1:]))
        if None not in types:
            ty = SExpr.ofParamType(['Tuple', *types])
            return expr.setType(ty)
        return expr

    def TrueExpr(self, env, expr, ty):
        return expr.setType('Bool')

    def FalseExpr(self, env, expr, ty):
        return expr.setType('Bool')

    def Vint(self, env, expr, ty):
        return expr.setType('Int')

    def Vfloat(self, env, expr, ty):
        return expr.setType('Float')

    def VString(self, env, expr, ty):
        return expr.setType('String')

    def VChar(self, env, expr, ty):
        return expr.setType('Char')

#keyList = ['{}', '#{}', '{}Expr', '#{}Expr']

class SourceSection(object):

    __slots__ = ['sb', 'indent', 'tab', 'lf', 'out']

    def __init__(self, out, indent = 0, tab = '   ', lf = '\n'):
        self.sb = []
        self.indent = indent
        self.tab = tab
        self.lf = lf
        self.out = out

    def perror(self, pos3, msg = 'Syntax Error'):
        self.out.perror(pos3, msg)

    def __repr__(self):
        return ''.join(self.sb)

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

    def pushEXPR(self, env, e: SExpr):
        if not hasattr(e, 'code'):
            self.pushSTR(str(e))
            return
        code = e.code
        if code is None:
            keys = e.keys()
            for key in keys:
                code = env[key].getcode() if key in env else None
                if code is not None:
                    break
        if code is None:
            e.emit(env, self)
        else:
            self.exec(env, e, code)

    def exec(self, env, e, cmds):
        for f, x in cmds:
            f(env, e, x, self)

codekeys = {
    '\t': 'indent', '\f': 'indent++', '\b': 'indent--', '\n': 'newline'
}

esckeys = '*0123456789%'

def STR(env, e, s, ss):
    ss.pushSTR(s)

def pINDENT(env, e, s, ss): ss.pushINDENT()
def pINC(env, e, s, ss): ss.incIndent()
def pDEC(env, e, s, ss): ss.decIndent()
def pLF(env, e, s, ss): ss.pushLF()

commands = {
    'indent': pINDENT,
    'indent++': pINC,
    'indent--': pDEC,
    'newline': pLF,
    '\t': pINDENT, '\f': pINC, '\b': pDEC, '\n': pLF,
}

def expr0(env, e): return e[0]
def expr1(env, e): return e[1]
def expr2(env, e): return e[2]
def expr3(env, e): return e[3]
def expr4(env, e): return e[4]
def expr1r(env, e): return e[-1]
def expr2r(env, e): return e[-2]
def expr3r(env, e): return e[-3]
def expr4r(env, e): return e[-4]
def this(env, e): return e
def exprdata(env, e): return e.data

def exprtype(env, e):
    return e.ty

def definedexpr(name):
    def curry(env, e):
        print('@TODO', name)
        return e
    return curry

def exprfunc(c):
    if c.endswith(')'):
        name, p = c[:-1].split('(')
        f = exprfunc(p)
        if name.startswith('@'):
            return f
        elif name =='type':
            return lambda env, e: exprtype(env, f(env, e))
        elif name.startsWith('#'):
            pass
        return lambda env, e: definedexpr(name)(f(env, e))

    if c == '1': return expr1
    elif c == '2': return expr2
    elif c == '3': return expr3
    elif c == '4': return expr4
    elif c == '-1': return expr1r
    elif c == '-2': return expr2r
    elif c == '-3': return expr3r
    elif c == '-4': return expr4r
    elif c == 'this': return this
    elif c == 's': return exprdata
    return expr0

def EXPR(env, e, f, ss):
    ss.pushEXPR(env, f(env, e))

def findindex(s, n):
    n = str(n)
    if s.find('%' + n) >= 0: return True
    if s.find('${' + n + '}') >= 0: return True
    if s.find('(' + n + ')}') >= 0: return True
    return False

def startindex(code: str):
    index = 1
    if findindex(code, 1):
        index = 2
    if findindex(code, 2):
        index = 3
    if findindex(code, 3):
        index = 4
    return index

def endindex(code: str):
    index = 0
    if findindex(code, -1):
        index = -1
    if findindex(code, -2):
        index = -2
    if findindex(code, -3):
        index = -3
    return index

def delimfunc(start, end):
    def curry(env, e, delim, ss):
        if delim is None: delim = [(STR, ',')]
        if start < len(e):
            ss.pushEXPR(env, e[start])
            if end == 0:
                for se in e[start+1:]:
                    ss.exec(env, se, delim)
                    ss.pushEXPR(env, se)
            else:
                for se in e[start+1:end]:
                    ss.exec(env, se, delim)
                    ss.pushEXPR(env, se)
    return curry

@lru_cache(maxsize=512)
def compile_code(code: str, delim = None):
    if delim is not None:
        delim = compile_code(delim, None)
    def append_string(l, c):
        if len(c) > 0: l.append((STR, c))
    def append_command(l, c):
        if c.endswith(')') or c in '0123456789-1-2-3-4this':
            l.append((EXPR, exprfunc(c)))
        elif ':' in c:
            if c.startswith(':'):
                c = str(startindex(code)) + c
            if c.endswith(':'):
                c = c + str(endindex(code))
            s,e = map(int, c.split(':'))
            l.append((delimfunc(s,e),delim))
        elif c == '*':
            l.append((delimfunc(startindex(code), endindex(code)), delim))
        elif c in commands:
            l.append((commands[c],None))
    index = 1
    start = 0
    i = 0
    l = []
    while i < len(code):
        if code[i] in codekeys:
            append_string(l, code[start: i])
            append_command(l, codekeys[code[i]])
            start = i+1
            i = start
            continue
        if code[i] == '%' and i+1 < len(code) and code[i+1] in esckeys:
            append_string(l, code[start: i])
            append_command(l, code[i+1])
            start = i+2
            i = start
            continue

        if not code.startswith('${',i):
            i += 1
            continue
        j = code.find('}', i + 1)
        if j == -1:
            i += 1
            continue
        append_string(l, code[start: i])
        cmd = code[i+2:j]
        append_command(l, cmd)
        start = j+1
        i = start
    append_string(l, code[start: i])
    return tuple(l)

#split_code('${indent}')
#split_code('def ${1}(${*}):\n\t${-1}')

def transpile_init(origami_files, out):
    env = Env()
    if len(origami_files) == 0:
        origami_files.append('common.origami')
    for file in origami_files:
        env.load(file, out)
    return env

def transpile(env, t, out):
    if env is None: env = transpile_init()
    if t == 'err':
        out.perror(t.pos3(), 'Syntax Error')
        return
    e = SExpr.of(t)
    print('@expr', e)
    Typer().asType(env, e, None)
    ss = SourceSection(out)
    ss.pushEXPR(env, e)
    return ss
