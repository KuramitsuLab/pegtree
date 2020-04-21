from pathlib import Path
import os
from pegtree.nez import Generator
from pegtree.terminal import DefaultConsole as console

# from pegtree import Generator, grammar

PASM0 = []
PASM1 = [ 'Option', 'OneMany', 'Seq3', 'Seq4', 'Ore3', 'Ore4', 'Dict' ]
PASM1_VARGS = [ 'Seq', 'Ore' ]
PASM1_LEX = [
    'AndChar', 'NotChar', 'ManyChar', 'OneManyChar', 'OptionChar',
    'AndRange', 'NotRange', 'ManyRange', 'OneManyRange', 'OptionRange',
]

CODE = {
    'lisp': {
        'pasm': PASM1 + PASM1_LEX + PASM1_VARGS,
        'apply': '({} {})',
        'delim': ' ',
    },
    'typescript': {
        'pasm': PASM1 + PASM1_LEX + PASM1_VARGS,
    },
    'ts': {
        'file': 'ts.txt',
        'prefix': 'p',
        'rule': '  {};',
        'pasm': PASM1 + PASM1_LEX + PASM1_VARGS,
    },
}

class PAsmGenerator(Generator):
    ESCTBL = str.maketrans(
        {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\v': '\\v', '\f': '\\f',
         '\\': '\\\\', "'": "\\'", '"': "\\\""})

    def __init__(self, **options):
        super().__init__()
        self.domains = []
        self.rule = '{}'
        self.apply = '{}({})'
        self.delim = ','
        self.string = '"{}"'
        self.prefix = os.environ.get('PREFIX', 'p')
        self.PASM = PASM1
        if options.get('-O', 2) == 0:
            self.PASM = PASM0
        self.rules = None

    def setup(self, spec):
        self.apply = spec.get('apply', '{}({})')
        self.string = spec.get('string', '"{}"')
        self.delim = spec.get('delim', ',')
        self.prefix = spec.get('prefix', os.environ.get('PREFIX', 'p'))
        if 'pasm' in spec and self.PASM != PASM0:
            self.PASM = set(spec['pasm'])
        self.rule = spec.get('rule', '{}')
        self.rules = []
        spec['rules'] = self.rules

    def emitRule(self, uname, pe):
        name = self.getref(uname)
        rule = self.rule.format(self.emitApply('Rule', 'peg', name, self.emit(pe, 0)))
        if isinstance(self.rules, list):
            self.rules.append(rule)
        else:
            print(rule)

    def emitParser(self, ref):
        pass

    def getref(self, name):
        if len(self.domains) > 0:
            return str(self.domains.index(name))
        return self.quote(name)

    def has(self, func):
        return func in self.PASM

    def emitApply(self, name, *args):
        name = f'{self.prefix}{name}'
        if len(args) == 0:
            return self.apply.format(name, '')
        elif len(args) == 1:
            return self.apply.format(name, args[0])
        else:
            try:
                return self.apply.format(name, self.delim.join(args))
            except:
                print('@FIXME', name, args)
                return 'FIXME'

    def quote(self, s):
        # if isinstance(s, tuple) or isinstance(s, list):
        #     sb = []
        #     for r in s:
        #         sb.append(r[0]+r[1])
        #     s = ''.join(sb)
        #     return '"' + s.translate(Parsec.ESCTBL) + '"'
        return self.string.format(str(s).translate(PAsmGenerator.ESCTBL))

    def param(self, pe):
        if hasattr(pe, 'text'):
            return (self.quote(pe.text),)
        if hasattr(pe, 'ranges'):
            return (self.quote(pe.chars), self.quote(pe.ranges))

    def PEmpty(self, pe, step):
        return self.emitApply('Empty')

    def PFail(self, pe, step):
        return self.emitApply('Fail')

    def PAny(self, pe, step):
        return self.emitApply('Any')

    def PChar(self, pe, step):
        if len(pe.text) == 0:
            return self.emitApply('Empty')
        return self.emitApply('Char', self.quote(pe.text))

    def PRange(self, pe, step):
        return self.emitApply('Range', self.quote(pe.chars), self.quote(pe.ranges))

    def PAnd(self, pe, step):
        e = pe.e
        cname = e.cname()[1:]
        if self.has(f'And{cname}'):
            return self.emitApply(f'And{cname}', *self.param(e))
        return self.emitApply('And', self.emit(e, step))

    def PNot(self, pe, step):
        e = pe.e
        cname = e.cname()[1:]
        if self.has(f'Not{cname}'):
            return self.emitApply(f'Not{cname}', *self.param(e))
        return self.emitApply('Not', self.emit(e, step))

    def PMany(self, pe, step):
        e = pe.e
        cname = e.cname()[1:]
        if self.has(f'Many{cname}'):
            return self.emitApply(f'Many{cname}', *self.param(e))
        return self.emitApply('Many', self.emit(e, step))

    def POneMany(self, pe, step):
        e = pe.e
        if self.has('OneMany'):
            cname = e.cname()[1:]
            if self.has(f'OneMany{cname}'):
                return self.emitApply(f'OneMany{cname}', *self.param(e))
            return self.emitApply('OneMany', self.emit(e, step))
        return self.emitApply('Seq2', self.emit(e, step), self.PMany(pe, pe.minLen()))

    def POption(self, pe, step):
        e = pe.e
        if self.has('Option'):
            cname = e.cname()[1:]
            if self.has(f'Option{cname}'):
                return self.emitApply(f'Option{cname}', *self.param(e))
            return self.emitApply('Option', self.emit(e, step))
        return self.emitApply('Ore2', e, self.emitApply('Empty'))

    def PSeq(self, pe, step):
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
    def POre(self, pe, step):
        if pe.isDict():
            ss = [s for s in pe.listDict()]
            return self.emitApply('Dict', self.quote(' '.join(ss)))
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

    def PAlt(self, pe, step):
        return self.POre(pe, step)

    def emitBin(self, name, fs):
        if len(fs) == 1:
            return fs[0]
        if len(fs) == 2:
            return self.emitApply(f'{name}2', fs[0], fs[1])
        if self.has(f'{name}4') and len(fs) >= 4:
            return self.emitApply(f'{name}4', fs[0], fs[1], fs[2], self.emitBin(name, fs[3:]))
        if self.has(f'{name}3') and len(fs) >= 3:
            return self.emitApply(f'{name}3', fs[0], fs[1], self.emitBin(name, fs[2:]))
        return self.emitApply(f'{name}2', fs[0], self.emitBin(name, fs[1:]))

    def PRef(self, pe, step):
        ref = self.getref(pe.uname(self.peg))
        return self.emitApply('Ref', 'peg', ref)

    # Tree Construction

    def PNode(self, pe, step):
        e = self.emit(pe.e, step)
        return self.emitApply('Node', e, self.quote(pe.tag), f'{pe.shift}')

    def PEdge(self, pe, step):
        e = self.emit(pe.e, step)
        return self.emitApply('Edge', self.quote(pe.edge), e, f'{pe.shift}')

    def PFold(self, pe, step):
        e = self.emit(pe.e, step)
        return self.emitApply('Fold', self.quote(pe.edge), e, self.quote(pe.tag), f'{pe.shift}')

    def PAbs(self, pe, step):
        e = self.emit(pe.e, step)
        return self.emitApply('Abs', e)

    def Skip(self, pe, step):
        return self.emitApply('Skip')

    def Symbol(self, pe, step):
        sid = self.getsid(str(pe.params[0]))
        e = self.emit(pe.e, step)
        return self.emitApply('Symbol', e, str(sid))

    def Exists(self, pe, step):
        sid = self.getsid(str(pe.params[0]))
        return self.emitApply('Exists', str(sid))

    def Match(self, pe, step):
        sid = self.getsid(str(pe.params[0]))
        return self.emitApply('Match', str(sid))

    def Scope(self, pe, step):
        e = self.emit(pe.e, step)
        return self.emitApply('Scope', e)

    def Def(self, pe, step):
        params = pe.params
        name = str(params[1]) if len(params) == 2 else str(params[0])
        e = self.emit(pe.e, step)
        return self.emitApply('Def', self.quote(name), e)

    def In(self, pe, step):
        params = pe.params
        name = str(params[0])
        return self.emitApply('In', self.quote(name))


def output(spec):
    if 'file' in spec:
        path = Path(__file__).resolve().parent / 'code' / spec['file']
        with path.open() as f:
            for line in f:
                if line.startswith('#@RULE'):
                    for rule in spec['rules']:
                        print(rule)
                else:
                    print(line, end='')
    else:
        for rule in spec['rules']:
            print(rule)


def parsec(peg, **options):
    generator = PAsmGenerator(**options)
    if 'format' in options:
        format = options['format']
        if format not in CODE:
            names = sorted(CODE.keys())
            print(console.bold('Supported format:'), ' '.join(names))
            return
        spec = CODE[format]
        generator.setup(spec)
        generator.generate(peg, **options)
        output(spec)
    else:
        generator.generate(peg, **options)

