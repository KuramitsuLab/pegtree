#!/usr/bin/python
# -*- coding: utf-8 -*-

from pathlib import Path
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

def isHira(s):
  return len(s) == 1 and ord('あ') <= ord(s) <= ord('ん')

class CJChunk(object):
  __slots__=['token', 'stem', 'pos', 'extra', 'arguments']

  def __init__(self, stem, pos, extra=None):
    self.token = stem
    self.stem = stem
    self.pos = pos
    self.extra = extra
    self.arguments = None

  def __repr__(self):
    ss = [self.getNormalForm(), self.pos]
    if isinstance(self.extra, list):
      ss.extend(self.extra)
    elif self.extra is not None:
      ss.append(self.extra)
    suffix = self.getSuffix()
    if suffix != '' and self.isNoun():
      ss.append(suffix)
    return repr(tuple(ss))

  def append(self, *values):
    for value in values:
      if value == '': continue
      if self.extra is None:
        self.extra = value
      else:
        if not isinstance(self.extra, list):
          self.extra = [self.extra]
        if value not in self.extra:
          self.extra.append(value)

  def remove(self, *values):
    for value in values:
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

  def isAdverb(self):
    return self.pos.startswith('NM')

  def isVerb(self):
    return self.pos.startswith('V')

  def isAdj(self):
    return self.pos.startswith('A')

  def isNounPrefix(self):
    if self.isNoun():
      if self.pos == 'NM': return False
      return self.token == self.stem or self.getSuffix().endswith('の')
    if self.isVerb() or self.isAdj():
      return not self.has('@then')

  def isVerbPrefix(self):
    if self.isNoun():
      return not self.getSuffix().endswith('の')
    return self.has('@then')

  def isAdjPrefix(self):
    if self.isNoun():
      return not self.getSuffix().endswith('の')
    return self.has('@then')

  def push(self, chunk):
    if self.arguments is None:
      self.arguments = []
    self.arguments.append(chunk)


class Tokenizer(object):
  def visit(self, node):
    tag = node.getTag()
    if tag == '':
      return self.visit(node[0])
    if tag.endswith('.') or len(node) == 0:
      tag = tag.replace('.', '')
      chunk = CJChunk(node.getToken(), self.pos(tag))      
    else:
      chunk = self.visit(node[0])
      if not tag.startswith('X'):
        chunk.pos = self.pos(tag)
    tags = tag.split('X')
    if len(tags) > 0:
      for meta in tags[1:]:
        if meta.startswith('_'): #X_then
          meta = '@'+meta[1:]
          chunk.remove(meta)
        elif meta != '':
          meta = '@'+meta
          chunk.append(meta)
    return chunk

  def pos(self, tag):
    if tag.startswith('X'): 
      return 'N'
    return tag.split('X')[0]

def readwords(file, suffix=''):
  path = Path(__file__).parent / f'cjdic/{file}'
  with path.open() as f:
    ws = []
    for line in f:
      line = line.replace('\n', suffix)
      ws.append(line)
  return ws


def fit_model(model, w, clz):
  w = w[::-1]
  if w in model:
    clz2 = model[w]
    if clz != clz2:
      model[w] = None
  else:
    model[w] = clz


def fit_word(model, w, i, clz):
  if len(w) == i:
    fit_model(model, w, clz)
  else:
    fit_model(model, w[0:i] + '.', clz)
    if i < 6:
      fit_word(model, w, i+1, clz)


class ReverseModel(object):
  def __init__(self, *dicts):
    self.model = {}
    model = {}
    for clz in dicts:
      ws = readwords(f'{clz}.txt')
      for w in ws:
        w = w[::-1]
        fit_word(model, w, 1, clz)
    for i in range(1, 6):
      for pat in model:
        if len(pat) != i:
          continue
        clz = model[pat]
        if clz is None:
          continue
        if self.predict(pat) is None:
          self.model[pat] = clz

  def predict(self, w, default=None):
    wlen = len(w)
    for p in range(1, 5):
      if p > wlen:
        break
      suffix = w[-p:]
      #print('@', suffix, model.get(suffix, None))
      if suffix in self.model:
        return self.model[suffix]
      if p + 1 > wlen:
        break
      suffix = '.' + suffix
      #print('@@', suffix, model.get(suffix, None))
      if suffix in self.model:
        return self.model[suffix]
    return default


