import pegpy.origami.typesys as ts
import pegpy.utils as u

## TypeSystem

class TypeSystem(ts.Origami):
    def __init__(self, out):
        super().__init__(out)

    def Source(self, env, expr, ty):
        env.ext = Arare();
        env.perror = perror
        expr = self.apply(env, expr, ty)
        expr.code = emitSource
        return expr

    def ConceptDecl(self, env, expr, ty):
        print('@Concept', expr)
        define_concept(env, expr[1], expr[2], expr[3])
        return expr.done()

    def ThereDecl(self, env, expr, ty):
        print('@There', expr)
        ename = None
        etype = expr[expr.find('name')]
        ebody = expr[expr.find('body')]
        if ename == '#Param':
            ename = etype[2]
            etype = etype[1]
        idx = expr.find('size')
        if idx != -1:
            pass
        define_body(env, ename, etype, 1, ebody)
        return expr.done()

class Arare(object):
    __slot__ = ['proto', 'bodies', 'errors']
    def __init__(self):
        self.proto = {
            '世界': {
                'type': 1,
                'width': 1000,
                'height': 1000,
            },
            '円': {
                'shape': '"circle"',
                'concept': ['円'],
            },
            '四角': {
                'shape': '"rectangle"',
                'concept': ['長方形'],
            },
            '振り子': {
                'shape': '"pendulum"',
                'concept': ['振り子'],
            },
            '壁': {
                'shape': '"rectangle"',
                'concept': ['壁', '長方形'],
                'isStatic': 'true',
            },
            '': {  # undefined
                'shape': '"circle"',
                'radius': 30,
                'concept': [],
            },
        }
        self.bodies = []
        self.errors = []

def perror(env, pos3, msg):
    if pos3 is not None:
        urn, pos, linenum, cols, line, mark = u.decpos3(pos3[0], pos3[1], pos3[2])
        e = {
            'type': type,
            'row': linenum-1,
            'column': cols,
            'text': repr(msg),
        }
        env.ext.errors.append(e)


## 用語の正規化

WORD = {
    '円形' : '円',
    '％': '%',
    '定位置': '固定',
}

def word(w):
    w = str(w)
    return WORD[w] if w in WORD else w


## 値

def eadd(a, b): return a.new('/', a, b)
def emul(a, b): return a.new('*', a, b)
def ediv(a, b): return a.new('/', a, b)

PERCENT = {
    'x': 'width', 'width': 'width', 'radius': 'width',
    'size': 'size', 'location': 'width',
    'y': 'height', 'height': 'height',
    'angle': '1.0',
}

def valueOf(env, name, evalue, norm = str, dic={}):
    if evalue == '#Tuple' and evalue == '#List':
        if len(evalue) == 2:
            return valueOf(env, name, evalue[1], norm, dic)
        for n in range(1, len(evalue)+1):
            evalue[n] = valueOf(env, name, evalue[n], norm, dic)
        return evalue
    if evalue == '#Or':
            return valueOf(env, name, evalue[1], norm, dic)
    if evalue == '#Name' and len(dic) > 0:
        v = norm(evalue)
        if v in dic:
            v = dic[v]
        else:
            _, v = random.choice(dic)
        return evalue.new2('#Raw', repr(v))
    if evalue == '#ThatOf':
        evalue.tag = '#GetExpr'
        evalue.data.insert(1, evalue.new2('#Name', name))
        return evalue
    if evalue == '#Unit':
        unit = word(evalue[2])
        evalue = valueOf(env, name, evalue[1], norm, dic)
        if unit == '%':
            return ediv(emul(evalue.new2('#Name', PERCENT[name]), evalue), 100)
        print('@unit', unit, evalue)
        return evalue
    print('@value', evalue.tag, evalue)
    return evalue

## 属性

def setName(env, c, evalue):
    v = valueOf(env, 'name', evalue)
    c['name'] = v

def setWidth(env, c, evalue):
    v = valueOf(env, 'width', evalue)
    c['width'] = v
    if not 'height' in c: c['height'] = v

def setHeight(env, c, evalue):
    v = valueOf(env, 'height', evalue)
    c['height'] = v

def setRadius(env, c, evalue):
    v = valueOf(env, 'radius', evalue)
    c['radius'] = v

def setSize(env, c, evalue):
    if 'circle' in c['shape']:
        setRadius(env, c, ediv(evalue,2))
    else:
        setRadius(env, c, evalue)

def setAngle(env, c, evalue):
    c['angle'] = valueOf(env, 'angle', evalue)


COLOR = {
    '赤': 'red',
    '青': 'blue',
    '黄': 'yellow',
    'オレンジ': 'orange',
    'ピンク': 'pink',
    '紫': 'purple',
    '緑': 'green',
    '黒': 'black',
    '白': 'white',
    '灰': 'gray',
    '茶': 'brown',
    '透明': 'transparent',
}

def normcolor(s):
    s = str(s)
    if s.endswith('色'): s = s[:-1]
    return s

def setColor(env, c, evalue):
    c['fillStyle'] = valueOf(env, 'fillStyle', evalue, dic=COLOR, norm=normcolor)


LOCATION = {
    '中央': [500, 500],
}

