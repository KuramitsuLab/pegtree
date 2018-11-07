#
import pegpy.origami.sexpr as e

class Env(object):
    __slots__ = ['parent', 'typeMap']

    def __init__(self, parent):
        self.parent = parent
        self.typeMap = {}

    def add(self, iname: str, ty):
        if isinstance(ty, str):
            ty = e.BaseType(ty)
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

