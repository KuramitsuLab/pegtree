#!/usr/local/bin/python
from pathlib import Path
import functools
import subprocess
# import readline
import time
import sys
import os
import importlib
# m = importlib.import_module('foo.some')  # -> 'module'
import pegpy.tpeg as tpeg


istty = True


def bold(s):
    return '\033[1m' + str(s) + '\033[0m' if istty else str(s)


COLOR = {
    "Black": '0;30', "DarkGray": '1;30',
    "Red": '0;31', "LightRed": '1;31',
    "Green": '0;32', "LightGreen": '1;32',
    "Orange": '0;33', "Yellow": '1;33',
    "Blue": '0;34', "LightBlue": '1;34',
    "Purple": '0;35', "LightPurple": '1;35',
    "Cyan": '0;36', "LightCyan": '1;36',
    "LightGray": '0;37', "White": '1;37',
}


def color(c, s):
    return '\033[{}m{}\033[0m'.format(COLOR[c], str(s)) + '' if istty else str(s)


def showing(pos, msg):
    if pos is None:
        print(msg)
    else:
        print(pos.showing(msg))


def log(type, pos, *msg):
    msg = ' '.join(map(str, msg))
    if type.startswith('err'):
        showing(pos, color('Red', '[error] ') + str(msg))
    elif type.startswith('warn'):
        showing(pos, color('Orange', '[warning] ') + str(msg))
    elif type.startswith('info') or type.startswith('notice'):
        showing(pos, color('Cyan', '[info] ') + str(msg))
    else:
        showing(pos, str(msg))


def version():
    print(bold('PEGPY - A PEG-based Parsing for Python'))


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


def parse_options(argv):
    options = {
        'grammar': ['-g', '--grammar'],
        'start': ['-s', '--start'],
        'parser': ['-p', '--parser'],
        'output': ['-o', '--output'],
        'verbose': ['--verbose'],
    }

    def parse_each(a, d):
        if a[0].startswith('-'):
            if len(a) > 1:
                for key, list in options.items():
                    for l in list:
                        if a[0] == l:
                            d[key] = a[1]
                            return a[2:]
            d['inputs'].append(a)
            raise CommandUsageError
        else:
            d['inputs'].append(a[0])
            return a[1:]

    d = {'inputs': []}
    while len(argv) > 0:
        argv = parse_each(argv, d)
    d['logger'] = log
    return d


class CommandUsageError(Exception):
    pass


def usage():
    print("Usage: pegpy <command> options inputs")
    print("  -g | --grammar <file>      specify a grammar file")
    print("  -s | --start <NAME>        specify a starting rule")
    print("  -o | --output <file>       specify an output file")
    print("  -D                         specify an optional value")
    print()

    print("Example:")
    print("  pegpy parse -g math.tpeg <inputs>")
    print("  pegpy example -g math.tpeg <inputs>")
    print("  pegpy nezcc -g math.tpeg nez.ts")

    print("The most commonly used nez commands are:")
    print(" parse      run an interactive parser")
    print(" example    test all examples")
    print(" nezcc      generate a cross-language parser")
    print(" update     update pegpy (via pip)")


def load_grammar(options, default=None):
    file = options.get('grammar', default)
    if file is None:
        raise CommandUsageError()
    if file == 'stdin.tpeg':
        data = sys.stdin.read()
        options['basepath'] = file
        return tpeg.grammar(data, **options)
    return tpeg.grammar(file, **options)


def generator(options):
    if 'parser' in options:
        m = importlib.import_module(options['parser'])
        return m.generate
    return tpeg.generate

# parse command


def parse(options, conv=None):
    peg = load_grammar(options)
    parser = generator(options)(peg, **options)
    inputs = options['inputs']
    if len(inputs) == 0:  # Interactive Mode
        try:
            while True:
                s = readlines(bold('>>> '))
                parser(s).dump()
        except (EOFError, KeyboardInterrupt):
            pass
    elif len(inputs) == 1:
        parser(read_inputs(inputs[0])).dump()
    else:
        for file in options['inputs']:
            st = time.time()
            t = parser(read_inputs(file))
            et = time.time()
            print(file, (et - st) * 1000.0, "[ms]:", t.tag)


def example(options):
    peg = load_grammar(options)
    if '@@example' not in peg:
        return
    parsers = {}
    test = 0
    ok = 0
    for testcase in peg['@@example']:
        name, pos4 = testcase
        if not name in peg:
            continue
        if not name in parsers:
            parsers[name] = generator(options)(peg, start=name)
        res = parsers[name](pos4.inputs, pos4.urn, pos4.spos, pos4.epos)
        if res == 'err':
            log('error', res, name)
        else:
            print(color('Green', f'OK {name}'), f' => {repr(res)}')
    if test > 0:
        print(color('Green', f'OK {ok}'), color(
            'Red', f'FAIL {test - ok}'), ok / test * 100.0, '%')


def peg(options):
    peg = load_grammar(options)
    print(peg)


def nezcc(options):
    from pegpy.nezcc import nezcc
    inputs = options['inputs']
    if len(inputs) == 0:
        inputs.append('empty.ts')
    peg = load_grammar(options)
    nezcc(input[0], peg)


'''
def json(opt, out):
    parse(opt, out, lambda t: t.asJSON())

def nezcc(opt, out):
    pass


def bench(opt):
    pass
'''


'''

def origami(opt, out, grammar='konoha6.tpeg', ts=None):
    from pegpy.origami.typesys import transpile, transpile_init
    g = load_grammar(opt, grammar)
    if 'Snippet' in g:
        g = g['Snippet']
    parser = switch_generator(opt, 'tpeg')(g)
    origami_files = [f for f in opt['inputs'] if f.endswith('.origami')]
    source_files = [f for f in opt['inputs'] if not f.endswith('.origami')]
    env = transpile_init(origami_files, ts, out)
    if len(source_files) == 0:
        try:
            linenum = 1
            while True:
                s = readlines(bold('[{}]>>> '.format(linenum)))
                t = parser(s, '[{}]>>> '.format(linenum))
                linenum += 1
                out.verbose(repr(t))
                out.println(repr(transpile(env, t, out)))
        except (EOFError, KeyboardInterrupt):
            pass
        return None
    else:
        for input in source_files:
            t = parser(read_inputs(input), input)
            out.println(repr(transpile(env, t, out)))

def test(opt, out):
    from pegpy.origami.arare import compile
    for f in opt['inputs']:
        print(f)
        print('---')
        print(compile(read_inputs(f)))
'''


def update(options):
    try:
        # pip3 install -U git+https://github.com/KuramitsuLab/pegpy.git
        subprocess.check_call(
            ['pip3', 'install', '-U', 'git+https://github.com/KuramitsuLab/pegpy.git'])
    except:
        pass


def main(argv=sys.argv):
    try:
        names = globals()
        if len(argv) > 1:
            cmd = argv[1]
            options = parse_options(argv[2:])
            if cmd in names:
                names[cmd](options)
                return
        raise CommandUsageError()
    except CommandUsageError:
        usage()


if __name__ == "__main__":
    main(sys.argv)
