import sys
import os
import errno
import inspect
from pathlib import Path
from pegtree.peg import *
import pegtree.pasm as pasm
from pegtree.tpeg_pasm import TPEGGrammar
from pegtree.terminal import DefaultConsole


# TPEGLoader

BuiltInNonTerminal = {
    'W': PRange('_', 'AZaz09'),
    '!W': PNot(PRange('_', 'AZaz09')),
    '_': PMany(PRange(' \t', '')),
}

class TPEGLoader(object):
    def __init__(self, peg, console, **options):
        self.names = {}
        self.peg = peg
        self.console = console
        self.isOnlyPEG = options.get('isOnlyPEG', False)

    def perror(self, ptree, msg):
        self.console.perror(ptree, msg)

    def pwarn(self, ptree, msg):
        self.console.pwarn(ptree, msg)

    def load(self, ptree):
        for stmt in ptree:
            if stmt == 'Rule':
                name = str(stmt.name)
                if name in self.names:
                    # pos4 = stmt['name'].getpos4()
                    self.perror(stmt.name, f'redefined name {name}')
                    continue
                self.names[name] = stmt.e
            elif stmt == 'Example':
                doc = stmt.doc
                for n in stmt.names:
                    self.example(str(n), doc)
            # elif stmt == 'Import':
            #     urn = str(stmt.name)
            #     apeg = grammar(urn, **options)
            #     for n in stmt.names:
            #         lname = str(n)  # ns.Expression
            #         name = lname
            #         if lname.find('.') != -1:
            #             name = lname.split('.')[-1]
            #         pos4 = n.getpos4()
            #         if not name in apeg:
            #             logger('perror', pos4, f'undefined name {name}')
            #             continue
            #         g.add(lname, Action(apeg.newRef(name),
            #                             'import', (name, urn), pos4))
        for name in self.names:
            ptree = self.names[name]
            self.peg[name] = self.conv(ptree, 0)

    def example(self, name, doc):
        self.peg['@@example'].append((name, doc))

    def conv(self, ptree, step):
        tag = ptree.getTag()
        pe = ptree
        if hasattr(self, tag):
            f = getattr(self, tag)
            pe = f(ptree, step)
        if not isinstance(pe, PExpr):
            print('FIXME(TPEGLoader(conv)', tag, type(pe), pe)
        return pe

    def Empty(self, ptree):
        return EMPTY

    def Any(self, ptree):
        return ANY

    def Char(self, ptree):
        s = ptree.getToken()
        sb = []
        while len(s) > 0:
            c, s = TPEGLoader.unquote(s)
            sb.append(c)
        return PChar(''.join(sb))

    @classmethod
    def unquote(cls, s):
        if s.startswith('\\'):
            if s.startswith('\\n'):
                return '\n', s[2:]
            if s.startswith('\\t'):
                return '\t', s[2:]
            if s.startswith('\\r'):
                return '\r', s[2:]
            if s.startswith('\\v'):
                return '\v', s[2:]
            if s.startswith('\\f'):
                return '\f', s[2:]
            if s.startswith('\\b'):
                return '\b', s[2:]
            if (s.startswith('\\x') or s.startswith('\\X')) and len(s) >= 4:
                c = int(s[2:4], 16)
                return chr(c), s[4:]
            if (s.startswith('\\u') or s.startswith('\\U')) and len(s) >= 6:
                c = chr(int(s[2:6], 16))
                if len(c) != 1:
                    c = ''  # remove unsupported unicode
                return c, s[6:]
            else:
                return s[1], s[2:]
        else:
            return s[0], s[1:]

    def Class(self, ptree):
        s = ptree.getToken()
        chars = []
        ranges = []
        while len(s) > 0:
            c, s = TPEGLoader.unquote(s)
            if s.startswith('-') and len(s) > 1:
                c2, s = TPEGLoader.unquote(s[1:])
                ranges.append(c + c2)
            else:
                chars.append(c)
        if len(chars) == 0 and len(ranges) == 0:
            return FAIL
        if len(chars) == 1 and len(ranges) == 0:
            return PChar(chars[0])
        return PRange(''.join(chars), ''.join(ranges))

    def newRef(self, name):
        if name in self.names:
            return self.peg.newRef(name)
        if name in BuiltInNonTerminal:
            return BuiltInNonTerminal[name]
        es = [PChar(name)]
        if len(name) > 0 and name[-1].isalnum():
            es.append(PNot(self.newRef('W')))
        es.append(self.newRef('_'))
        return PSeq(*es)

    def Name(self, ptree):
        name = ptree.getToken()
        if name in self.names:
            ref = self.peg.newRef(name)
            return PName(ref, ref.uname(), ptree)
        if name in BuiltInNonTerminal:
            return self.newRef(name)
        if name[0].isupper() or name.startswith('_'):  # or name[0].islower() :
            self.perror(ptree, f'undefined nonterminal {name}')
            self.peg[name] = EMPTY
            return self.peg.newRef(name)
        self.pwarn(ptree, f'undefined nonterminal {name}')
        return self.newRef(name)

    def Quoted(self, ptree):
        name = ptree.getToken()
        if name in self.names:
            ref = self.peg.newRef(name)
            return PName(ref, ref.uname(), ptree)
        self.pwarn(ptree, f'undefined nonterminal {name}')
        name = name[1:-1]
        return self.newRef(name)

    def Many(self, ptree):
        return PMany(self.conv(ptree.e))

    def Many1(self, ptree):
        return POneMany(self.conv(ptree.e))

    def OneMany(self, ptree):
        return POneMany(self.conv(ptree.e))

    def Option(self, ptree):
        return POption(self.conv(ptree.e))

    def And(self, ptree):
        return PAnd(self.conv(ptree.e))

    def Not(self, ptree):
        return PNot(self.conv(ptree.e))

    def Seq(self, ptree):
        return PSeq.new(*tuple(map(lambda p: self.conv(p), ptree)))

    def Ore(self, ptree):
        return POre.new(*tuple(map(lambda p: self.conv(p), ptree)))

    def Alt(self, ptree):
        self.pwarn(ptree, f'unordered choice is not supported')
        return POre.new(*tuple(map(lambda p: self.conv(p), ptree)))

    def Node(self, ptree):
        tag = ptree.getToken('tag', '')
        e = self.conv(ptree.e)
        return PNode(e, tag, 0)

    def Edge(self, ptree):
        edge = ptree.getToken('edge', '')
        e = self.conv(ptree.e)
        return PEdge(edge, e)

    def Fold(self, ptree):
        edge = ptree.getToken('edge', '')
        tag = ptree.getToken('tag', '')
        e = self.conv(ptree.e)
        return PFold(edge, e, tag, 0)

    FIRST = {'lazy', 'scope', 'symbol', 'def',
             'match', 'equals', 'contains', 'cat'}

    def Func(self, ptree):
        funcname = ptree.getToken(0)
        ps = [self.conv(p) for p in ptree[1:]]
        if funcname.startswith('choice'):
          return TPEGLoader.loadChoice(ptree, funcname, ps)
        if funcname in TPEGLoader.FIRST:
            return PAction(ps[0], funcname, tuple(ps), ptree)
        return PAction(EMPTY, funcname, tuple(ps), ptree)

    @classmethod
    def loadChoice(cls, ptree, funcname, ps):
        def feq(ss, n):
            return {x for x in ss if len(x) == n and not x.startswith('#')}

        def fgt(ss, n):
            return {x for x in ss if len(x) > n and not x.startswith('#')}
        n = funcname[6:]
        if n.isdigit():
            return TPEGLoader.choice(ptree.urn_, ps, int(n), feq)
        if n.startswith('G'):
            return TPEGLoader.choice(ptree.urn_, ps, int(n[1:]), fgt)
        return TPEGLoader.choice(ptree.urn_, ps, 0, fgt)

    @classmethod
    def fileName(cls, urn, file):
        if file.startswith('CJDIC'):
            file = file.replace('CJDIC', os.environ.get('CJDIC', 'cjdic'))
            return Path(file)
        return Path(urn).parent / file

    @classmethod
    def choice(cls, urn, es, n, fset):
        ds = set()
        for e in es:
            filename = str(e)[1:-1]
            file = TPEGLoader.fileName(urn, filename)
            try:
                with file.open(encoding='utf-8_sig') as f:
                    ss = [x.strip('\r\n') for x in f.readlines()]
                    ds |= fset(ss, n)
            except:
                if not filename.startswith('CJDIC'):
                    print(f'File Not Found: {file}')
        choice = [PChar(x) for x in sorted(ds, key=lambda x: len(x))[::-1]]
        return POre.new(*choice)



