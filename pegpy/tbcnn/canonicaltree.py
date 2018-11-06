import pegpy.ast as ast


class CanonicalTree(object):
    __slots__ = [
        'numberOfSiblings'  # int
        , 'positionInSiblings'  # int
        , 'code'  # np.array[float]
        , 'child'
    ]

    def __init__(self):
        self.numberOfSiblings = 0
        self.positionInSiblings = 0
        self.code = None
        self.child = []

    def serialize(self):
        raise NotImplementedError


class TreeInKernel(CanonicalTree):
    __slots__ = ['depth', 'code', 'numberOfSiblings',
                 'positionInSiblings', 'child']

    def __init__(self):
        super.__init__()
        self.depth = 0


'''
    def sample(t):
        t.tag
        len(t) == 0  # node なし
        t.asString()
        for label, subtree in t:
            label == ''
'''
