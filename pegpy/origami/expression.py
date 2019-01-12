import pegpy.utils as u

## Value

class ValueExpr(object):
    pass

class StringExpr(ValueExpr):
    __slots__ = ['data']

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return '"' + str(self.data) + '"'

class CharExpr(ValueExpr):
    __slots__ = ['data']

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "'" + str(self.data) + "'"

TypeType = None

class Expression(object):

    intern = u.string_intern()

    __slots__ = ['tag', 'data', 'pos3', 'context', 'ty', 'code']

    def __init__(self, tag, data, pos3 = None, ty = None):
        self.context = None
        self.tag = Expression.intern(tag)
        self.data = data
        self.pos3 = pos3
        self.ty = ty
        self.code = None

    def __str__(self):
        if self.isType():
            if self.isFuncType():
                return 'Func[' + ','.join(map(str, self.data)) + ']'
            if self.isParamType():
                return str(self.data[0]) + '[' + ','.join(map(str, self.data[1:])) + ']'
        if isinstance(self.data, list):
            return '(' + self.tag + ' ' + (' '.join(map(str, self.data))) + ')'
        return str(self.data)

    def __repr__(self):
        return str(self)

    def __len__(self):
        if isinstance(self.data, list):
            return len(self.data) + 1
        return 2

    def __getitem__(self, item):
        if isinstance(item, slice):
            # do your handling for a slice object:
            dec = lambda x : x if x is None else x-1
            return self.data[dec(item.start): dec(item.stop): item.step]
        else:
            if item < 0: item = len(self) + item
            if item == 0:
                return self.tag
            if item == 1 and not isinstance(self.data, list):
                return self.data
            return self.data[item - 1]

    def __setitem__(self, item, value):
        if item < 0: item = len(self) + item
        if item == 0:
            self.tag = value
        elif item == 1 and not isinstance(self.data, list):
            self.data = value
        else:
            self.data[item - 1] = value

    def find(self, *argv):
        if isinstance(self.data, list):
            for i, e in enumerate(self.data):
                if e.context in argv:
                    return i+1
        return -1

    def remove(self, idx):
        if idx > 0 and isinstance(self.data, list):
            del self.data[idx-1]

    def key(self):
        return self.tag

    def keys(self):
        if isinstance(self.data, list):
            return Expression.makekeys(self.tag, len(self.data), self.data[0].ty if len(self.data) > 0 else None)
        return [self.tag]

    ARGS = ['[]', '[a]', '[a,b]', '[a,b,c]', '[a,b,c,d]']

    def typekeys(self):
        if self.isParamType():
            [str(self), str(self.data[0]) + Expression.ARGS[len(self.data)-1]]
        return [str(self)]

    def isType(self):
        return self.tag.endswith('Type')

    def isFuncType(self):
        return self.tag.endswith('#FuncType')

    def isParamType(self):
        return self.tag.endswith('#ParamType')

    def getpos(self):
        if self.pos3 is not None:
            return self.pos3
        if isinstance(self.data, list):
            for e in self.data:
                pos3 = e.getpos()
                if pos3 is not None: return pos3
        return None

    def emit(self, env, ss):
        ss.pushSTR(str(self))

    def __eq__(self, symbol):
        return self.tag == symbol

    def isUntyped(self):
        return self.ty is None

    def setType(self, ty):
        if ty is not None:
            self.ty = Expression.ofType(ty)
        return self

    def isUncode(self):
        return self.code is None

    def setCode(self, code):
        if code is not None and self.code is None:
            self.code = code
        return self

    def err(self, msg, pos3 = None):
        e = Expression('#Error', self, self.getpos() if pos3 is None else pos3)
        e.context = msg
        return e

    def emit(self, env, ss):
        ss.pushSTR(str(self))

    def done(self):
        self.setType('Void')
        self.setCode([])
        return self

    ## class

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

    @classmethod
    def new(cls, *argv):
        tag = str(argv[0])
        cons = []
        for e in argv[1:]:
            if isinstance(e, Expression) :
                cons.append(e)
            else:
                cons.append(Expression.valueOf(e))
        if isinstance(argv[0], Expression):
            return Expression(tag, cons, argv[0].getpos())
        return Expression(tag, cons)

    @classmethod
    def new2(cls, tag, value):
        if isinstance(tag, Expression):
            return Expression(str(tag), value, tag.getpos())
        return Expression(tag, value)

    @classmethod
    def valueOf(cls, v):
        if isinstance(v, int):
            return Expression('#IntExpr', v)
        if isinstance(v, float):
            return Expression('#DoubleExpr', v)
        if isinstance(v, list):
            return Expression.new(*v)
        if v == True:
            return Expression('#TrueExpr', v)
        if v == False:
            return Expression('#FalseExpr', v)
        return Expression('#StringExpr', StringExpr(str(v)))

    VALUE_RULES = {
        'IntExpr': lambda s: int(s),
        'DoubleExpr': lambda s: float(s),
        'StringExpr': lambda s: StringExpr(s),
        'CharExpr': lambda s: CharExpr(s),
    }

    @classmethod
    def addValueRule(cls, key, conv):
        Expression.VALUE_RULES[key] = conv

    @classmethod
    def treeConv(cls, t):
        tag = '#' + t.tag
        cons = []
        for n, v in t:
            e = Expression.treeConv(v)
            e.context = n
            cons.append(e)
        if len(cons) > 0 or (tag == '#' and len(cons) == 0):
            return Expression(tag, cons, t.pos3())
        s = t.asString()
        if tag in Expression.VALUE_RULES:
            Expression(tag, Expression.VALUE_RULES[tag](s), t.pos3())
        return Expression(tag, s, t.pos3())

    TYPES = {}

    @classmethod
    def addType(cls, key, ty):
        Expression.TYPES[key] = ty
        ty.ty = TypeType
        return ty

    @classmethod
    def ofType(cls, ty):
        if isinstance(ty, str):
            if not ty in Expression.TYPES:
                return Expression.addType(ty, Expression('#BaseType', ty))
            return Expression.TYPES[ty]
        key = str(ty)
        if not key in Expression.TYPES:
            return Expression.addType(key, ty)
        return ty

    @classmethod
    def ofParamType(cls, *types):
        types = list(map(Expression.ofType, types))
        ty = Expression('#ParamType', types)
        key = str(ty)
        if not key in Expression.TYPES:
            return Expression.addType(key, ty)
        return Expression.TYPES[key]

    @classmethod
    def ofFuncType(cls, *types):
        types = list(map(Expression.ofType, types))
        ty = Expression('#FuncType', types)
        key = str(ty)
        if not key in Expression.TYPES:
            return Expression.addType(key, ty)
        return Expression.TYPES[key]

    '''
    @classmethod
    def ofDataType(cls, *names):
        names = list(names)
        names.sort()
        key = DataTypeExpr.typekey(names)
        if not key in SExpr.TYPES:
            SExpr.addType(DataTypeExpr(names))
        return SExpr.TYPES[key]
    '''

TypeType = Expression.ofType('Type')
TypeType.ty = TypeType