import numpy as np
import tensorflow as tf
from functools import reduce
from functools import lru_cache
import canonicaltree as ct


class Tree2Vec(object):

    __slots__ = [
        'leafEncoder'  # tag -> tf.Value[dtype = float, shape = (featuredimension,1)]
        , 'tagEncoder'  # Dict{tag, tf.Value[dtype = float, shape = (featuredimension,1)]}
        , 'feature_dimension'  # int
        , 'feature_detector'  # int
        , 'window_depth'  # int
        , 'w_conv_l', 'w_conv_t', 'w_conv_r', 'b_conv', 'w_agg', 'w_agg_r', 'w_agg_l', 'b_agg' # model parameters
    ]

    def __init__(self, setoftags, leafencoder, featureDetector=80, windowDepth=2):
        # generating tag encoder
        numberOfItems = len(setoftags)
        self.feature_dimension = numberOfItems + 1
        onehotVecList = tf.eye(numberOfItems, num_columns=numberOfItems + 1)
        encoder = {}
        for i in range(0, numberOfItems):
            encoder[setoftags[i]] = onehotVecList[i]
        self.tagEncoder = encoder
        leafUnitVector = tf.Variable([2 ** numberOfItems >> d & 1 for d in range(numberOfItems + 1)],dtype=tf.float32)
        self.leafEncoder = lambda leaf: tf.scalar_mul(leafencoder(leaf), leafUnitVector)
        self.feature_detector = featureDetector
        self.window_depth = windowDepth
        self.w_conv_l = tf.Variable(tf.random_normal([featureDetector, featureDetector], stddev=0.01))
        self.w_conv_r = tf.Variable(tf.random_normal([featureDetector, featureDetector], stddev=0.01))
        self.w_conv_t = tf.Variable(tf.random_normal([featureDetector, featureDetector], stddev=0.01))
        self.b_conv = tf.Variable(tf.random_normal([featureDetector], stddev=0.01))
        self.w_agg = tf.Variable(tf.random_normal([featureDetector, featureDetector], stddev=0.01))
        self.w_agg_l = tf.Variable(tf.random_normal([featureDetector, featureDetector], stddev=0.01))
        self.w_agg_r = tf.Variable(tf.random_normal([featureDetector, featureDetector], stddev=0.01))
        self.b_agg = tf.Variable(tf.random_normal([featureDetector], stddev=0.01))

    # tag -> tf.Variable(feature_dimension,1)
    def oneHotVector_coder(self, originalTag):
        if originalTag in self.tagEncoder:
            return self.tagEncoder[originalTag]
        else:
            return self.leafEncoder(originalTag)

    # ast2canonicalTree :: AST -> CanonicalTree
    def ast2canonicalTree(self, ast, sibpos=0, sibnum=0):
        topNode = ct.CanonicalTree(self.feature_dimension)
        topNode.code = self.oneHotVector_coder(ast.tag)
        topNode.numberOfSiblings = sibnum
        topNode.positionInSiblings = sibpos
        sibNum = len(ast)
        if sibNum != 0:
            sibPosCounter = 0
            for label, subtree in ast:
                topNode.child.append(self.ast2canonicalTree(subtree, sibpos=sibPosCounter, sibnum=sibNum-1))
                sibPosCounter += 1
        return topNode

    # canonicalTree2KernekTree :: CanonicalTree -> TreeInKernel
    def canonicalTree2KernelTree(self, canotree, depthcounter=0):
        topNode = ct.TreeInKernel(self.feature_detector)
        originalCode = canotree.code
        topNode.code = tf.pad(originalCode, [[0, self.feature_detector - self.feature_dimension]])
        topNode.numberOfSiblings = canotree.numberOfSiblings
        topNode.positionInSiblings = canotree.positionInSiblings
        topNode.depth = depthcounter
        if depthcounter < self.window_depth - 1:
            if len(canotree.child) == 0:
                # zero padding
                zeroNode = ct.CanonicalTree(self.feature_detector)
                zeroNode.code = np.zeros(self.feature_dimension)
                topNode.child = [self.canonicalTree2KernelTree(zeroNode, depthcounter=depthcounter + 1)]
            else:
                topNode.child = list(map(lambda t: self.canonicalTree2KernelTree(t, depthcounter=depthcounter + 1), canotree.child))
        else:
            topNode.child = []
        return topNode

    # tbcnn :: TreeInKernel -> tf.Value(shape=(feature_detector,1))
    def tbcnn(self, top):
        treeInKernel = top.serialize()
        w_dot_X = tf.zeros([self.feature_detector, 1])
        for i in range(0, len(treeInKernel)):
            eta_t_i = (self.window_depth - treeInKernel[i].depth) / self.window_depth
            n = treeInKernel[i].numberOfSiblings
            eta_r_i = 0 if n == 0 else (1 - eta_t_i) * treeInKernel[i].positionInSiblings / n
            eta_l_i = (1 - eta_r_i) * (1 - eta_t_i)
            weight_conv = tf.scalar_mul(eta_t_i, self.w_conv_t) + tf.scalar_mul(eta_r_i, self.w_conv_r) + tf.scalar_mul(eta_l_i, self.w_conv_l)
            code_vector = tf.cast(treeInKernel[i].code, dtype=tf.float32)
            w_dot_X += tf.matmul(weight_conv, tf.reshape(code_vector, shape=[self.feature_detector, 1]))
        return tf.tanh(w_dot_X + tf.reshape(self.b_conv, shape=[self.feature_detector, 1]))

    # tbcnn_layer :: CononicalTree -> CanonicalTree
    def tbcnn_layer(self, top):
        kerneltree = self.canonicalTree2KernelTree(top)
        top.code = self.tbcnn(kerneltree)
        for i in range(0, len(top.child)):
            top.child[i] = self.tbcnn_layer(top.child[i])
        return top

    # agg_layer :: CononinalTree -> tf.Value(shape=(feature_detector,1))
    @lru_cache(maxsize=100)
    def agg_layer(self, top):
        childNodes = top.child
        if len(childNodes) == 0:
            topCode = tf.reshape(top.code, shape=[self.feature_detector, 1])
            return tf.matmul(self.w_agg, topCode) + tf.reshape(self.b_agg, shape=[self.feature_detector, 1])
        else:
            sumUpAggChild = np.zeros(shape=[self.feature_detector, 1])
            for i in range(len(childNodes)):
                vec = self.agg_layer(childNodes[i])
                eta_l_i = (childNodes[i].positionInSiblings - 1) / (childNodes[i].numberOfSiblings - 1)
                w_agg_i = tf.scalar_mul(eta_l_i, self.w_agg_l) + tf.scalar_mul(1-eta_l_i, self.w_agg_r)
                sumUpAggChild += tf.matmul(w_agg_i, vec)
            return sumUpAggChild + tf.matmul(self.w_agg, tf.reshape(top.code,shape=[self.feature_detector, 1])) + tf.reshape(self.b_agg, shape=[self.feature_detector, 1])

    def vectorRepresentation(self, ast, convolutionTimes=3):
        ctree = self.ast2canonicalTree(ast)
        for i in range(0, convolutionTimes):
            ctree = self.tbcnn_layer(ctree)
        return self.agg_layer(ctree)