def setLocation(env, c, evalue):
    if evalue == '#And':
        if word(evalue[1]) == '固定':
            c['isStatic'] = evalue.new2('#TrueExpr', true)
            setLocation(env, c, evalue[2])
        elif word(evalue[2]) == '固定':
            c['isStatic'] = evalue.new2('#TrueExpr', true)
            setLocation(env, c, evalue[1])
        else:
            setLocation(env, c, evalue[1])
            setLocation(env, c, evalue[2])
        return
    if evalue.tag.startswith('#Tuple') and len(evalue) > 2:
        c['x'] = valueOf(env, 'x', evalue[1])
        c['y'] = valueOf(env, 'y', evalue[2])
        return
    c['location'] = valueOf(env, 'location', evalue)


def setDensity(env, c, evalue):
    c['density'] = valueOf(env, 'density', evalue)

def setAirFriction(env, c, evalue):
    c['airFriction'] = valueOf(env, 'airFriction', evalue)

def setFriction(env, c, evalue):
    c['friction'] = valueOf(env, 'friction', evalue)

def setGravity(env, c, evalue):
    c['gravity'] = valueOf(env, 'gravity', evalue)

def setRestitution(env, c, evalue):
    c['restitution'] = valueOf(env, 'restitution', evalue)

def setStiffness(env, c, evalue):
    c['stiffness'] = valueOf(env, 'stiffness', evalue)

def setDamping(env, c, evalue):
    c['damping'] = valueOf(env, 'damping', evalue)

ATTR = {
    '名前': setName,
    '大きさ': setSize, '直径': setSize,
    '幅': setWidth,     '横幅': setWidth,
    '高さ': setHeight,  '縦幅': setHeight,
    '半径': setRadius,
    '位置': setLocation,
    '色': setColor,
    '傾き': setAngle,
    '密度': setDensity,
    '摩擦': setFriction,
    '空気摩擦': setAirFriction,
    '重力': setGravity,
    '反発係数': setRestitution,
    '剛性': setStiffness, 'ばね定数': setStiffness,
    '減衰': setDamping,
}

ATTRFUNC = globals()

def add_attribute(env, c, ename, evalue):
    name = str(ename)
    if name in ATTR:
        func = ATTR[name]
        return func(env, c, evalue)

def extend_concept(env, ename, etype):
    parent = word(str(etype))
    if parent in env.ext.proto:
        parent = env.ext.proto[parent]
    else:
        perror(etype.getpos(), '{}とは何ですか？'.format(str(etype)))
        parent = env.ext.proto['']
    c = {}
    for k in parent:
        c[k] = parent[k]
    if ename is not None:
        name = str(ename)
        c['concept'] = [name] + c['concept']
        if name in c:
            perror(ename.getpos(), '同じ名前「{}」を既に使っています'.format(name))
        env.ext.proto[name] = c
    return c

def define_concept(env, ename, etype, eblock = [None]):
    c = extend_concept(env, ename, etype)
    for stmt in eblock[1:]:
        if stmt == '#Assign':
            add_attribute(env, c, stmt[1], stmt[2])
    return c

def define_body(env, ename, etype, num, eblock = [None]):
    c = define_concept(env, ename, etype, eblock)
    if ename is None:
        env.ext.bodies.append(c)

# resolve

def resolveSource(out):
    remain = [True]
    while remain[0]:
        remain[0] = False
        for cname in env.ext.proto:
            c = env.ext.proto[cname]
            for key in c:
                c[key] = resolve(c[key], out, remain)

def resolve(v, out, remain):
    if hasattr(v, 'tag'):
        if v.tag == '#GetExpr':
            cname = str(v[1])
            pname = str(v[2])
            if cname in env.ext.proto:
                if pname in env.ext.proto[cname]:
                    remain[0] = True
                    return env.ext.proto[cname][pname]
                else:
                    perror(v[1].getpos(), '{}の{}は定義されてません'.format(cname, pname))
            else:
                perror(v[1].getpos(), '{}は定義されてません'.format(cname))
                return 'undefined'
    return v

#emit

def emitSource(env, expr, ss):
    #resolveSource(env.ts.out)
    ss.begin(env, '(function(c){')
    ss.p(env, 'var width = ', env.ext.proto['世界']['width'], ';')
    ss.p(env, 'var height = ', env.ext.proto['世界']['height'], ';')
    emitJSON(env, env.ext.proto['世界'], ss, begin='c.world = {', end='};')
    ss.begin(env, 'c.bodies = [')
    for key in env.ext.proto:
        if key == '世界': continue
        c = env.ext.proto[key]
        if 'x' in c: emitJSON(env, c, ss)
    for c in env.ext.bodies:
        if 'x' in c: emitJSON(env, c, ss)
    ss.end(env, ']')
    ss.begin(env, 'c.errors = [')
    for e in env.ext.errors:
        emitJSON(env, e, ss)
    ss.end(env, ']')
    ss.end(env, '})(ArareCode)')

def emitJSON(env, c, ss, begin='{', end='},'):
    ss.begin(env, begin)
    for key in c:
        if ord(key[0])<128:
            ss.p(env, repr(key), ': ', c[key], ",")
    ss.end(env, end)

def compile(input):
    from pegpy.peg import Grammar,nez
    g = Grammar()
    g.load('arare.tpeg')
    parser = nez(g)
    env = ts.transpile_init(['js.origami'], TypeSystem, u.STDOUT)
    t = parser(input)
    return repr(ts.transpile(env, t, u.STDOUT))
