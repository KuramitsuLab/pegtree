from functools import lru_cache
from pegpy.peg import Grammar, nez
from pegpy.origami.sexpr import SExpr, ListExpr, AtomExpr, String, Char
import pegpy.utils as u

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
        f = u.find_path(path, 'origami').open()
        data = f.read()
        f.close()
        t = origami_parser(data, path)
        if t == 'err':
            out.verbose(u.serror(t.pos3()))
            return
        libs = tuple([])
        for _, stmt in t:
            #print(stmt)
            if stmt == 'CodeMap':
                ty = stmt.get('type', None, lambda t: SExpr.of(t))
                keys = Def.getkeys(stmt, ty)
                code = u.unquote_string(stmt['expr'].asString()) if 'expr' in stmt else None
                delim = u.unquote_string(stmt['delim'].asString()) if 'delim' in stmt else None
                d = Def(ty, libs, code, delim)
                self[keys[0]] = d
                for key in keys[1:]:
                    if not key in self:
                        self[key] = d
        #print('DEBUG', self.nameMap)

    def addName(self, name, ty):
        self[name] = Def(ty, None, None)

    def inferName(self, name):
        if name[-1] in "0123456789'_": name = name[:-1]
        if name in self:
            ty = self[name].ty
            if ty is not None: return ty
        if len(name) >= 1:
            return self.inferName(name[1:])
        return None

## Typing

class Typer(object):
    def __init__(self):
        pass

    def asType(self, env, expr, ty):
        if expr.isUntyped():
            expr = self.tryType(env, expr, ty)
        if ty is None or expr.ty is ty:
            return expr
        keys = SExpr.makekeys(str(ty), 1, expr.ty)
        for key in keys:
            defined = env[key]
            if defined is None: continue
            expr = SExpr.new('#Cast', expr)
            expr.setType(ty)
            expr.setCode(defined.getcode())
            return expr
        print('@type error', ty, expr, expr.ty, keys)
        return expr

    def typeAt(self, env, expr, n, ty):
        expr.data[n] = self.asType(env, expr.data[n],ty)

    def tryType(self, env, expr, ty):
        key = expr.asSymbol()
        if key.startswith('#'):
            try:
                f = getattr(self, key[1:])
                return f(env, expr, ty)
            except AttributeError:
                print('@TODO', key)
                pass
        if isinstance(expr, AtomExpr):
            return self.Var(env, expr, ty)
        else:
            return self.Apply(env, expr, ty)

    def Block(self, env, expr, ty):
        voidTy = expr.ofType('Void')
        for n in range(1, len(expr)):
            self.typeAt(env, expr, n, voidTy)
        return expr

    def AssumeDecl(self, env, expr, ty):
        ty = expr[-1]
        #print('a', expr, expr[0], expr[-1], type(expr[-1]))
        for name in expr[1:-1]:
            env.addName(str(name), ty)
        return expr.done()

    def FuncDecl(self, env, expr, ty):
        lenv = env.newLocal()
        for n in range(2, len(expr)):
            self.typeAt(lenv, expr, n, None)
        expr.setType('Void')
        return expr

    def Param(self, env, expr, ty):
        name = str(expr[1])
        if len(expr) == 2:
            ty = env.inferName(name)
        else:
            ty = expr[2]
        if ty is None: return expr.err('Untyped ' + name)
        expr[1].setType(ty)
        env[name] = Def(ty, None, name)
        expr.setType('Void')
        return expr

    def Var(self, env, expr, ty):
        key = expr.asSymbol()
        defined = env[key]
        if defined is not None:
            expr.setType(defined.ty)
            expr.setCode(defined.getcode())
            return expr
        return expr.err('Undefined ' + key)

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
                return expr
        return expr.err('Undefined ' + str(expr))

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

    __slots__ = ['sb', 'indent', 'tab', 'lf']

    def __init__(self, indent = 0, tab = '   ', lf = '\n'):
        self.sb = []
        self.indent = indent
        self.tab = tab
        self.lf = lf

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
        def ef(key):
            return env[key].getcode() if key in env else None
        code = e.code
        if code is None:
            keys = e.keys()
            for key in keys:
                code = ef(key)
                if code is not None:
                    break
        if code is None:
            self.pushSTR(str(e))
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

def exprtype(env, e): return e.ty

def returnexpr(env, e):
    return SExpr.new('#Return', e)

def definedexpr(name):
    def curry(env, e):
        print('@TODO', name)
        return e
    return curry

def exprfunc(c):
    if c.endswith(')'):
        name, p = c[:-1].split('(')
        f = exprfunc(p)
        if name=='type':
            return lambda env, e: exprtype(env, f(env, e))
        elif name=='@ret':
            return lambda env, e: returnexpr(env, f(env, e))
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
    Typer().asType(env, e, None)
    ss = SourceSection()
    if not e.perror():
        ss.pushEXPR(env, e)
    return ss
