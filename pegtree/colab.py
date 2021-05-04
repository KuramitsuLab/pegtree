import pegtree as pg
import pegtree.graph as graph
from IPython.display import Image, HTML, display
from IPython.core.magic import register_cell_magic, register_line_cell_magic

def parse_example(peg, line):
    if '@@example' in peg and len(peg['@@example']) > 0:
        name, doc = peg['@@example'][-1]
        parser = pg.generate(peg, start=str(name))
        return parser(str(doc))
    else:
        parser = pg.generate(peg)
        print('Input:', line)
        return parser(line)

@register_cell_magic
def TPEG(line, src):
    peg = pg.grammar(src)
    if '@error' not in peg:
        tree = parse_example(peg, line)
        if tree.isSyntaxError():
            print(repr(tree))
        else:
            print(repr(tree))
            return graph.draw_graph(tree) if tree is not None else None

@register_cell_magic
def pegtree(line, src):
    return TPEG(line, src)

@register_line_cell_magic
def example(line, src=''):
    print(line, line.strip())
    peg = pg.grammar(line.strip())
    if '@@example' not in peg:
        return
    parsers = {}
    for testcase in peg['@@example']:
        name, doc = testcase
        if not name in peg:
            continue
        if not name in parsers:
            parsers[name] = pg.generate(peg, start=name)
        res = parsers[name](doc.inputs_, doc.urn_, doc.spos_, doc.epos_)
        ok = doc.inputs_[doc.spos_:res.epos_]
        fail = doc.inputs_[res.epos_:doc.epos_]
        display(HTML(f'<b>{name}</b> {ok}<span style="background-color:#FFCACA;">{fail}</span>'))
        v = graph.draw_graph(tree)
        display(Image(v.render()))

@register_cell_magic
def parse(line, src='None'):
    peg = pg.grammar(line.strip())
    parser = pg.generate(peg)
    tree = parser(src, urn='(stdin)')
    print(repr(tree))
    return graph.draw_graph(tree)

@register_line_cell_magic
def match(line, src):
    peg = pg.grammar(src)
    if '@error' not in peg:
        parser = pg.generate(peg)
        res = parser(line)
        print(repr(res))

