from functools import lru_cache

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

    def pushEXPR(self, env, e):
        if not hasattr(e, 'code'):
            self.pushSTR(str(e))
            return
        if e == '#Error' or e == '#Warning' or e == '#Notice':
            self.out.perror(e.getpos(), e.context)
            self.pushEXPR(env, e[1])
            return
        code = e.code
        if code is None:
            keys = e.keys()
            #print('@pretty-printing', keys)
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
