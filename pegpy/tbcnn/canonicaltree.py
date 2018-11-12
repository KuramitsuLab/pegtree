import pegpy.ast as ast
import numpy as np


class CanonicalTree(object):
    __slots__ = [
        'numberOfSiblings'  # int
        , 'positionInSiblings'  # int
        , 'code'  # np.array[float]
        , 'child'
    ]

    def __init__(self, featuredetector):
        self.numberOfSiblings = 0
        self.positionInSiblings = 0
        self.code = None
        self.child = []

    def serialize(self):
        nodelist = [self]
        for childnode in self.child:
            nodelist.extend(childnode.serialize())
        return nodelist


class TreeInKernel(CanonicalTree):
    __slots__ = ['depth', 'code', 'numberOfSiblings', 'positionInSiblings', 'child']

    def __init__(self, featuredetector):
        super().__init__(featuredetector)
        self.depth = 0


'''
    def sample(t):
        t.tag
        len(t) == 0  # node なし
        t.asString()
        for label, subtree in t:
            label == ''
'''
