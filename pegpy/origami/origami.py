from pegpy.peg import Grammar, nez
from pegpy.origami.sexpr import SExpr, AtomExpr
import pegpy.utils as u

g = Grammar('konoha6')
g.load('konoha6.tpeg')
origami_parser = nez(g['OrigamiFile'])

def getkeys(stmt, ty):
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

class Def(object):
    __slots__ = ['ty', 'libs', 'code', 'delim']
    def __init__(self, ty, libs, code, delim):
        self.ty = ty
        self.libs = libs
        self.code = code
        self.delim = delim
    def __str__(self):
        return str(self.code)
    def __repr__(self):
        return repr(self.code)

class Env(object):
    __slots__ = ['parent', 'nameMap']

    def __init__(self, parent = None):
        self.parent = parent
        self.nameMap = {}

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

    def load(self, path):
        f = u.find_path(path, 'origami').open()
        data = f.read()
        f.close()
        t = origami_parser(data, path)
        if t == 'err':
            er = t.getpos()
            print('SyntaxError ({}:{}:{}+{})'.format(er[0], er[2], er[3], er[1]), '\n', er[4], '\n', er[5])
            return
        libs = tuple([])
        for _, stmt in t:
            #print(stmt)
            if stmt == 'CodeMap':
                ty = stmt.get('type', None, lambda t: SExpr.of(t))
                keys = getkeys(stmt, ty)
                expr = u.unquote_string(stmt['expr'].asString()) if 'expr' in stmt else None
                delim = u.unquote_string(stmt['delim'].asString()) if 'delim' in stmt else ' '
                d = Def(ty, libs, expr, delim)
                self[keys[0]] = d
                for key in keys[1:]:
                    if not key in self:
                        self[key] = d
        #print('DEBUG', self.nameMap)


class SourceSection(object):
    __slots__ = ['sb', 'indent', 'tab', 'lf']
    def __init__(self, indent = 0, tab = '   ', lf = '\n'):
        self.sb = []
        self.indent = indent
        self.tab = tab
        self.lf = lf

    def __repr__(self):
        return ''.join(self.sb)

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

    def pushEXPR(self, env, e):
        if isinstance(e, SExpr):
            if e.code is not None:
                self.pushFMT(e.code, e.data)
            else:
                keys = e.keys()
                for key in keys:
                    if key in env:
                        d = env[key]
                        if hasattr(d, 'emit'):
                            d.emit(env, e, self)
                        else:
                            self.pushFMT(env, d.code, d.delim, e.data)
                        return
                self.pushSTR(str(e))
        else:
            self.pushSTR(str(e))

    def pushFMT(self, env, code: str, delim:str, args: list):
        index = 1
        start = 0
        i = 0
        while i < len(code):
            c = code[i]
            i += 1
            if c == '\t' :
                self.pushSTR(code[start: i - 1])
                start = i
                self.pushTAB()
                continue
            if c == '\f' :
                self.pushSTR(code[start: i - 1])
                start = i
                self.incIndent()
                continue
            if c == '\b' :
                self.pushSTR(code[start: i - 1])
                start = i
                self.decIndent()
                continue
            if c == '\n':
                self.pushSTR(code[start: i - 1])
                start = i
                self.pushLF()
                continue
            if c == '%':
                c = code[i] if i < len(code) else '%'
                i += 1
                if c == '%':
                    self.pushSTR(code[start: i - 1])
                    start = i
                    continue
                self.pushSTR(code[start: i - 2])
                start = i
                if '0' <= c and c <= '9':
                    index = int(c)
                    self.pushEXPR(env, args[index])
                    index +=1
                    continue
                if c == 's':
                    self.pushEXPR(env, args[index])
                    index += 1
                    continue
                if c == '*':
                    cnt = 0
                    for a in args[index:]:
                        if cnt > 0 : self.pushDELIM(delim)
                        self.pushEXPR(env, a)
                        cnt += 1
                    continue
        #end while
        self.pushSTR(code[start:])

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


def transpile(t, origami_files = ['common.origami']):
    env = Env()
    for file in origami_files:
        env.load(file)
    e = SExpr.of(t)
    # TODO typecheck is HERE
    ss = SourceSection()
    ss.pushEXPR(env, e)
    return ss
