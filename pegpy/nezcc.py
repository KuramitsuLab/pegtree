from pathlib import Path
import json
import os
import sys
from pegpy.tpeg2 import grammar, Ref, Unary, Tuple, Char, Range

# NezCC


def makeNonterminalList(peg, pe, ns: list, es):
    if isinstance(pe, Ref):
        uname = pe.uname() if pe.peg != peg else pe.name
        if uname not in ns:
            ns.append(uname)
            es[uname] = pe.deref()
            makeNonterminalList(peg, es[uname], ns, es)
    if isinstance(pe, Unary):
        makeNonterminalList(peg, pe.e, ns, es)
    elif isinstance(pe, Tuple):
        for e in pe:
            makeNonterminalList(peg, e, ns, es)


class Combinator(object):
    ESCTBL = str.maketrans(
        {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\v': '\\v', '\f': '\\f',
         '\\': '\\\\', "'": "\\'", '"': "\\\""})

    def __init__(self, options={}):
        print(options)
        self.SIDs = {}
        self.apply = options.get('apply', '{}({})')
        self.delim = options.get('delim', ',')
        self.prefix = options.get('prefix', 'p')
        self.rule = options.get('rule', 'peg[{}] = {}')
        self.useArray = options.get('useArray', True)
        self.domains = []
        self.funcs = set(options.get('supported', []))

    def has(self, funcname):
        #print(funcname, funcname in self.funcs)
        return funcname in self.funcs

    def emitAll(self, peg, start=None):
        ns = [peg.start() if start is None else start]
        es = {ns[0]: peg[ns[0]]}
        makeNonterminalList(peg, peg[ns[0]], ns, es)
        ns.reverse()
        if self.useArray:
            self.domains = ns
        for n in ns[-5:]:
            ref = self.getref(n)
            print(self.rule.format(ref, self.emit(es[n])))

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
        '"' + s.translate(Combinator.ESCTBL) + '"'
        return '"' + s.translate(Combinator.ESCTBL) + '"'

    def getref(self, name):
        if len(self.domains) > 0:
            return str(self.domains.index(name))
        return self.quote(name)

    def emit(self, pe):
        tag = pe.__class__.__name__
        if tag == 'Action':
            tag = pe.func.capitalize()
        if hasattr(self, tag):
            f = getattr(self, tag)
            return f(pe)
        else:
            return self.Undefined(pe)

    def Undefined(self, pe):
        return f'TODO({pe})'

    def Char(self, pe):
        if len(pe.text) == 0:
            return self.emitApply('Empty')
        return self.emitApply('Char', self.quote(pe.text))

    def Range(self, pe):
        return self.emitApply('Range', self.quote(pe.chars), self.quote(pe.ranges))

    def Any(self, pe):
        return self.emitApply('Any')

    def param(self, pe):
        if isinstance(pe, Char):
            return (self.quote(pe.text),)
        if isinstance(pe, Range):
            return (self.quote(pe.chars), self.quote(pe.ranges))
        return ()

    def And(self, pe):
        if self.has(f'And{pe.e.cname()}'):
            return self.emitApply(f'And{pe.e.cname()}', *self.param(pe.e))
        return self.emitApply('And', self.emit(pe.e))

    def Not(self, pe):
        if self.has(f'Not{pe.e.cname()}'):
            return self.emitApply(f'Not{pe.e.cname()}', *self.param(pe.e))
        return self.emitApply('Not', self.emit(pe.e))

    def Many(self, pe):
        if self.has(f'Many{pe.e.cname()}'):
            return self.emitApply(f'Many{pe.e.cname()}', *self.param(pe.e))
        return self.emitApply('Many', self.emit(pe.e))

    def Many1(self, pe):
        e = self.emit(pe.e)
        if self.has('Many1'):
            return self.emitApply('Many1', e)
        return self.emitApply('Seq2', e, self.emitApply('Many', e))

    def Option(self, pe):
        e = self.emit(pe.e)
        if self.has('Option'):
            return self.emitApply('Option', e)
        return self.emitApply('Ore2', e, self.emitApply('Empty'))

    def emitBinary(self, name, fs):
        if len(fs) == 1:
            return fs[0]
        if len(fs) == 2:
            return self.emitApply(f'{name}2', fs[0], fs[1])
        if self.has(f'{name}4') and len(fs) >= 4:
            return self.emitApply(f'{name}4', fs[0], fs[1], fs[2], self.emitBinary(name, fs[3:]))
        if self.has(f'{name}3') and len(fs) >= 3:
            return self.emitApply(f'{name}3', fs[0], fs[1], self.emitBinary(name, fs[2:]))
        return self.emitApply(f'{name}2', fs[0], self.emitBinary(name, fs[1:]))

    def Seq(self, pe):
        fs = [self.emit(e) for e in pe]
        if len(fs) == 2:
            return self.emitApply('Seq2', *fs)
        if len(fs) == 3 and self.has('Seq3'):
            return self.emitApply('Seq3', *fs)
        if len(fs) == 4 and self.has('Seq4'):
            return self.emitApply('Seq4', *fs)
        if self.has('Seq'):
            return self.emitApply('Seq', *fs)
        return self.emitBinary('Seq', fs)

    def Ore(self, pe):
        fs = [self.emit(e) for e in pe]
        if len(fs) == 2:
            return self.emitApply('Ore2', *fs)
        if len(fs) == 3 and self.has('Ore3'):
            return self.emitApply('Ore3', *fs)
        if len(fs) == 4 and self.has('Ore4'):
            return self.emitApply('Ore4', *fs)
        if self.has('Ore'):
            return self.emitApply('Ore', *fs)
        return self.emitBinary('Ore', fs)

    def Alt(self, pe):
        return self.Ore(pe)

    def Ref(self, pe):
        ref = self.getref(pe.name)
        return self.emitApply('Ref', 'peg', ref)

    def Node(self, pe):
        e = self.emit(pe.e)
        return self.emitApply('Node', e, self.quote(pe.tag), '0')

    def Edge(self, pe):
        e = self.emit(pe.e)
        return self.emitApply('Edge', self.quote(pe.edge), e)

    def Fold(self, pe):
        e = self.emit(pe.e)
        return self.emitApply('Fold', self.quote(pe.edge), e, self.quote(pe.tag), '0')

    def Abs(self, pe):
        e = self.emit(pe.e)
        return self.emitApply('Abs', e)

    '''
    def Lazy(self, pe):
        params = pe.params
        name = pe.e.name
        peg = option.get('peg')
        fname = pe.func
        params = pe.params
        return self.Undefined(pe)
    '''

    def Skip(self, pe):
        return self.emitApply('pSkipErr')

    def getsid(self, name):
        if not name in self.SIDs:
            self.SIDs[name] = len(self.SIDs)
        return self.SIDs[name]

    def Symbol(self, pe):
        sid = self.getsid(str(pe.params[0]))
        e = self.emit(pe.e)
        return self.emitApply('Symbol', sid, e)

    def Exists(self, pe):
        sid = self.getsid(str(pe.params[0]))
        return self.emitApply('Exists', sid)

    def Match(self, pe):
        sid = self.getsid(str(pe.params[0]))
        return self.emitApply('Match', sid)

    def Scope(self, pe):
        e = self.emit(pe.e)
        return self.emitApply('Scope', e)

    # def example(self, g, options):
    #     for testcase in g['@@example']:
    #         name, pos4 = testcase
    #         if not name in g:
    #             continue
    #         text = pos4.inputs[pos4.spos:pos4.epos]
    #         indent = options['indent']
    #         print(indent + self.apply('example', repr(name), repr(text)))


def show_filelist():
    path = Path(__file__).resolve().parent / 'nezcc'
    print('Settings:', ', '.join(
        [file for file in os.listdir(path) if file.endswith('.json')]))
    sys.exit(1)


def load_options(file):
    path = Path(file)
    if not path.exists():
        path = Path(__file__).resolve().parent / 'nezcc' / path
    try:
        with path.open() as f:
            return json.load(f)
    except FileNotFoundError:
        show_filelist()
    # except:


def nezcc(file, peg, **options):
    c = Combinator(load_options(file))
    c.emitAll(peg, **options)

    # pegcc = NezCC(options)
    # with path.open() as f:
    #     for line in f.readlines():
    #         line = line.rstrip()
    #         if 'TPEG' in line:
    #             setline(line, options)
    #             generate(pegcc, g, **options)
    #         elif 'EXAMPLE' in line and '@@example' in g:
    #             setline(line, options)
    #             pegcc.example(g, options)
    #         else:
    #             print(line)


if __name__ == '__main__':
    peg = grammar('es.tpeg')
    nezcc('pegpy.json', peg)
