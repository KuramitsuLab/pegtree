import pegtree as pg
from pegtree import ParseTree

CJParser = None

def getParser():
  if CJParser is None:
    CJParser = pg.generate(pg.grammar('cj.tpeg'))
  return CJParser

def parse(text):
  return getParser()(text)

VerbType = {
    'VerbKA5': 'VK5',
    'VerbSA5': 'VS5',
    'VerbTA5': 'VT5',
    'VerbNA5': 'VN5',
    'VerbWA5': 'VW5',
    'VerbRA5': 'VR5',
    'VerbMA5': 'VM5',
    'VerbBA5': 'VB5',
    'VerbGA5': 'VG5',
    'Verb1': 'V1',
    'PVerbKA5': 'VK5',
    'PVerbSA5': 'VS5',
    'PVerbTA5': 'VT5',
    'PVerbNA5': 'VN5',
    'PVerbWA5': 'VW5',
    'PVerbRA5': 'VR5',
    'PVerbMA5': 'VM5',
    'PVerbBA5': 'VB5',
    'PVerbGA5': 'VG5',
    'PVerb1': 'V1',
    'Do': 'V',
}

def verbType(s):
  return VerbType.get(s, s)

VerbForm = {
  'VK5': {
      1: 'か',
      2: 'き',
      0: 'い',
      3: 'く',
      4: 'け',
      5: 'こ',
  },
  'VS5': {
      1: 'さ',
      2: 'し',
      0: 'し',
      3: 'す',
      4: 'せ',
      5: 'そ',
  },
  'VT5': {
      1: 'た',
      2: 'ち',
      0: 'っ',
      3: 'つ',
      4: 'て',
      5: 'と',
  },
  'VN5': { # 死
      1: 'な',
      2: 'に',
      0: 'ん',
      3: 'ぬ',
      4: 'ね',
      5: 'の',
  },
  'VM5': { # 読
      1: 'ま',
      2: 'み',
      0: 'ん',
      3: 'む',
      4: 'め',
      5: 'も',
  },
  'VR5': {  # 切
      1: 'ら',
      2: 'り',
      0: 'っ',
      3: 'る',
      4: 'れ',
      5: 'ろ',
  },
  'VW5': {  # 笑
      1: 'わ',
      2: 'い',
      0: 'っ',
      3: 'う',
      4: 'え',
      5: 'お',
  },
  'VG5': {  # 防ぐ
      1: 'が',
      2: 'ぎ',
      0: 'い',
      3: 'ぐ',
      4: 'げ',
      5: 'ご',
  },
  'VB5': {  # 遊ぶ
      1: 'ば',
      2: 'び',
      0: 'ん',
      3: 'ぶ',
      4: 'べ',
      5: 'ぼ',
  },
  'V1': { #過ぎ
    1: '',
    2: '',
    0: '',
    3: 'る',
    4: 'れ',
    5: 'よ',
    'N': '',
  },
  'V': {  # 行動
      1: 'し',
      2: 'し',
      0: 'し',
      3: 'する',
      4: 'すれ',
      5: 'しよ',
      'N': '',
  },
  'A': {  # 美し
      1: 'く',
      2: '',
      0: '',
      3: 'い',
      4: 'けれ',
      5: '',
  },
  'P': {  # しま
      1: 'せん',
      2: '',
      0: 'し',
      3: 'す',
      4: '',
      5: '',
  }
}

Mood = {
    'not': (1, 'な', 'A'),
    'base': (3, ''),
    'if': (4, 'ば'),
    'polite': (2, 'ま', 'P'),
    'noun': (2, ''),
    'past': (0, 'た'),
}


def format(prefix, pos, *moods):
  m = moods[0] if len(moods) > 0 else 'base'
  form = VerbForm.get(pos, {})
  mood = Mood.get(m, 'base')
  s = prefix
  if mood[0] in form:
    s = prefix + form[mood[0]] + mood[1]
    if len(mood) == 3:
      if len(moods) > 0:
        s = format(s, mood[2], *moods[1:])
      else:
        s = format(s, mood[2])
  return s


class Chunk(object):
  def __init__(self, base, pos, extra=None):
    self.base = base
    self.pos = pos
    self.extra = extra

  def data(self):
    if isinstance(self.extra, list) or isinstance(self.extra, tuple):
      return (format(self.base, self.pos), self.pos, *self.extra)
    if self.extra is not None:
      return (format(self.base, self.pos), self.pos, self.extra)
    return (format(self.base, self.pos), self.pos)

  def __repr__(self):
    return repr(self.data())

  def append(self, t):
    if t != '':
      if self.extra is None:
        self.extra = t
      else:
        if not isinstance(self.extra, list):
          self.extra = [self.extra]
        self.extra.append(t)

  def isNoun(self):
    return self.pos.startswith('N')

  def isVerb(self):
    return self.pos.startswith('V')

  def isAdj(self):
    return self.pos.startswith('A')

  def isN(self):
    return self.pos == 'N' and self.extra is None

  def concat(self, a):
    if self.isN():
      if a.pos == 'N':  # ('寄り', 'N') ('道', 'N')
        a.base = self.base + a.base
        return a
      if a.pos == 'V':  # ('道', 'N') ('', 'V')
        a.base = self.base + a.base
        return a
      if a.pos == 'A':  # ('青', 'N') ('白い', 'A')
        a.base = self.base + a.base
        return a
    return None


