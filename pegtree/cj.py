import pegtree as pg
from pegtree import ParseTree

CJParser = None

def getParser():
  global CJParser
  if CJParser is None:
    CJParser = pg.generate(pg.grammar('cj0.tpeg'))
  return CJParser

def parse(text):
  return getParser()(text)

VerbType = {
    'Verb1': 'V1',
    'PVerb1': 'V1',
    'Do': 'V',
}

def verbType(s):
  return VerbType.get(s, s)

VerbForm = {
  'VK5': {
      'A': 'か',
      'I': 'き',
      'T': 'い',
      'U': 'く',
      'E': 'け',
      'O': 'こ',
  },
  'VS5': {
      'A': 'さ',
      'I': 'し',
      'T': 'し',
      'U': 'す',
      'E': 'せ',
      'O': 'そ',
  },
  'VT5': {
      'A': 'た',
      'I': 'ち',
      'T': 'っ',
      'U': 'つ',
      'E': 'て',
      'O': 'と',
  },
  'VN5': { # 死
      'A': 'な',
      'I': 'に',
      'T': 'ん',
      'U': 'ぬ',
      'E': 'ね',
      'O': 'の',
  },
  'VM5': { # 読
      'A': 'ま',
      'I': 'み',
      'T': 'ん',
      'U': 'む',
      'E': 'め',
      'O': 'も',
  },
  'VR5': {  # 切
      'A': 'ら',
      'I': 'り',
      'T': 'っ',
      'U': 'る',
      'E': 'れ',
      'O': 'ろ',
  },
  'VW5': {  # 笑
      'A': 'わ',
      'I': 'い',
      'T': 'っ',
      'U': 'う',
      'E': 'え',
      'O': 'お',
  },
  'VG5': {  # 防ぐ
      'A': 'が',
      'I': 'ぎ',
      'T': 'い',
      'U': 'ぐ',
      'E': 'げ',
      'O': 'ご',
  },
  'VB5': {  # 遊ぶ
      'A': 'ば',
      'I': 'び',
      'T': 'ん',
      'U': 'ぶ',
      'E': 'べ',
      'O': 'ぼ',
  },
  'V1': { #過ぎ
    'A': '',
    'I': '',
    'T': '',
    'U': 'る',
    'E': 'れ',
    'O': 'よ',
  },
  'VS': {  # 行動
      'A': 'し',
      'I': 'し',
      'T': 'し',
      'U': 'する',
      'E': 'すれ',
      'O': 'しよ',
  },
  'VZ': {  # 論じる
      'A': 'じ',
      'I': 'じ',
      'T': 'じ',
      'U': 'ずる',
      'E': 'ずれ',
      'O': 'ぜよ',
  },
  'A': {  # 美し
      'A': 'く',
      'I': '',
      'T': '',
      'U': 'い',
      'E': 'けれ',
      'O': '',
  },
    'AVK5': {
      'A': 'か|く',
      'I': 'き',
      'T': 'い',
      'U': 'く|い',
      'E': 'け|けれ',
      'O': 'こ',
  },
  'AVW5': {
      'A': 'わ|く',
      'I': 'い',
      'T': 'っ',
      'U': 'ふ|い',
      'E': 'え|けれ',
      'O': 'お',
  },
  'P': {  # しま
      'A': 'せん',
      'I': '',
      'T': 'し',
      'U': 'す',
      'E': '',
      'O': '',
  }
}

Mood = {
    'not': ('A', 'な', 'A'),
    'base': ('U', ''),
    'if': ('E', 'ば'),
    'polite': ('I', 'ま', 'P'),
    'noun': ('I', ''),
    'past': ('T', 'た'),
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

def isHira(s):
  return len(s) == 1 and ord('あ') <= ord(s) <= ord('ん')

class Chunk(object):
  def __init__(self, base, pos, extra=None):
    self.base = base
    self.pos = pos
    self.token = base
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
        a.token = self.token + a.token
        return a
      if a.pos == 'VS' or a.pos == 'VSx':  # ('道', 'N') ('', 'V')
        a.base = self.base + a.base
        a.token = self.token + a.token
        a.pos = 'VS'
        return a
      if a.pos == 'A':  # ('青', 'N') ('白い', 'A')
        a.base = self.base + a.base
        a.token = self.token + a.token
        return a
    if self.pos == 'N':
      if isHira(self.base):  # ('お', 'N') ('どろく', 'A')
        a.base = self.token + a.base
        a.token = self.token + a.token
        return a
    return None


CJTagMethods = {
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
    if tag == '':
      return self.visit(node[0])
    if tag.endswith('.') or len(node) == 0:
      tag = tag.replace('.', '')
      chunk = Chunk(node.getToken(), self.pos(tag))      
    else:
      chunk = self.visit(node[0])
      if not tag.startswith('X'):
        chunk.pos = self.pos(tag)
    tags = tag.split('X')
    if len(tags) > 0:
      for meta in tags[1:]:
        if meta == '':
          meta = self.suffix2(node)
        else:
          meta = '@'+meta
        chunk.append(meta)
    return chunk

  def pos(self, tag):
    if tag.startswith('X'): 
      return 'N'
    return tag.split('X')[0]

  def suffix2(self, node):
    if len(node) > 0:
      base = node[0]
      s = node.substring(None, base)
      return s
    return ''




def tokenize(text_or_tree):
  if not isinstance(text_or_tree, ParseTree):
    try:
      tree = getParser()(text_or_tree)
    except RecursionError:
      print('FIXME(RecursionError)', text_or_tree)
      return []
  else:
    tree = text_or_tree
  tokenizer = Tokenizer()
  ts = []
  for node in tree.getSubNodes():
    s = node.getToken()
    token = tokenizer.visit(node)
    token.token = s
    if len(ts)>0:
      cat = ts[-1].concat(token)
      if cat is not None: ts[-1] = cat; continue
    ts.append(token)
  return ts


