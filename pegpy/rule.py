from pegpy.expression import *

def isRec(pe: ParsingExpression, name: str, visited : dict) -> bool:
    if isinstance(pe, Ref):
        if pe.name == name: return True
        if not pe.name in visited:
            visited[pe.name] = True
            return isRec(pe.deref(), name, visited)
    if hasattr(pe, 'inner'):
        return isRec(pe.inner, name, visited)
    if hasattr(pe, 'left'):
        rec = isRec(pe.left, name, visited)
        return rec if rec else isRec(pe.right, name, visited)
    return False

def addmethod(*ctags):
    def _match(func):
        name = ctags[-1]
        for ctag in ctags[:-1]:
            setattr(ctag, name, func)
        return func
    return _match

def treeCheck(pe, ts):
    if not hasattr(pe, 'tc'):
        @addmethod(ParsingExpression, 'tc')
        def checkEmpty(pe, ts): return pe

        @addmethod(TreeAs, 'tc')
        def checkTree(pe, ts):
            if ts == T.Unit:
                return treeCheck(pe.inner, T.Unit)
            if ts == T.Tree:
                pe.inner = treeCheck(pe.inner, T.Mut)
                return pe
            if ts == T.Mut:
                pe.inner = treeCheck(pe.inner, T.Mut)
                return LinkAs('', pe)
            if ts == T.Fold:
                pe.inner = treeCheck(pe.inner, T.Mut)
                return FoldAs('', pe.tag, pe.inner)

        @addmethod(LinkAs, 'tc')
        def checkLink(pe, ts):
            if ts == T.Unit or ts == T.Fold:
                return treeCheck(pe.inner, T.Unit)
            if ts == T.Tree:
                return treeCheck(pe.inner, T.Tree)
            if ts == T.Mut:
                ts0 = treeState(pe.inner)
                if ts0 == T.Unit or ts0 == T.Fold: pe.inner = TreeAs('', treeCheck(pe.inner, T.Unit))
                if ts0 == T.Tree: pe.inner = treeCheck(pe.inner, T.Tree)
                if ts0 == T.Mut: pe.inner = TreeAs('', treeCheck(pe.inner, T.Mut))
                return pe

        @addmethod(FoldAs, 'tc')
        def checkFold(pe, ts):
            if ts == T.Unit:
                return treeCheck(pe.inner, T.Unit)
            if ts == T.Tree:
                pe.inner = treeCheck(pe.inner, T.Mut)
                return TreeAs(pe.tag, pe.inner)
            if ts == T.Mut:
                pe.inner = treeCheck(pe.inner, T.Mut)
                return LinkAs(pe.ltag, pe.inner)
            if ts == T.Fold:
                pe.inner = treeCheck(pe.inner, T.Mut)
                return pe

        @addmethod(Seq, 'tc')
        def checkSeq(pe, ts):
            if ts == T.Unit or ts == T.Mut or ts == T.Fold:
                pe.left = treeCheck(pe.left, ts)
                pe.right = treeCheck(pe.right, ts)
                return pe
            ts0 = treeState(pe.left)
            if ts0 == T.Unit:
                pe.left = treeCheck(pe.left, T.Unit)
                pe.right = treeCheck(pe.right, ts)
                return pe
            if ts0 == T.Tree:
                pe.left = treeCheck(pe.left, T.Tree)
                pe.right = treeCheck(pe.right, T.Fold)
                return pe

        @addmethod(Ore, Alt, 'tc')
        def checkAlt(pe, ts):
            pe.left = treeCheck(pe.left, ts)
            pe.right = treeCheck(pe.right, ts)
            return pe

        @addmethod(Many, Many1, 'tc')
        def checkMany(pe, ts):
            if ts == T.Unit:
                pe.inner = treeCheck(pe.inner, T.Unit)
                return pe
            if ts == T.Tree:
                pe.inner = treeCheck(pe.inner, T.Unit)
                return TreeAs('', pe)
            if ts == T.Mut:
                ts0 = treeState(pe.inner)
                if ts0 == T.Unit or ts0 == T.Fold: pe.inner = treeCheck(pe.inner, T.Unit)
                if ts0 == T.Tree or ts0 == T.Mut: pe.inner = treeCheck(pe.inner, T.Mut)
                return pe
            if ts == T.Fold:
                pe.inner = treeCheck(pe.inner, T.Fold)
                return pe

        @addmethod(Ref, 'tc')
        def checkRef(pe: Ref, ts):
            if not pe.isNonTerminal(): return pe
            ts0 = treeState(pe)
            if ts == ts0: return pe
            if ts == T.Unit: Detree(pe)
            if ts == T.Tree:
                if ts0 == T.Unit or ts0 == T.Mut: return TreeAs('', pe)
                if ts0 == T.Fold: return seq(TreeAs('', EMPTY), pe)
            if ts == T.Mut:
                if ts0 == T.Unit: return pe
                if ts0 == T.Tree: return LinkAs('', pe)
                if ts0 == T.Fold: return LinkAs('', seq(TreeAs('', EMPTY), pe))
            if ts == T.Fold:
                if ts0 == T.Unit: return pe
                if ts0 == T.Tree: return FoldAs('', '', pe)
                if ts0 == T.Mut: return FoldAs('', '', TreeAs('', pe))
    return pe.tc(ts)

def testRules(g):
    for name in dir(g):
        if not name[0].isupper(): continue
        p = getattr(g, name)
        p.checkRule()