Vt5Model = ReverseModel('VR5', 'VW5', 'VT5')
Vd5Model = ReverseModel('VM5', 'VB5')

CA = "濃篤広弛無怪なこ短狡幼弱紅イ堆聰旨貴好醜白酷汚普善潔憎快暗悪洽著眠太長え尊多懈角硬よ儚永敏穢近眩賢煙軽怖暑高明安固黒遠ぽ煩薄恐偉低畏厚良強狭旧痛鈍古淡粘辛異聡荒憂少凄緩遍熱堅深甘鋭浅豪渋若稚苦恥蒼臭痒羨青吝易乏拙遅い惨温難疎清速懶早幽寒丸赤繁腥細脆円粗佳重酸"
CNA = "恣稀別希妙歪素朧更嫌縦罪酷厭密徒闌端酣初俄切邪変乙主雑暇露粋艷楽急俗顕や雅生純義円重"

CTAIL = {
    #一文字形容詞は以下の文字に限る
    # 'VK5': "繙書乾卷発厭挽画築慄退利戴う届わ拱で囁抱搗急傾欠着履吹扱佩ま敲空弾焼堰抄い割梳び咲ねヤ" +\
    # "靡炊のさ灼頭捌妬が突嘆るふ惹敷あ掻閃なや背曵ゆせ捲砕沸麾碾喚お呟解轟抜聞戦む就し導鳴げ眩驚付" +\
    # "透撒きご耀好描嘯噴劈従ぬ頂撞往ぶ裂覗置た飽浮躓剥懐葺引巻跪塞訊措省溶束泣若焚ら嘶づ漉俯説" +\
    # "どろ行轢除向蠢逝啼磨暴とず拓招咳掃於ば渇は赴め穿破附動哭明如働蠕基釈牽舂て漬点貫疼曳湧歩" +\
    # "播放瞬ぴ輝索舁ぞつざ続涌だ肯蒔結衝研聴か誘徨ひ効呻す欺吐叩布拭斎開じ鋤頷裁碎雪こ響",
    'VT5': "穿落みぎつ過射充待こごた立保経ぶぼ佇育が峙放克分断ま撃満勝なう裁だ建発打滾も伐託擲激か持討毀絶起截",
    'VN5' :"往しい死",
    'VG5': "よ急防ろ戦め訃殺和継拉揺担濯す注扇仰え薙と祝凪瞬し嗣た漱煽稼寛か祈游へ削凌紡ほ告な漕るおゃ騒跨塞炊そ禦剥こ次ぬやはもせ脱接矧喘寿鬻鬱ねわ嗅研扱傾む雪らつ嫁泳さ繋貢の磨",
    # CVW5T = "ぬ唱渫訪被患払犒抗粧負担伝補整報買支結詠諾添よ誓従糾憩あ唄濯逢追疑ゆ迷誘粉る救遣歌" +\
    # "逐恋奪遭喪ま闘向篩ゃ言詛か飼購交揮た養攫願撓謂扱震拭諂随貰戦繕合問通蹲賜請培く酔遵喰ど" +\
    # "構拐伺杓そ嫌希拾の思い纏ろ襲揃狂競わ能祝縫宣会鎧伴使叶争傭厭商衒賄狙掬弔云囲祓舞なぐ倣" +\
    # "這習と候遇蔽匂食笑躇給斎調乞紛幾吸ごも洗失ぶ想ば雇す潤綯漂が沿ふ装贖覆占冀謳やだこ浚窺適償匿" +\
    # "行ょ惑煩ら集呪弄憂奮違謡臭庇お敬慕は曰労"
}

