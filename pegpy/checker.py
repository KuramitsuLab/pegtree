from pegpy.expression import *

verbose = True

def debug(*p):
    if verbose: print(*p)

#TreeCheck

def checkTree(pe, inside):
    if not hasattr(LinkAs, 'checkTree'):
        method = 'checkTree'

        @addmethod(ParsingExpression, method)
        def checkTree(pe, inside):
            if hasattr(pe, 'inner'):
                pe.inner = checkTree(pe.inner, inside)
            if hasattr(pe, 'left'):
                pe.left = checkTree(pe.left, inside)
                pe.right = checkTree(pe.right, inside)
            return pe

        @addmethod(TreeAs, method)
        def checkTree(pe, inside):
            pe.inner = checkTree(pe.inner, TreeAs)
            return LinkAs('', pe) if inside == TreeAs else pe

        @addmethod(LinkAs, method)
        def checkTree(pe, inside):
            ts = treeState(pe.inner)
            if ts != T.Tree:
                debug('@link', ts, pe.inner)
                pe.inner = TreeAs('', pe.inner)
            checkTree(pe.inner, LinkAs)
            return pe

        @method(Ref, method)
        def checkTree(pe, inside):
            ts = treeState(pe)
            if ts == T.Tree and inside == TreeAs:
                return LinkAs('', pe)
            return pe

    return pe.treeCheck(inside)


