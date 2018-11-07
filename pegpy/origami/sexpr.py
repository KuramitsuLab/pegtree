from pathlib import Path
import pegpy.utils as u

## Value

class String(object):
    __slots__ = ['value']
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Type(object):
    __slots__ = ['name']
    def __init__(self, name):
        self.name = name
    def __eq__(self, other):
        return self is other
    def __str__(self):
        return self.name

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
    }

    @classmethod
    def addRule(cls, key, conv):
        SExpr.ORIGAMI[key] = conv

    @classmethod
    def of(cls, t, intern, rules = ORIGAMI):
        if t is None:
            return ListExpr(())
        key = t.tag
        if len(t) == 0 :  #AtomExpr
            if key in rules:
                e = rules[key](t)
                return e if isinstance(e, SExpr) else AtomExpr(rules[key](t), t.pos3())
            else:
                return AtomExpr(intern(t.asString()), t.pos3())

        lconv = rules[key] if key in rules else None
        def flatadd(l, e):
            if isinstance(e, ListExpr) and e.first() == '':
                # flatten [# e e]
                for e2 in e.data[1:]: l.append(e2)
            else:
                l.append(e)
        if isinstance(lconv, str):
            lconv = tuple(lconv.split())
            rules[key] = tuple
        if isinstance(lconv, tuple):
            cons = []
            for name in lconv:
                if name.startswith('#'):
                    cons.append(AtomExpr(intern(name[1:]), t.pos3()))
                else:
                    flatadd(cons, SExpr.of(t[name], intern, rules))
            return ListExpr(cons)
        elif callable(lconv):
            return lconv(t, intern, rules)
        else:
            cons = []
            cons.append(AtomExpr(intern(key.lower()), t.pos3()))
            for n, v in t:
                flatadd(cons, SExpr.of(v, intern, rules))
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
    __slots__ = ['data', 'pos3', 'ty', 'code']
    def __init__(self, data, pos3 = None, ty = None):
        self.data = data
        self.pos3 = pos3
        self.ty = ty
        self.code = None
    def __str__(self):
        return str(self.data)

    def keys(self):
        return [type(self.data).__name__, str(self.data)]

    def typeCheck(self, ty):
        self.ty = ty

    def inferType(self, env):
        if self.ty is None:
            for iname in self.keys():
                ty = env.getType(iname)
                if ty is not None:
                    self.typeCheck(ty)
                    break
        if self.code is None:
            for iname in self.keys():
                syn = env.getSyntax(iname)
                if syn is not None:
                    self.code = syn
                    break

class ListExpr(SExpr):
    __slots__ = ['data', 'ty', 'code']
    def __init__(self, data, ty = None):
        self.data = tuple(data)
        self.ty = ty
        self.code = None
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

    def typeCheck(self, ty):
        assert(ty.isFuncType())
        for ty in ty.paramType():
            self.data[1]
            #TODO

    def inferType(self, env):
        if self.ty is None:
            for e in self.data[1:]:
                e.inferType(env)
            for iname in self.keys():
                ty = env.getType(iname)
                if ty is not None:
                    self.typeCheck(ty)
                    break




def sconv(t):
    intern = u.string_intern()
    return SExpr.of(t, intern)

## Type

class TypeExpr(object):
    def isFuncType(self): return False

class BaseTypeExpr(AtomExpr, TypeExpr):
    __slots__ = ['data', 'pos3', 'ty']
    def __init__(self, data, ty = None):
        super().__init__(data, None, ty)
    def __str__(self):
        return str(self.data)
    def joinkeys(self, keys):
        return [keys[0]+'@'+str(self.data)] + keys

typeMap = {
    'Type': BaseTypeExpr(Type('Type'))
}

TypeType =typeMap['Type']
TypeType.ty = TypeType

def BaseType(n):
    if not n in typeMap:
        typeMap[n] = BaseTypeExpr(Type(n), TypeType)
    return typeMap[n]

def cBaseType(t):
    return BaseType(t.asString())

IntType = BaseType('Int')

def tyconv(ty):
    if isinstance(ty, SExpr):
        return ty
    return BaseType(str(ty))

class ParamTypeExpr(ListExpr, TypeExpr):
    __slots__ = ['data', 'ty']
    def __init__(self, data):
        super().__init__(data, TypeType)
    def __str__(self):
        return str(self.data[1]) + '[' + (','.join(map(str, self.data[2:]))) + ']'
    def keys(self):
        m = str(self.data[1])
        return [ m + str(self.data[2]), m] + super().keys()[1:]
    def joinkeys(self, keys):
        return [keys[0]+'@'+str(self.data)] + keys

def ParamType(*types):
    types = list(map(tyconv, types))
    key = ' '.join(map(str, types))
    if not key in typeMap:
        typeMap[key] = ParamTypeExpr(['paramtype', *types])
    return typeMap[key]

def cParamType(t, intern, rules):
    type = [SExpr.of(t['base'], intern, rules)]
    for l,se in t['params']:
        type.append(SExpr.of(se, intern, rules))
    return ParamType(*type)

class FuncTypeExpr(ListExpr, TypeExpr):
    __slots__ = ['data', 'ty']
    def __init__(self, data):
        super().__init__(data, TypeType)
    def __str__(self):
        return 'Func['+ (','.join(map(str, self.data[1:])))+']'

    def isFuncType(self):
        return True
    def joinkeys(self, keys):
        return [keys[0]+'@'+str(self.data)] + keys

def FuncType(*types):
    types = list(map(tyconv, types))
    key = 'F(' + '->'.join(map(str, types)) + ')'
    if not key in typeMap:
        typeMap[key] = FuncTypeExpr(['functype', *types])
    return typeMap[key]

def cFuncType(t, intern, rules):
    types = []
    base = t['base']
    if base.tag == 'TupleType':
        for l,se in t['base']:
            types.append(SExpr.of(se, intern, rules))
    else:
        types.append(SExpr.of(base, intern, rules))
    types.append(SExpr.of(t['type'], intern, rules))
    return FuncType(*types)

SExpr.addRule('BaseType', cBaseType)
SExpr.addRule('ParamType', cParamType)
SExpr.addRule('FuncType', cFuncType)






## SyntaxMapper


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