# た行５段活用 活用前の1文字

#
AKA = [
    ('A', 1, '散も善々惨憎濃聡寒ウ易紅ョ白ド粘無荒愛弛色短脆早サ悪イ安ぐ異コぽゃ速怖強み倒少遍尊ガ著ぱ緩堆稚よ低手良ち労疎淡旨憂吝懶高多煩丸辛重ワ固恐狡赤ょ鋭貴懈酸遠豪粗硬細黒円難潔儚篤薄古敏ぼ弱繁臭浅清普腥ロ快暑味温長青佳厚凄幽拙角タく痛け近遅賢畏酷堅渋聰え汚軽煙苦穢醜眠蝿ん暗痒そ恥怪乏幼度深熱狭甘ラ旧鈍ー永洽蒼広偉太羨映'),
    ('VK5', 1, '引頂敲碎て戴哭釈ヤ砕就向画嘶は佩梳解渇戦浮裂働ふ暴焼俯衝轟捲除付割喚で抄驚づ掃歩束湧鋤撒耀跪妬傾吹泣厭効放背響閃結抜牽肯動掻懐咳届説沸抱灼急漬塞研招呻置破於曳乾行築慄繙如従索拓鳴嘆轢省続頭ぬ挽着播斎瞬碾拱曵溶び突拭靡囁基扱ぴ呟往透穿退ひ漉蒔飽惹噴劈剥ざ弾徨聞啼輝空の炊撞開卷赴発逝吐搗訊描嘯捌焚堰点蠢覗附履導欺舂躓麾雪葺頷欠聴書咲疼叩磨舁蠕涌貫敷裁誘巻措利布'),
    ('A', 2, 'いさ|けぶ|とお|好い|かし|頭な|たな|うば|くら|切な|柔か|厳し|馨し|賎し|応し|れし|物し|均し|ら若|むな|しな|めか|にぶ|そば|ふと|がな|った|上な|がし|っこ|ろこ|凛し|慌し|見好|くと|曲し|カし|人し|ちか|ぼろ|ぶか|もた|禍し|斐な|易し|刺し|らた|もし|鹿し|賢し|訳な|荒し|軽し|地好|悪し|味し|騒し|ぼし|つな|だる|ょろ|ざう|どな|さし|はゆ|がる|宜し|いた|どし|気な|そし|暖か|新し|さな|ぢか|もじ|ばし|さま|空し|慮な|なし|しわ|角し|らか|欲し|あま|険し|愛し|清し|妖し|痛し|猛し|くさ|めし|愉し|んど|淋し|のし|重た|ほし|かる|捗し|訝し|可な|危う|題な|むご|陶し|得な|ちな|むた|笑し|らし|あさ|めた|久し|委し|等し|明る|眩し|々し|情な|疾し|びろ|いな|どお|あお|赦な|大き|目好|うし|遽し|詳し|忌し|えご|平た|やわ|らな|芳し|こい|ちろ|すご|怪し|合し|麗し|わか|枉し|つこ|べた|るし|うま|くろ|おぞ|わろ|難し|神し|近し|きな|華し|覚し|ねば|えな|んき|もな|わる|事し|ゲし|ごわ|ねた|とな|賑し|なめ|わい|じか|忙し|しろ|ゆし|ねむ|若し|仰し|侘し|ふる|敢な|香し|まじ|眠た|著し|貧し|ばゆ|るさ|たる|づき|だか|まだ|ふか|目な|軟か|遠し|酷し|継し|哀し|かい|女し|生し|みな|囂し|こわ|映ゆ|男し|しる|斐し|っご|おお|でた|おき|寂し|親し|うた|恥し|由し|うと|せな|けし|すど|疎し|恋し|ぴろ|ひど|うぶ|いし|さと|浅ま|逞し|思し|忝な|床し|てし|あな|際ど|がら|ぬる|くな|香ば|花し|夥し|まな|乏し|美し|ぴど|じろ|うす|烈し|れな|恭し|弱し|ぐろ|ぶせ|危な|福し|びし|まか|けむ|冷た|くし|小さ|あか|でか|こす|好き|ぶな|楽し|えし|雄し|図し|かた|わし|かあ|ずる|のろ|懐こ|まし|卑し|んな|ちい|あら|っき|儀な|おし|から|精し|ばや|厳つ|はや|姦し|ちた|かな|ぐさ|さむ|虚し|憎し|やさ|いろ|労し|悔し|わな|ぐら|まる|こし|やば|なが|細し|ぜな|優し|わゆ|ずき|るど|ずし|げし|せこ|うな|体な|双な|つら|温か|ぎし|とろ|ひろ|たゆ|よわ|ぶと|悲し|白し|初し|っさ|にが|じな|毒し|涼し|がゆ|ぶし|せま|激し|えら|どう|方な|とし|惜し|やし|しこ|珍し|だし|たし|少な|許な|ゆる|むさ|ぎな|くす|あし|ろな|よな|ろし|重し|あや|細か|かゆ|もろ|がた|のう|らう|煙た|喧し|瑞し|やう|懐し|疚し|づら|あつ|わど|たか|しげ|なる|あわ|嬉し|すし|正し|ろう|けな|愛な|げな|ざと|苦し|やす'),
    ('VK5', 2, 'なず|なげ|ちゆ|春め|りむ|くだ|きさ|なな|めゆ|浮つ|軋め|ふぶ|ミつ|艷め|ブつ|ずつ|えつ|かま|しお|心ゆ|りぞ|えお|はた|ラつ|たぶ|てお|粘つ|わむ|りさ|いだ|げつ|さや|だめ|タつ|わめ|うぞ|夏め|ろゆ|似つ|たむ|みが|えす|傷つ|時め|芽ぶ|のめ|ちつ|ため|せつ|とつ|めお|仄め|やぶ|そむ|ぼや|ほど|まめ|ゆわ|すず|えが|しだ|さめ|ぼつ|うず|っつ|らつ|いお|けつ|もむ|ろめ|ざめ|みむ|よめ|秋め|娜め|なつ|にま|りお|ゆが|いぶ|ぞめ|犇め|につ|さば|くつ|煌め|ぶつ|きず|色め|りま|しご|くじ|ばつ|すだ|らめ|あが|がつ|めぶ|ある|息ま|おむ|ろつ|ひら|皮む|渦ま|つむ|かわ|つめ|えき|そぶ|ずま|もど|れつ|ゃつ|かず|わつ|さつ|はぶ|てつ|とか|びゆ|でむ|しめ|うご|囁や|うめ|るめ|もと|寝つ|やめ|きま|つつ|ぎゆ|たた|しず|ぶや|ただ|のぞ|はじ|らま|れき|きめ|りつ|わぶ|いつ|きお|びつ|みつ|ばた|ごめ|ぱた|たつ|もが|がや|あば|ぼめ'),
    ('A', 3, 'まりな|でっか|りりし|たっと|限りな|頼りな|あたら|並びな|らびな|がめつ|ちくど|さみし|だざむ|どぎつ|あくど|よりな|きまず|りくど|わりな|いとど|いかつ|足りな|あまね|弔りし|気まず|たりな|ぎりな'),
    ('VK5', 3, 'だきつ|のびな|ちりし|ざまず|ひっか|はたら|すりな|いきつ|なきつ|しまね|きとど|ふりし|まごつ|とどろ|やきつ|くみし|こぎつ|ゆきつ|泣きつ|抱きつ|せびな|むかつ|まきつ|引っか|じめつ|つまず|きくど|行きつ|よぎつ|あざむ|ほっと|こまね'),
    ('A', 4, 'ろおどろ')
]
AWA = [
    ('A', 1, '散善々惨憎濃聡寒ウ易紅ョ白せド粘無荒愛弛色短脆早サ悪イ若安異コぽ速怖強み倒少遍尊ガ著ぱう緩堆稚ぞ低手良ちげ疎淡旨吝つ懶高多丸辛重ワ固恐狡ず赤鋭貴懈酸遠豪粗硬細し黒円難潔儚明篤薄古敏ぼ弱じ繁浅清普腥ロ快暑む味温長青佳厚凄幽拙角タ痛け近遅賢畏酷堅渋ね聰え汚眩軽煙苦さ穢醜眠蝿ん暗痒恥め怪乏幼度深熱狭甘好ラ旧き鈍ー永洽蒼広偉太羨映'),
    ('VW5', 1, '通嫌拾衒鎧攫撓払向宣遣伺這紛は弄漂襲狂唱囲賜戦纏篩遇冀祝ふ笑償迷思狙謳整養闘負担逢候失購唄抗拐奪蹲使謂集伝厭祓請結曰占揃誓贖随呪潤雇救揮訪躇被装能交患追合問震遭恋喰行幾従会犒乞支想窺ぬ詠粧斎食調補違培拭叶掬扱酔諂粉願慕添吸渫糾言覆匿買飼構争の弔喪憩適縫浚繕諾沿匂敬疑競商庇杓伴倣報云希奮濯歌貰賄洗詛舞習遵逐傭綯謡誘給蔽惑'),
    ('A', 2, 'けぶ|とお|えぐ|好い|頭な|たな|切な|づよ|どよ|水臭|柔か|別臭|散臭|むな|めか|にぶ|そば|ふと|った|上な|ひく|っこ|ろこ|とど|人臭|黴臭|くと|ぼろ|気臭|斐な|ぶか|もた|らた|び臭|乳臭|やす|つな|だる|ょろ|どな|はゆ|がる|いた|磯臭|つよ|気な|暖か|さな|ぢか|さま|慮な|ろよ|しわ|鹿臭|あま|小煩|しぶ|っと|そ臭|んど|重た|かる|こよ|可な|むご|題な|得な|ちな|むた|りな|めた|土臭|明る|げ臭|情な|びろ|いな|どお|あお|っか|赦な|えご|平た|やわ|こい|ちろ|すご|わか|べた|つこ|向臭|うま|落臭|わろ|照臭|地よ|びな|ねば|えな|わる|ごわ|ぼそ|ねた|わい|じか|しろ|くど|ぬく|敢な|眠た|ばゆ|たる|心憂|な臭|た臭|だか|タ臭|まだ|ふか|目な|軟か|ほそ|かい|かく|みな|こわ|映ゆ|ぎよ|しる|柿臭|っご|でた|うと|せな|すど|ぴろ|ひど|うぶ|さと|浅ま|忝な|さく|焦臭|暮臭|あな|際ど|がら|ぬる|くな|香ば|まな|じろ|金臭|ぴど|うす|とも|れな|ぐろ|危な|ちよ|めよ|どろ|まか|冷た|あか|きよ|でか|こす|ぶな|かた|倒臭|香臭|かあ|ずる|懐こ|の憂|んな|ちい|古臭|みよ|儀な|ばや|はや|ちた|労労|いろ|味よ|泥臭|わな|ぐら|まる|れ臭|やば|なが|ぜな|わゆ|るど|せこ|うな|体な|口煩|双な|温か|とろ|よわ|たゆ|ぶと|にが|にく|がゆ|程よ|せま|好よ|青臭|えら|方な|しこ|生臭|少な|許な|ゆる|くす|物憂|ろな|よな|あや|細か|かゆ|もろ|がた|煙た|見よ|づら|わど|なる|あわ|けな|愛な|げな|ざと|訳な'),
    ('VW5', 2, 'じあ|い煩|りあ|荷な|さよ|けあ|そぐ|しあ|きそ|いら|巣く|やと|ぎわ|にな|かま|みま|らそ|そお|けお|つろ|さら|りそ|映ろ|休ら|つど|もら|かば|むく|むら|計ら|まが|安ら|びか|そろ|つだ|かこ|びあ|むか|きら|語ら|ちが|ずら|にあ|きあ|ちあ|いわ|しら|ねら|べな|なら|づか|れそ|はら|ざな|れあ|たま|向か|きわ|ぎら|てが|てら|ねあ|であ|よろ|まご|住ま|つが|みあ|まよ|すら|まど|よそ|さそ|こな|あた|じわ|のい|出あ|かが|腹ば|しま|めら|めあ|いこ|すく|ぱら|じら|にお|まと|振る|せお|るお|ゃく|たが|行な|ぐな|いあ|らば|やま|喰ら|わら|じま|ねが|味わ|だよ|ちそ|いと|くま|るま|した|じゃ|逆ら|くば|らが|くる|うろ|すま|ちま|ゆた|損な|食ら|立あ|きお|つか|ぬぐ|おぶ|たぐ|もや|きか|つた|賑わ'),
    ('A', 3, 'はかな|よしな|かとな|まらな|しがな|もとな|わしな|ぢきな|かうば|忙しな|ったか|下らな|堪らな|まから|っかな|つもな|うもな|いじな|ずおお|うがな|れおお|おから|てあら|すかな|きしょ|好かな|よぎな|てしな|軟らか|ずたか|たとな|だらな|さがな|あたら|すから|っちゃ|でもな|わらか|たらな|なかよ|ごとな|つがな|りおお|ならな|らうた|もくろ|らしな|っから|ばひろ|柔らか|つかな|るぎな|ておも|っくろ|じきな'),
    ('VW5', 3, 'おとな|似かよ|あがな|うしな|つくろ|にかよ|かたら|はから|からか|へつら|のおも|やしな|うらな|まじな|あきな|んくら|つちか|まかな|げつら|さから|おぎな|面くら'),
    ('A', 4, 'っともな|あたたか'),
    ('VW5', 4, 'いともな')
]


