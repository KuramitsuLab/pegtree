import sys
from pathlib import Path
import unicodedata
import subprocess
import shutil


def template(s, node, edge):
    return (
        'digraph sample {\n'
        '    graph [\n'
        '        charset = "UTF-8",\n'
        '        label = "%s",\n'
        '        labelloc = t,\n'
        '        fontsize = 18,\n'
        '        dpi = 300,\n'
        '    ];\n\n'
        '    edge [\n'
        '        dir = none,\n'
        '        fontname = "MS Gothic",\n'
        '        fontcolor = "#252525",\n'
        '        fontsize = 12,\n'
        '    ];\n\n'
        '    node [\n'
        '        shape = box,\n'
        '        style = "rounded,filled",\n'
        '        color = "#3c3c3c",\n'
        '        fillcolor = "#f5f5f5",\n'
        '        fontname = "MS Gothic",\n'
        '        fontsize = 16,\n'
        '        fontcolor = "#252525",\n'
        '    ];\n\n'
        '    %s\n\n'
        '    %s\n'
        '}' % (s, node, edge))


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
    node_code = ';\n    '.join(d['node'])
    edge_code = ';\n    '.join(d['edge'])
    return template(escape(t.inputs), node_code, edge_code)


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

