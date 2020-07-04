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
  'AV1': {  # 情けない 曲げない
    'A': 'なく|',
    'I': 'な|',
    'T': 'な|',
    'U': 'ない|る',
    'E': 'なけれ|れ',
    'O': '|よ',
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

# [('情け', 'AV1', '@not')] 形容詞か一段動詞の否定形

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
      # if a.pos == 'VS' or a.pos == 'VSx':  # ('道', 'N') ('', 'V')
      #   a.base = self.base + a.base
      #   a.token = self.token + a.token
      #   a.pos = 'VS'
      #   return a
      # if a.pos == 'A':  # ('青', 'N') ('白い', 'A')
      #   a.base = self.base + a.base
      #   a.token = self.token + a.token
      #   return a
    # if self.pos == 'N':
    #   if isHira(self.base):  # ('お', 'N') ('どろく', 'A')
    #     a.base = self.token + a.base
    #     a.token = self.token + a.token
    #     return a
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

class ChunkChecker(object):
  def visit(self, chunk):
    method = f'accept{chunk.pos}'
    if hasattr(self, method):
      return getattr(self, method)(chunk)
    return chunk

  def acceptNA(self, chunk):
    w = chunk.base
    if len(w) == 2 and w[0] not in CNA:
      chunk.pos = 'N'
    return chunk

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

# 一文字形容動詞は以下の者に限る
CNA = "恣稀別希妙歪素朧更嫌縦罪酷厭密徒闌端酣初俄切邪変乙主雑暇露粋艷楽急俗顕や雅生純義円重"


## AKV5
CVK5 = "轟哭欠梳惹動利暴続塞放聴覗だ発巻め働履葺従効磨裂焼衝敷麾引炊鋤砕戦釈布佩傾曵飽で" +\
    "挽急叩蠢掻な湧いこ索卷於耀背斎た響舂肯劈乾疼浮訊づ漉泣お頂咲書除俯拱つぬ灼と轢拓牽" +\
    "わ画割附涌抄ど置聞扱戴届捲や輝穿招説か敲掃搗向破渇省空驚し繙頷瞬ひ咳沸靡描就跪眩す曳弾" +\
    "貫透抱呻碎若碾呟誘点撒焚嘆導嘶裁せ懐鳴吹う歩蒔逝明ゆ播赴む妬舁あ如溶噴拭囁啼撞好" +\
    "喚剥研抜退築付ま着往嘯措の堰蠕躓閃基突てき開欺解吐は捌厭結行さざびふぶ"
# CVK5のうち、形容詞の末尾になりうるもの
CADJT = "せゆなましか眩すむいあおう好さ明わやとだこ若たきど"

ADJT = ("ぶあつ,きつ,厳つ,いかつ,ごつ,手あつ,あつ,がめつ,むしあつ,てあつ,どぎつ,ねつ,"+\
    "うぶ,けぶ,にぶ,しぶ").split(',')

VK5T = ("ことか,いただ,あば,さしお,ささや,引っぱた,あが,とめお,みが,わなな,みむ,うすず," +\
    "くじ,すすりな,ひっか,かしず,ばらま,伸びゆ,かたむ,しのびな,さっぴ,すてお,引きさ," +\
    "けむにま,もれき,のびゆ,すだ,囁や,とど,むせびな,うわむ,吹雪,ひきさ,渦ま,もど,装束," +\
    "すえお,ひざまず,取りま,はばた,いだ,たちゆ,つたえき,羽ばた,しだ,さば,彷徨,おちゆ," +\
    "しりぞ,ぼや,ききお,かわ,くみし,なげ,とりま,ひら,はた,くど,うず,見えす,引っか,ゆが," +\
    "みちゆ,言いお,かず,ひもと,しゃうぞ,みえす,くだ,ふりむ,とめゆ,すりむ,もが,点頭,振りま," +\
    "うご,一皮む,そむ,こころゆ,ほっと,えが,ボヤ,うつむ,ひっぱた,うずま,ある,さかま,はじ," +\
    "きず,ほど,はたら,とりお,たた,あおむ,つぶや,まばた,水漬,かがや,いなな,いきま,息ま," +\
    "しご,とどろ,戦慄,のぞ,ゆわ,おもむ,ちりし,まね,さてお,いいお,心ゆ,あざむ,すぎゆ,ひとかわむ," +\
    "しばた,しょっぴ,擦りむ,つまず,ふりし,うなず,でむ,おどろ,さうぞ,きりさ,ふりま").split(',')

# AVW5T = ['と', 'ちゃ', 'お', 'る', '憂', 'ま', 'じな', 'ぶ', 'ひろ', 'な', 'だ',
#          'おも', 'きな', 'が', 'らか', 'ど', 'ご', 'も', 'あら', 'つら', '労', 'たら',
#          'かよ', 'しょ', 'うた', 'ば', 'おそ', 'たか', 'から', 'らな', '煩', 'ら', 'がな',
#          'もな', 'ふる', 'ともな', 'す', 'く', 'そ', 'のろ', 'ぎな', 'よ', 'ゆ', 'あ', 'た',
#          'くら', '臭', 'ちか', 'や', 'とな', 'おお', 'ぐ', 'い', 'こ', 'かな', 'ろ', 'ょ',
#          'しな', 'わ', 'うば', 'か', 'くろ', 'たたか', 'ゃ']

# 確実にワ行５段活用の語尾
VW5T = ['ぐな', 'いともな', 'けお', '商', 'めあ', '損な', '買', '倣', '云', '慕',
        'にな', '合', '杓', '撓', '習', '篩', 'ゃく', '宣', '漂', 'いと', '購', '補',
        'かば', 'あがな', 'るま', '適', '傭', 'げつら', '誘', '逆ら', '扱', 'おとな',
        '構', '訪', '匂', 'ねが', '飼', '償', '培', 'うろ', '集', 'しま', '向', '追',
        '狙', '諾', '思', '患', '喪', 'まど', '行', '疑', 'まと', '詛', '向か', '吸',
        'さよ', '願', 'はら', 'らそ', '逢', '巣く', '揮', '養', '沿', '冀', '蔽', 'つくろ',
        'そろ', 'たま', '謳', 'のい', '諂', 'やま', '喰', '縫', 'かたら', '失', '腹ば',
        '違', '渫', '掬', 'きお', 'せお', '粧', 'じま', '歌', '安ら', 'ちあ', 'であ',
        '立あ', '誓', '競', '幾', 'きわ', 'づか', '贖', '賑わ', '払', '敬', '蹲', '弄',
        'かが', 'つちか', '謂', '憩', '衒', '闘', 'らが', '映ろ', '呪', '窺', 'よろ',
        'なら', '伝', '洗', '戦', '揃', '争', 'うらな', 'ゆた', '担', 'くま', 'へつら',
        'もら', 'つど', '装', '奪', 'てが', '味わ', 'ぎわ', 'さそ', 'あきな', '攫', 'たぐ',
        '庇', 'こな', '拭', '面くら', '会', 'まが', 'つが', '謡', '笑', '遇', '繕', 'した',
        '問', '使', 'さら', '覆', '賜', '計ら', '休ら', '振る', '伴', 'やと', 'れそ', 'みま',
        'はから', 'ちそ', '支', 'じら', 'みあ', '匿', '嫌', '整', 'くる', 'きか', 'たが',
        '纏', 'ねら', 'まご', '襲', 'もや', '結', '潤', '祝', 'つた', '浚', '伺', '這', 'ふ',
        'おぎな', 'いこ', 'くば', '似かよ', 'きあ', 'ちま', '負', '濯', '酔', '語ら', 'りあ',
        'まかな', '交', '糾', 'ぬぐ', 'いら', 'いあ', '震', 'きそ', 'まよ', 'むか', '調',
        'そぐ', 'わら', 'むく', '惑', 'じわ', '綯', '添', '犒', '給', 'い煩', 'すく',
        'かこ', 'よそ', '言', 'てら', 'つか', '住ま', '弔', '唄', '乞', 'いわ', 'けあ',
        '出あ', '食ら', '斎', 'むら', 'だよ', 'ねあ', '救', 'そお', 'らば', '奮', '被',
        'びか', 'ざな', '恋', '詠', '祓', 'ずら', '希', '狂', 'めら', 'すま', 'べな',
        'にかよ', 'つろ', '食', '喰ら', '粉', '舞', 'かま', 'つだ', 'れあ', 'しら', '賄',
        '随', 'おぶ', '荷な', 'んくら', '迷', '報', 'やしな', 'ちが', 'さから', 'しあ',
        'きら', 'ぱら', '逐', 'びあ', 'のおも', '遣', '遭', '叶', '拾', '遵', 'は', '囲',
        '唱', 'ぎら', '抗', 'すら', 'ぬ', '想', 'りそ', '雇', '従', '行な', 'あた', '躇',
        'の', 'にお', 'るお', 'からか', '占', '通', 'じゃ', 'にあ', '紛', 'うしな', '能',
        '拐', '厭', '鎧', '貰', '請', 'まじな', 'じあ', '候', '曰']

# 形容詞かワ行５段活用か判定できないが、形容詞としない
AVW5T = ['憂', 'ともな', 'ひろ', 'おも', 'らか', 'あら', '労', 'たら',
         'かよ', 'しょ', 'うた', 'おそ', 'から', '煩',
         'ふる', 'ともな', 'のろ',
         'くら', '臭', 'ちか', 'おお', 'うば', 'くろ', 'たたか']

def setpos(c: Chunk, pos):
  c.pos = pos
  return c

def normalize(chunk):
  if chunk.pos == 'AN':
    w = chunk.base
    if len(w) == 2 and w[0] not in CNA:
      chunk.pos = 'N'
  if chunk.pos == 'AVK5':
    w = chunk.base
    if len(w) == 1 and w in CVK5:
      return setpos(chunk, 'VK5')
    tc = w[-1]
    if tc == 'つ' or tc == 'ぶ':
      for tail in ADJT:
        if w.endswith(tail): return setpos(chunk,'A')
      return setpos(chunk, 'VK5')
    if tc in CVK5 and tc not in CADJT:
      return setpos(chunk, 'VK5')
    for tail in VK5T:
      if w.endswith(tail):
        return setpos(chunk, 'VK5')
    return setpos(chunk, 'A')
  if chunk.pos == 'NA':
    w = chunk.base[:-1]
    for tail in VW5T:
      if w.endswith(tail):
        return setpos(chunk, 'N')
    for tail in AVW5T:
      if w.endswith(tail):
        return setpos(chunk, 'N')
    chunk.base = w
    return setpos(chunk, 'A')
  return chunk


def concat2(c: Chunk, c2: Chunk):
  c2.token = c.token + c2.token
  return c2 

def concat(c: Chunk, c2: Chunk):
  # ぐいっと[('ぐい', 'NA'), ('っ', 'N', 'と')]
  if c2.pos == 'N': 
    w = c2.base
    if len(w) == 1 and isHira(w):
      c2.base = c.token + c2.base
      return concat2(c, c2)
  return c.concat(c2)

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
    chunk = tokenizer.visit(node)
    chunk.token = s
    chunk = normalize(chunk)
    if len(ts)>0:
      cat = concat(ts[-1], chunk)
      if cat is not None: ts[-1] = cat; continue
    ts.append(chunk)
  return ts


