from pegtree.pasm import ParseTree

try:
  from graphviz import Digraph
  is_graphviz_avaiable = True
except ModuleNotFoundError:
  is_graphviz_avaiable = False


class GenId(object):
  def __init__(self):
    self.c = 0

  def gen(self):
    self.c += 1
    return self.c


def draw_node(g, t, c):
  nid = c.gen()
  nodeid = f'n{nid}'
  g.node(nodeid, label=f'#{t.getTag()}')
  es = []
  for i, child in enumerate(t):
    es.append((child.spos_, child, i))
  for key in t.keys():
    child = t.get(key)
    es.append((child.spos_, child, key))
  es.sort()
  if len(es) == 0:
    childid = f'c{nid}'
    g.node(childid, label=repr(t.getToken()), shape='rectangle')
    g.edge(nodeid, childid)
  else:
    for i, e in enumerate(es):
      _, child, edge = e
      childid = draw_node(g, child, c)
      g.edge(nodeid, childid, label=f'{edge}')
  return nodeid


def draw_graph(ptree: ParseTree, name='G'):
  if is_graphviz_avaiable == False:
    print('Install graphviz FIRST')
    return
  g = Digraph(name, format='png')
  g.attr('node', fontname='MS Gothic')
  g.attr('edge', fontname='MS Gothic')
  draw_node(g, ptree, GenId())
  #g.view()
  return g

def Viz(tree_or_parser):
  if isinstance(tree_or_parser, ParseTree):
    return draw_graph(tree_or_parser)
  return lambda s: draw_graph(tree_or_parser(s))
