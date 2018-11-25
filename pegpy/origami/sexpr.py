from pathlib import Path
import pegpy.utils as u

## Value

class String(object):
    __slots__ = ['data', 'code']
    def __init__(self, data):
        self.data = data
        self.code = None
    def __str__(self):
        return str(self.data)
    def __len__(self):
        return 0
    def __getitem__(self, item):
        return None
    def first(self):
        return self
    def keys(self):
        return []
    def typeCheck(self, env, ty):
        if self.ty == None or self.ty is ty:
            self.ty = ty
            return
        ty.match(self.ty)

class Char(object):
    __slots__ = ['data', 'code']
    def __init__(self, data):
        self.data = data
        self.code = None
    def __str__(self):
        return str(self.data)
    def __len__(self):
        return 0
    def __getitem__(self, item):
        return None
    def first(self):
        return self
    def keys(self):
        return []
    def typeCheck(self, env, ty):
        if self.ty == None or self.ty is ty:
            self.ty = ty
            return
        ty.match(self.ty)

'''
class Type(object):
    __slots__ = ['name']
    def __init__(self, name):
        self.name = name
    def __eq__(self, other):
        return self is other
    def __str__(self):
        return self.name
'''

## SExpression

class SExpr(object):
    ORIGAMI = {
        'Unary': 'name expr',
        'Infix': 'name left right',
        'ApplyExpr': 'recv params',
        'MethodExpr': 'name recv params',
        'NameExpr' : lambda t: t.asString(),
        'IntExpr': lambda t: int(t.asString()),
        'DoubleExpr': lambda t: float(t.asString()),
        'StringExpr': lambda t: String(t.asString()),
        'CharExpr': lambda t: Char(t.asString()),
        'TrueExpr': lambda t: 'true',
        'FalseExpr': lambda t: 'false',
    }

    @classmethod
    def addRule(cls, key, conv):
        SExpr.ORIGAMI[key] = conv

    @classmethod
    def of(cls, t, intern = u.string_intern(), rules = ORIGAMI):
        if t is None:
            return ListExpr(())
        key = t.tag
        if len(t) == 0 :  #AtomExpr
            if key in rules:
                e = rules[key](t)
                return e if isinstance(e, SExpr) else AtomExpr(rules[key](t), t.pos3())
            else:
                return ListExpr([AtomExpr(intern(t.asString()), t.pos3())])

        lconv = rules[key] if key in rules else None
        ##
        def flatadd(l, e):
            if isinstance(e, ListExpr) and e.first() == '#':
                # flatten [# e e]
                for e2 in e.data[1:]: l.append(e2)
            else:
                l.append(e)
        if isinstance(lconv, str):
            lconv = tuple(lconv.split())
            rules[key] = lconv
        if isinstance(lconv, tuple):
            cons = []
            for name in lconv:
                if name.startswith('#'):
                    cons.append(AtomExpr(intern(name), t.pos3()))
                else:
                    flatadd(cons, SExpr.of(t[name], intern, rules))
            return ListExpr(cons)
        elif callable(lconv):
            #print('@DEBUG', type(lconv), lconv)
            return lconv(t, intern, rules)
        else:
            cons = []
            cons.append(AtomExpr(intern("#"+key), t.pos3()))
            for n, v in t:
                flatadd(cons, SExpr.of(v, intern, rules))
            return ListExpr(cons)

    @classmethod
    def new(cls, *l):
        cons = []
        for e in l:
            if isinstance(e, SExpr) :
                cons.append(e)
            else:
                cons.append(AtomExpr(e))
        return ListExpr(cons)

    @classmethod
    def new2(cls, s):
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

    def asType(self, env, ty = None):
        if ty is not None:
            return self.typeCheck(env, ty)

        if self.ty is None:
            for iname in self.keys():
                tf = env.getType(iname)
                if isinstance(tf, TypeExpr):
                    return self.typeCheck(env, tf)
                elif tf is not None:
                    return tf(self, env)

class AtomExpr(SExpr):
    __slots__ = ['data', 'pos3', 'ty', 'code']
    def __init__(self, data, pos3 = None, ty = None):
        self.data = data
        self.pos3 = pos3
        self.ty = ty
        self.code = None
    def __str__(self):
        return str(self.data)

    def __len__(self):
        return 0
    def __getitem__(self, item):
        return None

    def first(self):
        return self

    def keys(self):
        return [type(self.data).__name__, str(self.data)]

    def typeCheck(self, env, ty):
        if self.ty == None or self.ty is ty:
            self.ty = ty
            return
        ty.match(self.ty)

class ListExpr(SExpr):
    __slots__ = ['data', 'ty', 'code']
    def __init__(self, data, ty = None):
        self.data = tuple(data)
        self.ty = ty
        self.code = None
    def __str__(self):
        return '(' + (' '.join(map(str, self.data))) + ')'
    def __len__(self):
        return len(self.data)
    def __getitem__(self, item):
        return self.data[item]

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
    def match(self, ty, vars = {}):
        if self is ty: return True
        if len(self.data) == len(ty.data) and self.data[0] == ty.data[0]:
            for t1,t2 in zip(self.data[1:], ty.data[1:]):
                if not t1.match(t2, vars): return False
            return True
        return False

class BaseTypeExpr(AtomExpr, TypeExpr):
    __slots__ = ['data', 'pos3', 'ty']
    def __init__(self, data, ty = None):
        super().__init__(data, None, ty)
    def __str__(self):
        return str(self.data)
    def __eq__(self, other):
        return self is other or self.data == other

    def joinkeys(self, keys):
        return [keys[0]+'@'+str(self.data)] + keys

    def isVarType(self):
        return len(self.data) == 1 and self.data.islower()

    def match(self, ty: TypeExpr, vars = {}):
        if self is ty: return True
        tname = self.data
        if self.isVarType():
            if tname in vars:
                return vars[tname].match(ty, vars)
            else:
                vars[tname] = ty
            return True
        return tname == ty.data

    def resolve(self, vars):
        if self.isVarType():
            return vars[self.data]
        return self

typeMap = {
    'Type': BaseTypeExpr('Type')
}

TypeType = typeMap['Type']
TypeType.ty = TypeType

def BaseType(n: str):
    if not n in typeMap:
        typeMap[n] = BaseTypeExpr(n, TypeType)
    return typeMap[n]

def cBaseType(t):
    return BaseType(t.asString())

def tyconv(ty):
    if isinstance(ty, SExpr):
        return ty
    return BaseType(str(ty))

def resolve_curry(vars):
    def f(ty):
        if isinstance(ty, TypeExpr):
            return ty.resolve(vars)
        return ty
    return f

class ParamTypeExpr(ListExpr, TypeExpr):
    __slots__ = ['data', 'ty']
    def __init__(self, data):
        super().__init__(data, TypeType)
    def __str__(self):
        return str(self.data[1]) + '[' + (','.join(map(str, self.data[2:]))) + ']'
    def __eq__(self, other):
        return self.data[1] is other or self.data[1] == other

    def keys(self):
        m = str(self.data[1])
        return [ m + str(self.data[2]), m] + super().keys()[1:]
    def joinkeys(self, keys):
        return [keys[0]+'@'+str(self.data)] + keys
    def resolve(self, vars):
        ParamType(*map(resolve_curry(vars), self.data))

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
    def __len__(self):
        return len(self.data)-2
    def __getitem__(self, item):
        return self.data[item+1]
    def joinkeys(self, keys):
        return [keys[0]+'@'+str(self.data)] + keys
    def resolve(self, vars):
        FuncType(*map(resolve_curry(vars), self.data))

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
