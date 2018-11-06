import numpy as np
import tensorflow as tf
from keras.utils import np_utils
from functools import reduce
from pegpy.ast import *
from functools import lru_cache
import canonicaltree as ct


class Tree2Vec(object):

    __slots__ = [
        'leafEncoder'  # tag -> np.array[float ** featureDemention]
        , 'tagEncoder'  # Dict{tag, np.array}
        , 'feature_demention'  # int
        , 'feature_detector'  # int
        , 'window_depth'  # int
        # model parameters
        , 'w_conv_l', 'w_conv_t', 'w_conv_r', 'b_conv', 'w_agg', 'w_agg_r', 'w_agg_l', 'b_agg'
    ]

    def __init__(self, setoftags, leafencoder, featureDemention=100, featureDetector=80, windowDepth=2):
        # generating tag encoder
        numberOfItems = len(setoftags)
        onehotVecList = np.eye(numberOfItems, numberOfItems + 1)
        encoder = {}
        for i in range(0, numberOfItems):
            encoder[setoftags[i]] = onehotVecList[i]
        self.tagEncoder = encoder
        self.leafEncoder = leafencoder
        self.feature_demention = featureDemention
        self.feature_detector = featureDetector
        self.window_depth = windowDepth
        self.w_conv_l = tf.Variable(tf.random_normal(
            [featureDetector, featureDemention], stddev=0.01))
        self.w_conv_r = tf.Variable(tf.random_normal(
            [featureDetector, featureDemention], stddev=0.01))
        self.w_conv_t = tf.Variable(tf.random_normal(
            [featureDetector, featureDemention], stddev=0.01))
        self.b_conv = tf.Variable(tf.random_normal(
            [featureDemention], stddev=0.01))
        self.w_agg = tf.Variable(tf.random_normal(
            [featureDetector, featureDemention], stddev=0.01))
        self.w_agg_l = tf.Variable(tf.random_normal(
            [featureDetector, featureDemention], stddev=0.01))
        self.w_agg_r = tf.Variable(tf.random_normal(
            [featureDetector, featureDemention], stddev=0.01))
        self.b_agg = tf.Variable(tf.random_normal(
            [featureDemention], stddev=0.01))

    def oneHotVector_coder(self, originalTag):
        if originalTag in self.tagEncoder:
            return self.tagEncoder[originalTag]
        else:
            return self.leafEncoder(originalTag)

    # ast2canonicalTree :: AST -> CanonicalTree
    def ast2canonicalTree(self, ast, sibpos=0, sibnum=0):
        topNode = ct.CanonicalTree()
        topNode.code = self.oneHotVector_coder(ast.tag)
        topNode.numberOfSiblings = sibnum
        topNode.positionInSiblings = sibpos
        sibNum = len(ast)
        if sibNum != 0:
            sibPosCounter = 0
            for label, subtree in ast:
                topNode.child.append(self.ast2canonicalTree(
                    subtree, sibpos=sibPosCounter, sibnum=sibNum))
                sibPosCounter += 1
        return topNode

    # canonicalTree2KernekTree :: CanonicalTree -> TreeInKernel
    def canonicalTree2KernelTree(self, canotree, depth=0):
        topNode = ct.TreeInKernel()
        topNode.code = canotree.code
        topNode.numberOfSiblings = canotree.numberOfSiblings
        topNode.positionInSiblings = canotree.positionInSiblings
        topNode.depth = depth
        topNode.child = map(lambda t: self.canonicalTree2KernelTree(
            t, depth=depth + 1), canotree.child)
        return topNode

    # tbcnn :: TreeInKernel -> np.array
    def tbcnn(self, top):
        treeInKernel = top.serialize()
        w_dot_X = np.zeros([self.feature_demention])
        for i in range(0, len(treeInKernel)):
            eta_t_i = (self.window_depth -
                       treeInKernel[i].depth) / self.window_depth
            n = treeInKernel[i].numberOfSiblings
            eta_r_i = 0 if n == 0 else (
                1 - eta_t_i) * treeInKernel[i].positionInSiblings / n
            eta_l_i = (1 - eta_r_i) * (1 - eta_t_i)
            weight_conv = eta_t_i * self.w_conv_t + eta_r_i * \
                self.w_conv_r + eta_l_i * self.w_conv_l
            w_dot_X += weight_conv * treeInKernel[i].code
        return np.tanh(w_dot_X + self.b_conv)

    # tbcnn_layer :: CononicalTree -> CanonicalTree
    def tbcnn_layer(self, top):
        kerneltree = self.canonicalTree2KernelTree(top)
        top.code = self.tbcnn(kerneltree)
        for i in range(0, len(top.child)):
            top.child[i] = self.tbcnn_layer(top.child[i])
        return top

    # agg_layer :: CononinalTree -> np.array
    @lru_cache(maxsize=100)
    def agg_layer(self, top):
        childNodes = top.child
        if childNodes == None:
            return self.w_agg * top.code + self.b_agg
        else:
            sumUpAggChild = np.zeros([self.feature_demention])
            for i in range(len(childNodes)):
                vec = self.agg_layer(childNodes[i])
                eta_l_i = (childNodes[i].positionInSiblings -
                           1) / (childNodes.numberOfSiblings - 1)
                w_agg_i = eta_l_i * self.w_agg_l + (1 - eta_l_i) * self.w_agg_r
                sumUpAggChild += w_agg_i * vec
            return sumUpAggChild + self.w_agg * top.code + self.b_agg
