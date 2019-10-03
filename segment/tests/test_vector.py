import networkx as nx


def test_hierarchy_level():
    g = nx.DiGraph()
    g.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4)])
    assert len(nx.ancestors(g, 3)) == 3
