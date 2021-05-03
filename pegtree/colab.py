import pegtree as pg
import pegtree.graph as graph
from IPython.core.magic import register_cell_magic

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

@register_cell_magic
def match(line, src):
    peg = pg.grammar(src)
    if '@error' not in peg:
        parser = pg.generate(peg)
        res = parser(line)
        print(repr(res))


@register_cell_magic
def parse(line, src):
    peg = pg.grammar(src)
    if '@error' not in peg:
        parser = pg.generate(peg)
        res = parser(line)
        if res.isSyntaxError():
            print(repr(res))
        else:
            print(repr(res))
            return graph.draw_graph(res) if res is not None else None
