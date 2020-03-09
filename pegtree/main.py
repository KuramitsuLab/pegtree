#!/usr/local/bin/python
from pathlib import Path
import functools
import subprocess
# import readline
import time
import sys
import os
import importlib
import pegtree
import pegtree.treeconv as treeconv

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
    print(bold('PEGTree Parsing for Python3'))


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
    print("Usage: pegtree <command> options inputs")
    print("  -g | --grammar <file>      specify a grammar file")
    print("  -s | --start <NAME>        specify a starting rule")
    print("  -o | --output <file>       specify an output file")
    print("  -D                         specify an optional value")
    print()

    print("Example:")
    print("  pegtree parse -g math.tpeg <inputs>")
    print("  pegtree example -g math.tpeg <inputs>")
    print("  pegtree pasm -g math.tpeg")
    print()

    print("The most commonly used pegtree commands are:")
    print(" parse      run an interactive parser")
    print(" pasm       generate a parser combinator function")
    print(" example    test all examples")
    print(" update     update pegtree (via pip)")


showingTPEG = True


def load_grammar(options, default=None):
    global showingTPEG
    file = options.get('grammar', default)
    if file is None:
        print('Enter a TPEG grammar')
        sb = []
        try:
            while True:
                s = input()
                if s == '' or s is None:
                    break
                sb.append(s)
        except:
            pass
        data = '\n'.join(sb)
        options['basepath'] = '(stdin)'
        showingTPEG = False
        return pegtree.grammar(data, **options)
    if file == 'stdin.tpeg':
        data = sys.stdin.read()
        options['basepath'] = file
        return pegtree.grammar(data, **options)
    return pegtree.grammar(file, **options)


def generator(options):
    if 'parser' in options:
        m = importlib.import_module(options['parser'])
        return m.generate
    return pegtree.generate


def getstart(peg, options):
    if 'start' in options:
        return options['start']
    return peg.start()


def dump(t):
    if t.isSyntaxError():
        return t.message(color('Red', 'Syntax Error'))
    else:
        unconsumed = ''
        if t.epos_ < len(t.inputs_):
            unconsumed = ' + ' + color('Purple', t.inputs_[t.epos_:])
        sb = []
        t.strOut(sb, token=lambda x: color('Blue', x),
                 tag=lambda x: color('Cyan', x))
        return "".join(sb) + unconsumed

# parse command


def parse(options, conv=None):
    peg = load_grammar(options)
    parser = generator(options)(peg, **options)
    inputs = options['inputs']
    tdump = treeconv.treedump(options, dump)
    if len(inputs) == 0:  # Interactive Mode
        try:
            if showingTPEG:
                print(peg)
            start = getstart(peg, options)
            while True:
                s = readlines(color('Blue', start) + bold(' <<< '))
                print(tdump(parser(s, urn='(stdin')))
        except (EOFError, KeyboardInterrupt):
            pass
    elif len(inputs) == 1:
        dump(read_inputs(inputs[0]))
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
    for testcase in peg['@@example']:
        name, doc = testcase
        if not name in peg:
            continue
        if not name in parsers:
            parsers[name] = generator(options)(peg, start=name)
        res = parsers[name](doc.inputs_, doc.urn_, doc.spos_, doc.epos_)
        # print()
        ok = doc.inputs_[doc.spos_:res.epos_]
        fail = doc.inputs_[res.epos_:doc.epos_]
        print(bold(f'parsing {name}'), color(
            'Green', f'{ok}')+color('Red', f'{fail}'), bold('=> '), end='')
        dump(res)


def dumpError(lines, line, s):
    errs = 0
    for t in s:
        cur = str(t)
        if t.isSyntaxError():
            errs = 1
            s = max(0, t.spos_ - 10)
            prev = t.inputs_[s:t.spos_]
            # print(line)
            print(lines, color('Green', f'{prev}') + color('Red', f'{cur}'))
    return errs


def test(options):
    peg = load_grammar(options)
    parser = generator(options)(peg, **options)
    inputs = options['inputs']
    st = time.time()
    lines = 0
    fail = 0
    for file in options['inputs']:
        with open(file) as f:
            for line in f:
                lines += 1
                t = parser(line)
                fail += dumpError(lines, line, t)
    et = time.time()
    if lines > 0:
        print(f'{fail}/{lines} {fail/lines} {(et - st) * 1000.0} ms')


def peg(options):
    peg = load_grammar(options)
    print(peg)


def pasm0(options):
    from pegtree.parsec import parsec
    peg = load_grammar(options)
    options['optimized'] = 0
    parsec(peg, **options)


def pasm(options):
    from pegtree.parsec import parsec
    peg = load_grammar(options)
    parsec(peg, **options)


def update(options):
    try:
        # pip3 install -U git+https://github.com/KuramitsuLab/pegpy.git
        subprocess.check_call(
            ['pip3', 'install', '-U', 'pegtree'])
    except:
        pass


def update_beta(options):
    try:
        # pip3 install -U git+https://github.com/KuramitsuLab/pegpy.git
        subprocess.check_call(
            ['pip3', 'install', '-U', 'git+https://github.com/KuramitsuLab/pegtree.git'])
    except:
        pass


def main(argv=sys.argv):
    names = globals()
    if len(argv) > 1:
        cmd = argv[1]
        options = parse_options(argv[2:])
        cs = cmd.split('.')
        if len(cs) == 2:
            cmd = cs[0]
            options['ext'] = cs[1]
        if cmd in names:
            names[cmd](options)
            return
    usage()


if __name__ == "__main__":
    main(sys.argv)
