from pegpy.origami.sexpr import SExpr, ListExpr, AtomExpr
from pegpy.origami.origami import Env, SourceSection
from functools import reduce

class Def:
    __slots__ = ['name', 'object', 'x', 'y', 'radius', 'width', 'height', 'value', 'color', 'code']
    def __init__(self, name, object, code):
        self.name = name
        self.object = object
        self.code = code
        self.x = 'cvsw/ratew/2'
        self.y = 'cvsh/rateh/2'
        self.radius = 'cvsh/rateh/10'
        self.width = 'cvsw/ratew/10'
        self.height = 'cvsh/cvsh/10'
        self.value = 'text'
        self.color = 'white'

    def __str__(self):
        return self.code.format(name=self.name, object=self.object, x=self.x, y=self.y, radius=self.radius, width=self.width, height=self.height, value=self.value, color=self.color)

class Source:
    __slots__ = ['stmts', 'sb', 'objectID', 'definded', 'defs', 'rules']
    def __init__(self, e, sb = []):
        self.stmts = list(e[1:])
        self.sb = sb
        self.objectID = 0
        self.definded = []
        self.defs = []
        self.rules = []

    def __str__(self):
        return reduce(lambda x, y: x+'\n'+str(y), self.rules, reduce(lambda x, y: x+'\n'+str(y), self.defs, ''))

    def rename(self, name):
        self.objectID += 1
        return name + '@' + str(self.objectID)

    def add_def(self, d):
        if d.name == '壁':
            self.add_name(self, '右壁')
            self.add_name(self, '左壁')
        else:
            self.add_name(self, d.name)
        self.defs(d)

    def add_name(self, name):
        if name in self.definded:
            raise DefindedError
        else:
            self.definded.append(name)

    def push(self):
        for stmt in self.stmts:
            getattr(Rule, str(stmt[0])[1:].lower())(self, stmt[1].first(), stmt[2:])
            #if str(stmt[0]) == '#JS':
            #    self.sb.append(stmt[1].first())
            #    break

        return str(self)

class Rule:
    def definition(src, name, stmts):
        cuted_name, o_name, code = search_dict(name)
        if cuted_name == name:
            name = src.rename(name)
        o = Def(name, o_name, code)
        for s in stmts:
            object(o, s[1:])
        src.defs.append(o)

    def statement():
        pass
    def ifstmt():
        pass

def object(o, s):
    a = s[0][1][1].first()
    if a in attr:
        setattr(o, attr[a], s[1].first()[:-3])
    else:
        raise AttributeError

def search_dict(main_name, i = 0):
    if len(main_name) <= -i:
        raise UnknownNameError
    else:
        name = main_name if i == 0 else main_name[:i]
        if name in object_names:
            return (name, *object_names[name])
        else:
            return search_dict(main_name, i - 1)

def transpile(t):
    if t.tag == 'err':
        return 'Parse Error'

    e = SExpr.of(t, rules = {})
    s = Source(e)
    return s.push()

color = {
    '赤': 'red',
    '赤色': 'red',
    '青': 'blue',
    '青色': 'blue',
    '黄': 'yellow',
    '黄色': 'yellow',
    'オレンジ': 'orange',
    'オレンジ色': 'orange',
    'ピンク': 'pink',
    'ピンク色': 'pink',
    '紫': 'purple',
    '紫色': 'purple',
    '緑': 'green',
    '緑色': 'green',
    '黒': 'black',
    '黒色': 'black',
    '白': 'white',
    '白色': 'white',
    '灰': 'gray',
    '灰色': 'gray',
    '茶': 'brown',
    '茶色': 'brown',
}

modifier = {
    '少し': '0.2',
    'すこし': '0.2',
    'ちょっと': '0.1',
    'めっちゃ': '0.5',
    'ごっつ': '0.4',
    'すごく': '0.4',
    'ぐーんと': '0.4',
    'がくっと': '0.4',
    'ぐぐーんと': '0.5',
    'がくーん': '0.5',
    '超': '0.5',
    'ちょう': '0.5',
    'ちょー': '0.5',
    '大分': '0.4',
    'だいぶ': '0.4',
    '結構': '0.5',
    'けっこう': '0.5',
}

