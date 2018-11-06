import unittest
from tree2vec import Tree2Vec
from pegpy.peg import *
import os


def parsetree(opt):
    g = Grammar('x')
    path = os.path.join(os.path.dirname(os.path.abspath(
        __file__)), '../..', 'grammar', opt['grammar'])
    g.load(path)
    print('')
    p = nez(g)
    return map(lambda i: p(i), opt['inputs'])


class TestTree2Vec(unittest.TestCase):

    def setUp(self):
        print("test cases for ")
        inputstring_0 = "1+2+3"
        inputstring_1 = "1+2-3"
        setOfTags = ["Infix", "Int"]
        parseoption = {'grammar': "math.tpeg",
                       'inputs': [inputstring_0, inputstring_1]}
        self.parsetrees = parsetree(parseoption)
        self.t2v = Tree2Vec(setoftags=setOfTags, leafencoder=(lambda x: x))

    def test_ast2canonicalTree(self):
        for originalTree in self.parsetrees:
            print(originalTree)
            for label, subtree in originalTree:
                print(subtree)
            #canotree = self.t2v.ast2canonicalTree(originalTree)
            #self.assertEqual(canotree.positionInSiblings, 0)

    def tearDown(self):
        del self.parsetrees
        del self.t2v


if __name__ == "__main__":
    unittest.main()
