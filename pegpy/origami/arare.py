import pegpy.origami.typesys as ts
import pegpy.utils as u

## TypeSystem

class TypeSystem(ts.Origami):
    def __init__(self, out):
        super().__init__(out)

    def Source(self, env, expr, ty):
        env.ext = Arare();
        env.perror = perror
        env['#Vec'] = ts.Def(None, None, '{x: ${1}, y: ${2}}')
        env['rgba@4'] = ts.Def(None, None, "'rgba(${1},${2},${3},${4})'")
        env['rgba@3'] = ts.Def(None, None, "'rgba(${1},${2},${3},1.0)'")
        expr = self.apply(env, expr, ty)
        expr.code = emitSource
        return expr

    def ConceptDecl(self, env, expr, ty):
        #print('@Concept', expr)
        define_concept(env, expr[1], expr[2], expr[3])
        return expr.done()

    def ThereDecl(self, env, expr, ty):
        print('@There', expr)
        ename = None
        etype = expr[expr.find('name')]
        ebody = expr[expr.find('body')]
        if etype == '#Param':
            ename = etype[2]
            etype = etype[1]
        idx = expr.find('size')
        if idx != -1:
            pass
        define_body(env, ename, etype, 1, ebody)
        return expr.done()

    def VarDecl(self, env, expr, ty):
        #print('@There', expr)
        ename = expr[expr.find('left')]
        evalue = expr[expr.find('right')]
        if ename == '#GetExpr':
            base = word(ename[1])
            if base in env.ext.proto:
                c = env.ext.proto[base]
            else:
                perror(ename[1].getpos(), 'undefined')
                return expr.done()
            name = word(ename[2])
        else:
            name = str(ename)
            if name in env.ext.proto:
                c = env.ext.proto[name]
            else:
                c = {'name': repr(name)}
                env.ext.proto[name] = c
            name = 'value'
        add_attribute(env, c, name, evalue)
        return expr.done()

    def CollisionRule(self, env, expr, ty):
        pass

class Arare(object):
    __slot__ = ['proto', 'bodies', 'errors']
    def __init__(self):
        self.proto = {
            '世界': { 'width': 1000, 'height': 1000, },
            '円': { 'shape': '"circle"', 'concept': ['円'], },
            '四角': { 'shape': '"rectangle"', 'concept': ['長方形'], },
            '振り子': { 'shape': '"pendulum"', 'concept': ['振り子'], },
            '壁': { 'shape': '"rectangle"', 'concept': ['壁', '長方形'], 'isStatic': 'true', 'chamfer': 'true',},
            '変数': { 'value': 0 },
            '': { 'shape': '"circle"', 'radius': 30, 'concept': [], },
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
    'angle': 'Math.PI',
}

def valueOf(env, name, evalue, norm = str, dic={}):
    evalue = env.ts.asType(env, evalue, None)
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
    #print('@value', evalue.tag, evalue)
    return evalue

## 属性

def setAttr(c, name, evalue):
    if evalue != '#Null':
        c[name] = evalue
    else:
        del c[name]

def addAttr(c, name, evalue):
    if evalue != '#Null' and name not in c:
        c[name] = evalue

def setAngle(env, c, evalue):
    v = valueOf(env, 'angle', evalue)
    setAttr(c, 'angle', emul(v, evalue.new2('#Name', 'Math.PI')))

def setRadius(env, c, evalue):
    v = valueOf(env, 'width', evalue)
    setAttr(c, 'width', ediv(v, 2))
    setAttr(c, 'height', ediv(v, 2))

def setSize(env, c, evalue):
    if evalue == '#Tuple' and len(evalue) > 2:
        width = valueOf(env, 'width', evalue[1])
        height = valueOf(env, 'height', evalue[2])
        setAttr(c, 'width', width)
        setAttr(c, 'height', height)
    else:
        v = valueOf(env, 'width', evalue)
        setAttr(c, 'width', v)
        setAttr(c, 'height', v)

def setScale(env, c, evalue):
    if evalue == '#Tuple' and len(evalue) > 2:
        x = valueOf(env, 'x', evalue[1])
        y = valueOf(env, 'y', evalue[2])
        setAttr(c, 'xScale', x)
        setAttr(c, 'yScale', y)
    else:
        v = valueOf(env, 'x', evalue)
        setAttr(c, 'xScale', v)
        setAttr(c, 'yScale', v)

def setGravity(env, c, evalue):
    if evalue == '#Tuple' and len(evalue) > 2:
        x = valueOf(env, 'x', evalue[1])
        y = valueOf(env, 'y', evalue[2])
        setAttr(c, 'xGravity', x)
        setAttr(c, 'yGravity', y)
    else:
        v = valueOf(env, 'x', evalue)
        setAttr(c, 'yGravity', v)

def setForce(env, c, evalue):
    if evalue == '#Tuple' and len(evalue) > 2:
        x = valueOf(env, 'x', evalue[1])
        y = valueOf(env, 'y', evalue[2])
        setAttr(c, 'force', evalue.new('#Vec', x, y))

def setSpeed(env, c, evalue):
    if evalue == '#Tuple' and len(evalue) > 2:
        x = valueOf(env, 'x', evalue[1])
        y = valueOf(env, 'y', evalue[2])
        setAttr(c, 'velocity', evalue.new('#Vec', x, y))
    else:
        v = valueOf(env, 'x', evalue)
        setAttr(c, 'speed', v)