def infer(dataset, w, default_pos='A'):

  for pos, size, pat in dataset:
      if len(w) >= size and w[-size:] in pat:
        return pos
  return default_pos


def setpos(c: CJChunk, pos):
  c.pos = pos
  return c

# check_nai(chunk)

def check_nai(chunk):
  CNAI = 'わらいみけらいかがんむげぜらびちま'
  WNAI = 'おもいがけ|ちがい|あじけ|危なげ|惜しみ|いわけ|なにげ|おとなげ|ほい|おおけ|なさけ|のっぴきなら|もうしわけ|つまら|くだら|そぐわ|ままなら|まちがい|おしみ|あっけ|居たたまら|たわい|思いがけ|いけ好か|しようが|違い|間違い|びん|情け|いけすか|つつが|やむ|味け|しょうが|大人げ|がんぜ|くちさが|すげ|たまら|あい|はか|下ら|しが|ならび|並び|ぎこち|じょさい|つまん|もったい|しどけ|ふがい|おほけ|おもん|あどけ|すけ|かたじけ|居た堪ら|おぼつか|たあい|済ま|ぎごち|さりげ|そっけ|にげ|口さが|ものたら|おっか|いたたまら|申しわけ|あたじけ|いとけ|せん|しょざい'
  if chunk.pos.startswith('V') and chunk.has('@not'):
    stem = chunk.getStem()
    if len(stem) > 1:
      if stem[-1] not in CNAI or stem in WNAI:
        nstem = chunk.stem + 'な'
        if chunk.token.startswith(nstem):
          chunk.stem = nstem
          chunk.append(f'@verb({chunk.pos})')
          chunk.pos = 'A'
          chunk.remove('@not', '@can', '@passive', '@make')
          return chunk
  return chunk

