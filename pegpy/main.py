#!/usr/local/bin/python
import sys, os, errno
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pegpy.peg import *
import pegpy.utils as u

def bold(s):
    return '\033[1m' + str(s) + '\033[0m'

def read_inputs(a):
    try:
        f = open(a, 'rb')
        data = f.read()
        f.close()
        return data
    except:
        return a.encode()

def readlines(prompt):
    s = input(prompt)
    if s != '':
        return s
    else:
        l = []
        while True:
            prev = s
            s = input()
            l.append(s)
            if prev == '' and s == '':
                break
        return '\n'.join(l)

def load_grammar(opt, default = None):
    file = default if not 'grammar' in opt else opt['grammar']
    if file is None:
        raise CommandError(opt)
    g = Grammar(file)
    g.load(u.find_path(file))
    return g

def parse(opt):
    g = load_grammar(opt)
    parser = nez(g)
    if len(opt['inputs']) == 0:
        try:
            version()
            while True:
                s = readlines(bold('>>> '))
                print(parser(s))
        except EOFError:
            pass
    else:
        for input in opt['inputs']:
            print(parser(read_inputs(input)))

def json(opt):
    pass

def example(opt):
    g = load_grammar(opt)
    g.testAll()

def origami(opt):
    from pegpy.origami.origami import transpile
    g = load_grammar(opt, 'konoha6.tpeg')
    parser = nez(g)
    origami_files = [f for f in opt['inputs'] if f.endswith('.origami')]
    source_files = [f for f in opt['inputs'] if not f.endswith('.origami')]
    for input in source_files:
        t = parser(read_inputs(input))
        transpile(t, origami_files)

def nezcc(opt):
    pass

def bench(opt):
    pass

def main():
    try:
        argv = sys.argv
        if len(argv) < 2:
            raise CommandError({})

        cmd = argv[1]
        d = parse_opt(argv[2:])
        names = globals()
        if cmd in names:
            names[cmd](d)
        else:
            raise CommandError(d)
    except CommandError as e:
        usage(e.opt)

def parse_opt(argv):
    def parse_each(a, d):
        if a[0].startswith('-'):
            if len(a) > 1:
                if a[0] == '-g':
                    d['grammar'] = a[1]
                    return a[2:]
                elif a[0] == '-s':
                    d['start'] = a[1]
                    return a[2:]
                elif a[0] == '-X':
                    d['extension'] = a[1]
                    return a[2:]
                elif a[0] == '-D':
                    d['option'] = a[1]
                    return a[2:]
            d['inputs'].extend(a)
            raise CommandError(d)
        else:
            d['inputs'].append(a[0])
            return a[1:]
    d  = {'inputs': []}
    while len(argv) > 0:
        argv = parse_each(argv, d)
    return d

def version():
    print(bold('PEGPY - A PEG-based Parsering Tools for Python'))

def usage(opt):
    print("Usage: pegpy <command> options inputs");
    print("  -g | --grammar <file>      specify a grammar file");
    print("  -s | --start <NAME>        specify a starting rule");
    print("  -D                         specify an optional value");
    print()

    print("Example:");
    print("  pegpy parse -g math.tpeg <inputs>");
    print("  pegpy json -g math.tpeg <inputs>");
    print("  pegpy origami -g konoha6.tpeg python.origami <inputs>")
    print();

    print("The most commonly used nez commands are:");
    print(" parse      run an interactive parser");
    print(" nezcc      generate a nez parser");
    print(" origami    transpiler")
    print(" bench      the bench mark")
    print(" json       output tree as json file")

class CommandError(Exception):
    def __init__(self, opt):
        self.opt = opt

if __name__ == "__main__":
    main()

'''
  st = time.time()
  t = parse(s, len(s)-1, newAST, subAST)
  et = time.time()
  sys.stderr.write(a + " " + str((et-st) * 1000.0) + "[ms]: ")
  sys.stderr.flush()
  sys.stdout.write(str(t))
  sys.stdout.flush()
  sys.stderr.write('\n')
'''
