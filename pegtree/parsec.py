from pegtree.pegtree import Generator, Grammar


class Parsec(Generator):
    ESCTBL = str.maketrans(
        {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\v': '\\v', '\f': '\\f',
         '\\': '\\\\', "'": "\\'", '"': "\\\""})

    def __init__(self):
        super().__init__(self)

    def generate(self, peg, **option):
        self.peg = peg
        name = option.get('start', peg.start())
        start = peg.newRef(name)
        # if 'memos' in option and not isinstance(option['memos'], list):
        memos = option.get('memos', peg.N)
        ps = self.makelist(start, {}, [])

        for ref in ps:
            assert isinstance(ref, Ref)
            uname = ref.uname()
            self.generating_nonterminal = uname
            A = self.emit(ref.deref(), 0)
            self.generating_nonterminal = ''
            idx = memos.index(ref.name)
            # if idx != -1 and ref.peg == peg:
            #     A = self.memoize(idx, len(memos), A)
            self.generated[uname] = A

        pf = self.generated[start.uname()]

    def emitRule(self, ref):
        ref = self.getref()
        self.emitApply('Rule', 'peg', ref, self.emit(ref.deref(), 0))

    def emitApply(self, name, *args):
        name = f'{self.prefix}{name}'
        if len(args) == 0:
            return self.apply.format(name, '')
        elif len(args) == 1:
            return self.apply.format(name, args[0])
        else:
            return self.apply.format(name, self.delim.join(args))

    def quote(self, s):
        if isinstance(s, tuple) or isinstance(s, list):
            sb = []
            for r in s:
                sb.append(r[0]+r[1])
            s = ''.join(sb)
        '"' + s.translate(Parsec.ESCTBL) + '"'
        return '"' + s.translate(Parsec.ESCTBL) + '"'

    def param(self, pe):
        if isinstance(pe, Char):
            return (self.quote(pe.text),)
        if isinstance(pe, Range):
            return (self.quote(pe.chars), self.quote(pe.ranges))

    def getref(self, name):
        if len(self.domains) > 0:
            return str(self.domains.index(name))
        return self.quote(name)

    def Empty(self, pe, step):
        return self.emitApply('Empty')

    def Fail(self, pe, step):
        return self.emitApply('Fail')

    def Any(self, pe, step):
        return self.emitApply('Any')

    def Char(self, pe, step):
        if len(pe.text) == 0:
            return self.emitApply('Empty')
        return self.emitApply('Char', self.quote(pe.text))

    def Range(self, pe, step):
        return self.emitApply('Range', self.quote(pe.chars), self.quote(pe.ranges))

    def And(self, pe, step):
        cname = pe.e.cname()
        if self.has(f'And{cname}'):
            return self.emitApply(f'And{cname}', *self.param(pe.e))
        return self.emitApply('And', self.emit(pe.e))

    def Not(self, pe, step):
        cname = pe.e.cname()
        if self.has(f'Not{cname}'):
            return self.emitApply(f'Not{cname}', *self.param(pe.e))
        return self.emitApply('Not', self.emit(pe.e))

    def Many(self, pe, step):
        cname = pe.e.cname()
        if self.has(f'Many{cname}'):
            return self.emitApply(f'Many{cname}', *self.param(pe.e))
        return self.emitApply('Many', self.emit(pe.e))

    def Many1(self, pe, step):
        if self.has('Many1'):
            cname = pe.e.cname()
            if self.has(f'Many1{cname}'):
                return self.emitApply(f'Many1{cname}', *self.param(pe.e))
            return self.emitApply('Many1', self.emit(pe.e, step))
        return self.emitApply('Seq2', self.emit(pe.e, step), self.Many(pe, pe.minLen()))

    def Option(self, pe, step):
        if self.has('Option'):
            cname = pe.e.cname()
            if self.has(f'Option{cname}'):
                return self.emitApply(f'Option{cname}', *self.param(pe.e))
            return self.emitApply('Option', self.emit(pe.e))
        return self.emitApply('Ore', pe, self.emitApply('Empty'))

    def Seq(self, pe, step):
        fs = []
        for e in pe:
            fs.append(self.emit(e, step))
            step += e.minLen()
        if len(fs) == 2:
            return self.emitApply('Seq2', *fs)
        if len(fs) == 3 and self.has('Seq3'):
            return self.emitApply('Seq3', *fs)
        if len(fs) == 4 and self.has('Seq4'):
            return self.emitApply('Seq4', *fs)
        if self.has('Seq'):
            return self.emitApply('Seq', *fs)
        return self.emitBin('Seq', fs)

    # Ore
    def Ore(self, pe: Ore, step):
        fs = [self.emit(e, step) for e in pe]
        if len(fs) == 2:
            return self.emitApply('Ore2', *fs)
        if len(fs) == 3 and self.has('Ore3'):
            return self.emitApply('Ore3', *fs)
        if len(fs) == 4 and self.has('Ore4'):
            return self.emitApply('Ore4', *fs)
        if self.has('Ore'):
            return self.emitApply('Ore', *fs)
        return self.emitBin('Ore', fs)

    def Alt(self, pe, step):
        return self.Ore(pe, step)

    def Ref(self, pe, step):
        ref = self.getref(pe.name)
        return self.emitApply('Ref', 'peg', ref)

    # Tree Construction

    def TNode(self, pe, step):
        e = self.emit(pe.e, step)
        return self.emitApply('Node', e, self.quote(pe.tag), '0')

    def TEdge(self, pe, step):
        e = self.emit(pe.e, step)
        return self.emitApply('Edge', self.quote(pe.edge), e)

    def TFold(self, pe, step):
        e = self.emit(pe.e, step)
        return self.emitApply('Fold', self.quote(pe.edge), e, self.quote(pe.tag), '0')

    def TAbs(self, pe, step):
        e = self.emit(pe.e, step)
        return self.emitApply('Abs', e)

    def Skip(self, pe, step):
        return self.emitApply('Skip')

    def Symbol(self, pe, step):
        sid = self.getsid(str(pe.params[0]))
        e = self.emit(pe.e, step)
        return self.emitApply('Symbol', sid, e)

    def Exists(self, pe, step):
        sid = self.getsid(str(pe.params[0]))
        return self.emitApply('Exists', sid)

    def Match(self, pe, step):
        sid = self.getsid(str(pe.params[0]))
        return self.emitApply('Match', sid)

    def Scope(self, pe, step):
        e = self.emit(pe.e, step)
        return self.emitApply('Scope', e)


generator = Parsec()


def parsec(peg: Grammar, **options):
    return generator.generate(peg, **options)


PExpr
