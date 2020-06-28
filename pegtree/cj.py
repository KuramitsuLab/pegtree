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
      return (format(self.base, self.pos), self.base, self.pos, *self.extra)
    if self.extra is not None:
      return (format(self.base, self.pos), self.base, self.pos, self.extra)
    return (format(self.base, self.pos), self.base, self.pos)

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
  'VB': 'acceptVerb5X',
  'VS': 'acceptVerbDo',
  'VZ': 'acceptVerbDo',
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

  def acceptTen(self, node: ParseTree):
    return Chunk(node.getToken(), 'T')

  def acceptEOS(self, node: ParseTree):
    return Chunk(node.getToken(), 'EOS')

  def acceptEmpty(self, node: ParseTree):
    return Chunk('', 'N')

  def acceptExpression(self, node: ParseTree):
    return Chunk(node.getToken(), 'NC', node)

  def acceptBase(self, node: ParseTree):
    #print('FIXME', repr(node))
    return self.visit(node[0])

  def acceptAnd(self, node: ParseTree):
    return self.append(node, '@@then')

  def acceptNot(self, node: ParseTree):
    return self.append(node, '@not')

  def acceptAd(self, node: ParseTree):
    return Chunk(node.getToken(), 'M')

  def acceptAdj(self, node: ParseTree):
    return Chunk(node.getToken(), 'A')

  def acceptAdjN(self, node: ParseTree):
    return Chunk(node.getToken(), 'AN')

  def acceptNotOrAdj(self, node: ParseTree):
    chunk = self.append(node, '@not')
    chunk.append('@adj')
    return chunk

  def acceptNoun(self, node: ParseTree):
    return Chunk(node.getToken(), 'N')

  def acceptSNoun(self, node: ParseTree):
    return Chunk(node.getToken(0), 'NR')

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
    if len(node) == 0:
      print('FIXME', repr(node))
    base = node[0]
    chunk = self.visit(base)
    if chunk.isVerb():
      return chunk
    chunk.pos = 'VS'
    return chunk

  def acceptCommand(self, node: ParseTree):
    return self.append(node, '@command')

  def acceptPolite(self, node: ParseTree):
    return self.append(node, '@polite')

  def acceptPast(self, node: ParseTree):
    return self.append(node, '@past')

  def acceptBeen(self, node: ParseTree):
    return self.append(node, '@passive')

  def acceptCan(self, node: ParseTree):
    chunk = self.append(node, '@can')
    if chunk.pos == 'N':
      chunk.pos = 'VS'
    return chunk

  def acceptWould(self, node: ParseTree):
    return self.append(node, '@would')

  def acceptMay(self, node: ParseTree):
    return self.append(node, '@may')

  def acceptMust(self, node: ParseTree):
    return self.append(node, '@must')

  def acceptShould(self, node: ParseTree):
    return self.append(node, '@should')

  def acceptTry(self, node: ParseTree):
    return self.append(node, '@try')

  def acceptVerb1(self, node: ParseTree):
    return Chunk(node.getToken(), verbType(node.getTag()))

  def acceptIf(self, node: ParseTree):
    return self.append(node, '@@if')

  def acceptWhile(self, node: ParseTree):
    return self.append(node, '@@while')

  def acceptEvenIf(self, node: ParseTree):
    return self.append(node, '@@evenif')

  def acceptAfter(self, node: ParseTree):
    return self.append(node, '@@after')

  def acceptConjunction(self, node: ParseTree):
    return Chunk(node.getToken(), 'C')

  def acceptThat(self, node: ParseTree):
    return Chunk(node.getToken(), 'C')



def tokenize(text_or_tree):
  if not isinstance(text_or_tree, ParseTree):
    tree = getParser()(text_or_tree)
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


