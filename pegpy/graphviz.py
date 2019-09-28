import sys
from pathlib import Path
import re
import unicodedata
import subprocess
import shutil


def parse_ast(ast_str):
    class AST():
        def __init__(self, s, p):
            self.s = s
            self.pos = p

    class Tree():
        def __init__(self, tag_str, node_id, nodes_list, label_str):
            self.name = tag_str
            self.nid = node_id
            self.node = nodes_list
            self.label = label_str

    class Leaf():
        def __init__(self, inner_str, leaf_id):
            self.name = inner_str
            self.nid = leaf_id

    def get_tree(ast, nid, label):
        require(ast, '[')
        tag = get_tag(ast)
        ast.pos += 1
        node = get_node(ast, f'{nid}')
        require(ast, ']')
        return Tree(tag, nid, node, label)

    def get_node(ast, nid):
        node = []
        if ast.s[ast.pos:].startswith('\''):
            return [get_leaf(ast, f'{nid}_0')]
        label = get_label(ast)
        if ast.s[ast.pos:].startswith('['):
            while ast.s[ast.pos] != ']':
                inner = get_tree(ast, f'{nid}_{len(node)}', label)
                node.append(inner)
                if ast.s[ast.pos] == ' ':
                    ast.pos += 1
                    label = get_label(ast)
            return node
        else:
            print(f'pos:{ast.pos} don\'t start with "\'" or "["')
            sys.exit()

    def get_leaf(ast, nid):
        require(ast, '\'')
        name = ''
        while not ast.s[ast.pos:].startswith('\']'):
            name += escape(ast.s[ast.pos])
            ast.pos += 1
        require(ast, '\'')
        return Leaf(name, nid)

    def get_tag(ast):
        tag = ''
        while ast.s[ast.pos] != ' ':
            tag += ast.s[ast.pos]
            ast.pos += 1
        return tag

    def get_label(ast):
        label = 'None'
        label_match = re.match('[a-zA-Z0-9_]+=\[#', ast.s[ast.pos:])
        if label_match:
            label = label_match.group()[:-3]
            ast.pos += len(label) + 1
        return label

    def escape(s):
        after = ''
        META_LITERAL = ['\\', '"']
        for c in s:
            if c in META_LITERAL:
                after += f'\\{c}'
            else:
                after += c
        return after

    def require(ast, target):
        if ast.s[ast.pos:].startswith(target):
            ast.pos += len(target)
        else:
            print(f'pos:{ast.pos} don\'t match with {target}')
            sys.exit()

    def make_dict(tree, d):
        if isinstance(tree, Tree):
            for n in tree.node:
                label = n.label if isinstance(n, Tree) else ''
                d[str(n.nid)] = {'tag': n.name, 'parent': tree.nid, 'label': label}
                make_dict(n, d)

    ast = AST(ast_str, 0)
    tree = get_tree(ast, 0, 'top')
    d = {}
    d[str(tree.nid)] = {'tag': tree.name, 'parent': '', 'label': tree.label}
    make_dict(tree, d)
    return d


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
        '%s\n'
        '%s'
        '}' % (s, node, edge))


def gen_dot(input_str, d):
    def_node = ''
    def_edge = ''
    for k, v in d.items():
        bt = ''
        for c in v["tag"]:
            if unicodedata.east_asian_width(c) in ['W', 'F', 'H']:
                bt = ', labelloc = "bottom"'
                break
        label = '' if v["label"] == '' else f' [label = "{v["label"]}"]'
        def_node += f'    n_{k} [label = "{v["tag"]}"{bt}];\n'
        def_edge += '' if v["parent"] == '' else f'    n_{v["parent"]} -> n_{k}{label};\n'
    return template(input_str, def_node, def_edge)


def gen_graph(input_str, ast_str):
    GEN_DOT_PATH = '.temp.dot'
    if not shutil.which('dot'):
        print('Not find "dot" command')
        print('Please install "Graphviz"')
        sys.exit()
    with open(GEN_DOT_PATH, mode='w', encoding='utf_8') as f:
        f.write(gen_dot(input_str, parse_ast(ast_str)))
    cmd = ['dot', '-Tpng', GEN_DOT_PATH, '-o', f'graph.png']
    res = subprocess.call(cmd)
    if res != 0:
        Path(GEN_DOT_PATH).rename(f'.erred.dot')
    Path(GEN_DOT_PATH).unlink()


# <Test>
# txt = 'number = 123'
# ast = '[#Test14 left=[#Var \'number\'] right=[#Num \'123\']]'
# gen_graph(txt, ast)