attr = {
    'x': 'x',
    'x座標': 'x',
    'y': 'y',
    'y座標': 'y',
    '半径': 'radius',
    '横': 'width',
    '縦': 'height',
    '値': 'value',
    '色': 'color',
}

no_name_direct = {
    '上': ('cvsw/ratew/2', '0', 0),
    '下': ('cvsw/ratew/2', 'cvsh/rateh', 0),
    '右': ('cvsw/ratew', 'cvsh/rateh/2', 0),
    '左': ('0', 'cvsh/rateh/2', 0),
    '真ん中': ('cvsw/ratew/2', 'cvsh/rateh/2', 0),
    '中心': ('cvsw/ratew/2', 'cvsh/rateh/2', 0),
    '右上': ('cvsw/ratew', '0', 0),
    '右下': ('cvsw/ratew', 'cvsh/rateh', 0),
    '左上': ('0', '0', 0),
    '左下': ('0', 'cvsh/rateh', 0),
}

object_direct = {
    '上': ("checkComposite(objectMap['{0}'], 'position').x", "checkComposite(objectMap['{0}'], 'position').y - (checkComposite(objectMap['{0}'], 'bounds').max.y - checkComposite(objectMap['{0}'], 'bounds').min.y)", 1),
    '下': ("checkComposite(objectMap['{0}'], 'position').x", "checkComposite(objectMap['{0}'], 'position').y + (checkComposite(objectMap['{0}'], 'bounds').max.y - checkComposite(objectMap['{0}'], 'bounds').min.y)", 2),
    '右': ("checkComposite(objectMap['{0}'], 'position').x + (checkComposite(objectMap['{0}'], 'bounds').max.x - checkComposite(objectMap['{0}'], 'bounds').min.x)", "checkComposite(objectMap['{0}'], 'position').y", 10),
    '左': ("checkComposite(objectMap['{0}'], 'position').x - (checkComposite(objectMap['{0}'], 'bounds').max.x - checkComposite(objectMap['{0}'], 'bounds').min.x)", "checkComposite(objectMap['{0}'], 'position').y", 20),
    '真ん中': ("checkComposite(objectMap['{0}'], 'position').x", "checkComposite(objectMap['{0}'], 'position').y", 0),
    '中心': ("checkComposite(objectMap['{0}'], 'position').x", "checkComposite(objectMap['{0}'], 'position').y", 0),
    '右上': ("checkComposite(objectMap['{0}'], 'position').x + (checkComposite(objectMap['{0}'], 'bounds').max.x - checkComposite(objectMap['{0}'], 'bounds').min.x)", "checkComposite(objectMap['{0}'], 'position').y - (checkComposite(objectMap['{0}'], 'bounds').max.y - checkComposite(objectMap['{0}'], 'bounds').min.y)", 12),
    '右下': ("checkComposite(objectMap['{0}'], 'position').x + (checkComposite(objectMap['{0}'], 'bounds').max.x - checkComposite(objectMap['{0}'], 'bounds').min.x)", "checkComposite(objectMap['{0}'], 'position').y + (checkComposite(objectMap['{0}'], 'bounds').max.y - checkComposite(objectMap['{0}'], 'bounds').min.y)", 11),
    '左上': ("checkComposite(objectMap['{0}'], 'position').x - (checkComposite(objectMap['{0}'], 'bounds').max.x - checkComposite(objectMap['{0}'], 'bounds').min.x)", "checkComposite(objectMap['{0}'], 'position').y - (checkComposite(objectMap['{0}'], 'bounds').max.y - checkComposite(objectMap['{0}'], 'bounds').min.y)", 22),
    '左下': ("checkComposite(objectMap['{0}'], 'position').x - (checkComposite(objectMap['{0}'], 'bounds').max.x - checkComposite(objectMap['{0}'], 'bounds').min.x)", "checkComposite(objectMap['{0}'], 'position').y + (checkComposite(objectMap['{0}'], 'bounds').max.y - checkComposite(objectMap['{0}'], 'bounds').min.y)", 21),
}

