from pegpy.origami.sexpr import SExpr, ListExpr, AtomExpr
from pegpy.origami.origami import Env, SourceSection
from functools import reduce

class Source:
    __slots__ = ['stmts', 'endf', 'ends', 'sb', 's', 'past_main', 'definded']
    def __init__(self, e, sb = []):
        self.stmts = list(e[1:])
        self.endf = []
        self.ends = []
        self.sb = sb
        self.s = ''
        self.past_main = None
        self.definded = []

    def clear(self):
        self.endf = []
        self.ends = []
        self.s = ''

    def push(self):
        for stmt in self.stmts:
            if str(stmt[0]) == '#JS':
                self.sb.append(str(stmt[1])[1:-1])
                break
            for s in stmt[1:]:
                sec = Section(s, self.past_main)
                if sec.main is not None:
                    for r, l in lambdas:
                        if sec.verb in r:
                            l(self, sec)
                            break

            if len(self.s) != 0:
                for e in self.endf:
                    self.s = e(self.s)
                for e in self.ends:
                    self.s = e(self.s)
                self.sb.append(self.s)
            self.clear()

        return '\n'.join(self.sb)

class Section:
    __slots__ = ['subject', 'object', 'direction', 'mod', 'verb', 'main']
    def __init__(self, sec, past_main):
        self.subject = sec[0][1:] if len(sec[0]) != 0 else None
        self.object = sec[1][1:] if len(sec[1]) != 0 else None
        self.direction = sec[2] if len(sec[2]) != 0 else None
        self.mod = str(sec[3]) if isinstance(sec[3], AtomExpr) else None
        self.verb = str(sec[4]) if isinstance(sec[4], AtomExpr) else None
        self.main = self.subject if self.subject is not None else self.object if self.object is not None else past_main

MACARON = {
    'Section': 'subject object direction mod verb',
    'Subject': 'modifier subname mainname',
    'Object': 'modifier subname mainname',
    'Direction': 'modifier subname mainname',
    'Modifier': lambda t: t.asString(),
    'Verb': lambda t: t.asString(),
    'Unary': 'name expr',
    'Infix': 'name left right',
    'NameExpr' : lambda t: t.asString(),
    'IntExpr': lambda t: int(t.asString()),
    'DoubleExpr': lambda t: float(t.asString()),
}

option = {
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
}

object_names = {
    'ボール': 'circle',
    '玉': 'circle',
    '球': 'circle',
    '球形': 'circle',
    '丸': 'circle',
    '円': 'circle',
    '円形': 'circle',
    '四角': 'rectangle',
    '四角形': 'rectangle',
    '正多角形': 'polygon',
    '台形': 'trapezoid',
    '車': 'car',
    '文字': 'text'
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

directive = ['これ', 'あれ', 'それ', 'こ', 'あ', 'そ']
be = ['おく', 'ある', 'いる', '置く', 'いらっしゃる', 'おられる', 'おき', 'あり', 'おり', '置き', 'いらっしゃり', 'おられり', 'おいて', 'あって', 'いて', '置いて', 'いらっしゃって', 'おられて']
crash = ['衝突するとき', '衝突するなら', '衝突するならば', '衝突したとき', '衝突したら', '衝突したならば', '当たるとき', '当たるなら', '当たるならば', '当たったとき', '当たったなら', '当たったならば', 'あたるとき', 'あたるなら', 'あたるならば', 'あたったとき', 'あたったなら', 'あたったならば']
add = ['増加する', '増加して', '増加し', '増やす', '増やして', '増やし', '増える', '増えて', '増え', '増す', '増して', '増し', 'ふやす', 'ふやして', 'ふやし', 'ふえる', 'ふえて', 'ふえ', 'ます', 'まして', 'まし']
subtract = ['減少する', '減少して', '減少し', '減らす', '減らして', '減らし', '減る', '減って', '減り', 'へらす', 'へらして', 'へらし', 'へる', 'へって', 'へり']

def for_main(func, src, sec):
    for m in sec.main:
        func(m, src, sec)

def get_place(src, sec):
    if sec.direction is not None:
        p = str(sec.direction[2])
        if isinstance(sec.direction[1], AtomExpr):
            d1 = str(sec.direction[1])
            d1 = str(src.past_main[2]) if d1 in directive and src.past_main is not None else d1
            direct = text_direct if searchDict(d1, 0) == 'text' else object_direct
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

def text(main, src, sec, main_name, object_name):
    ss = "textMap['%s']=" % main_name
    p = get_place(src, sec)
    ss += "{x: %s, y: %s, value: '%s', textColor: '%s'}" % (p[0], p[1], str(main[1]), option[str(main[0])])
    src.sb.append(ss)
    src.sb.append('writeAllText();')

def object(main, src, sec, main_name, object_name):
    ss = "objectMap['%s']=Bodies.%s(" % (main_name, object_name)
    p = get_place(src, sec)
    ss += '%s, %s, ' % (p[0], p[1])

    #半径等の長さの指定
    if isinstance(main[1], ListExpr) and len(main[1]) != 0:
        if str(main[1][0]) == '#Radius':
            ss += str(main[1][1])
        elif str(main[1][0]) == '#DRadius':
            ss += str(main[1][1]) + '/2'
    else:
        ss += 'cvsh/rateh*0.1'

    #optionの指定
    if isinstance(main[0], AtomExpr):
        color = str(main[0])
        if color in option:
            ss += ",{render:{fillStyle:'%s'}}" % option[color]

    ss += ");\nWorld.add(engine.world, objectMap['%s']);" % main_name
    src.sb.append(ss)

def rule(main, src, sec):
    main_name = str(main[2])
    if main_name in src.definded:
        raise DefindedException
    object_name = searchDict(main_name, 0)

    if object_name == 'text':
        text(main, src, sec, main_name, object_name)
    else:
        object(main, src, sec, main_name, object_name)

    src.definded.append(main_name)
    src.past_main = main

def searchDict(main_name, i):
    if len(main_name) <= -i:
        return main_name #->World 要確認
    else:
        if i != 0 and main_name in object_names:
            return object_names[main_name]
        elif main_name[:i] in object_names:
            return object_names[main_name[:i]]
        else:
            return searchDict(main_name, i - 1)

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
    src.s += text

def assign(infix, main, src, sec):
    main_name = str(main[1]) if isinstance(main[1], AtomExpr) else str(main[2])
    if main_name in src.definded and searchDict(main_name, 0) == 'text':
        text = "\n\t\t\ttextMap['{1}'].value = String(Number(textMap['{1}'].value) {0} {2});$*".format(infix, main_name, sec.mod if sec.mod is not None else '1')
        src.endf.append(lambda s: s.replace('$*', text))
        src.ends.append(lambda s: s.replace('$*', '\n\t\t\twriteAllText();'))
    src.past_main = main

lambdas = [
    (be, lambda src, sec: for_main(rule, src, sec)),
    (add, lambda src, sec: for_main(lambda m, src, sec: assign('+', m, src, sec), src, sec)),
    (subtract, lambda src, sec: for_main(lambda m, src, sec: assign('-', m, src, sec), src, sec)),
    (crash, lambda src, sec: event('collisionEnd', src, sec)),
]

def transpile(t):
    #env = Env()
    #env.load('macaron.origami')

    e = SExpr.of(t, rules = MACARON)
    sb = []
    s = Source(e, sb)
    return s.push()
