import pegtree as pg
from pegtree import ParseTree

CJParser = None

def getParser():
  global CJParser
  if CJParser is None:
    CJParser = pg.generate(pg.grammar('cj0.tpeg'))
  return CJParser

VerbForm = {
  'VK5': { 'A': 'か', 'I': 'き', 'T': 'い', 'U': 'く', 'E': 'け', 'O': 'こ', },
  'VS5': { 'A': 'さ', 'I': 'し', 'T': 'し', 'U': 'す', 'E': 'せ', 'O': 'そ', },
  'VT5': { 'A': 'た', 'I': 'ち', 'T': 'っ', 'U': 'つ', 'E': 'て', 'O': 'と', },
  'VN5': { 'A': 'な', 'I': 'に', 'T': 'ん', 'U': 'ぬ', 'E': 'ね', 'O': 'の', },
  'VM5': { 'A': 'ま', 'I': 'み', 'T': 'ん', 'U': 'む', 'E': 'め', 'O': 'も', },
  'VR5': { 'A': 'ら', 'I': 'り', 'T': 'っ', 'U': 'る', 'E': 'れ', 'O': 'ろ', },
  'VW5': { 'A': 'わ', 'I': 'い', 'T': 'っ', 'U': 'う', 'E': 'え', 'O': 'お', },
  'VG5': { 'A': 'が', 'I': 'ぎ', 'T': 'い', 'U': 'ぐ', 'E': 'げ', 'O': 'ご', },
  'VB5': { 'A': 'ば', 'I': 'び', 'T': 'ん', 'U': 'ぶ', 'E': 'べ', 'O': 'ぼ', },
  'V1': { 'A': '', 'I': '', 'T': '', 'U': 'る', 'E': 'れ', 'O': 'よ', },
  'VS': { 'A': 'し', 'I': 'し', 'T': 'し', 'U': 'する', 'E': 'すれ', 'O': 'しよ',},
  'VZ': { 'A': 'じ', 'I': 'じ', 'T': 'じ', 'U': 'ずる', 'E': 'ずれ', 'O': 'ぜよ',},
  'A': { 'A': 'く', 'I': '', 'T': '', 'U': 'い', 'E': 'けれ', 'O': '', },
  'P': { 'A': 'せん', 'I': '', 'T': 'し', 'U': 'す', 'E': '', 'O': '', }, 
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

class CJChunk(object):
  __slots__=['token', 'stem', 'pos', 'extra']
  def __init__(self, stem, pos, extra=None):
    self.stem = stem
    self.pos = pos
    self.token = stem
    self.extra = extra

  def __repr__(self):
    if self.extra is None:
      return repr((self.getNormalForm(), self.pos))
    elif isinstance(self.extra, list):
      return repr((self.getNormalForm(), self.pos, *self.extra))
    return repr((self.getNormalForm(), self.pos, self.extra))

  def append(self, value):
    if value == '': return
    if self.extra is None:
      self.extra = value
    else:
      if not isinstance(self.extra, list):
        self.extra = [self.extra]
      if value not in self.extra:
        self.extra.append(value)

  def remove(self, value):
    if isinstance(self.extra, list):
      if value in self.extra:
        self.extra.remove(value)
      if len(self.extra) == 0:
        self.extra = None
    elif self.extra == value:
      self.extra = None

  def has(self, value):
    if isinstance(self.extra, list):
      return value in self.extra
    return self.extra == value

  def getToken(self):
    return self.token

  def getStem(self):
    return self.stem

  def getSuffix(self):
    return self.token[len(self.stem):]

  def getNormalForm(self, polite=False, pos=None):
    if pos is None:
      pos = self.pos
    if pos in VerbForm:
      return self.stem + VerbForm[pos]['U']
    return self.stem


  def isNoun(self):
    return self.pos.startswith('N')

  def isVerb(self):
    return self.pos.startswith('V')

  def isAdj(self):
    return self.pos.startswith('A')


# def verb(s, *moods):
#   if isinstance(s, CJChunk):
#     return format(s.base, s.pos, *moods)
#   tokens = tokenize(str(s))
#   prefix = ''
#   for token in tokens:
#     if token.pos in VerbForm:
#       return format(prefix+token.base, token.pos, *moods)
#     else:
#       prefix += token.base
#   return format(prefix, 'V', *moods)

# class ChunkChecker(object):
#   def visit(self, chunk):
#     method = f'accept{chunk.pos}'
#     if hasattr(self, method):
#       return getattr(self, method)(chunk)
#     return chunk

#   def acceptNA(self, chunk):
#     w = chunk.base
#     if len(w) == 2 and w[0] not in CNA:
#       chunk.pos = 'N'
#     return chunk

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


#一文字形容詞は以下の文字に限る
CA = "濃篤広弛無怪なこ短狡幼弱紅イ堆聰旨貴好醜白酷汚普善潔憎快暗悪洽著眠太長え尊多懈角硬" +\
    "よ儚永敏穢近眩賢煙軽怖暑高明安固黒遠ぽ煩薄恐偉低畏厚良強狭旧痛鈍古淡粘辛異聡荒憂少凄緩" +\
    "遍熱堅深甘鋭浅豪渋若稚苦恥蒼臭痒羨青吝易乏拙遅い惨温難疎清速懶早幽寒丸赤繁腥" +\
    "細脆円粗佳重酸"

# 一文字形容動詞は以下の者に限る
CNA = "恣稀別希妙歪素朧更嫌縦罪酷厭密徒闌端酣初俄切邪変乙主雑暇露粋艷楽急俗顕や雅生純義円重"

# た行５段活用 活用前の1文字
CVK5T = "繙書乾卷発厭挽画築慄退利戴う届わ拱で囁抱搗急傾欠着履吹扱佩ま敲空弾焼堰抄い割梳び咲ねヤ" +\
    "靡炊のさ灼頭捌妬が突嘆るふ惹敷あ掻閃なや背曵ゆせ捲砕沸麾碾喚お呟解轟抜聞戦む就し導鳴げ眩驚付" +\
    "透撒きご耀好描嘯噴劈従ぬ頂撞往ぶ裂覗置た飽浮躓剥懐葺引巻跪塞訊措省溶束泣若焚ら嘶づ漉俯説" +\
    "どろ行轢除向蠢逝啼磨暴とず拓招咳掃於ば渇は赴め穿破附動哭明如働蠕基釈牽舂て漬点貫疼曳湧歩" +\
    "播放瞬ぴ輝索舁ぞつざ続涌だ肯蒔結衝研聴か誘徨ひ効呻す欺吐叩布拭斎開じ鋤頷裁碎雪こ響"
CVT5T = "穿落みぎつ過射充待こごた立保経ぶぼ佇育が峙放克分断ま撃満勝なう裁だ建発打滾も伐託擲激か"+\
  "持討毀絶起截"
CVN5T = "往しい死"
CVG5T = "よ急防ろ戦め訃殺和継拉揺担濯す注扇仰え薙と祝凪瞬し嗣た漱煽稼寛か祈游へ削凌紡ほ告な"+\
  "漕るおゃ騒跨塞炊そ禦剥こ次ぬやはもせ脱接矧喘寿鬻鬱ねわ嗅研扱傾む雪らつ嫁泳さ繋貢の磨"
CVW5T = "ぬ唱渫訪被患払犒抗粧負担伝補整報買支結詠諾添よ誓従糾憩あ唄濯逢追疑ゆ迷誘粉る救遣歌" +\
    "逐恋奪遭喪ま闘向篩ゃ言詛か飼購交揮た養攫願撓謂扱震拭諂随貰戦繕合問通蹲賜請培く酔遵喰ど" +\
    "構拐伺杓そ嫌希拾の思い纏ろ襲揃狂競わ能祝縫宣会鎧伴使叶争傭厭商衒賄狙掬弔云囲祓舞なぐ倣" +\
    "這習と候遇蔽匂食笑躇給斎調乞紛幾吸ごも洗失ぶ想ば雇す潤綯漂が沿ふ装贖覆占冀謳やだこ浚窺適償匿" +\
    "行ょ惑煩ら集呪弄憂奮違謡臭庇お敬慕は曰労"
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

# # 形容詞かワ行５段活用か判定できないが、形容詞としない
# AVW5T = ['憂', 'ともな', 'ひろ', 'おも', 'らか', 'あら', '労', 'たら',
#          'かよ', 'しょ', 'うた', 'おそ', 'から', '煩',
#          'ふる', 'ともな', 'のろ',
#          'くら', '臭', 'ちか', 'おお', 'うば', 'くろ', 'たたか']

def setpos(c: Chunk, pos):
  c.pos = pos
  return c


NNO = 'その,あの,どの,この'.split(',')

def normalize(chunk):
  w = chunk.base
  if chunk.pos == 'N':
    if len(w) == 1 and isHira(w) and chunk.token not in NNO:
      chunk.base = chunk.token
      chunk.extra = None
    return chunk
  if chunk.pos == 'AN':
    if len(w) == 2 and w[0] not in CNA:
      chunk.pos = 'N'
    return chunk
  if chunk.pos == 'A':
    if len(w) == 1 and w not in CA:
      chunk.pos = 'N'
      chunk.base = chunk.token
    return chunk
  if chunk.pos == 'VT5':
    if w[-1] not in CVT5T:
      #print('DEBUG', w, chunk)
      chunk.base = chunk.token
      chunk.pos = 'N'
    return chunk
  if chunk.pos == 'VN5':
    if w[-1] not in CVN5T:
      #print('DEBUG', w, chunk)
      chunk.base = chunk.token
      chunk.pos = 'N'
    return chunk
  if chunk.pos == 'VG5':
    if w[-1] not in CVG5T:
      #print('DEBUG', w, chunk)
      chunk.base = chunk.token
      chunk.pos = 'N'
    return chunk
  if chunk.pos == 'VW5':
    if w[-1] not in CVW5T:
      #print('DEBUG', w, chunk)
      chunk.base = chunk.token
      chunk.pos = 'N'
    return chunk
  if chunk.pos == 'AVK5':
    if len(w) == 1 and w in CVK5:
      return setpos(chunk, 'VK5')
    tc = w[-1]
    if tc == 'つ' or tc == 'ぶ':
      for tail in ADJT:
        if w.endswith(tail): return normalize(setpos(chunk,'A'))
      return setpos(chunk, 'VK5')
    if tc in CVK5 and tc not in CADJT:
      return setpos(chunk, 'VK5')
    for tail in VK5T:
      if w.endswith(tail):
        return setpos(chunk, 'VK5')
    return normalize(setpos(chunk, 'A'))
  if chunk.pos == 'NA':
    w = chunk.base[:-1]
    for tail in VW5T:
      if w.endswith(tail):
        return setpos(chunk, 'N')
    chunk.base = w
    return normalize(setpos(chunk, 'A'))
  return chunk


def isPrefix(c: Chunk, pos):
  return c.pos == pos and c.extra is None

def isComposable(c: Chunk):
  pos = c.pos
  return pos == 'N' or pos.startswith('V') or pos.startswith('A')


def isToken(c: Chunk, pos, token):
  return c.pos == pos and c.token == token

def concat1(c: Chunk, c2: Chunk):
  c.token = c.token + c2.token
  return c

def concat2(c: Chunk, c2: Chunk):
  c2.token = c.token + c2.token
  return c2

def concat(c: Chunk, c2: Chunk):
  #ルール1 の前に、名詞 
  #格好いい[('格好い', 'A'), ('い', 'N')]
  if isToken(c2, 'N', 'い'):
    c.pos = 'A'
    c.append(f'@suffix({c2.token})')
    return concat1(c, c2)
  if isToken(c2, 'N', 'り'):
    c2.base = c.token + c2.base
    c2.append(f'@suffix({c2.token})')
    return concat2(c, c2)
  # ルール1. 名詞NVは接続される
  # [('もの', 'N'), ('ぐるわしい', 'A')]
  if isPrefix(c, 'NV') and isComposable(c2):
      #print('@concat', c.token, c2.token)
      c2.base = c.token + c2.base
      c2.append(f'@prefix({c.token})')
      return concat2(c, c2)
  # ルール1. 名詞は接続される
  # [('もの', 'N'), ('ぐるわしい', 'A')]
  # if isPrefix(c) and isComposable(c2):
  #     print('@concat', c.token, c2.token)
  #     c2.base = c.token + c2.base
  #     c2.append(f'@prefix({c.token})')
  #     return concat2(c, c2)
  # 動詞の次に形容詞はこない
  # どす黒い[('どす', 'VS5'), ('黒い', 'A')]
  # ちいさい[('ちい', 'A'), ('さい', 'A')]
  # if (c.pos.startswith('V') or c.pos.startswith('A')) and c2.pos.startswith('A'):
  #     c2.base = c.token + c2.base
  #     c2.append(f'@prefix({c.token})')
  #     return concat2(c, c2)
  # いいふくめる [('いい', 'A'), ('ふくめる', 'V1')]
  # if c.pos.startswith('A') and c.token.endswith('い') and c2.pos.startswith('V'):
  #     c2.base = c.token + c2.base
  #     c2.append(f'@prefix({c.token})')
  #     return concat2(c, c2)
  return None

def tokenize(text, parser = None):
  if parser is None:
    parser = getParser()
  try:
    tree = getParser()(text)
  except RecursionError:
    print('FIXME(RecursionError)', text)
    return []
  tokenizer = Tokenizer()
  chunks = []
  for node in tree.getSubNodes():
    s = node.getToken()
    chunk = tokenizer.visit(node)
    chunk.token = s
    chunk = normalize(chunk)
    if len(chunks)>0:
      cat = concat(chunks[-1], chunk)
      if cat is not None: chunks[-1] = cat; continue
    chunks.append(chunk)
  return chunks


def segment(s: str, sep='/', parser = None):
  chunks = tokenize(s, parser)
  return sep.join([x.token for x in chunks])
