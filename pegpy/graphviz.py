import sys
from pathlib import Path
import unicodedata
import subprocess
import shutil
import string


DOT = '''\
digraph sample {
    graph [
        charset = "UTF-8",
        label = "$input_text",
        labelloc = t,
        fontsize = 18,
        dpi = 300,
    ];

    edge [
        dir = none,
        fontname = "MS Gothic",
        fontcolor = "#252525",
        fontsize = 12,
    ];

    node [
        shape = box,
        style = "rounded,filled",
        color = "#3c3c3c",
        fillcolor = "#f5f5f5",
        fontname = "MS Gothic",
        fontsize = 16,
        fontcolor = "#252525",
    ];

    $node_description

    $edge_description
}'''


def escape(s):
        after = ''
        META_LITERAL = ['\\', '"']
        for c in s:
            if c in META_LITERAL:
                after += f'\\{c}'
            else:
                after += c
        return after


def bottom_check(s):
        for c in s:
            if unicodedata.east_asian_width(c) in ['W', 'F', 'H']:
                return ', labelloc = "bottom"'
        return ''


def make_dict(t, d, nid):
    d['node'].append(f'n{nid} [label="#{t.tag}"]')
    if len(t.subs()) == 0:
        leaf = str(t)
        d['node'].append(f'n{nid}_0 [label="{escape(leaf)}"{bottom_check(leaf)}]')
        d['edge'].append(f'n{nid} -> n{nid}_0')
    else:
        for i, (fst, snd) in enumerate(t.subs()):
            label = f' [label="{fst}"]' if fst != '' else ''
            d['edge'].append(f'n{nid} -> n{nid}_{i}{label}')
            make_dict(snd, d, f'{nid}_{i}')


def gen_dot(t):
    d = {'node': [], 'edge': []}
    make_dict(t, d, 0)
    context = {
        'input_text': escape(t.inputs),
        'node_description': ';\n    '.join(d['node']),
        'edge_description': ';\n    '.join(d['edge']),
    }
    return string.Template(DOT).substitute(context)


def gen_graph(parse_tree):
    GEN_DOT_PATH = '.temp.dot'
    if not shutil.which('dot'):
        print('Not find "dot" command')
        print('Please install "Graphviz"')
        sys.exit()
    with open(GEN_DOT_PATH, mode='w', encoding='utf_8') as f:
        f.write(gen_dot(parse_tree))
    cmd = ['dot', '-Tpng', GEN_DOT_PATH, '-o', f'graph.png']
    res = subprocess.call(cmd)
    if res != 0:
        Path(GEN_DOT_PATH).rename(f'.erred.dot')
    else:
        Path(GEN_DOT_PATH).unlink()


# if __name__ == "__main__":
#     from pegpy.main import *
#     options = parse_options(['-g', 'math.tpeg'])
#     peg = load_grammar(options)
#     parser = generator(options)(peg, **options)
#     s = '12+34*56/2'
#     gen_graph(parser(s))
