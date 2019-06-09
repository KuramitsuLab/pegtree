from functools import lru_cache, reduce


class Source(object):
    __slots__ = ['buffers', 'indent', 'tab', 'lf', 'errors']

    def __init__(self, indent=0, tab='   ', lf='\n'):
        self.buffers = []
        self.indent = indent
        self.tab = tab
        self.lf = lf
        self.errors = []

    def __repr__(self):
        return ''.join(self.buffers)

    def __str__(self):
        return ''.join(self.buffers)

    def format(self, expr, fmt=None):
        if not isinstance(expr, SExpr):
            self.pushSTR(str(expr))
            return
        if fmt is None:
            fmt = expr.fmt
        if fmt is None:
            self.pushSTR(expr)
            return
        '''
        if e == '#Error' or e == '#Warning' or e == '#Notice':
            self.out.perror(e.getpos(), e.context)
            self.pushEXPR(env, e[1])
            return
        '''
        for cf in codify(fmt):
            self.eval(expr, cf)

    def eval(self, expr, suffix):
        if isinstance(suffix, int):  # 1
            self.format(expr[suffix])
            return
        if isinstance(suffix, str):
            self.pushSTR(suffix)
            return
        assert(isinstance(suffix, tuple))  #
        cmd = suffix[0]
        if isinstance(cmd, str):
            if cmd in ['LF', 'BEGIN', 'END']:
                self.command(cmd)
                return
            # {type, (": ", "")} => ("type", ": ", "")
            if cmd == 'type':
                expr = expr.ty
            elif cmd in expr.imap and expr.imap[cmd] < len(expr):
                expr = expr[expr.imap[cmd]]
            else:
                expr = None
            if expr is not None:
                self.pushSTR(suffix[1])
                self.format(expr[suffix])
                self.pushSTR(suffix[2])
        else:  # {(1,None,",")} => (1, None, ",")
            c = 0
            for e in expr[suffix[0]:suffix[1]]:
                self.push(e)
                if c > 0:
                    self.pushSTR(suffix[2])
                c += 1

    def command(self, cmd):
        if cmd == 'LF':
            self.buffers.append(self.lf)
            self.buffers.append(self.tab * self.indent)
        elif cmd == 'BEGIN':
            self.indent += 1
        elif cmd == 'END':
            self.indent -= 1

    def push(self, *exprs):
        if len(exprs) != 1:
            for expr in exprs:
                self.format(expr)
        else:
            self.format(exprs[0])

    def pushSTR(self, s):
        if len(s) > 0:
            self.buffers.append(s)

    def perror(self, pos4, msg='Syntax Error'):
        self.errors.append((0, pos4, msg))

    '''
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
    '''


def codify_command(l, code):
    cmd = []
    while len(code) > 0:
        c = code[0]
        if c == '}':
            code = code[1:]
            break
        if c == ' ' or c == ',':
            code = code[1:]
        elif c == ':':
            cmd.append(None)
            code = code[1:]
        elif c == '"' or c == "'":
            for i in range(1, len(code)):
                if c == code[i]:
                    break
            cmd.append(code[1:i])
            code = code[i+1:]
        elif c == '-' or c.isdigit():
            for i in range(1, len(code)):
                if not code[i].isdigit():
                    break
            cmd.append(int(code[0:i]))
            code = code[i:]
            if code.startswith(':'):
                code = code[1:]
        else:
            for i in range(1, len(code)):
                c = code[i]
                if c == ' ' or c == '}':
                    break
            cmd.append(code[0:i])
            if len(cmd) > 1:
                cmd[0], cmd[1] = cmd[1], cmd[0]
            code = code[i:]
    if len(cmd) == 1:
        if isinstance(cmd[0], int):
            l.append(cmd[0])
        else:
            cmd.append('')
            cmd.append('')
            l.append(tuple(cmd))
    elif len(cmd) == 2:
        cmd.append('')
        l.append(tuple(cmd))
    elif len(cmd) == 3:
        l.append(tuple(cmd))
    return code


@lru_cache(maxsize=512)
def codify(fmt: str):
    l = []
    code = fmt
    while len(code) > 0:
        spos = code.find('${')
        if spos == -1:
            break
        if spos > 0:
            l.append(code[:spos])
        code = codify_command(l, code[spos+2:])
    if len(code) > 0:
        l.append(code)
    return tuple(l)


print(codify('${:1} + ${2}'))
print(codify('a${1:2 ", " } + ${-1}b'))
print(codify('${" :" type} + ${-1}'))
