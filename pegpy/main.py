#!/usr/local/bin/python
import sys, time, readline, subprocess, functools
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pegpy.peg import *
from pegpy.gparser.gnez import gnez
import pegpy.utils as u

def bold(s):
    return '\033[1m' + str(s) + '\033[0m'

def version():
    print(bold('PEGPY - A PEG-based Parsering Tools for Python'))

def read_inputs(a):
    path = Path(a)
    if path.exists():
        f = path.open()
        data = f.read()
        f.close()
        return data
    else:
        return a

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

def init_output(opt):
    out = u.Writer(opt['output'] if 'output' in opt else None)
    return out

def load_grammar(opt, default = None):
    file = default if not 'grammar' in opt else opt['grammar']
    if file is None:
        raise CommandError(opt)
    g = Grammar(file)
    g.load(file)
    return g

def switch_generator(opt, default = 'math.tpeg'):
    file = default if not 'grammar' in opt else opt['grammar']
    if file.endswith('.gpeg'):
        return gnez
    return nez

# parse command

def parse(opt, out, conv=None):
    g = load_grammar(opt)
    parser = switch_generator(opt)(g, conv)
    inputs = opt['inputs']
    if len(inputs) == 0:   #Interactive Mode
        try:
            while True:
                s = readlines(bold('>>> '))
                out.dump(parser(s))
        except (EOFError, KeyboardInterrupt):
            pass
        return
    if len(inputs) == 1:
        out.dump(parser(read_inputs(inputs[0])))
        return
    else:
        for file in opt['inputs']:
            st = time.time()
            t = parser(read_inputs(file))
            et = time.time()
            out.println(file, (et - st) * 1000.0, "[ms]:", t.tag)
        return

def json(opt, out):
    parse(opt, out, lambda t: t.asJSON())

def example(opt, out):
    g = load_grammar(opt)
    p = {}
    test = 0
    ok = 0
    for testcase in g.examples:
        name, inputs, output = testcase
        if not name in g: continue
        if not name in p:
            p[name] = g.pgen(name)
        res = p[name](inputs)
        if output == None:
            if res == 'err':
                out.perror(res.pos3(), 'NG ' + name)
            else:
                out.println('OK', name, '=>', str(res))
        else:
            t = str(res).replace(" b'", " '")
            test += 1
            if t == output:
                out.println('OK', name, inputs)
                ok += 1
            else:
                out.println('NG', name, inputs, output, '!=', t)
    if test > 0:
        out.println('OK', ok, 'FAIL', test - ok, ok / test * 100.0, '%')

def peg(opt, out):
    g = load_grammar(opt)
    g.dump(out)

def origami(opt, out):
    from pegpy.origami.origami import transpile, transpile_init
    g = load_grammar(opt, 'konoha6.tpeg')
    parser = switch_generator(opt, 'konoha6.tpeg')(g)
    origami_files = [f for f in opt['inputs'] if f.endswith('.origami')]
    source_files = [f for f in opt['inputs'] if not f.endswith('.origami')]
    env = transpile_init(origami_files, out)
    if len(source_files) == 0:
        try:
            while True:
                s = readlines(bold('>>> '))
                t = parser(s, '>>>')
                out.println(repr(t))
                out.println(repr(transpile(env, t, out)))
        except (EOFError, KeyboardInterrupt):
            pass
        return None
    else:
        for input in source_files:
            t = parser(read_inputs(input))
            out.println(repr(transpile(env, t, out)))

def macaron(opt, out, default = 'npl.tpeg'):
    from pegpy.origami.macaron import transpile
    g = load_grammar(opt, default)
    parser = switch_generator(opt, default)(g)
    inputs = opt['inputs']
    if len(inputs) == 0:
        try:
            while True:
                s = readlines(bold('>>> '))
                t = parser(s)
                out.print(repr(transpile(t)))
        except (EOFError, KeyboardInterrupt):
            pass
        return None
    else:
        for input in inputs:
            t = parser(read_inputs(input))
            out.println(transpile(t))

def nezcc(opt, out):
    pass

def bench(opt):
    pass

def update(opt, out):
    try:
        subprocess.check_call(['pip3', 'install', '-U', 'git+https://github.com/KuramitsuLab/pegpy.git'])
    except:
        pass

def parse_opt(argv):
    def parse_each(a, d):
        if a[0].startswith('-'):
            if len(a) > 1:
                if a[0] == '-g' or a[0] == '--grammar':
                    d['grammar'] = a[1]
                    return a[2:]
                elif a[0] == '-s' or a[0] == '--start':
                    d['start'] = a[1]
                    return a[2:]
                elif a[0] == '-o' or a[0] == '--output':
                    d['output'] = a[1]
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
    print("Usage: pegpy <command> options inputs")
    print("  -g | --grammar <file>      specify a grammar file")
    print("  -s | --start <NAME>        specify a starting rule")
    print("  -o | --output <file>       specify an output file")
    print("  -D                         specify an optional value")
    print()

    print("Example:")
    print("  pegpy parse -g math.tpeg <inputs>")
    print("  pegpy json -g math.tpeg <inputs>")
    print("  pegpy origami -g konoha6.tpeg common.origami <inputs>")
    print()

    print("The most commonly used nez commands are:")
    print(" parse      run an interactive parser")
    print(" nezcc      generate a cross-language parser")
    print(" origami    transpiler")
    print(" bench      the bench mark")
    print(" json       output tree as json file")
    print(" update     update pegpy")

class CommandError(Exception):
    def __init__(self, opt):
        self.opt = opt

def main2(argv):
    cmd = argv[1]
    opt = parse_opt(argv[2:])
    names = globals()
    if cmd in names:
        out = init_output(opt)
        names[cmd](opt, out)
        return out
    else:
        raise CommandError(opt)

def main():
    argv = sys.argv
    try:
        if len(argv) < 2: raise CommandError({})

        if functools.reduce(lambda x, y: x or ('edit' in y), argv[1:], False):
            from pegpy.playground.server import playground
            playground(argv, main2)
        else:
            main2(argv)

    except CommandError as e:
        usage(e.opt)

if __name__ == "__main__":
    main()
