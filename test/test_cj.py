import unittest
import pegtree.cj as cj


S='''
青白く丸い人が寄り道する
大きなノッポの古時計をみた
ハワイについて述べました
ハワイに着いて考えられる
'''.split('\n')

ADJ='''高い
高くない
高過ぎる
高め
高める
高さ
'''.split('\n')

def t(s): return cj.tokenize(s)[0].data()

class TestCJ(unittest.TestCase):

    def test_parse(self):
      for s in S:
        print(repr(cj.parse(s)))

    def test_tokenize(self):
      for s in S:
        print(cj.tokenize(s))

    def test_adj(self):
      self.assertTupleEqual(t('高い'), ('高い', 'A'))
      self.assertTupleEqual(t('高くない'), ('高い', 'A', '@not'))
      self.assertTupleEqual(t('高かった'), ('高い', 'A', '@past'))
      self.assertTupleEqual(t('高くなかった'), ('高い', 'A', '@not', '@past'))
      self.assertTupleEqual(t('高め'), ('高め', 'N'))
      self.assertTupleEqual(t('高める'), ('高める', 'V1'))
      self.assertTupleEqual(t('高さ'), ('高さ', 'N'))
      self.assertTupleEqual(t('青白い'), ('青白い', 'A'))
      self.assertTupleEqual(t('美味しい'), ('美味しい', 'A'))
      self.assertTupleEqual(t('おいしい'), ('おいしい', 'A'))
      print(t('情けない'))
    def test_verb(self):
      print(cj.verb('勝つ', 'polite'))
      print(cj.verb('勝つ', 'not'))
      print(cj.verb('勝つ', 'past'))



if __name__ == '__main__':
    unittest.main()