text_direct = {
    '上': ("textMap['{0}'].x", "textMap['{0}'].y - fontSize", 1),
    '下': ("textMap['{0}'].x", "textMap['{0}'].y + fontSize", 2),
    '右': ("textMap['{0}'].x + textMap['{0}'].value.length * fontSize / 2", "textMap['{0}'].y", 10),
    '左': ("textMap['{0}'].x - textMap['{0}'].value.length * fontSize / 2", "textMap['{0}'].y", 20),
    '真ん中': ("textMap['{0}'].x", "textMap['{0}'].y", 0),
    '中心': ("textMap['{0}'].x", "textMap['{0}'].y", 0),
    '右上': ("textMap['{0}'].x + textMap['{0}'].value.length * fontSize / 2", "textMap['{0}'].y - fontSize", 12),
    '右下': ("textMap['{0}'].x + textMap['{0}'].value.length * fontSize / 2", "textMap['{0}'].y + fontSize", 11),
    '左上': ("textMap['{0}'].x - textMap['{0}'].value.length * fontSize / 2", "textMap['{0}'].y - fontSize", 22),
    '左下': ("textMap['{0}'].x - textMap['{0}'].value.length * fontSize / 2", "textMap['{0}'].y + fontSize", 21),
}

object_names = {
    'ボール': ('circle', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {radius}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '玉': ('circle', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {radius}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '球': ('circle', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {radius}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '球形': ('circle', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {radius}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '丸': ('circle', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {radius}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '円': ('circle', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {radius}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '円形': ('circle', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {radius}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '四角': ('rectangle', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {width}, {height}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '四角形': ('rectangle', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {width}, {height}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '箱': ('rectangle', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {width}, {height}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '正多角形': ('polygon', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {width}, {height}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '台形': ('trapezoid', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {width}, {height}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '車': ('car', "objectMap['{name}'] = Bodies.{object}({x}, {y}, {width}, {height}, {{render:{{fillStyle:'{color}'}}}})\nWorld.add(engine.world, objectMap['{name}']);"),
    '文字': ('text', "textMap['{name}'] = {{x: {x}, y: {y}, value: '{value}', textColor: '{color}'}\nwriteAllText();"),
    '地面': "objectMap['地面'] = Bodies.rectangle(cvsw/ratew/2, cvsh/rateh*99/100, cvsw/ratew, cvsh/rateh/50, {isStatic: true});\nWorld.add(engine.world, objectMap['地面']);",
    '天井': "objectMap['天井'] = Bodies.rectangle(cvsw/ratew/2, cvsh/rateh/100, cvsw/ratew, cvsh/rateh/50, {isStatic: true});\nWorld.add(engine.world, objectMap['天井']);",
    '壁': "objectMap['右壁'] = Bodies.rectangle(cvsw/ratew*99/100, cvsh/rateh/2, cvsw/ratew/50, cvsh/rateh, {isStatic: true});\nobjectMap['左壁'] = Bodies.rectangle(cvsw/ratew/100, cvsh/rateh/2, cvsw/ratew/50, cvsh/rateh, {isStatic: true});\nWorld.add(engine.world, objectMap['右壁']);\nWorld.add(engine.world, objectMap['左壁']);",
    '右壁': "objectMap['右壁'] = Bodies.rectangle(cvsw/ratew*99/100, cvsh/rateh/2, cvsw/ratew/50, cvsh/rateh, {isStatic: true});\nWorld.add(engine.world, objectMap['右壁']);",
    '左壁': "objectMap['左壁'] = Bodies.rectangle(cvsw/ratew/100, cvsh/rateh/2, cvsw/ratew/50, cvsh/rateh, {isStatic: true});\nWorld.add(engine.world, objectMap['左壁']);",
}

world_name = {
    '地面': ['地面'],
    '天井': ['天井'],
    '壁': ['右壁', '左壁'],
    '右壁': ['右壁'],
    '左壁': ['左壁'],
}

directive = ['これら', 'あれら', 'それら', 'これ', 'あれ', 'それ', 'こ', 'あ', 'そ']
be = ['おく', 'ある', 'いる', '置く', 'いらっしゃる', 'おられる', 'おき', 'あり', 'おり', '置き', 'いらっしゃり', 'おられり', 'おいて', 'あって', 'いて', '置いて', 'いらっしゃって', 'おられて']
crash = ['衝突するとき', '衝突するなら', '衝突するならば', '衝突したとき', '衝突したら', '衝突したならば', '当たるとき', '当たるなら', '当たるならば', '当たったとき', '当たったなら', '当たったならば', 'あたるとき', 'あたるなら', 'あたるならば', 'あたったとき', 'あたったなら', 'あたったならば']
add = ['増加する', '増加して', '増加し', '増やす', '増やして', '増やし', '増える', '増えて', '増え', '増す', '増して', '増し', 'ふやす', 'ふやして', 'ふやし', 'ふえる', 'ふえて', 'ふえ', 'ます', 'まして', 'まし']
subtract = ['減少する', '減少して', '減少し', '減らす', '減らして', '減らし', '減る', '減って', '減り', 'へらす', 'へらして', 'へらし', 'へる', 'へって', 'へり']

lambdas = [
    (be, lambda src, sec: for_main(rule, src, sec)),
    (add, lambda src, sec: for_main(lambda m, src, sec: assign('+', m, src, sec), src, sec)),
    (subtract, lambda src, sec: for_main(lambda m, src, sec: assign('-', m, src, sec), src, sec)),
    (crash, lambda src, sec: event('collisionEnd', src, sec)),
]

def get_place(src, sec):
    if sec.direction is not None:
        p = str(sec.direction[2])
        if isinstance(sec.direction[1], AtomExpr):
            d1 = str(sec.direction[1])
            if d1 in directive and len(src.past_main_names) != 0:
                d1 = src.past_main_names[0]
            direct = text_direct if search_dict(d1)[1] == 'text' else object_direct
            d = tuple(map(lambda x: x.format(d1) if isinstance(x, str) else x, direct[p] if p in direct else direct['中心']))
        else:
            d = no_name_direct[p] if p in no_name_direct else no_name_direct['中心']

        if isinstance(sec.direction[0], AtomExpr):
            dir_mod = str(sec.direction[0])
            magni = modifier[dir_mod] if dir_mod in modifier else dir_mod
            return (calc_mod(d[0], int(d[2] / 10), 'cvsw/ratew', magni), calc_mod(d[1], d[2] % 10, 'cvsh/rateh', magni))
        else:
            return (d[0], d[1])
    else:
        center = no_name_direct['中心']
        return (center[0], center[1])

def calc_mod(dir, id, txt, magni):
    return dir if id == 0 else dir + '+' + txt + '*' + magni if id == 1 else dir + '-' + txt + '*' + magni

def event(e, src, sec):
    objects = list(map(lambda x: str(x[2]), sec.main))
    if not reduce(lambda x, o: x and (o in src.definded), objects, True):
        return
    text = "Matter.Events.on(engine, '%s', function(event) {\n\tpairs = event.pairs;\n\tfor (var i = 0; i < pairs.length; i++) {\n\t\tvar pair = pairs[i];\n\t\tif (pair.bodyA.id == objectMap['$1'].id && pair.bodyB.id == objectMap['$2'].id || pair.bodyA.id == objectMap['$2'].id && pair.bodyB.id == objectMap['$1'].id) {$*\n\t\t}\n\t}\n});" % e
    for i in range(len(objects)):
        text = text.replace('$' + str(i + 1), objects[i])
    src.past_main = sec.main
    src.past_main_names = objects
    src.s += text

def assign(infix, main, src, sec):
    main_name = str(main[1]) if isinstance(main[1], AtomExpr) else str(main[2])
    if main_name in src.definded and search_dict(main_name)[1] == 'text':
        text = "\n\t\t\ttextMap['{1}'].value = String(Number(textMap['{1}'].value) {0} {2});$*".format(infix, main_name, sec.mod if sec.mod is not None else '1')
        src.endf.append(lambda s: s.replace('$*', text))
        src.ends.append(lambda s: s.replace('$*', '\n\t\t\twriteAllText();'))
    src.past_main = main
    src.past_main = [main_name]

class DefindedError(Exception):
    pass

class UnknownNameError(Exception):
    pass
