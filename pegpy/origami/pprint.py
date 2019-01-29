from functools import lru_cache, reduce

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
        if type(code) == type(STR):
            code(env, e, self)
            return
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

    def push(self, env, *argv):
        for e in argv:
            if isinstance(e, str):
                self.pushSTR(e)
            else:
                self.pushEXPR(env, e)

    def begin(self, env, *argv):
        self.pushINDENT()
        self.push(env, *argv)
        self.incIndent()
        self.pushLF()

    def p(self, env, *argv):
        self.pushINDENT()
        self.push(env, *argv)
        self.pushLF()

    def end(self, env, *argv):
        self.decIndent()
        self.pushINDENT()
        self.push(env, *argv)
        self.pushLF()


## format function

def typefmt(env, e, x, ss):
    if e.ty is None:
        ss.pushSTR(env['Any'].code)
    else:
        ss.pushEXPR(env, e.ty)

def retfmt(env, e, x, ss):
    if e.ty is None:
        ss.pushSTR(env['Any'].code)
    elif e.ty.isFuncType():
        ss.pushEXPR(env, e.ty[-1])
    else:
        ss.pushEXPR(env, e.ty)

def bytefmt(env, e, x, ss):
    ss.pushSTR(reduce(lambda x, y: x + format(ord(y), '04x'), str(e), 'v_'))

FMTFUNC = {
    'type': typefmt,
    'ret':  retfmt,
    'byte': bytefmt,
}

## builtin function

def STR(env, e, s, ss): ss.pushSTR(s)
def EXPR(env, e, f, ss): ss.pushEXPR(env, e)
def THIS(env, e, f, ss): f(env, e, ss)

def pINDENT(env, e, s, ss): ss.pushINDENT()
def pINC(env, e, s, ss): ss.incIndent()
def pDEC(env, e, s, ss): ss.decIndent()
def pLF(env, e, s, ss): ss.pushLF()

def pNL(env, e, s, ss):
    ss.pushLF()
    ss.pushINDENT()

def pINCNL(env, e, s, ss):
    ss.incIndent()
    ss.pushLF()
    ss.pushINDENT()

def pDECNL(env, e, s, ss):
    ss.decIndent()
    ss.pushLF()
    ss.pushINDENT()

BUILTINS = {
    'NL': pNL,
    '+NL': pINCNL,
    '-NL': pDECNL,

    'TAB': pINDENT,
    'LF': pLF,
    'indent++': pINC,
    'indent--': pDEC,
    '+': pINC,
    '-': pDEC,
    'this': THIS,
}

def append_string(l, c):
    if len(c) > 0: l.append((STR, c))

DELIM = tuple([(STR, ',')])

def append_command(l, cmd, delim, f = EXPR):
    #print('@cmd', cmd)
    if cmd.endswith(')'):
        idx = cmd.find('(')
        name = cmd[0:idx]
        arg = cmd[idx + 1:-1]
        if name in FMTFUNC:
            append_command(l, arg, delim, FMTFUNC[name])
        else:
            append_command(l, arg, delim, f)
        return

    if cmd in BUILTINS:
        l.append((BUILTINS[cmd], f))
        return

    if cmd == '*': cmd = '1:'
    if ':' in cmd:
        if cmd.startswith(':'): cmd = '1' + cmd
        if cmd.endswith(':'):
            start, end = int(cmd[:-1]), None
        else:
            start, end = map(int, cmd.split(':'))

        def SUB(env, e, f, ss):
            if start < len(e):
                nonfirst = False
                for se in e[start:end]:
                    if nonfirst: ss.exec(env, e, delim)
                    if se == '#Done': continue
                    f(env, se, None, ss)
                    nonfirst = True
        return l.append((SUB, f))

    try :
        idx = int(cmd)
        def INDEX(env, e, f, ss):
            #print('@idx', idx, '<', e, type(e.data), len(e))
            f(env, e[idx], None, ss)
        return l.append((INDEX, f))

    except ValueError:
        def NAME(env, e, f, ss):
            idx = e.find(cmd)
            if idx != -1:
                #print('@idx', cmd, idx, f)
                f(env, e[idx], None, ss)
        return l.append((NAME, f))

@lru_cache(maxsize=512)
def compile_code(code: str, delim = None):
    delim = DELIM if delim is None else compile_code(delim, None)
    start = 0
    l = []
    while True:
        spos = code.find('${', start)
        if spos == -1:
            append_string(l, code[start:])
            break
        epos = code.find('}', spos)
        if epos == -1:
            start = spos+1
            continue
        append_string(l, code[start: spos])
        append_command(l, code[spos+2:epos], delim)
        start = epos+1
    return tuple(l)