#NNO = 'その,あの,どの,この'.split(',')

def normalize(chunk: CJChunk):
  w = chunk.stem
  if chunk.pos == 'AN':
    if len(w) == 2 and w[0] not in CNA:
      chunk.pos = 'N'
    return chunk
  if chunk.pos in CTAIL and w[-1] not in CTAIL[chunk.pos] :
    chunk.stem = chunk.token
    chunk.pos = 'N'
    return chunk
  if chunk.pos == 'AVK5':
    chunk.pos = infer(AKA, w)
    if chunk.pos == 'VK5':
      chunk.remove('@then')
    return chunk
  if chunk.pos == 'Vd5':
    chunk.pos = Vd5Model.predict(w, 'VM5')
    return chunk
  if chunk.pos == 'Vt5':
    chunk.pos = Vt5Model.predict(w, 'VR5')
    return chunk
  return check_nai(chunk)


def isPrefix(c: CJChunk, pos):
  return c.pos == pos and c.extra is None

def isComposable(c: CJChunk):
  pos = c.pos
  return pos == 'N' or pos.startswith('V') or pos.startswith('A')

def isToken(c: CJChunk, pos, token):
  return c.pos == pos and c.token == token

def concat1(c: CJChunk, c2: CJChunk):
  c.token = c.token + c2.token
  return c

