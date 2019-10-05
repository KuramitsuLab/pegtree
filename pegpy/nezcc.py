from pathlib import Path
import pegpy.tpeg as peg


class NezCC(object):
    def __init__(self, options):
        self.SIDs = {}
        self.applyfmt = options.get('apply', '{}({})')
        self.delimfmt = options.get('delim', ',')

    def apply(self, name, *args):
        if len(args) == 0:
            return self.applyfmt.format(name, '')
        elif len(args) == 1:
            return self.applyfmt.format(name, args[0])
        else:
            return self.applyfmt.format(name, self.delimfmt.join(args))

    def emit(self, pe, **options):
        tag = pe.__class__.__name__
        if tag == 'Action':
            tag = pe.func.capitalize()
        if hasattr(self, tag):
            f = getattr(self, tag)
            return f(pe, **options)
        else:
            return self.Undefined(pe, **options)

    def Undefined(self, pe, **options):
        return f'TODO({pe})'

    def Char(self, pe, **options):
        quote = options['quote']
        if len(pe.text) == 0:
            return self.apply('pEmpty')
        return self.apply('pChar', quote(pe.text))

    def Range(self, pe, **options):
        quote = options['quote']
        chars = quote(pe.chars)
        delim = options.get('listdelim', ',')
        listfmt = options.get('list', '[{}]')
        ranges = listfmt.format(delim.join(
            [quote(r[0]+r[1]) for r in pe.ranges]))
        return self.apply('pRange', chars, ranges)

    def Any(self, pe, **options):
        return self.apply('pAny')

    def And(self, pe, **options):
        e = self.emit(pe.e, **options)
        return self.apply('pAnd', e)

    def Not(self, pe, **options):
        e = self.emit(pe.e, **options)
        return self.apply('pNot', e)

    def Many(self, pe, **options):
        e = self.emit(pe.e, **options)
        return self.apply('pMany', e)

    def Many1(self, pe, **options):
        e = self.emit(pe.e, **options)
        return self.apply('pMany1', e)

    def Option(self, pe, **options):
        e = self.emit(pe.e, **options)
        return self.apply('pOption', e)

    def Seq2(self, pe, **options):
        fs = [self.emit(e, **options) for e in pe]
        if len(fs) == 2:
            return self.apply('pSeq2', *fs)
        if len(fs) == 3:
            return self.apply('pSeq3', *fs)
        return self.apply('pSeq', *fs)

    def Ore2(self, pe, **options):
        fs = [self.emit(e, **options) for e in pe]
        if len(fs) == 2:
            return self.apply('pOre2', *fs)
        return self.apply('pOre', *fs)

    def Alt2(self, pe, **options):
        return self.Ore2(pe, **options)

    def Ref(self, pe, **options):
        quote = options['quote']
        return self.apply('pRef', quote(pe.name))

    def Node(self, pe, **options):
        e = self.emit(pe.e, **options)
        quote = options['quote']
        return self.apply('pNode', e, quote(pe.tag), '0')

    def Edge2(self, pe, **options):
        quote = options['quote']
        e = self.emit(pe.e, **options)
        return self.apply('pEdge', quote(pe.edge), e)

    def Fold2(self, pe, **options):
        quote = options['quote']
        e = self.emit(pe.e, **options)
        return self.apply('pFold', quote(pe.edge), e, quote(pe.tag), '0')

    def Abs(self, pe, **options):
        e = self.emit(pe.e, **options)
        return self.apply('pAbs', e)

    '''
    def Lazy(self, pe, **options):
        params = pe.params
        name = pe.e.name
        peg = option.get('peg')
        fname = pe.func
        params = pe.params
        return self.Undefined(pe, **options)
    '''

    def Skip(self, pe, **options):
        return self.apply('pSkipErr')

    def getsid(self, name):
        if not name in self.SIDs:
            self.SIDs[name] = len(self.SIDs)
        return self.SIDs[name]

    def Symbol(self, pe, **options):
        sid = self.getsid(str(pe.params[0]))
        e = self.emit(pe.e, **options)
        return self.apply('pSymbol', str(sid), e)

    def Exists(self, pe, **options):
        sid = self.getsid(str(pe.params[0]))
        return self.apply('pExists', str(sid))

    def Match(self, pe, **options):
        sid = self.getsid(str(pe.params[0]))
        return self.apply('pMatch', str(sid))

    def Scope(self, pe, **options):
        e = self.emit(pe.e, **options)
        return self.apply('pScope', e)


def generate(g, **options):
    nezcc = NezCC(options)
    quote = options.get('quote', repr)
    indent = options.get('indent', '\t')
    rule = options.get('rule', '{}peg[{}] = {};')
    for name in g.N:
        func = nezcc.emit(g[name], **options)
        print(rule.format(indent, quote(name), func))


def getoption(path: Path, line: str):
    options = {}
    indent = []
    for c in line:
        if c != ' ' and c != '\t':
            break
        indent.append(c)
    options['indent'] = ''.join(indent)
    if 'quote' not in options:
        options['quote'] = repr
    return options


def nezcc(file, g):
    path = Path(file)
    if not path.exists():
        path = Path(__file__).resolve().parent / 'nezcc' / path
    with path.open() as f:
        for line in f.readlines():
            line = line.rstrip()
            if 'TPEG' in line:
                options = getoption(path, line)
                generate(g, **options)
            else:
                print(line)


if __name__ == '__main__':
    g = peg.grammar('''
A = 'abc' [A]
''')
    nezcc('empty.ts', g)
