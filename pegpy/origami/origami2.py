from pegpy.peg import Grammar, nez
from pegpy.origami.expression import Expression
from pegpy.origami.desugar import desugar
from pegpy.origami.pprint import SourceSection, compile_code

import pegpy.utils as u

g = Grammar('konoha6')
g.load('konoha6.tpeg')
origami_parser = nez(g['OrigamiFile'])

class Def(object):
    __slots__ = ['ty', 'libs', 'code', 'delim']

    def __init__(self, ty, libs, code, delim = None):
        self.libs = libs
        self.ty = ty
        self.code = code
        self.delim = delim

    def __str__(self):
        return str(self.code)

    def __repr__(self):
        return repr(self.code)

    def getcode(self):
        return None if self.code is None else compile_code(self.code, self.delim)

    @classmethod
    def getkeys(cls, stmt, ty):
        iname = stmt['name'].asString()
        name = iname.split('@')[0] if '@' in iname else iname
        keys = []
        if ty is not None and ty.isFuncType():
            iname = name + '@' + str(len(ty))
            keys.append(iname + '@' + str(ty[0]))
        keys.append(iname)
        if iname != name:
            keys.append(name)
        return keys

class Env(object):
    __slots__ = ['parent', 'nameMap']

    def __init__(self, parent = None):
        self.parent = parent
        self.nameMap = {}

    def newLocal(self):
        return Env(self)

    def __contains__(self, item):
        if item in self.nameMap:
            return True
        if self.parent is not None:
            return item in self.parent
        return False

    def __getitem__(self, item):
        if item in self.nameMap:
            return self.nameMap[item]
        if self.parent is not None:
            return self.parent[item]
        return None

    def __setitem__(self, item, value):
        self.nameMap[item] = value

    def load(self, path, out):
        path = u.find_path(path, 'origami')
        f = path.open()
        data = f.read()
        f.close()
        t = origami_parser(data, path)
        if t == 'err':
            out.verbose(u.serror(t.pos3()))
            return
        libs = None
        for _, stmt in t:
            #print(stmt)
            if stmt == 'CodeMap':
                ty = Expression.ofType(Expression.treeConv(stmt['type'])) if 'type' in stmt else None
                keys = Def.getkeys(stmt, ty)
                code = u.unquote_string(stmt['expr'].asString()) if 'expr' in stmt else None
                delim = u.unquote_string(stmt['delim'].asString()) if 'delim' in stmt else None
                d = Def(ty, libs, code, delim)
                self.add(keys, d)
            elif stmt == 'Include':
                file = stmt['file'].asString()
                file = u.find_importPath(path.absolute(), file)
                out.verbose('loading...', file)
                self.load(file, out)
        #print('DEBUG', self.nameMap)

    def add(self, keys, defined):
        if isinstance(keys, str):
            self[keys] = defined
        else:
            self[keys[0]] = defined
            for key in keys[1:]:
                if not key in self:
                    self[key] = defined

    def addName(self, name, ty):
        self[name] = Def(ty, None, None)

    def inferName(self, name):
        if name[-1] in "0123456789'_": name = name[:-1]
        if name in self:
            ty = self[name].ty
            if ty is not None: return ty
        if len(name) >= 2:
            return self.inferName(name[1:])
        return None

## Typing

