import unittest
import tests
from pegpy.peg import Grammar, nez

class TestTPEG(unittest.TestCase):

    def test_math(self):
        g = Grammar("math")
        g.load('math.tpeg')
        g.example('Expression,Int', '123', "[#Int '123']")
        g.example('Expression', '1+2*3', "[#Infix left=[#Int '1'] name=[# '+'] right=[#Infix left=[#Int '2'] name=[# '*'] right=[#Int '3']]]")
        self.exTest(g, nez)

    def test_manyb(self):
        g = Grammar("manyb")
        g.load('manyb.gpeg')
        self.exTest(g, nez)

    def test_nl(self):
        g = Grammar("nl")
        g.load('sample.gpeg')
        self.exTest(g, nez)


if __name__ == '__main__':
    unittest.main()
