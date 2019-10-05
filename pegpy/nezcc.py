from pathlib import Path
import pegpy.tpeg as peg


class NezCC(object):
    def __init__(self):
        self.SIDs = {}

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
            return 'pEmpty()'
        return f'pChar({quote(pe.text)})'

    def Range(self, pe, **options):
        quote = options['quote']
        chars = quote(pe.chars)
        ranges = ','.join([quote(r[0]+r[1]) for r in pe.ranges])
        return f'pRange({chars}, [{ranges}])'

    def Any(self, pe, **options):
        return 'pAny()'

    def And(self, pe, **options):
        e = self.emit(pe.e, **options)
        return f'pAnd({e})'

    def Not(self, pe, **options):
        e = self.emit(pe.e, **options)
        return f'pNot({e})'

    def Many(self, pe, **options):
        e = self.emit(pe.e, **options)
        return f'pMany({e})'

    def Many1(self, pe, **options):
        e = self.emit(pe.e, **options)
        return f'pMany1({e})'

    def Option(self, pe, **options):
        e = self.emit(pe.e, **options)
        return f'pOption({e})'

    def Seq2(self, pe, **options):
        fs = ','.join([self.emit(e, **options) for e in pe])
        if len(fs) == 2:
            return f'pSeq2({fs[0]},{fs[1]})'
        if len(fs) == 3:
            return f'pSeq3({fs[0]},{fs[1]},{fs[2]})'
        return f'pSeq({fs})'

    def Ore2(self, pe, **options):
        fs = ','.join([self.emit(e, **options) for e in pe])
        if len(fs) == 2:
            return f'pOre2({fs[0]},{fs[1]})'
        return f'pOre({fs})'

    def Alt2(self, pe, **options):
        fs = ','.join([self.emit(e, **options) for e in pe])
        return f'pOre({fs})'

    def Ref(self, pe, **options):
        quote = options['quote']
        return f'pRef{quote(pe.name)})'

    def Node(self, pe, **options):
        e = self.emit(pe.e, **options)
        quote = options['quote']
        return f'pNode({e},{quote(pe.tag)},0)'

    def Edge2(self, pe, **options):
        quote = options['quote']
        e = self.emit(pe.e, **options)
        return f'pEdge({quote(pe.edge)}, {e})'

    def Fold2(self, pe, **options):
        quote = options['quote']
        e = self.emit(pe.e, **options)
        return f'pFold({quote(pe.edge)}, {e}, {quote(pe.tag)}, 0)'

    def Abs(self, pe, **options):
        e = self.emit(pe.e, **options)
        return f'pAbs({e})'

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
        return 'pSkipErr()'

    def getsid(self, name):
        if not name in self.SIDs:
            self.SIDs[name] = len(self.SIDs)
        return self.SIDs[name]

    def Symbol(self, pe, **options):
        sid = self.getsid(str(pe.params[0]))
        e = self.emit(pe.e, **options)
        return f'pSymbol({sid}, {e})'

    def Exists(self, pe, **options):
        sid = self.getsid(str(pe.params[0]))
        e = self.emit(pe.e, **options)
        return f'pExists({sid})'

    def Match(self, pe, **options):
        sid = self.getsid(str(pe.params[0]))
        return f'pMatch({sid})'

    def Scope(self, pe, **options):
        e = self.emit(pe.e, **options)
        return f'pScope({e})'


def generate(g, **options):
    nezcc = NezCC()
    quote = options.get('quote', repr)
    indent = options.get('indent', '\t')
    rule = options.get('rule', '{}{} = {};')
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
    nezcc('nez.ts', g)