CJTagMethods = {
  'PNoun': 'acceptNoun',
  'PAdj': 'acceptAdj',
  'PVerb1': 'acceptVerb1',
  'PPNoun': 'acceptNoun',
  'PPAdj': 'acceptAdj',
  'PPVerb1': 'acceptVerb1',
  'VK5': 'acceptVerb5',
  'VS5': 'acceptVerb5',
  'VT5': 'acceptVerb5',
  'VN5': 'acceptVerb5',
  'VM5': 'acceptVerb5',
  'VR5': 'acceptVerb5',
  'VW5': 'acceptVerb5',
  'VG5': 'acceptVerb5',
  'VB5': 'acceptVerb5',
  'Vi5': 'acceptVerb5X',
  'Vt5': 'acceptVerb5X',
  'Vd5': 'acceptVerb5X',
  'VS': 'acceptVerbDo',
  'VSx': 'acceptVerbDoX',
  'Object': 'acceptArgument',
}

def verb(s, *moods):
  if isinstance(s, Chunk):
    return format(s.base, s.pos, *moods)
  tokens = tokenize(str(s))
  prefix = ''
  for token in tokens:
    if token.pos in VerbForm:
      return format(prefix+token.base, token.pos, *moods)
    else:
      prefix += token.base
  return format(prefix, 'V', *moods)



class Tokenizer(object):
  def visit(self, node):
    tag = node.getTag()
    if tag in CJTagMethods:
      method = CJTagMethods[tag]
    else:
      method = f'accept{tag}'
      CJTagMethods[tag] = method
    if not hasattr(self, method):
      method = 'acceptUnknown'
      CJTagMethods[tag] = method
    return getattr(self, method)(node)

  def suffix(self, node, base):
    s = node.substring(None, base)
    return '' if s == '' else '+'+s

  def append(self, node: ParseTree, anno):
    chunk = self.visit(node[0])
    chunk.append(anno)
    return chunk

  def acceptUnknown(self, node: ParseTree):
    print('FIXME', repr(node))
    return Chunk(node.getToken(), 'U', node)

  def acceptBase(self, node: ParseTree):
    #print('FIXME', repr(node))
    return self.visit(node[0])

  def acceptAnd(self, node: ParseTree):
    return self.append(node, '@@then')

  def acceptNot(self, node: ParseTree):
    return self.append(node, '@not')

  def acceptAd(self, node: ParseTree):
    return Chunk(node.getToken(), 'AD')

  def acceptAdj(self, node: ParseTree):
    return Chunk(node.getToken(), 'A')

  def acceptNoun(self, node: ParseTree):
    return Chunk(node.getToken(), 'N')

  def acceptArgument(self, node):
    chunk = self.visit(node[0])
    chunk.append(self.suffix(node, node[0]))
    return chunk

  def acceptVerb5(self, node):
    token = node.getToken(0) if len(node)>0 else node.getToken()
    return Chunk(token, node.getTag())

  def acceptVerb5X(self, node):
    chunk = self.visit(node[0])
    if chunk.isVerb():
      return chunk
    token = node.getToken(0)
    return Chunk(token, node.getTag())

  def acceptVerbDo(self, node):
    if len(node) == 0:
      return Chunk('', 'VS')
    chunk = self.visit(node[0])
    chunk.pos = 'VS'
    return chunk

  def acceptVerbDoX(self, node):
    if len(node) == 0:
      return Chunk('', 'VSx')
    chunk = self.visit(node[0])
    chunk.pos = 'VSx'
    return chunk


  def acceptVerb(self, node):
    base = node[0]
    chunk = self.visit(base)
    if chunk.isVerb():
      return chunk
    return Chunk(base.getToken(), verbType(base.getTag()))


  def acceptPast(self, node: ParseTree):
    return self.append(node, '@past')

  def acceptBeen(self, node: ParseTree):
    return self.append(node, '@passive')

  def acceptCan(self, node: ParseTree):
    return self.append(node, '@can')

  def acceptMay(self, node: ParseTree):
    return self.append(node, '@may')

  def acceptMust(self, node: ParseTree):
    return self.append(node, '@must')

  def acceptVerb1(self, node: ParseTree):
    return Chunk(node.getToken(), verbType(node.getTag()))

  def acceptIf(self, node: ParseTree):
    return self.append(node, '@@if')


def tokenize(text_or_tree):
  if not isinstance(text_or_tree, ParseTree):
    tree = getParser()(text_or_tree)
  else:
    tree = text_or_tree
  tokenizer = Tokenizer()
  ts = []
  for node in tree.getSubNodes():
    token = tokenizer.visit(node)
    if len(ts)>0:
      cat = ts[-1].concat(token)
      if cat is not None: ts[-1] = cat; continue
    ts.append(token)
  return ts


