from pegpy.peg import Grammar, nez
from pegpy.origami.sexpr import SExpr, AtomExpr
import pegpy.utils as u

g = Grammar('konoha6')
g.load('konoha6.tpeg')
origami_parser = nez(g['OrigamiFile'])

def getkeys(stmt):
    name = stmt['name'].asString()
    expr = stmt['expr'].asString()
    keys = []
    if 'from' in stmt:
        fromty = SExpr.of(stmt['from'])
        key = name + '@' + str(fromty)
        if 'to' in stmt:
            toty = SExpr.of(stmt['to'])
            keys.append(key + '@' + str(toty))
        keys.append(key)
    keys.append(name)
    if '@' in name:
        keys.append(name.split('@')[0])
    return keys

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

    def getType(self, iname):
        return self[iname]

    def getSyntax(self, iname):
        return self[iname]

    def load(self, path):
        f = open(u.find_path(path, 'origami'))
        data = f.read()
        f.close()
        t = origami_parser(data, path)
        if t == 'err':
            er = t.getpos()
            print('SyntaxError ({}:{}:{}+{})'.format(er[0], er[2], er[3], er[1]), '\n', er[4], '\n', er[5])
            return
        for _, stmt in t:
            print(stmt)
            if stmt == 'CodeMap':
                keys = getkeys(stmt)
                expr = stmt['expr'].asString()
                self[keys[0]] = expr
                for key in keys[1:]:
                    if not key in self:
                        self[key] = expr
            elif stmt == 'TypeMap':
                keys = getkeys(stmt)
                keys = list(map(lambda x: ' ' + x, keys))
                ty = SExpr.of(stmt['type'])
                self[keys[0]] = expr
                for key in keys[1:]:
                    if not key in self:
                        self[key] = expr


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

    def pushEXPR(self, env, e):
        if isinstance(e, SExpr):
            if e.code is not None:
                self.pushFMT(e.code, e.data)
            else:
                keys = e.keys()
                for key in keys:
                    if key in env:
                        rule = env[key]
                        if hasattr(rule, 'emit'):
                            rule.emit(env, e, self)
                        else:
                            self.pushFMT(rule, e.data)
                        return
                if isinstance(e, AtomExpr):
                    self.pushSTR(str(e))
                else:
                    self.pushFMT(self, self.syntaxMap['TODO'], e.data)
        else:
            self.pushSTR(str(e))

    def pushFMT(self, env, fmt: str, args: list):
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


def transpile(t, origami_files = ['python.origami']):
    env = Env()
    for file in origami_files:
        env.load(file)
    e = SExpr.of(t)
    # TODO typecheck is HERE
    ss = SourceSection()
    ss.pushEXPR(env, e)
    print(ss)