def setAngleSpeed(env, c, evalue):
    if evalue == '#Tuple' and len(evalue) > 2:
        x = valueOf(env, 'x', evalue[1])
        y = valueOf(env, 'y', evalue[2])
        setAttr(c, 'angularVelocity', evalue.new('#Vec', x, y))
    else:
        v = valueOf(env, 'x', evalue)
        setAttr(c, 'angularSpeed', v)

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

def setLabel(env, c, evalue):
    c['value'] = valueOf(env, 'value', evalue)
    c['print'] = evalue.new2('#Raw', 'function(x) { return x.value; }')

def setFontColor(env, c, evalue):
    c['fontFillStyle'] = valueOf(env, 'fillStyle', evalue, dic=COLOR, norm=normcolor)

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
    if evalue == '#Tuple' and len(evalue) > 2:
        c['x'] = valueOf(env, 'x', evalue[1])
        c['y'] = valueOf(env, 'y', evalue[2])
        return
    c['location'] = valueOf(env, 'location', evalue)

DICT = {
    '名前': 'name',
    '幅': 'width', '縦': 'width',
    '高さ': 'height', '横': 'height',
    '傾き': 'angle',
    '質量': 'mass', '密度': 'density', '体積': 'area', '容積': 'area',
    '摩擦係数': 'friction', '静止摩擦係数': 'frictionStatic',
    '空気摩擦係数': 'airFriction',
    '反発係数': 'restitution', '跳ね返り係数': 'restitution', 'はねかえり係数': 'restitution',
    '回転力': "torque", '力のモーメント': "torque",
    '剛性': 'stiffness', 'ばね定数': 'stiffness',
    'センサー': 'isSensor',
    '減衰': 'damping',
    'フォント': 'font',
    '画像': 'texture',
    '描画': 'visible',
}

ATTR = {
    '重力': setGravity,
    '大きさ': setSize,
    '傾き': setAngle,
    '半径': setRadius,
    '位置': setLocation,
    'スケール': setScale,  #'オフセット': setOffset.
    '速度': setSpeed,
    '角速度': setAngleSpeed,
    '力': setForce,
    '色': setColor,
    'ラベル': setLabel, '値': setLabel,
    '文字色': setFontColor, 'フォント色': setFontColor,
}

def add_attribute(env, c, ename, evalue):
    name = word(ename)
    if name in ATTR:
        func = ATTR[name]
        return func(env, c, evalue)
    elif name in DICT:
        name = DICT[name]
    c[name] = valueOf(env, name, evalue)

def extend_concept(env, ename, etype):
    parent = word(etype)
    if parent == '世界':
        return env.ext.proto[parent]
    elif parent in env.ext.proto:
        parent = env.ext.proto[parent]
    else:
        perror(env, etype.getpos(), '{}は未定義です'.format(str(etype)))
        parent = env.ext.proto['']
    c = {}
    for k in parent: c[k] = parent[k]
    name = None
    if ename is not None:
        name = str(ename)
        c['name'] = repr(name)
    if name is not None:
        if 'concept' in c: c['concept'] = [name] + c['concept']
        if name in env.ext.proto:
            perror(env, ename.getpos(), '「{}」は既に定義されてます'.format(name))
        env.ext.proto[name] = c
    return c

def define_concept(env, ename, etype, eblock = [None]):
    c = extend_concept(env, ename, etype)
    for stmt in eblock[1:]:
        if stmt == '#Assign':
            add_attribute(env, c, stmt[1], stmt[2])
        else:
            print('@todo', stmt)
    return c

def define_body(env, ename, etype, num, eblock = [None]):
    print('@there', ename, etype)
    c = define_concept(env, ename, etype, eblock)
    if ename is None and str(etype) != '世界':
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
        if 'x' in c or 'shape' not in c : emitJSON(env, c, ss)
    for c in env.ext.bodies:
        if 'x' in c: emitJSON(env, c, ss)
    ss.end(env, ']')
    ss.begin(env, 'c.errors = [')
    for e in env.ext.errors:
        emitJSON(env, e, ss)
    ss.end(env, ']')
    ss.end(env, '})(ArareCode)')

##


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


'''
  /* 物体属性 */
  Arare.OPTION = [
    "angle", "angularSpeed", "angularVelocity",
    "area", "axes", "bounds", //境界
    "density",
    "force", //（ベクトル）
    "friction", //摩擦
    "frictionAir", //空気抵抗
    "inertia", //慣性
    "inverseInertia", //慣性逆モーメント
    "inverseMass", //逆質量
    "isSleeping", //スリープ中か
    "isStatic", //静的か
    "mass", //質量
    "motion", //運動量
    "position", //位置 { x: 0, y: 0 }
    "restitution", //弾力性
    "sleepThreshold", //スリープのしきい値
    "speed", //速度（スカラー）
    "timeScale", //タイムスケール
    //"type",//オブジェクトの型
    "label", //剛体のラベル
    "velocity", //速度（ベクトル)"vertices",//剛体の頂点
    "number",
  ];
  
  Matter.Events.on(engine, 'collisionEnd', function(event) {
    pairs = event.pairs;
    for (var i = 0; i < pairs.length; i++) {
        var pair = pairs[i];
        if(pair.bodyA.name == name && pair.bodyB.concept.indexOf(name) !=1) {
            var x = pair.bodyA;
            var y = pair.bodyB;
            ctx.vars['SCORE'].value += 1;
            x.update = x.update || {}
            x.update.image = 'hello';
        }
    }
});
'''