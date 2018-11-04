#
import pegpy.origami.sexpr as e

class TypeExpr(object):
    def isFuncType(self): return False

class SimpleTypeExpr(e.AtomExpr, TypeExpr):
    __slots__ = ['data', 'pos3', 'ty']
    def __init__(self, data, ty = None):
        super().__init__(data, None, ty)
    def joinkeys(self, keys):
        return [keys[0]+'@'+str(self.data)] + keys

typeMap = {
    'Type': SimpleTypeExpr(e.Type('Type'))
}

TypeType =typeMap['Type']
TypeType.ty = TypeType

def SimpleType(n):
    if not n in typeMap:
        typeMap[n] = SimpleTypeExpr(e.Type(n), TypeType)
    return typeMap[n]


IntType = SimpleType('Int')

def tyconv(ty):
    if isinstance(ty, e.SExpr):
        return ty
    return SimpleType(str(ty))

class ParamTypeExprExpr(e.ListExpr, TypeExpr):
    __slots__ = ['data', 'ty']
    def __init__(self, data):
        super().__init__(data, TypeType)
    def keys(self):
        m = str(self.data[1])
        return [ m + str(self.data[2]), m] + super().keys()
    def joinkeys(self, keys):
        return [keys[0]+'@'+str(self.data)] + keys

def ParamType(*types):
    types = list(map(tyconv, types))
    key = ' '.join(map(str, types))
    if not key in typeMap:
        typeMap[key] = ParamTypeExprExpr(['paramtype', *types])
    return typeMap[key]

class FuncTypeExprExpr(e.ListExpr, TypeExpr):
    __slots__ = ['data', 'ty']
    def __init__(self, data):
        super().__init__(data, TypeType)
    def isFuncType(self):
        return True
    def joinkeys(self, keys):
        return [keys[0]+'@'+str(self.data)] + keys

def FuncType(*types):
    types = list(map(tyconv, types))
    key = 'F(' + '->'.join(map(str, types)) + ')'
    if not key in typeMap:
        typeMap[key] = FuncTypeExprExpr(['functype', *types])
    return typeMap[key]

class Env(object):
    __slots__ = ['parent', 'typeMap']

    def __init__(self, parent):
        self.parent = parent
        self.typeMap = {}

    def add(self, iname: str, ty):
        if isinstance(ty, str):
            ty = SimpleType(ty)
        self.typeMap[iname] = iname

    def __contains__(self, item):
        if item in self.typeMap:
            return True
        if self.parent is not None:
            return item in self.parent
        return False

    def __getitem__(self, item):
        if item in self.typeMap:
            return self.typeMap[item]
        if self.parent is not None:
            return self.parent[item]
        return None

