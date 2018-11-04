from pegpy.expression import *

def match(*ctags):
    def _match(func):
        name = ctags[-1]
        for ctag in ctags[:-1]:
            setattr(ctag, name, func)
        return func
    return _match

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

def checkRec(pe: ParsingExpression, name: str, visited : dict) -> bool:
    if hasattr(pe, 'left'):
        if isinstance(pe, Seq):
            return checkRec(pe.left, name, visited) and checkRec(pe.right, name, visited)
        else: #Ore, Alt
            c0 = checkRec(pe.left, name, visited)
            c1 = checkRec(pe.right, name, visited)
            return c0 or c1
    if hasattr(pe, 'inner'):
        rec = checkRec(pe.inner, name, visited)
        return True if isinstance(pe, Not) or isinstance(pe, Many) or isinstance(pe, And) else rec
    if isinstance(pe, Ref):
        if pe.name == name:
            print("TODO left recursion", name)
        if not pe.name in visited:
            visited[pe.name] = True
            checkRec(pe.deref(), name, visited)
        return not pe.prop().isConsumed()
    return isinstance(pe, Empty) # False if (Char,Range,Any)

def isAlwaysConsumed(pe: ParsingExpression):
    if not hasattr(pe, 'cc'):
        @match(Char, Any, Range, 'cc')
        def consumed(pe): return True

        @match(Many, Not, And, Empty, 'cc')
        def consumed(pe): return False

        @match(Many1, LinkAs, TreeAs, FoldAs, Detree, Meta, 'cc')
        def unary(pe):
            return isAlwaysConsumed(pe.inner)

        @match(Seq, 'cc')
        def seq(pe):
            if not isAlwaysConsumed(pe.left): return False
            return isAlwaysConsumed(pe.right)

        @match(Ore, Alt, 'cc')
        def ore(pe):
            return isAlwaysConsumed(pe.left) and isAlwaysConsumed(pe.right)

        @match(Ref, 'cc')
        def memo(pe: Ref):
            if not pe.isNonTerminal():
                return True
            key = 'null' + pe.name
            memoed = pe.getmemo('null')
            if memoed == None:
                pe.setmemo('null', True)
                memoed = isAlwaysConsumed(pe.deref())
                pe.setmemo('null', memoed)
            return memoed
    return pe.cc()

## TreeState
TUnit = 0
TTree = 1
TMut = 2
TFold = 3

def treeState(pe):
    if not hasattr(pe, 'ts'):
        @match(Char, Any, Range, Not, Detree, 'ts')
        def stateUnit(pe):
            return TUnit

        @match(TreeAs, 'ts')
        def stateTree(pe):
            return TTree

        @match(LinkAs, 'ts')
        def stateMut(pe):
            return TMut

        @match(FoldAs, 'ts')
        def stateFold(pe):
            return TFold

        @match(Seq, 'ts')
        def stateSeq(pe):
            ts0 = treeState(pe.left)
            return ts0 if ts0 != TUnit else treeState(pe.right)

        @match(Ore, Alt, 'ts')
        def stateAlt(pe):
            ts0 = treeState(pe.left)
            if ts0 != TUnit: return ts0
            ts1 = treeState(pe.right)
            return TMut if ts1 == TTree else ts1

        @match(Many, Many1, And, 'ts')
        def stateAlt(pe):
            ts0 = treeState(pe.inner)
            return TMut if ts0 == TTree else ts0

        @match(Ref, 'ts')
        def memo(pe: Ref):
            if not pe.isNonTerminal(): return TUnit
            memoed = pe.getmemo('ts')
            if memoed == None:
                pe.setmemo('ts', TUnit)
                memoed = treeState(pe.deref())
                pe.setmemo('ts', memoed)
            return memoed
    return pe.ts()