def concat2(c: CJChunk, c2: CJChunk):
  c2.token = c.token + c2.token
  return c2

def concat(c: CJChunk, c2: CJChunk):
  #ルール1 の前に、名詞 
  #格好いい[('格好い', 'A'), ('い', 'N')]
  if isToken(c2, 'N', 'い'):
    c.pos = 'A'
    c.append(f'@suffix({c2.token})')
    return concat1(c, c2)
  if isToken(c2, 'N', 'り'):
    c2.stem = c.token + c2.stem
    c2.append(f'@suffix({c2.token})')
    return concat2(c, c2)
  # ルール1. 名詞NVは接続される
  # [('もの', 'N'), ('ぐるわしい', 'A')]
  if isPrefix(c, 'NV') and isComposable(c2):
      #print('@concat', c.token, c2.token)
      c2.stem = c.token + c2.stem
      c2.append(f'@prefix({c.token})')
      return concat2(c, c2)
  return None

def push_argument(chunk, prefix):
  if chunk.arguments is not None:
    for a in chunk.arguments[::-1]:
      if push_argument(a, prefix):
        return True
  if chunk.isNoun() and prefix.isNounPrefix():
    print('pushN', repr(prefix), repr(chunk))
    chunk.push(prefix)
    return True
  if chunk.isVerb() and prefix.isVerbPrefix():
    print('pushV', repr(prefix), repr(chunk))
    chunk.push(prefix)
    return True
  if chunk.isAdj() and prefix.isAdjPrefix():
    print('pushA', repr(prefix), repr(chunk))
    chunk.push(prefix)
    return True
  print('!push', repr(prefix), repr(chunk))
  return False

def stringfy_arguments(chunk):
  if chunk.arguments is None:
    return repr(chunk)
  ss = []
  for argument in chunk.arguments[::-1]:
    ss.append(stringfy_arguments(argument))
  ss.append(repr(chunk))
  return '[' + ' '.join(ss) + ']'

def make_arguments(chunks):
  if len(chunks) == 0:
    return
  chunks = chunks[::-1]
  target = chunks[0]
  for prefix in chunks[1:]:
    push_argument(target, prefix)
  print('@@', stringfy_arguments(target))

def tokenize(text, parser = None):
  if isinstance(text, ParseTree):
    tree = text
  else:
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
  #make_arguments(chunks)
  return chunks

def segment(s: str, sep='/', parser = None):
  chunks = tokenize(s, parser)
  return sep.join([x.token for x in chunks])

#print(tokenize('望遠鏡で子犬が泳ぐのを見た'))
#print(tokenize('望遠鏡で{{すべての子犬が泳ぐのを}}見た'))
