from pathlib import Path
import pegpy.utils as u

## Value

class String(object):
    __slots__ = ['data']
    def __init__(self, data):
        self.data = data
    def __str__(self):
        return '"' + str(self.data) + '"'

class Char(object):
    __slots__ = ['data']
    def __init__(self, data):
        self.data = data
    def __str__(self):
        return "'" + str(self.data) + "'"

## SExpression

class SExpr(object):

    STNTAX_RULES = {
        'Symbol' : lambda t, rules: t.asString(),
        'NameExpr' : lambda t, rules: t.asString(),
        'IntExpr': lambda t, rules: int(t.asString()),
        'DoubleExpr': lambda t, rules: float(t.asString()),
        'StringExpr': lambda t, rules: String(t.asString()),
        'CharExpr': lambda t, rules: Char(t.asString()),
    }

    @classmethod
    def addRule(cls, key, conv):
        SExpr.STNTAX_RULES[key] = conv

    @classmethod
    def flatadd(cls, l, e):
        if isinstance(e, ListExpr) and len(e) > 1 and e.first() == '#':
            for e2 in e.data[1:]: l.append(e2)
        else:
            l.append(e)

    intern = u.string_intern()

    @classmethod
    def of(cls, t, rules = STNTAX_RULES):
        tag = t.tag
        if tag in rules:
            e = rules[tag](t, rules)
            return e if isinstance(e, SExpr) else AtomExpr(e, t.pos3())
        cons = []
        cons.append(AtomExpr(SExpr.intern("#" + tag), t.pos3()))
        for n, v in t:
            SExpr.flatadd(cons, SExpr.of(v, rules))
        return ListExpr(cons)

    @classmethod
    def new(cls, *argv):
        cons = []
        for e in argv:
            if isinstance(e, SExpr) :
                cons.append(e)
            else:
                cons.append(AtomExpr(e))
        return ListExpr(cons)

    '''TODO
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
    '''

    TYPES = {}

    @classmethod
    def addType(cls, ty):
        SExpr.TYPES[str(ty)] = ty
        return ty

    @classmethod
    def ofType(cls, ty):
        if isinstance(ty, str):
            if not ty in SExpr.TYPES:
                SExpr.addType(BaseTypeExpr(ty))
            return SExpr.TYPES[ty]
        assert isinstance(ty, TypeExpr)
        return ty

    @classmethod
    def ofParamType(cls, *types):
        types = list(map(SExpr.ofType, types))
        key = ParamTypeExpr.typekey(types)
        if not key in SExpr.TYPES:
            SExpr.addType(ParamTypeExpr(types))
        return SExpr.TYPES[key]

    @classmethod
    def ofFuncType(cls, *types):
        types = list(map(SExpr.ofType, types))
        key = FuncTypeExpr.typekey(types)
        if not key in SExpr.TYPES:
            SExpr.addType(FuncTypeExpr(types))
        return SExpr.TYPES[key]

    @classmethod
    def ofDataType(cls, *names):
        names = list(names)
        names.sort()
        key = DataTypeExpr.typekey(names)
        if not key in SExpr.TYPES:
            SExpr.addType(DataTypeExpr(names))
        return SExpr.TYPES[key]

    @classmethod
    def makekeys(cls, key, n = None, ty = None):
        if '@' in key:
            name = key.split('@')[0]
            pname = key
        else:
            if n is None: return [key]
            name = key
            pname = key + '@' + str(n)
        if ty is None:
            return [pname, name]
        l = []
        for tkey in ty.typekeys():
            l.append(pname + '@' + tkey)
        l.append(pname)
        l.append(name)
        return l

    def __repr__(self):
        return str(self)

    def __eq__(self, symbol):
        return self.asSymbol() == symbol

    def isUntyped(self):
        return self.ty is None

    def setType(self, ty):
        if ty is not None:
            self.ty = SExpr.ofType(ty)
        return self

    def isUncode(self):
        return self.code is None

    def setCode(self, code):
        if code is not None and self.code is None:
            self.code = code
        return self

    def err(self, msg, pos3 = None):
        return ErrorExpr(msg, self, pos3)

    def keys(self):
        return []

    def emit(self, env, ss):
        ss.pushSTR(str(self))

    def done(self):
        self.setType('Void')
        self.setCode([])
        return self


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

    def emit(self, env, ss):
        ss.pushSTR(str(self))


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

    def __setitem__(self, key, value):
        self.data[key] = value

    def isSymbol(self):
        return isinstance(self.data[0], AtomExpr)

    def asSymbol(self): return self.data[0].asSymbol()


    def first(self):
        return str(self.data[0])

    def keys(self):
        return SExpr.makekeys(str(self.data[0]), len(self)-1,
                       self.data[1].ty if len(self) > 1 else None)

    def getpos(self):
        for e in self.data:
            pos3 = e.getpos()
            if pos3 is not None: return pos3
        return None

