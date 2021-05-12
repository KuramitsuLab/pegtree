from .pasm import *


def isLink(ptree):
    return len(ptree) == 2 and not isinstance(ptree[0], str)


def isEdge(ptree):
    return len(ptree) == 2 and isinstance(ptree[0], str)


def isNode(ptree):
    return len(ptree) == 4


def edgefy(edge, node):
    return node if edge == '' else (edge, node)


def nodefy(ptree, spos, epos):
    if ptree is None:
        return ('', spos, epos, None)
    if len(ptree) == 2:
        return nodefy(ptree[1], spos, epos)
    assert isNode(ptree)
    return ptree


def split_prev_tail(ptree):
    if ptree is None:
        return None, None
    if isLink(ptree):
        return ptree[0], ptree[1]
    return None, ptree


def pNode(e, tag, shift):
    def match(px: PContext):
        pos = px.pos
        prev = px.ptree
        px.tree = None
        if e(px):
            px.ptree = (prev, (tag, pos+shift, px.pos, px.ptree))
            return True
        return False
    return match


def pEdge(edge, e, shift=0):
    def match(px: PContext):
        pos = px.pos
        prev = px.ptree
        px.ptree = None
        if e(px):
            px.ptree = (prev, edgefy(edge, nodefy(px.ptree, pos, px.pos)))
            return True
        return False
    return match


def pFold(edge, e, tag, shift):
    def match(px: PContext):
        pos = px.pos
        prev, px.tree = split_prev_tail(edgefy(edge, px.ptree))
        if e(px):
            ptree = (prev, (tag, pos+shift, px.pos, px.ptree))
            return True
        return match
    return match


def PTreeNode(pt, urn, inputs, spos, epos):
    if isNode(pt):
        tag, spos, epos, child = pt
        tree = ParseTree(tag, inputs, spos, epos, urn)
    else:
        child = pt
        tree = ParseTree('', inputs, epos, spos, urn)
    while child is not None:
        child, tail = split_prev_tail(child)
        if isEdge(tail):
            tree.set(tail[0], PTreeNode(
                tail[1], urn, inputs, spos, epos), spos, epos)
        else:
            tree.set('', PTreeNode(tail, urn, inputs, spos, epos), spos, epos)
    for i in range(len(tree)//2):
        tree[i], tree[-(1+i)] = tree[-(1+i)], tree[i]
    return tree
