from pathlib import Path
import pegpy.utils as u

## Value

class Type(object):
    __slots__ = ['name']
    def __init__(self, name):
        self.name = name
    def __eq__(self, other):
        return self is other
    def __str__(self):
        return self.name

class String(object):
    __slots__ = ['value']
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

## SExpression

class SExpr(object):
    ORIGAMI = {
        'Unary': 'name expr',
        'Infix': 'name left right',
        'IfExpr': '#if cond then else',
        'FuncExpr' '#lambda params right'
        'IntExpr': lambda t: int(t.asString()),
        'DoubleExpr': lambda t: float(t.asString()),
        'StringExpr': lambda t: String(t.asString()),
        'CharExpr': lambda t: t.asString(),
        'TrueExpr': lambda t: 'true',
        'FalseExpr': lambda t: 'false',
        'BaseType': lambda t: Type(t.asString()),
    }

    @classmethod
    def addRule(cls, key, conv):
        SExpr.ORIGAMI[key] = conv

    @classmethod
    def of(cls, t, intern, conv = ORIGAMI):
        if t is None: return ListExpr(())
        key = t.tag
        if len(t) == 0 :  #AtomExpr
            if key in conv:
                return AtomExpr(conv[key](t), t.pos3())
            else:
                return AtomExpr(intern(t.asString()), t.pos3())

        lconv = conv[key] if key in conv else None
        cons = []
        def flatadd(l, e):
            if isinstance(e, ListExpr) and e.first() == '':
                # flatten [# e e]
                for e2 in e.data[1:]: l.append(e2)
            else:
                l.append(e)
        if isinstance(lconv, str):
            for name in lconv.split():
                if name.startswith('#'):
                    cons.append(AtomExpr(intern(name[1:]), t.pos3()))
                else:
                    flatadd(cons, SExpr.of(t[name], intern, conv))
            return ListExpr(cons)
        else:
            cons.append(AtomExpr(intern(key.lower()), t.pos3()))
            for n, v in t:
                flatadd(cons, SExpr.of(v, intern, conv))
            return ListExpr(cons)

    @classmethod
    def new(cls, s):
        """
        >>> parse_sexp("(+ 5 (+ 3 5))")
        [['+', '5', ['+', '3', '5']]]
        """
        sexp = [[]]
        word = ''
        in_str = False
        for char in s:
            if char == '(' and not in_str:
                sexp.append([])
            elif char == ')' and not in_str:
                if word:
                    sexp[-1].append(word)
                    word = ''
                temp = sexp.pop()
                sexp[-1].append(temp)
            elif char in (' ', '\n', '\t') and not in_str:
                if word:
                    sexp[-1].append(word)
                    word = ''
            elif char == '\"':
                in_str = not in_str
            else:
                word += char
        return sexp[0]

class AtomExpr(SExpr):
    __slots__ = ['data', 'pos3', 'ty']
    def __init__(self, data, pos3 = None, ty = None):
        self.data = data
        self.pos3 = pos3
        self.ty = ty
    def __str__(self):
        return str(self.data)
    def keys(self):
        return [type(self.data).__name__, str(self.data)]

class ListExpr(SExpr):
    __slots__ = ['data', 'ty']
    def __init__(self, data, ty = None):
        self.data = tuple(data)
        self.ty = ty
    def __str__(self):
        return '(' + (' '.join(map(str, self.data))) + ')'
    def first(self):
        return str(self.data[0])
    def keys(self):
        key = str(self.data[0])
        keys = ['{}@{}'.format(key, len(self.data)-1), key]
        if self.ty is not None:
            return self.ty.joinkeys(keys)
        return keys

def sconv(t):
    intern = u.string_intern()
    return SExpr.of(t, intern)

class SyntaxMapper(object):
    __slots__ = ['syntaxMap']

    def __init__(self):
        self.syntaxMap = {}
        self.syntaxMap['TODO'] = 'TODO(%*)\v '

    def addSyntax(self, key, fmt):
        self.syntaxMap[key] = fmt

    def emit(self, e, ss):
        keys = e.keys()
        for key in keys:
            if key in self.syntaxMap:
                rule = self.syntaxMap[key]
                if hasattr(rule, 'emit'):
                    rule.emit(e, ss)
                else:
                    ss.pushFMT(self, rule, e.data)
                return
        if isinstance(e, AtomExpr):
            ss.pushSTR(str(e))
        else:
            ss.pushFMT(self, self.syntaxMap['TODO'], e.data)

    def load(self, file):
        path = Path(file)
        if not path.exists():
            path = Path(__file__).parent / path
        f = path.open('r')
        libs = ()
        for line in f.readlines():
            if line.startswith('#include'):
                for file in line.split()[1:]:
                    self.load(file)
                continue
            if line.startswith('#require'):
                libs = line.split()[1:]
                print(libs)
                continue
            if line.startswith('#'):
                continue
            loc = line.find('\t=')
            if loc == -1:
                loc = line.find(' =')
            if loc != -1:
                key = line[:loc].strip()
                value = u.unquote_string(line[loc+2:].strip())
                #print('@', key, value)
                self.addSyntax(key, value)
        f.close()

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
        if isinstance(e, SExpr):
            syn.emit(e, self)
        else:
            self.pushSTR(str(e))

    def pushFMT(self, syn: SyntaxMapper, fmt: str, args: list):
        index = 1
        start = 0
        i = 0
        delim = ''
        loc = fmt.find('\v')
        if loc >= 0:
            delim = fmt[loc+1:]
            fmt = fmt[0: loc]
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
                self.decIndent()
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
                if c == '*':
                    cnt = 0
                    for a in args[index:]:
                        if cnt > 0 : self.pushDELIM(delim)
                        self.pushEXPR(syn, a)
                        cnt += 1
                    continue
        #end while
        self.pushSTR(fmt[start:])

    def pushDELIM(self, fmt: str):
        for c in fmt:
            if c == '\t' :
                self.pushTAB()
            elif c == '\f' :
                self.incIndent()
            elif c == '\b' :
                self.decIndent()
            elif c == '\n':
                self.pushLF()
            else:
                self.pushSTR(c)
