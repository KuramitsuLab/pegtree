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
from pegtree.terminal import DefaultConsole

bold = DefaultConsole.bold
color = DefaultConsole.color

'''
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
'''


def version():
    print(DefaultConsole.bold(
        'PEGTree - A PEG Parser Generator with Tree Annotation'))


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
        '-v': ('verbose', True),
        '-verbose': ('verbose', True),
        '-g': ('grammar', None),
        '--grammar': ('grammar', None),
        '-s': ('start', None),
        '--start': ('start', None),
        '-e': ('expression', None),
        '--expr': ('expression', None),
        '-f': ('format', None),
        '--format': ('format', None),
        '-O0': ('-O', 0),
        '-O1': ('-O', 1),
        '-O2': ('-O', 2),
        '-O2': ('-O', 3),
    }

    def parse_each(a, d):
        first = a[0]
        if first.startswith('-'):
            if first in options:
                key, value = options[first]
                if value is None:
                    if len(a) > 1:
                        d[key] = a[1]
                        return a[2:]
                else:
                    d[key] = value
                    return a[1:]
            # d['inputs'].append(a)
            raise CommandUsageError
        else:
            d['inputs'].append(a[0])
            return a[1:]

    d = {'inputs': [], '-O': 2, 'verbose': False}
    while len(argv) > 0:
        argv = parse_each(argv, d)
    #print('OPTION', d)
    if d['verbose']:
        DefaultConsole.isverbose = True
    return d


class CommandUsageError(Exception):
    pass


def usage():
    print(bold('PEGTree - A PEG Parser Generator with Tree Annotation'))
    print("Usage: pegtree <command> options inputs")
    print("  -g | --grammar <file>      specify a grammar file")
    print("  -e | --expr <expression>   specify a parsing expression")
    print("  -s | --start <NAME>        specify a starting rule")
    print("  -f | --format <file>       specify an output format")
    print()

    print("Example:")
    print("  pegtree parse -g math.tpeg <inputs>")
    print("  pegtree example -g math.tpeg <inputs>")
    print("  pegtree pasm -g math.tpeg")
    print("  pegtree update")
    print()

    print("The most commonly used pegtree commands are:")
    print(" parse      run a generated parser")
    print(" example    test all examples")
    print(" pasm       generate a pasm combinator function")
    print(" list       all sample grammars")
    print(" update     update pegtree (via pip)")


showingTPEG = False


def load_grammar(options, default=None):
    global showingTPEG
    expr = options.get('expression', None)
    if expr is not None:
        grammar = 'A = ' + expr
        options['urn'] = f'(-e {repr(expr)})'
        return pegtree.grammar(grammar, **options)
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
        options['urn'] = '(stdin)'
        showingTPEG = False
        return pegtree.grammar(data, **options)
    if file == 'stdin.tpeg':
        data = sys.stdin.read()
        options['urn'] = file
        return pegtree.grammar(data, **options)
    options['urn'] = file
    return pegtree.grammar(file, **options)


def generator(options):
    # if 'parser' in options:
    #    m = importlib.import_module(options['parser'])
    #    return m.generate
    return pegtree.generate


def getstart(peg, options):
    if 'start' in options:
        return options['start']
    return peg.start()


def colorTree(t):
    if t.isSyntaxError():
        return t.message(color('Red', 'Syntax Error'))
    else:
        # unconsumed = ''
        # if epos < len(t.inputs_):
        #     unconsumed = ' + ' + color('Purple', t.inputs_[epos:])
        sb = []
        t.strOut(sb, token=lambda x: color('Blue', x),
                 tag=lambda x: color('Cyan', x))
        return "".join(sb)

# parse command


def sample(options):
    files = os.listdir(Path(__file__).parent / 'grammar')
    files.sort()
    for file in files:
        if file.endswith('.tpeg'):
            print(file)


def tpeg(options):
    peg = load_grammar(options)
    print(peg)
    if '@@example' in peg:
        print()
        prefix = color('Blue', 'example')
        quote = color("Red", "'''")
        for testcase in peg['@@example']:
            name, doc = testcase
            name = bold(name)
            doc = doc.getToken()
            if doc.find('\n') > 0:
                print(prefix, name, quote)
                print(doc, quote, sep='\n')
            else:
                print(prefix, name, doc)


def peg(options):
    options['isPurePEG'] = True
    peg = load_grammar(options)
    print(peg)


def optimize(options):
    from pegtree.optimizer import prepare
    peg = load_grammar(options)
    start, refs, rules, memos = prepare(peg)
    for ref in refs:
        uname = ref.uname(peg)
        print(uname, '=', rules[uname])
    print('memo:', ' '.join(memos))


def parse(options, conv=None):
    peg = load_grammar(options)
    parser = generator(options)(peg, **options)
    inputs = options['inputs']
    tdump = treeconv.treedump(options, colorTree)
    if len(inputs) == 0:  # Interactive Mode
        try:
            start = getstart(peg, options)
            while True:
                s = readlines(color('Blue', start) + bold(' <<< '))
                tree = parser(s, urn='(stdin)')
                print(tdump(tree))
        except (EOFError, KeyboardInterrupt):
            pass
    elif len(inputs) == 1:
        colorTree(read_inputs(inputs[0]))
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
        print(colorTree(res))


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
    try:
        for file in options['inputs']:
            with open(file) as f:
                for line in f:
                    lines += 1
                    try:
                        t = parser(line)
                        fail += dumpError(lines, line, t)
                    except RecursionError:
                        print(color('Red', line))
                        fail += 1
    except KeyboardInterrupt:
        pass
    et = time.time()
    if lines > 0:
        print(f'{fail}/{lines} {fail/lines} {(et - st) * 1000.0} ms')


def pasm(options):
    from pegtree.nezcc import parsec
    peg = load_grammar(options)
    parsec(peg, **options)


def jsonfy(options):
    from .visitor import JSONfy
    import json
    peg = load_grammar(options)
    parser = generator(options)(peg, **options)
    for file in options['inputs']:
        tree = parser(read_inputs(file))
        value = JSONfy.convert(tree)
        print(json.dumps(value))


def pasmcc(options):
    from pegtree.nezcc import parsec
    peg = load_grammar(options)
    parsec(peg, **options)


def cjtoken(options, conv=None):
    import pegtree.cj as cj
    peg = load_grammar(options)
    parser = generator(options)(peg, **options)
    inputs = options['inputs']
    for file in options['inputs']:
        with open(file) as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue
                line = line.replace('\n', '')
                print(line)
                tree = parser(line)
                print(repr(tree))
                for token in cj.tokenize(tree):
                    print(repr(token))
                print()


def update(options):
    try:
        # pip3 install -U git+https://github.com/KuramitsuLab/pegpy.git
        subprocess.check_call(
            ['pip3', 'install', '-U', 'pegtree'])
    except:
        pass


def update_beta(options):
    try:
        # pip3 install -U git+https://github.com/KuramitsuLab/pegtree.git
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