class ErrorExpr(SExpr):
    __slots__ = ['data', 'pos3', 'msg', 'ty', 'code']

    def __init__(self, msg, data: SExpr, pos3 = None):
        self.data = data
        self.pos3 = data.getpos() if pos3 is None else pos3
        self.msg = msg
        self.ty = data.ty
        self.code = None

    def __str__(self):
        return '(* {} {} *)'.format(self.msg, self.data)

    def getpos(self):
        return self.data.getpos()

    def emit(self, env, ss):
        ss.perror(self.pos3, self.msg)
        ss.pushEXPR(env, self.data)

## Type

def typestr(ty):
    return '?' if ty is None else str(ty)

def resolve_curry(vars):
    def f(ty):
        if isinstance(ty, TypeExpr):
            return ty.resolve(vars)
        return ty
    return f


class TypeExpr(object):

    def isFuncType(self): return False

    def isVarType(self): return False

    def isDataType(self): return False

    '''
    def match(self, ty, vars = {}):
        if self is ty: return True
        if len(self.data) == len(ty.data) and self.data[0] == ty.data[0]:
            for t1,t2 in zip(self.data[1:], ty.data[1:]):
                if not t1.match(t2, vars): return False
            return True
        return False
    '''
TypeType = None

class BaseTypeExpr(AtomExpr, TypeExpr):
    __slots__ = ['data', 'pos3', 'ty']

    def __init__(self, data, ty = None):
        super().__init__(data, None, TypeType)

    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        return self is other or self.data == other

    def isVarType(self):
        return len(self.data) == 1 and self.data.islower()

    def keys(self):
        return ['#' + str(self.data)]

    def typekeys(self):
        return [str(self.data)]

    '''
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
    '''

TypeType = SExpr.addType(BaseTypeExpr('Type'))
TypeType.ty = TypeType

''''
def BaseType(n: str):
    if not n in typeMap:
        typeMap[n] = BaseTypeExpr(n, TypeType)
    return typeMap[n]


def tyconv(ty):
    if isinstance(ty, TypeExpr):
        return ty
    return BaseType(str(ty))
'''


# ParamType

class ParamTypeExpr(ListExpr, TypeExpr):
    __slots__ = ['data', 'ty']

    def __init__(self, data):
        super().__init__(data, TypeType)

    def __str__(self):
        return ParamTypeExpr.typekey(self.data)

    def __eq__(self, other):
        return self.data[1] is other or self.data[1] == other

    @classmethod
    def typekey(cls, types):
        return str(types[0]) + '[' + (','.join(map(str, types[1:]))) + ']'

    def keys(self):
        raw = '#' + str(self.data[0])
        return [ raw + str(self.data[1]), raw, '#ParamType' ]

    '''
    def resolve(self, vars):
        ParamType(*map(resolve_curry(vars), self.data))
    '''

#FuncType

class FuncTypeExpr(ListExpr, TypeExpr):

    __slots__ = ['data', 'ty']

    def __init__(self, data):
        super().__init__(data, TypeType)

    @classmethod
    def typekey(cls, types):
        return 'FuncType['+ (','.join(map(str, types)))+']'

    def __str__(self):
        return FuncTypeExpr.typekey(self.data)

    def isFuncType(self):
        return True

    def __len__(self):
        return len(self.data)-1

    def __getitem__(self, item):
        return self.data[item]

    def ret(self):
        return self.data[-1]

    def keys(self):
        return [ '#'+ str(self), '#FuncType' ]

    def typekeys(self):
        return [str(self)]

    '''
    def resolve(self, vars):
        FuncType(*map(resolve_curry(vars), self.data))
    '''

'''
def FuncType(*types):
    types = list(map(tyconv, types))
    key = 'F(' + '->'.join(map(str, types)) + ')'
    if not key in typeMap:
        typeMap[key] = FuncTypeExpr(['functype', *types])
    return typeMap[key]
'''

#DataType

class DataTypeExpr(ListExpr, TypeExpr):
    __slots__ = ['data', 'ty']

    def __init__(self, data):
        super().__init__(data, TypeType)

    @classmethod
    def typekey(cls, names):
        return '{'+ (','.join(names))+'}'

    def __str__(self):
        return DataTypeExpr.typekey(self.data)

    def isDataType(self):
        return True

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def keys(self):
        return ['#DataType']

    def typekeys(self):
        return [str(self)]


## TypeRule

def BaseTypeRule(t, rules):
    return SExpr.ofType(t.asString())

def ParamTypeRule(t, rules):
    types = [SExpr.of(t['base'], rules)]
    for l,se in t['params']:
        types.append(SExpr.of(se, rules))
    return SExpr.ofParamType(*types)

def FuncTypeRule(t, rules):
    types = []
    base = t['base']
    if base.tag == 'TupleType':
        for l,se in t['base']:
            types.append(SExpr.of(se, rules))
    else:
        types.append(SExpr.of(base, rules))
    types.append(SExpr.of(t['type'], rules))
    return SExpr.ofFuncType(*types)

def DataTypeRule(t, rules):
    names = []
    for _,name in t:
        names.append(name.asString())
    return SExpr.ofDataType(*names)

SExpr.addRule('BaseType', BaseTypeRule)
SExpr.addRule('ParamType', ParamTypeRule)
SExpr.addRule('FuncType', FuncTypeRule)
SExpr.addRule('DataType', DataTypeRule)


