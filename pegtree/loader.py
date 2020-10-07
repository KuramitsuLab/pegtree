import sys
import os
import errno
import inspect
from pathlib import Path
from pegtree.peg import *
import pegtree.pasm as pasm
from pegtree.tpeg_pasm import TPEGGrammar
from pegtree.terminal import DefaultConsole as console

#
# BuiltIn_NonTerminal
# 

BuiltIn_NonTerminal = {
    'W': PRange('_', 'AZaz09'),
    'LF': POre(PChar('\r\n'), PChar('\n')),
    'EOF': PNot(PAny()),
    '_': PMany(PRange(' \t', '')),
    '__': PMany(PRange(' \t\r\n', '')),
}


class TPEGLoader(object):
    def __init__(self, peg, **options):
        self.names = {}
        self.peg = peg
        self.isOnlyPEG = options.get('isPurePEG', False)

    def load(self, ptree):
        for stmt in ptree:
            if stmt == 'Rule':
                name = str(stmt.name)
                if name in self.names:
                    # pos4 = stmt['name'].getpos4()
                    console.perror(stmt.name, f'redefined name {name}')
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
            self.peg[name] = self.conv(ptree)

    def example(self, name, doc):
        self.peg['@@example'].append((name, doc))

    def conv(self, ptree):
        tag = ptree.getTag()
        pe = ptree
        if hasattr(self, tag):
            f = getattr(self, tag)
            pe = f(ptree)
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
        if name in BuiltIn_NonTerminal:
            return BuiltIn_NonTerminal[name]
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
        if name in BuiltIn_NonTerminal:
            return self.newRef(name)
        if name[0].isupper() or name.startswith('_'):  # or name[0].islower() :
            console.perror(ptree, f'undefined nonterminal {console.bold(name)}')
            self.peg['@error'] = True
            self.peg[name] = EMPTY
            return self.peg.newRef(name)
        console.pwarn(ptree, f'undefined nonterminal {console.bold(name)}')
        return self.newRef(name)

    def Quoted(self, ptree):
        name = ptree.getToken()
        if name in self.names:
            ref = self.peg.newRef(name)
            return PName(ref, ref.uname(), ptree)
        console.pwarn(ptree, f'undefined terminal {console.bold(name)}')
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
        return e if self.isOnlyPEG else PNode(e, tag, 0) 

    def Edge(self, ptree):
        edge = ptree.getToken('edge', '')
        e = self.conv(ptree.e)
        return e if self.isOnlyPEG else PEdge(edge, e)

    def Fold(self, ptree):
        edge = ptree.getToken('edge', '')
        tag = ptree.getToken('tag', '')
        e = self.conv(ptree.e)
        return e if self.isOnlyPEG else PFold(edge, e, tag, 0)

    FIRST = {'lazy', 'scope', 'symbol', 'def',
             'match', 'equals', 'contains', 'cat'}

    def Func(self, ptree):
        funcname = ptree.getToken(0)
        ps = [self.conv(p) for p in ptree[1:]]
        if funcname.startswith('choice'):
          return TPEGLoader.loadChoice(ptree, funcname, ps)
        if funcname in TPEGLoader.FIRST:
            return ps[0] if self.isOnlyPEG else PAction(ps[0], funcname, tuple(ps), ptree)
        return EMPTY if self.isOnlyPEG else PAction(EMPTY, funcname, tuple(ps), ptree)

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
            file = file.replace('CJDIC', os.environ.get('CJDIC', '__unknown__'))
            return None if '__unknown__' in file else Path(file)
        return Path(urn).parent / file

    @classmethod
    def choice(cls, urn, es, n, fset):
        ds = set()
        for e in es:
            filename = str(e)[1:-1]
            file = TPEGLoader.fileName(urn, filename)
            if file is None:
                continue
            try:
                with file.open(encoding='utf-8_sig') as f:
                    ss = [x.strip('\r\n') for x in f.readlines()]
                    ds |= fset(ss, n)
            except:
                print(f'can\'t read: {filename} {file}')
        choice = [PChar(x) for x in sorted(ds, key=lambda x: len(x))[::-1]]
        return POre.new(*choice)

class LeftRef(PVisitor):
    EMPTYSET = set()

    def __init__(self, checkLeftRec=True):
        self.checkLeftRec = checkLeftRec
        self.memos = {}

    def PChar(self, pe): return LeftRef.EMPTYSET
    def PAny(self, pe): return LeftRef.EMPTYSET
    def PRange(self, pe): return LeftRef.EMPTYSET

    def PRef(self, pe):
        uname = pe.uname()
        if uname not in self.memos:
            memos[uname] = LeftRef.EMPTYSET
            memos[uname] = self.visit(pe.deref())
        return set(pe)

    def PName(self, pe):
        if self.checkLeftRec:
            self.visit(pe.e)
            return set(pe)
        return self.visit(pe.e)

    def PAnd(self, pe): return self.visit(pe.e)
    def PNot(self, pe): return self.visit(pe.e)
    def PMany(self, pe): return self.visit(pe.e)
    def POneMany(self, pe): return self.visit(pe.e)
    def POption(self, pe): return self.visit(pe.e)

    def PSeq(self, pe):
        result = set()
        for e in pe:
            result |= self.visit(e)
            if self.checkLeftRec & isAlwaysConsumed(e):
                break
        return result

    def POre(self, pe):
        result = set()
        for e in pe:
            result |= self.visit(e)
        return result

    def PNode(self, pe): return self.visit(pe.e)
    def PFold(self, pe): return self.visit(pe.e)
    def PEdge(self, pe): return self.visit(pe.e)
    def PAbs(self, pe): return self.visit(pe.e)

    def PAction(self, pe): return self.visit(pe.e)

#def checkLeftRecursion(peg: Grammar):


TPEGParser = pasm.generate(TPEGGrammar['Start'])

def load_grammar(peg, file_or_text, **options):
    # pegparser = pasm.generate(options.get('peg', TPEGGrammar))
    
    if isinstance(file_or_text, Path) and file_or_text.is_file():
        f = file_or_text.open(encoding=options.get('encoding', 'utf-8_sig'))
        data = f.read()
        f.close()
        basepath = str(file_or_text)
        ptree = TPEGParser(data, basepath)
    else:
        if 'basepath' in options:
            basepath = options['basepath']
        else:
            basepath = inspect.currentframe().f_back.f_code.co_filename
        ptree = TPEGParser(file_or_text, options.get('urn', basepath))
        basepath = (str(Path(basepath).resolve().parent))
    options['basepath'] = basepath
    if ptree.isSyntaxError():
        console.perror(ptree, 'Syntax Error')
        peg['@error'] = True
        return
    pconv = TPEGLoader(peg, **options)
    pconv.load(ptree)

def findpath(paths, file_or_text):
    if file_or_text.find('=') > 0 or file_or_text.find('<-') > 0:
        return file_or_text
    for p in paths:
        path = Path(p) / file_or_text
        if path.is_file():
            return path.absolute()
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_or_text)

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
    if key.endswith('peg'):
        GrammarDB[key] = peg
    return peg

if __name__ == '__main__':
    peg = grammar('es4.tpeg')
