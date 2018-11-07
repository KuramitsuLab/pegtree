#!/usr/local/bin/python
import sys, os, errno
from pathlib import Path
#sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pegpy.peg import *

def read_inputs(a):
    try:
        f = open(a, 'rb')
        data = f.read() + b'\0'  # Zero Termination
        f.close()
        return data
    except:
        return a.encode() + b'\0' # Zero Termination

def parse(opt):
    g = Grammar('x')
    if not 'grammar' in opt:
        raise CommandError(opt)
    else:
        path = Path(opt['grammar'])
        if path.exists():
            g.load(path)
        else:
            path = Path(__file__).resolve().parent / 'grammar' / opt['grammar']
            if path.exists():
                g.load(path)
            else:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), opt['grammar'])

    #g.dump()
    #g.testAll()
    #print('')
    p = nez(g)
    for input in opt['inputs']:
        print(p(read_inputs(input)))

def nezcc(opt):
    pass

def tojson(opt):
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

def usage(opt):
    print("Usage: nez <command> options inputs");
    print("  -g | --grammar <file>      specify a grammar file");
    print("  -s | --start <NAME>        specify a starting rule");
    print("  -X                         specify an extension class");
    print("  -D                         specify an optional value");
    print()

    print("Example:");
    print("  pegpy parse -g math.tpeg <inputs>");
    print("  pegpy tojson -g math.tpeg <inputs>");
    print();

    print("The most commonly used nez commands are:");
    print(" parse      run an interactive parser");
    print(" nezcc      generate a nez parser");

class CommandError(Exception):
    def __init__(self, opt):
        self.opt = opt

if __name__ == "__main__":
    main()

'''
def parse2(opt):
    peg = PEG()
    peg.load(opt['grammar'])
    peg.pegp()
'''

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
