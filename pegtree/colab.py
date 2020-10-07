import pegtree as pg
import pegtree.graph as graph
from IPython.core.magic import register_cell_magic


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
      return graph.Viz(res) if res is not None else None
