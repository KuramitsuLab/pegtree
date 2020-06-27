import string
from pegtree.pasm import ParseTree


def make_graph(t: ParseTree, nodes, edges, c):
    es = []
    for i, child in enumerate(t):
        es.append((child.spos_, child, i))
    for key in t.keys():
        child = t.get(key)
        es.append((child.spos_, child, key))
    es.sort()
    if len(es) > 0:
        parentId = c
        nodes.append((parentId, t.getTag(), None))
        for i, e in enumerate(es):
            _, child, edge = e
            childId = c+1
            c = make_graph(child, nodes, edges, childId)
            edges.append((parentId, childId, edge))
        return c
    if t != '':
        nodes.append((parentId, t.getTag(), None))
        edges.append((parentId, parentId+1, None))
        nodes.append((parentId+1, None, str(t)))
        return parentId+1
    nodes.append((c, None, str(t)))
    return c

# dot


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


'''
def bottom_check(s):
    for c in s:
        if unicodedata.east_asian_width(c) in ['W', 'F', 'H']:
            return ', labelloc = "bottom"'
    return ''


def make_dot(nodes, edges, t: ParseTree, idc: int):
    tid = idc
    for i, child in enumerate(t):
        idc = make_dot(nodes, edges, child, idc)
        edge = f'n{tid} -> n{idc}   [label="[{0}]"]'
        edges.append(edge)
        hasContent = True
    for key in t.keys():
        idc = make_dot(nodes, edges, t.get(key), idc)
        edge = f'n{tid} -> n{idc}   [label="{key}"]'
        edges.append(edge)
        hasContent = True
    if not hasContent:
        node = f'n{tid} [label="#{t.getTag()}"]'
        nodes.append(node)
        idc = tid+1
        node = f'n{idc} [label="#{t.getTag()}"]'
        edge = f'n{tid} -> n{idc}'
        edges.append(edge)
    return idc
      d['node'].append(f'n{nid} [label="#{t.tag}"]')
       if len(t.subs()) == 0:
            leaf = str(t)
            d['node'].append(
                f'n{nid}_0 [label="{escape(leaf)}"{bottom_check(leaf)}]')
            d['edge'].append(f'n{nid} -> n{nid}_0')
        else:
            for i, (fst, snd) in enumerate(t.subs()):
                label=f' [label="{fst}"]' if fst != '' else ''
                d['edge'].append(f'n{nid} -> n{nid}_{i}{label}')
                make_dot(snd, d, f'{nid}_{i}')
'''


def dot_node(nodeId, tag, token):
    if tag is not None:
        label = f'[label="#{tag}"]'
    else:
        label = f'[label={dot_quote(token)}]'
    return f'n{nodeId} {label}'


def dot_edge(parentId, childId, edge):
    if edge == None:
        label = ''
    else:
        if isinstance(edge, int):
            edge = f'[{edge}]'
        label = f'[label={dot_quote(edge)}]'
    return f'n{parentId} -> n{childId}  {label}'


DOTESC = str.maketrans(
    {'\n': '\\n', '\t': '\\t', '\r': '\\r', '\v': '\\v', '\f': '\\f',
     '\\': '\\\\', "'": "\\'"})


def dot_quote(s):
    return '"' + s.translate(DOTESC) + '"'


def dot(t: ParseTree):
    nodes = []
    edges = []
    make_graph(t, nodes, edges, 0)
    context = {
        'input_text': dot_quote(t.inputs),
        'node_description': ';\n    '.join([dot_node(*x) for x in nodes]),
        'edge_description': ';\n    '.join([dot_edge(*x) for x in nodes]),
    }
    return string.Template(DOT).substitute(context)


def synttree(t, fmt='\\synttree{{1}}{}'):
    sb = []
    sb.append(f'[\\Tag{{{t.getTag()}}}')
    subs = t.subs()
    if len(subs) > 0:
        for _, sub in subs:
            #sb.append(' ')
            sb.append(synttree(sub, None))
    else:
        #sb.append(' ')
        sb.append(f'[\\Token{{{str(t)}}}]')
    sb.append(']')
    s = ' '.join(sb)
    return s if fmt is None else fmt.format(s)


def qtree(t, fmt='\\Tree {}'):
    sb = []
    sb.append(f'[.\\Tag{{{t.getTag()}}}')
    subs = t.subs()
    if len(subs) > 0:
        c = -(len(subs)+1)//2
        for label, sub in subs:
            if label != '':
                pos = 'left' if c <= 0 else 'right'
                sb.append(f'\\edge node[midway,{pos}]{{\\Edge{{{label}}}}};')
            sb.append(qtree(sub, None))
            c += 1
    else:
        #sb.append(' ')
        sb.append(f'\\Token{{{str(t)}}}')
    sb.append(']')
    s = ' '.join(sb)
    return s if fmt is None else fmt.format(s)

import pegtree.cj as cj 
def cjdump(tree):
    s = repr(tree)
    tokens = cj.tokenize(tree)
    return s + '\n' + repr(tokens)

def treedump(options, dump):
    ext = options.get('format')
    if ext == 'dot':
        return dot
    if ext == 'qtree':
        return qtree
    if ext == 'synttree' or ext == 'syntree':
        return synttree
    if ext == 'cj':
        return cjdump
    return dump
