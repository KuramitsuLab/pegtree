from pegpy.peg import Grammar, nez
from pegpy.origami.expression import Expression
from pegpy.origami.desugar import desugar
from pegpy.origami.pprint import SourceSection, compile_code

import pegpy.utils as u

g = Grammar()
g.load('origami.tpeg')
origami_parser = nez(g['File'])

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

class Env(object):
    __slots__ = ['parent', 'ts', 'nameMap']

    def __init__(self, ts, parent = None):
        self.parent = parent
        self.ts = ts
        self.nameMap = {}

    def newLocal(self):
        return Env(self.ts, self)

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

    def asType(self, expr, ty):
        return self.ts.asType(self, expr, ty)

    def load(self, path, out):
        path = u.find_path(path, 'origami')
        f = path.open()
        data = f.read()
        f.close()
        t = origami_parser(data, path)
        self.loadTree(path, t, out)

    def loadTree(self, path, t, out):
        if t == 'err':
            out.verbose(u.serror(t.pos3()))
            return
        libs = ''
        ts = self.ts
        for _, stmt in t:
            #print(stmt)
            if stmt == 'CodeMap':
                name = stmt['name'].asString()
                psize = None
                if '@' in name:
                    name, psize = name.split('@')
                    psize = u.safeint(psize, None)
                if 'extends' in stmt:
                    tys = ts.asType(self, Expression.treeConv(stmt['extends']), None)
                    continue
                ty = ts.asType(self, Expression.treeConv(stmt['type']),None) if 'type' in stmt else None
                code = u.unquote_string(stmt['expr'].asString()) if 'expr' in stmt else None
                delim = u.unquote_string(stmt['delim'].asString()) if 'delim' in stmt else None
                d = Def(ty, libs, code, delim)
                if ty is not None and ty.isFuncType():
                    keys = Expression.makekeys(name, len(ty), ty[1])
                else:
                    keys = Expression.makekeys(name, psize, None)
                self.add(keys, d)
            elif stmt == 'Require':
                libs = stmt['file'].asString()
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
                if not '@' in key: break
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
    __slot__ = ['methodMap', 'out']
    def __init__(self, out):
        self.methodMap = {}
        self.out = out

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
        #print('@undefined', expr.tag, expr)
        return self.apply(env, expr, ty)

    VoidType = Expression.ofType('Void')
    BoolType = Expression.ofType('Bool')

    def matchType(self, given, expected):
        #print(expected, id(expected))
        #print(given, id(given))
        #print(expected == given, expected is given)
        return expected is given

    def asType(self, env, expr, ty):
        if expr.isUntyped():
            desugar(env, expr)
            method = self.lookupMethod(expr.key())
            expr = method(env, expr, ty)
        if ty is None or expr.ty is None or self.matchType(expr.ty, ty):
            return expr
        for key in Expression.makekeys(str(ty), 1, expr.ty):
            defined = env[key]
            if defined is None: continue
            expr = Expression.new('#Cast', expr, ty)
            expr.setCode(defined.getcode())
            return expr.setType(ty)
        expr = expr.err('type error {}=>{}'.format(expr.ty, ty), expr.getpos())
        return expr.setType(ty)

    def typeAt(self, env, expr, n, ty):
        if isinstance(expr[n], Expression):
            expr[n] = self.asType(env, expr[n],ty)

    def BaseType(self, env, expr, ty):
        return Expression.ofType(expr[1])

    def FuncType(self, env, expr, ty):
        return Expression.ofFuncType(*map(lambda e: self.asType(env, e, None), expr[1:]))

    def ParamType(self, env, expr, ty):
        return Expression.ofParamType(*map(lambda e: self.asType(env, e, None), expr[1:]))

    def Cast(self, env, expr, ty):
        idx = expr.find('type')
        if idx != -1:
            self.typeAt(env, expr, idx, ty)
            ty = expr[idx]
        idx = expr.find('expr', 1)
        self.typeAt(env, expr, idx, ty)
        if ty is None or expr.ty is None or self.matchType(expr.ty, ty):
            return expr
        for key in Expression.makekeys(str(ty), 1, expr[idx].ty):
            defined = env[key]
            if defined is None: continue
            expr.setCode(defined.getcode())
            return expr.setType(ty)
        expr = expr.err('type error {}=>{}'.format(expr[idx].ty, ty), expr[idx].getpos())
        return expr.setType(ty)

    def Source(self, env, expr, ty):
        if len(expr) == 1: return expr.setType(ty)
        for n in range(1, len(expr)-1):
            self.typeAt(env, expr, n, Origami.VoidType)
        self.typeAt(env, expr, -1, ty)
        return expr.setType(expr[-1].ty)

    def Block(self, env, expr, ty):
        lenv = env.newLocal()
        if len(expr) == 1: return expr.setType(ty)
        for n in range(1, len(expr)-1):
            self.typeAt(lenv, expr, n, Origami.VoidType)
        self.typeAt(lenv, expr, -1, ty)
        return expr.setType(expr[-1].ty)

    def CodeMapTree(self, env: Env, expr, ty):
        t = expr.data
        path = u.decpos3(*t.pos3())[0]
        env.loadTree(path, t, env.ts.out)
        return expr.done()

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

    def checkFuncMatch(self, expr, names):
        if expr == '#Block' and len(expr)>1:
            expr = expr[-1]
        if expr == '#Match':
            n = 0
            for case in expr:
                if case == '#Case':
                    if 'case' in case: continue
                    e = Expression.new('#Infix', '==', names[0], n)
                    case.data.append(e.label('case'))
                n += 1

    def FuncExpr(self, env, expr, ty):
        lenv = env.newLocal()
        for n in range(1, len(expr)):
            self.typeAt(lenv, expr, n, None)
        types = list(map(lambda e: e.ty, expr[1:]))
        if None not in types:
            ty = Expression.ofFuncType(*types)
            return expr.setType(ty)
        return expr

    def Return(self, env, expr, ty):
        if len(expr) == 2:
            self.typeAt(env, expr, 1, None)
            return expr.setType(expr[1].ty)
        else:
            return expr.setType('Void')

    def LetDecl(self, env, expr, ty):
        ty = None
        idx = expr.find('type')
        if idx != -1:
            self.typeAt(env, expr, idx, None)
            ty = expr[idx]
        idx = expr.find('expr', 'right')
        self.typeAt(env, expr, idx, ty)
        if ty is not None:
            idx = expr.find('name', 'left')
            name = str(expr[idx])
            expr[idx].setType(ty)
            env[name] = Def(ty, None, name)
        return expr.setType('Void')

    def VarDecl(self, env, expr, ty):
        return self.LetDecl(env, expr, ty)

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

    def Name(self, env, expr, ty):
        key = expr[1]
        defined = env[key]
        if defined is not None:
            expr.setCode(defined.getcode())
            return expr.setType(defined.ty)
        return expr.err('undefined name: ' + key)

    def If(self, env, expr, ty):
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
        op = self.apply(env, op, ty)
        if op.isUncode():
            expr.ty = op.ty
            expr[2] = op[1]
            return expr
        return op

    def Get(self, env, expr, ty):
        getter = Expression.new(expr[2], expr[1])
        getter = self.apply(env, getter, ty)
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
        binary = self.apply(env, binary, ty)
        if binary.isUncode():
            expr.ty = binary.ty
            expr[1] = binary[1]
            expr[3] = binary[2]
            return expr
        return binary

    def ApplyExpr(self, env, expr, ty):
        app = Expression.new(*expr.data)
        app = self.apply(env, app, ty)
        if app.isUncode():
            expr.ty = app.ty
            for i in range(1, len(app)):
                expr.data[i] = app[i]
            return expr
        return app

    def MethodExpr(self, env, expr, ty):
        app = ListExpr(expr.data[1:])
        app[0], app[1] = app[1], app[0]  # swap callee, funcname
        app = self.apply(env, app, ty)
        if app.isUncode():
            expr.ty = app.ty
            app[0], app[1] = app[1], app[0] # swap callee, funcname
            for i in range(0, len(app)):
                expr.data[i+1] = app[i]
            return expr
        return app

    def apply(self, env, expr, ty):
        for n in range(1, len(expr)):
            self.typeAt(env, expr, n, None)
        for key in expr.keys():
            defined = env[key]
            if defined is None: continue
            expr.setCode(defined.getcode())
            if expr.isUntyped() and defined.ty is not None:
                funcTy = defined.ty
                #print('@ret', defined.ty, defined.ty[-1])
                for n in range(1, len(expr)):
                    self.typeAt(env, expr, n, funcTy[n-1])
                expr.setType(funcTy[-1])
            if not expr.isUntyped() and not expr.isUncode():
                break
        return expr

    def Tuple(self, env, expr, ty):
        if len(expr) == 2:
            expr.tag = '#Group'
            return self.Group(env, expr, ty)
        if len(expr) == 1:
            expr.tag = '#Empty'
            return expr.setType('Void')
        for n in range(1, len(expr)):
            self.typeAt(env, expr, n, None)
        types = list(map(lambda e: e.ty, expr[1:]))
        if None not in types:
            types.insert(0, Expression.ofType('Tuple'))
            ty = Expression.ofParamType(*types)
            return expr.setType(ty)
        return expr

    def List(self, env, expr, ty):
        listty = 'List'
        valty = None
        if ty is not None and ty.isParamType():
            listty = ty[1]
            valty = ty[2]
        for n in range(1, len(expr)):
            self.typeAt(env, expr, n, valty)
        if len(expr)>1 and valty is None:
            valty = expr[1].ty
        return expr.setType(Expression.ofParamType(listty, valty))

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

    def TrueExpr(self, env, expr, ty):
        return expr.setType('Bool')

    def FalseExpr(self, env, expr, ty):
        return expr.setType('Bool')


def transpile_init(origami_files, out):
    env = Env(Origami(out))
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
    #print('@expr', e)
    env.asType(e, None)
    ss = SourceSection(out)
    ss.pushEXPR(env, e)
    return ss
