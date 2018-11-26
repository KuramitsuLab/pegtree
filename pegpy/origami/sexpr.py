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
        'NullExpr': lambda t: 'null',
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

    @classmethod
    def ofType(cls, ty):
        return BaseType(ty) if isinstance(ty, str) else ty

    @classmethod
    def makekeys(cls, key, n, ty = None):
        key2 = key + '@' + str(n)
        l = []
        if ty is not None:
            for tkey in ty.typekeys():
                l.append(key2 + '@' + str(tkey))
        l.append(key2)
        l.append(key)
        return l

    def isUntyped(self):
        return self.ty is None

    def setType(self, ty):
        self.ty = BaseType(ty) if isinstance(ty, str) else ty
        return self

    def isUncode(self):
        return self.code is None

    def setCode(self, code):
        if code is not None and self.code is None:
            self.code = code
        return self

    def err(self, msg):
        return ErrorExpr(msg, self.getpos())

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

    def asSymbol(self):
        return self.data if isinstance(self.data, str) else '#V' + type(self.data).__name__

    def first(self):
        return self

    def keys(self):
        return ['#' + type(self.data).__name__, str(self.data)]

    def getpos(self):
        return self.pos3

    def perror(self):
        return False

class ListExpr(SExpr):
    __slots__ = ['data', 'ty', 'code']
    def __init__(self, data, ty = None):
        self.data = list(data)
        self.ty = ty
        self.code = None

    def __str__(self):
        return '(' + (' '.join(map(str, self.data))) + ')'

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def isSymbol(self):
        return isinstance(self.data[0], AtomExpr)

    def asSymbol(self):
        return self.data[0].asSymbol()

    def first(self):
        return str(self.data[0])

    def keys(self):
        return SExpr.makekeys(str(self.data[0]), len(self)-1,
                       self.data[1].ty if len(self) > 1 and not self.data[1].isUntyped() else None)

    def getpos(self):
        for e in self.data:
            pos3 = e.getpos()
            if pos3 is not None: return pos3
        return None

    def perror(self):
        res = False
        for e in self.data:
            if e.perror(): res = True
        return res

class ErrorExpr(SExpr):
    __slots__ = ['data', 'pos3', 'ty']

    def __init__(self, msg, pos3 = None):
        self.data = msg
        self.pos3 = pos3
        self.ty = None

    def __str__(self):
        return '<<{}>>'.format(self.data)

    def getpos(self):
        return self.pos3

    def perror(self):
        u.perror(self.pos3, self.data)
        return True





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

    def keys(self):
        return [str(self.data)]

    def typekeys(self):
        return [str(self.data)]

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

    def typekeys(self):
        return [str(self.data), str(self.data[1])]

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

    def ret(self):
        return self.data[-1]

    def typekeys(self):
        return [str(self)]

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