class Origami(object):
    __slot__ = ['methodMap']
    def __init__(self):
        self.methodMap = {}

    def lookupMethod(self, key):
        if key in self.methodMap:
            return self.methodMap[key]
        if key.startswith('#'):
            name = key.replace('#', '')
            if hasattr(self, name):
                self.methodMap[key] = getattr(self, name)
                return self.methodMap[key]
        if key.endswith('Expr'):
            name = key[1:].replace('Expr', '')
            if hasattr(self, name):
                self.methodMap[key] = getattr(self, name)
                return self.methodMap[key]
        return self.undefined

    def undefined(self, env, expr, ty):
        if expr.tag.endswith('Type'):
            ty = Expression.addType(str(expr), expr)
            return ty
        #print('@undefined', expr.tag, expr)
        return self.Apply(env, expr, ty)

    VoidType = Expression.ofType('Void')
    BoolType = Expression.ofType('Bool')

    def asType(self, env, expr, ty):
        if expr.isUntyped():
            desugar(env, expr)
            expr = self.tryType(env, expr, ty)
        if ty is None or expr.ty is None or expr.ty is ty:
            return expr
        for key in Expression.makekeys(str(ty), 1, expr.ty):
            defined = env[key]
            if defined is None: continue
            expr = Expression.new('#Cast', expr, ty)
            expr.setCode(defined.getcode())
            return expr.setType(ty)
        return expr.err('Type Error: Expected={} Given={}'.format(ty, expr.ty))

    def tryType(self, env, expr, ty):
        method = self.lookupMethod(expr.key())
        return method(env, expr, ty)

    def typeAt(self, env, expr, n, ty):
        if isinstance(expr[n], Expression):
            expr[n] = self.asType(env, expr[n],ty)

    def CastExpr(self, env, expr, ty):
        self.typeAt(env, expr, 1, None)
        ty = expr[2]
        for key in Expression.makekeys(str(ty), 1, expr[1].ty):
            defined = env[key]
            if defined is None: continue
            expr.setCode(defined.getcode())
            return expr.setType(ty)
        if expr[1].ty is not None:
            expr = expr.err('undefined cast {}=>{}'.format(expr[1].ty, ty), expr[2].getpos())
        return expr.setType(ty)

    def Scope(self, env, expr, ty):
        lenv = env.newLocal()
        if len(expr) == 1: return expr.setType(ty)
        for n in range(1, len(expr)-1):
            self.typeAt(lenv, expr, n, Origami.VoidType)
        self.typeAt(lenv, expr, -1, ty)
        return expr.setType(expr[-1].ty)

    def Block(self, env, expr, ty):
        if len(expr) == 1: return expr.setType(ty)
        for n in range(1, len(expr)-1):
            self.typeAt(env, expr, n, Origami.VoidType)
        self.typeAt(env, expr, -1, ty)
        return expr.setType(expr[-1].ty)

    def AssumeDecl(self, env, expr, ty):
        ty = expr[-1]
        for name in expr[1:-1]:
            env.addName(str(name), ty)
        return expr.done()

    def FuncDecl(self, env, expr, ty):
        lenv = env.newLocal()
        for n in range(2, len(expr)):
            self.typeAt(lenv, expr, n, None)
        idx = expr.find('type')
        if idx != -1:
            ret = expr[idx]
            expr.remove(idx)
            expr[1].ty = ret
        else:
            expr[1].ty = expr[-1].ty
        types = list(map(lambda e: e.ty, expr[2:]))
        if None not in types:
            ty = Expression.ofFuncType(*types)
            keys = Expression.makekeys(str(expr[1]), len(types)-1, ty[0])
            env.add(keys, Def(ty, None, None))
        return expr.setType('Void')

    def Param(self, env, expr, ty):
        name = str(expr[1])
        if len(expr) == 2:
            ty = env.inferName(name)
        else:
            ty = expr[2]
        env[name] = Def(ty, None, name)
        if ty is None:
            return expr.err('untyped ' + name)
        expr[1].setType(ty)
        expr.data.append(ty)
        return expr.setType('Void')

    def Return(self, env, expr, ty):
        if len(expr) == 2:
            self.typeAt(env, expr, 1, None)
            return expr.setType(expr[1].ty)
        else:
            return expr.setType('Void')

    def FuncExpr(self, env, expr, ty):
        lenv = env.newLocal()
        for n in range(1, len(expr)):
            self.typeAt(lenv, expr, n, None)
        types = list(map(lambda e: e.ty, expr[1:]))
        if None not in types:
            ty = Expression.ofFuncType(*types)
            return expr.setType(ty)
        return expr

    def LetDecl(self, env, expr, ty):
        if len(expr) == 3:
            self.typeAt(env, expr, 2, None)
            ty = expr[2].ty
        else:
            ty = expr[2]
            self.typeAt(env, expr, 3, ty)
        if ty is not None:
            name = str(expr[1])
            env[name] = Def(ty, None, name)
        return expr.setType('Void')

    def VarDecl(self, env, expr, ty):
        if len(expr) == 3:
            self.typeAt(env, expr, 2, None)
            ty = expr[2].ty
        else:
            ty = expr[2]
            self.typeAt(env, expr, 3, ty)
        if ty is not None:
            name = str(expr[1])
            env[name] = Def(ty, None, name)
        return expr.setType('Void')

    def Assign(self, env, expr, ty):
        left = expr[1]
        if left == '#GetExpr':
            setter = Expression.new(left[2], left[1], expr[2])
            setter = self.Apply(env, setter, ty)
            if not setter.isUncode(): return setter
        elif left == '#IndexExpr':
            pass
        self.typeAt(env, expr, 1, None)
        ty = expr[2].ty
        self.typeAt(env, expr, 2, ty)
        return expr.setType('Void')

    def Var(self, env, expr, ty):
        key = expr.asSymbol()
        defined = env[key]
        if defined is not None:
            expr.setCode(defined.getcode())
            return expr.setType(defined.ty)
        return expr.err('Undefined Name: ' + key)

    def IfExpr(self, env, expr, ty):
        self.typeAt(env, expr, 1, Origami.BoolType)
        if len(expr) == 4:
            self.typeAt(env, expr, 2, ty)
            self.typeAt(env, expr, 3, expr[2].ty)
            return expr.setType(expr[3].ty)
        else:
            self.typeAt(env, expr, 2, Origami.VoidType)
            return expr.setType(Origami.VoidType)

    def Group(self, env, expr, ty):
        self.typeAt(env, expr, 1, ty)
        return expr.setType(expr[1].ty)

    def Unary(self, env, expr, ty):
        op = Expression(expr[1], expr[2])
        op = self.Apply(env, op, ty)
        if op.isUncode():
            expr.ty = op.ty
            expr[2] = op[1]
            return expr
        return op

    def GetExpr(self, env, expr, ty):
        getter = Expression.new(expr[2], expr[1])
        getter = self.Apply(env, getter, ty)
        if getter.isUncode():
            expr.ty = getter.ty
            expr[1] = getter[1]
            if expr[1].ty is not None and expr[1].ty.isDataType():
                name = str(expr[2])
                dataty = expr[1].ty
                if not name in dataty:
                    return expr.err('undefined name: {} in {}'.format(name, dataty))
                return expr.setType(env.inferName(name))
            return expr
        return getter

    def Infix(self, env, expr, ty):
        binary = Expression.new(expr[2], expr[1], expr[3])
        binary = self.Apply(env, binary, ty)
        if binary.isUncode():
            expr.ty = binary.ty
            expr[1] = binary[1]
            expr[3] = binary[2]
            return expr
        return binary

    def ApplyExpr(self, env, expr, ty):
        app = Expression.new(*expr.data[1:])
        app = self.Apply(env, app, ty)
        if app.isUncode():
            expr.ty = app.ty
            for i in range(0, len(app)):
                expr.data[i+1] = app[i]
            return expr
        return app

    def MethodExpr(self, env, expr, ty):
        app = ListExpr(expr.data[1:])
        app[0], app[1] = app[1], app[0]  # swap callee, funcname
        app = self.Apply(env, app, ty)
        if app.isUncode():
            expr.ty = app.ty
            app[0], app[1] = app[1], app[0] # swap callee, funcname
            for i in range(0, len(app)):
                expr.data[i+1] = app[i]
            return expr
        return app

    def Apply(self, env, expr, ty):
        for n in range(1, len(expr)):
            self.typeAt(env, expr, n, None)
        #print('@keys', expr.keys())
        for key in expr.keys():
            defined = env[key]
            #print(key, defined)
            if defined is None: continue
            expr.setCode(defined.getcode())
            if expr.isUntyped() and defined.ty is not None:
                expr.setType(defined.ty[-1])
                for n in range(1, len(expr)):
                    self.typeAt(env, expr, n, defined.ty[n-1])
            if not expr.isUntyped() and not expr.isUncode():
                break
        return expr

    def TupleExpr(self, env, expr, ty):
        if len(expr) == 2:
            expr.data[0].data = '#Group'
            return self.Group(env, expr, ty)
        for n in range(1, len(expr)):
            self.typeAt(env, expr, n, None)
        types = list(map(lambda e: e.ty, expr[1:]))
        if None not in types:
            ty = Expression.ofParamType(['Tuple', *types])
            return expr.setType(ty)
        return expr

    def TrueExpr(self, env, expr, ty):
        return expr.setType('Bool')

    def FalseExpr(self, env, expr, ty):
        return expr.setType('Bool')

    def Int(self, env, expr, ty):
        return expr.setType('Int')

    def Float(self, env, expr, ty):
        return expr.setType('Float')

    def Double(self, env, expr, ty):
        return expr.setType('Double')

    def String(self, env, expr, ty):
        return expr.setType('String')

    def Char(self, env, expr, ty):
        return expr.setType('Char')


def transpile_init(origami_files, out):
    env = Env()
    if len(origami_files) == 0:
        origami_files.append('common.origami')
    for file in origami_files:
        env.load(file, out)
    return env

def transpile(env, t, out):
    if t == 'err':
        out.perror(t.pos3(), 'Syntax Error')
        return
    e = Expression.treeConv(t)
    print('@expr', e)
    Origami().asType(env, e, None)
    ss = SourceSection(out)
    ss.pushEXPR(env, e)
    return ss