def treeCheck(pe, ts):
    if not hasattr(pe, 'tc'):
        @match(ParsingExpression, 'tc')
        def checkEmpty(pe, ts): return pe

        @match(TreeAs, 'tc')
        def checkTree(pe, ts):
            if ts == TUnit:
                return treeCheck(pe.inner, TUnit)
            if ts == TTree:
                pe.inner = treeCheck(pe.inner, TMut)
                return pe
            if ts == TMut:
                pe.inner = treeCheck(pe.inner, TMut)
                return LinkAs('', pe)
            if ts == TFold:
                pe.inner = treeCheck(pe.inner, TMut)
                return FoldAs('', pe.tag, pe.inner)

        @match(LinkAs, 'tc')
        def checkLink(pe, ts):
            if ts == TUnit or ts == TFold:
                return treeCheck(pe.inner, TUnit)
            if ts == TTree:
                return treeCheck(pe.inner, TTree)
            if ts == TMut:
                ts0 = treeState(pe.inner)
                if ts0 == TUnit or ts0 == TFold: pe.inner = TreeAs('', treeCheck(pe.inner, TUnit))
                if ts0 == TTree: pe.inner = treeCheck(pe.inner, TTree)
                if ts0 == TMut: pe.inner = TreeAs('', treeCheck(pe.inner, TMut))
                return pe

        @match(FoldAs, 'tc')
        def checkFold(pe, ts):
            if ts == TUnit:
                return treeCheck(pe.inner, TUnit)
            if ts == TTree:
                pe.inner = treeCheck(pe.inner, TMut)
                return TreeAs(pe.tag, pe.inner)
            if ts == TMut:
                pe.inner = treeCheck(pe.inner, TMut)
                return LinkAs(pe.ltag, pe.inner)
            if ts == TFold:
                pe.inner = treeCheck(pe.inner, TMut)
                return pe

        @match(Seq, 'tc')
        def checkSeq(pe, ts):
            if ts == TUnit or ts == TMut or ts == TFold:
                pe.left = treeCheck(pe.left, ts)
                pe.right = treeCheck(pe.right, ts)
                return pe
            ts0 = treeState(pe.left)
            if ts0 == TUnit:
                pe.left = treeCheck(pe.left, TUnit)
                pe.right = treeCheck(pe.right, ts)
                return pe
            if ts0 == TTree:
                pe.left = treeCheck(pe.left, TTree)
                pe.right = treeCheck(pe.right, TFold)
                return pe

        @match(Ore, Alt, 'tc')
        def checkAlt(pe, ts):
            pe.left = treeCheck(pe.left, ts)
            pe.right = treeCheck(pe.right, ts)
            return pe

        @match(Many, Many1, 'tc')
        def checkMany(pe, ts):
            if ts == TUnit:
                pe.inner = treeCheck(pe.inner, TUnit)
                return pe
            if ts == TTree:
                pe.inner = treeCheck(pe.inner, TUnit)
                return TreeAs('', pe)
            if ts == TMut:
                ts0 = treeState(pe.inner)
                if ts0 == TUnit or ts0 == TFold: pe.inner = treeCheck(pe.inner, TUnit)
                if ts0 == TTree or ts0 == TMut: pe.inner = treeCheck(pe.inner, TMut)
                return pe
            if ts == TFold:
                pe.inner = treeCheck(pe.inner, TFold)
                return pe

        @match(Ref, 'tc')
        def checkRef(pe: Ref, ts):
            if not pe.isNonTerminal(): return pe
            ts0 = treeState(pe)
            if ts == ts0: return pe
            if ts == TUnit: Detree(pe)
            if ts == TTree:
                if ts0 == TUnit or ts0 == TMut: return TreeAs('', pe)
                if ts0 == TFold: return seq(TreeAs('', EMPTY), pe)
            if ts == TMut:
                if ts0 == TUnit: return pe
                if ts0 == TTree: return LinkAs('', pe)
                if ts0 == TFold: return LinkAs('', seq(TreeAs('', EMPTY), pe))
            if ts == TFold:
                if ts0 == TUnit: return pe
                if ts0 == TTree: return FoldAs('', '', pe)
                if ts0 == TMut: return FoldAs('', '', TreeAs('', pe))
    return pe.tc(ts)


def testRules(g):
    for name in dir(g):
        if not name[0].isupper(): continue
        p = getattr(g, name)
        p.checkRule()

# Rule

class Rule(Ref):
    __slots__ = ['peg', 'name', 'pos3', 'inner', 'checked']
    def __init__(self, peg, name, inner):
        super().__init__(name, peg)
        self.inner = ParsingExpression.new(inner)
        self.checked = False
    def __str__(self):
        return self.name + ' = ' + str(self.inner)
    def deref(self):
        return self.inner

    def isConsumed(self):
        if not hasattr(self, 'nonnull'):
            self.nonnull = isAlwaysConsumed(self.inner)
        return self.nonnull
    def treeState(self):
        if not hasattr(self, 'ts'):
            self.ts = treeState(self.inner)
        return self.ts
    def checkRule(self):
        if not self.checked:
            s0 = str(self.inner)
            if isRec(self.inner, self.name, {}):
                checkRec(self.inner, self.name, {})
            ts = treeState(self.inner)
            ts = treeCheck(self.inner, ts)
            s1 = str(self.inner)
            if s0 != s1:
                print(self.name, s0, s1)
