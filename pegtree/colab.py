import json
import pegtree as pg
import pegtree.graph as graph
from IPython.display import Image, HTML, SVG, display
from IPython.core.magic import register_cell_magic, register_line_cell_magic


def is_env_notebook():
    """Determine wheather is the environment Jupyter Notebook"""
    if 'get_ipython' not in globals():
        # Python shell
        return False
    env_name = get_ipython().__class__.__name__
    if env_name == 'TerminalInteractiveShell':
        # IPython shell
        return False
    # Jupyter Notebook
    return True


def parse_example(peg, line):
    if '@@example' in peg and len(peg['@@example']) > 0:
        name, doc = peg['@@example'][-1]
        parser = pg.generate(peg, start=str(name))
        print(f'example: {name}', str(line))
        return parser(str(doc))
    else:
        parser = pg.generate(peg)
        print('Input:', line)
        return parser(line)


def start_option(line):
    if line.startswith('-s ') or line.startswith('--start '):
        _, start, path = line.split()
        return start, path
    return None, line


def test_example(peg, start=None):
    if '@@example' not in peg:
        return
    parsers = {}
    for testcase in peg['@@example']:
        name, doc = testcase
        if not name in peg:
            continue
        if start is not None and name != start:
            continue
        if not name in parsers:
            parsers[name] = pg.generate(peg, start=name)
        tree = parsers[name](doc.inputs_, doc.urn_, doc.spos_, doc.epos_)
        ok = doc.inputs_[doc.spos_:tree.epos_]
        fail = doc.inputs_[tree.epos_:doc.epos_]
        display(
            HTML(f'<b>{name}</b> {ok}<span style="background-color:#FFCACA;">{fail}</span>'))
        v = graph.draw_graph(tree)
        v.format = 'SVG'
        display(SVG(v.render()))


def get_parser(start, path):
    peg = pg.grammar(path)
    if start is None:
        parser = pg.generate(peg)
    else:
        parser = pg.generate(peg, start=start)
    return parser


@register_cell_magic
def peg(path_to_save: str, grammar: str):
    """display syntax trees of examples defined in a grammar of code cell

    Args:
        path_to_save (str): file to save (optional)
        grammar (str): a PegTree grammar with example
    """
    peg = pg.grammar(grammar)
    if '@@error' in peg:
        return
    test_example(peg, None)
    file = path_to_save.strip()
    if file.endswith('peg') or file.endswith('.pegtree'):
        with open(file, 'w') as f:
            f.write(grammar)
            print(f'wrote {file}')


@register_line_cell_magic
def example(line, src=''):
    start, path = start_option(line.strip())
    peg = pg.grammar(path)
    test_example(peg, start)


@register_cell_magic
def parse(line, src=''):
    start, path = start_option(line.strip())
    peg = pg.grammar(path)
    if start is None:
        parser = pg.generate(peg)
    else:
        parser = pg.generate(peg, start=start)
    tree = parser(src, urn='(stdin)')
    print(repr(tree))
    return graph.draw_graph(tree)


@register_line_cell_magic
def pegtree(grammar_file, input_string=''):
    """display a syntax tree by parsing input_string with pegtree grammar_file.

    Args:
        grammar_file (str): pegtree grammar file (e.g., math.pegtree)
        input_string (str, optional): an input string for parsing
    """
    if input_string == '':
        return example(grammar_file, input_string)
    else:
        return parse(grammar_file, input_string)


@register_line_cell_magic
def pasm(grammar_file, configuration=''):
    """pasm by converting pegtree grammar_file

    Args:
        grammar_file (str): PegTree grammar file
        configuration (str, optional): JSON-style configuration.
    """
    start, path = start_option(grammar_file.strip())
    peg = pg.grammar(path)
    from .nezcc import parsec
    if configuration != '':
        config = json.loads(configuration)
    else:
        config = {}
    parsec(peg, **config)


@register_line_cell_magic
def jsonfy(grammar_file: str, input_string: str):
    """display a json data by converting an input_string using pegtree grammar_file

    Args:
        grammar_file (str): pegtree grammar filename
        input_string (str): input string for converting

    """
    start, path = start_option(grammar_file.strip())
    parser = get_parser(start, path)
    from .visitor import JSONfy
    value = JSONfy(parser).convert(input_string)
    print(json.dumps(value, ensure_ascii=False))


@register_line_cell_magic
def jsontree(grammar_file, input_string=''):
    """display a json-encoded tree by converting an input_string using pegtree grammar_file

    Args:
        grammar_file (str): pegtree grammar filename
        input_string (str): input string for converting

    """
    start, path = start_option(grammar_file.strip())
    parser = get_parser(start, path)
    from .visitor import JSONTree
    import json
    value = JSONTree(parser).convert(input_string)
    print(json.dumps(value, ensure_ascii=False))


@register_line_cell_magic
def match(line, src):
    peg = pg.grammar(src)
    if '@error' not in peg:
        parser = pg.generate(peg)
        res = parser(line)
        print(repr(res))

# new command


def parse_option(ss):
    d = {}
    options = []
    arguments = []
    for i, s in enumerate(ss):
        if s.startswith('--'):
            if i + 1 < len(ss):
                d[s] = ss[i+1]
                options.append(ss[i+1])
            else:
                d[s] = ''
        else:
            arguments.append(s)
    for s in options:
        arguments.remove(s)
    return arguments, d


def load_grammar(files, options):
    peg = pg.grammar(files[0])
    return peg


@register_line_cell_magic
def extract(line, cell=''):
    files, options = parse_option(line.split())
    peg = load_grammar(files, options)
    start = options.get('--start', peg.start())
    start = f'extract_{start}'
    if start not in peg:
        peg.addExtract(start)
    parser = pg.generate(peg, start=start)
    file_or_text = options.get('--from', cell)
