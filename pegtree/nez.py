from pegtree.peg import *
import pegtree.pasm as pasm
from pegtree.optimizer import prepare
from pegtree.terminal import DefaultConsole as console


class Generator(object):
    def __init__(self):
        self.peg = None
        self.generated = {}
        self.generating_nonterminal = ''
        self.sids = {}
        self.memos = []
        self.Ooox = True
        self.Olex = True

    def getsid(self, name):
        if not name in self.sids:
            self.sids[name] = len(self.sids)
        return self.sids[name]

    def generate(self, peg, **option):
        self.peg = peg
        self.generated = {}
        start, refs, rules, memos = prepare(
            peg, option.get('start', peg.start()))
        self.memos = memos
        for ref in refs:
            assert isinstance(ref, PRef)
            uname = ref.uname(peg)
            self.generating_nonterminal = uname
            self.emitRule(uname, rules[uname])
            self.generating_nonterminal = ''
        return self.emitParser(start)

    def emitRule(self, uname, pe: PExpr):
        A = self.emit(pe, 0)
        if uname in self.memos:
            idx = self.memos.index(uname)
            if idx != -1:
                A = pasm.pMemo(A, idx, len(self.memos))
                # A = pasm.pMemoDebug(ref.name, A, idx, self.memos)
        self.generated[uname] = A

    def emitParser(self, start):
        return pasm.generate(self.generated[start.uname(self.peg)])

    def emit(self, pe: PExpr, step: int):
        cname = pe.cname()
        if hasattr(self, cname):
            f = getattr(self, cname)
            return f(pe, step)
        print('@TODO(Generator)', cname, pe)
        return self.PChar(EMPTY, step)

    def PAny(self, pe, step):
        return pasm.pAny()

    def PChar(self, pe, step):
        return pasm.pChar(pe.text)

    def PRange(self, pe, step):
        return pasm.pRange(pe.chars, pe.ranges)

    def PAnd(self, pe, step):
        e = pe.e
        if(self.Olex and isinstance(e, PChar)):
            return pasm.pAndChar(e.text)
        if(self.Olex and isinstance(e, PRange)):
            return pasm.pAndRange(e.chars, e.ranges)
        return pasm.pAnd(self.emit(e, step))

    def PNot(self, pe, step):
        e = pe.e
        if(self.Olex and isinstance(e, PChar)):
            return pasm.pNotChar(e.text)
        if(self.Olex and isinstance(e, PRange)):
            return pasm.pNotRange(e.chars, e.ranges)
        return pasm.pNot(self.emit(e, step))

    def PMany(self, pe, step):
        e = pe.e
        if(self.Olex and isinstance(e, PChar)):
            return pasm.pManyChar(e.text)
        if(self.Olex and isinstance(e, PRange)):
            return pasm.pManyRange(e.chars, e.ranges)
        return pasm.pMany(self.emit(e, step))

    def POneMany(self, pe, step):
        e = pe.e
        if(self.Olex and isinstance(e, PChar)):
            return pasm.pOneManyChar(e.text)
        if(self.Olex and isinstance(e, PRange)):
            return pasm.pOneManyRange(e.chars, e.ranges)
        return pasm.pOneMany(self.emit(e, step))

    def POption(self, pe, step):
        e = pe.e
        if(self.Olex and isinstance(e, PChar)):
            return pasm.pOptionChar(e.text)
        if(self.Olex and isinstance(e, PRange)):
            return pasm.pOptionRange(e.chars, e.ranges)
        return pasm.pOption(self.emit(e, step))

    def PSeq(self, pe, step):
        pfs = []
        for e in pe:
            pfs.append(self.emit(e, step))
            step += e.minLen()
        pfs = tuple(pfs)
        if len(pfs) == 2:
            return pasm.pSeq2(pfs[0], pfs[1])
        if len(pe) == 3:
            return pasm.pSeq3(pfs[0], pfs[1], pfs[2])
        if len(pe) == 4:
            return pasm.pSeq4(pfs[0], pfs[1], pfs[2], pfs[3])
        return pasm.pSeq(*pfs)

    # Ore
    def POre(self, pe: POre, step):
        if pe.isDict():
            return pasm.pDict(pe.listDict())
        pfs = tuple(map(lambda e: self.emit(e, step), pe))
        if len(pfs) == 2:
            return pasm.pOre2(pfs[0], pfs[1])
        if len(pe) == 3:
            return pasm.pOre3(pfs[0], pfs[1], pfs[2])
        if len(pe) == 4:
            return pasm.pOre4(pfs[0], pfs[1], pfs[2], pfs[3])
        return pasm.pOre(*pfs)

    def PRef(self, pe, step):
        return pasm.pRef(self.generated, pe.uname(self.peg))

    def PName(self, pe: PName, step):
        if step == 0 and self.generating_nonterminal == pe.e.uname(self.peg):
            console.perror(pe.position, 'Left recursion')
            return self.emit(FAIL, step)
        return self.PRef(pe.e, step)

    # Tree Construction

    def PNode(self, pe, step):
        fs = self.emit(pe.e, step)
        return pasm.pNode(fs, pe.tag, pe.shift)

    def PEdge(self, pe, step):
        return pasm.pEdge(pe.edge, self.emit(pe.e, step), pe.shift)

    def PFold(self, pe, step):
        fs = self.emit(pe.e, step)
        return pasm.pFold(pe.edge, fs, pe.tag, pe.shift)

    def PAbs(self, pe, step):
        return pasm.pAbs(self.emit(pe.e, step))

    def Skip(self, pe, step):  # @skip()
        return pasm.pSkip()

    def Symbol(self, pe, step):  # @symbol(A)
        params = pe.params
        sid = self.getsid(str(params[0]))
        return pasm.pSymbol(self.emit(pe.e, step), sid)

    def Scope(self, pe, step):
        return pasm.pScope(self.emit(pe.e, step))

    def Exists(self, pe, step):  # @Match(A)
        params = pe.params
        sid = self.getsid(str(params[0]))
        return pasm.pExists(sid)

    def Match(self, pe, step):  # @Match(A)
        params = pe.params
        sid = self.getsid(str(params[0]))
        return pasm.pMatch(sid)

    def Def(self, pe, step):  # @def(A, '名詞')
        params = pe.params
        name = str(params[1]) if len(params) == 2 else str(params[0])
        pf = self.emit(pe.e, step)
        #print('@def', pf, name)
        return pasm.pDef(name, pf)

    def In(self, pe, step):  # @in(A)
        params = pe.params
        name = str(params[0])
        #print('@in', name)
        return pasm.pIn(name)


generator = Generator()


def generate(peg, **options):
    return generator.generate(peg, **options)
