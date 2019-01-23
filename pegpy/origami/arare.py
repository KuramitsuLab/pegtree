import pegpy.origami.typesys as ts
import pegpy.utils as u

class TypeSystem(ts.Origami):
    def __init__(self, out):
        super().__init__(out)
        #out.perror = perror

    def Source(self, env, expr, ty):
        expr = self.apply(env, expr, ty)
        expr.code = emitSource
        return expr

    def JSONDecl(self, env, expr, ty):
        print('//JSON', expr)
        defineConcept(env, expr[1], expr[2], expr[3])
        return expr.done()

    def ConceptDecl(self, env, expr, ty):
        print('@Concept', expr)
        defineConcept(env, expr[1], expr[2], expr[3])
        return expr.done()

# エラー処理用

ERROR = []

def perror(pos3, msg, type = 'error'):
    if pos3 is not None:
        urn, pos, linenum, cols, line, mark = u.decpos3(pos3[0], pos3[1], pos3[2])
        e = {
            'type': type,
            #'path': repr(urn),
            'row': linenum-1,
            'column': cols,
            #'pos': pos,
            'text': repr(msg),
        }
        ERROR.append(e)

## 用語の正規化

WORD = {
    '円形' : '円',
}

def word(w):
    return WORD[w] if w in WORD else w

CONCEPT = {
    '世界': {
        'type': 1,
        'width': 1000,
        'height': 1000,
    },
    '円' : {
        'type': '"circle"',
        'concept': ['円'],
    },
    '': {  # undefined
        'type': '"circle"',
        'radius': 30,
        'concept': [],
    },
}

def extend(env, name, parent0):
    name = str(name)
    parent = word(str(parent0))
    if parent in CONCEPT:
        parent = CONCEPT[parent]
    else:
        perror(parent0.getpos(), '{}とは何ですか？'.format(str(parent0)))
        parent = CONCEPT['']
    c = {}
    #print('@parent', parent)
    for k in parent:
        c[k] = parent[k]
    c['concept'] = [name] + c['concept']
    CONCEPT[name] = c
    return c

def defineConcept(env, name, parent, block = [None]):
    c = extend(env, name, parent)
    for stmt in block[1:]:
        #print('@stmt')
        if stmt == '#Assign':
            addAttribute(env, c, stmt[1], stmt[2])
    print('@concept', c)

## 値

def valueExpr(env, name, value, dic={}):
    #print('@value', value.tag, value)
    if value == '#ThatOf':
        value.tag = '#GetExpr'
        value.data.insert(1,value.new2('#Name', name))
        return value
    if value == '#Name':
        v = str(value)
        v = dic[v] if v in dic else v
        return value.new2('#Raw', repr(v))
    return value

## 属性

def setName(env, c, name:str, value):
    v = valueExpr(env, name, value)
    c[name] = v
    c['name'] = v

def setWidth(env, c, name, value):
    v = valueExpr(env, name, value)
    c[name] = v
    if not 'width' in c: c['width'] = v
    if not 'height' in c: c['height'] = v

def setHeight(env, c, name, value):
    v = valueExpr(env, name, value)
    c[name] = v
    if not 'width' in c: c['width'] = v
    if not 'height' in c: c['height'] = v

def setRadius(env, c, name, value):
    v = valueExpr(env, name, value)
    c[name] = v
    c['radius'] = v

def setSize(env, c, name, value):
    v = valueExpr(env, name, value)
    c[name] = v
    if not 'width' in c: c['width'] = v
    if not 'height' in c: c['height'] = v

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
}

def setColor(env, c, name, value):
    v = valueExpr(env, name, value, COLOR)
    c['色'] = v
    c['fillStyle'] = v

WORLD_X = 1000
WORLD_Y = 1000

LOCATION = {
    '中央': [500, 500],
}

def setLocation(env, c, name, value):
    if value.tag.startswith('#Tuple') and len(value) > 2:
        c['x'] = value[1]
        c['y'] = value[2]
        return
    v = valueExpr(env, name, value, COLOR)

ATTR = {
    '名前': setName,
    '大きさ': setSize,
    '幅': setWidth,     '横幅': setWidth,
    '高さ': setHeight,  '縦幅': setHeight,
    '半径': setRadius,
    '色': setColor,
    '位置': setLocation,
}

ATTRFUNC = globals()

def addAttribute(env, c, name, value):
    name = str(name)
    if name in ATTR:
        func = ATTR[name]
        return func(env, c, name, value)


# resolve

def resolveSource(out):
    remain = [True]
    while remain[0]:
        remain[0] = False
        for cname in CONCEPT:
            c = CONCEPT[cname]
            for key in c:
                c[key] = resolve(c[key], out, remain)

def resolve(v, out, remain):
    if hasattr(v, 'tag'):
        if v.tag == '#GetExpr':
            cname = str(v[1])
            pname = str(v[2])
            if cname in CONCEPT:
                if pname in CONCEPT[cname]:
                    remain[0] = True
                    return CONCEPT[cname][pname]
                else:
                    perror(v[1].getpos(), '{}の{}は定義されてないよ'.format(cname, pname))
            else:
                perror(v[1].getpos(), '{}は定義されてないよ'.format(cname))
                return 'undefined'
    return v



#emit

def emitSource(env, expr, ss):
    resolveSource(env.ts.out)
    ss.begin(env, '(function(c){')
    ss.p(env, 'var w = ', CONCEPT['世界']['width'], ';')
    ss.p(env, 'var h = ', CONCEPT['世界']['height'], ';')
    emitJSON(env, CONCEPT['世界'], ss, begin='c.world = {', end='};')
    ss.begin(env, 'c.bodies = [')
    for key in CONCEPT:
        if key == '世界': continue
        c = CONCEPT[key]
        emitJSON(env, c, ss)
    ss.end(env, ']')
    ss.begin(env, 'c.errors = [')
    for e in ERROR:
        emitJSON(env, e, ss)
    ss.end(env, ']')
    ss.end(env, '})(ArareCode)')

def emitJSON(env, c, ss, begin='{', end='},'):
    ss.begin(env, begin)
    for key in c:
        if ord(key[0])<128:
            ss.p(env, repr(key), ': ', c[key], ",")
    ss.end(env, end)