TPEGParser = pasm.generate(TPEGGrammar['Start'])

def load_grammar(peg, text, **options):
    console = options.get('console', DefaultConsole)
    # pegparser = pasm.generate(options.get('peg', TPEGGrammar))
    
    if isinstance(text, Path) and text.is_file():
        f = text.open(encoding=options.get('encoding', 'utf-8_sig'))
        data = f.read()
        f.close()
        t = TPEGParser(data, options.get('urn', text))
        basepath = str(text)
    else:
        if 'basepath' in options:
            basepath = options['basepath']
        else:
            basepath = inspect.currentframe().f_back.f_code.co_filename
        t = TPEGParser(text, options.get('urn', basepath))
        basepath = (str(Path(basepath).resolve().parent))
    options['basepath'] = basepath
    if t == 'err':
        console.log('error', t, 'Syntax Error')
        return
    pconv = TPEGLoader(peg, console, **options)
    pconv.load(t)

def findpath(paths, file):
    if file.find('=') > 0 or file.find('<-') > 0:
        return file
    for p in paths:
        path = Path(p) / file
        if path.is_file():
            return path.resolve()
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)

GrammarDB = {}

def grammar(file_or_text, **options):
    paths = []
    basepath = options.get('basepath', '')
    if basepath == '':
        paths.append('')
    else:
        paths.append(str(Path(basepath).resolve().parent))
    framepath = inspect.currentframe().f_back.f_code.co_filename
    paths.append(str(Path(framepath).resolve().parent))
    paths.append(str(Path(__file__).resolve().parent / 'grammar'))
    paths += os.environ.get('GRAMMAR', '').split(':')
    path = findpath(paths, file_or_text)
    key = str(path)
    if key in GrammarDB:
        return GrammarDB[key]
    peg = Grammar()
    load_grammar(peg, path, **options)
    GrammarDB[key] = peg
    return peg

if __name__ == '__main__':
    peg = grammar('es.tpeg')
