from pegpy.peg import Grammar, nez
from pegpy.origami.sexpr import SExpr, ListExpr, AtomExpr, String, Char
import pegpy.utils as u

g = Grammar('konoha6')
g.load('konoha6.tpeg')
origami_parser = nez(g['OrigamiFile'])

def getkeys(stmt, ty):
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

class Def(object):
    __slots__ = ['ty', 'libs', 'code']
    def __init__(self, ty, libs, code):
        self.ty = ty
        self.libs = libs
        self.code = code
    def __str__(self):
        return str(self.code)
    def __repr__(self):
        return repr(self.code)

class Env(object):
    __slots__ = ['parent', 'nameMap']

    def __init__(self, parent = None):
        self.parent = parent
        self.nameMap = {}

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

    def load(self, path):
        f = u.find_path(path, 'origami').open()
        data = f.read()
        f.close()
        t = origami_parser(data, path)
        if t == 'err':
            er = t.getpos()
            print('SyntaxError ({}:{}:{}+{})'.format(er[0], er[2], er[3], er[1]), '\n', er[4], '\n', er[5])
            return
        libs = tuple([])
        for _, stmt in t:
            #print(stmt)
            if stmt == 'CodeMap':
                ty = stmt.get('type', None, lambda t: SExpr.of(t))
                keys = getkeys(stmt, ty)
                code = u.unquote_string(stmt['expr'].asString()) if 'expr' in stmt else ''
                if 'delim' in stmt:
                    delim = u.unquote_string(stmt['delim'].asString())
                    delim = split_code(delim)
                    code = split_code(code, delim)
                d = Def(ty, libs, code)
                self[keys[0]] = d
                for key in keys[1:]:
                    if not key in self:
                        self[key] = d
        #print('DEBUG', self.nameMap)

keyList = ['{}', '#{}', '{}Expr', '#{}Expr']

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
            if key in env:
                d = env[key]
                code = d.code
                if isinstance(code, str):
                    code = split_code(code)
                    d.code = code
                return code
            return None

        code = e.code
        if code is None:
            keys = e.keys()
            for key in keys:
                code = ef(key)
                if code is not None:
                    break

        if code is None:
            if isinstance(e, AtomExpr):
                if isinstance(e.data, String):
                    for k in keyList:
                        key = k.format('String')
                        code = ef(key)
                        if code is not None:
                            break

                elif isinstance(e.data, Char):
                    for k in keyList:
                        key = k.format('Char')
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

#ORIGAMI

#ORIGAMI

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
    #assert(isinstance(e, SExpr))
    #print('@', f, e, '->', f(env, e))
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
        if delim is None:
            delim = [(STR, ',')]
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

def split_code(code: str, delim=None):
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
            l.append((delimfunc(s,e),None))
        elif c == '*':
            l.append((delimfunc(startindex(code), endindex(code)), None))
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

def transpile(t, origami_files = ['common.origami']):
    env = Env()
    if len(origami_files) == 0:
        env.load('common.origami')
    else:
        for file in origami_files:
            env.load(file)

    e = SExpr.of(t)
    # TODO typecheck is HERE
    ss = SourceSection()
    ss.pushEXPR(env, e)
    return ss
