import networkx as nx
import pandas as pd
import pytest

from segment.communities import split_graph, save_pandas


def test_happy_path():
    g = nx.barbell_graph(6, 1)
    for add_capacity in g.nodes:
        g.nodes[add_capacity]["capacity"] = 1
    labeled, hierarchy = split_graph(g, 8)
    assert len(hierarchy) == 3
    assert (2, 1) in hierarchy.edges
    assert (3, 1) in hierarchy.edges
    for n in labeled.nodes:
        assert labeled.nodes[n]["group"] in {2, 3}
        print(f"node {n} label {labeled.nodes[n]['group']}")
    print(nx.to_edgelist(hierarchy))


def test_larger():
    g = nx.fast_gnp_random_graph(100, 0.2)
    for add_capacity in g.nodes:
        g.nodes[add_capacity]["capacity"] = 1
    labeled, hierarchy = split_graph(g, 8)
    print(nx.to_edgelist(hierarchy))


@pytest.mark.skip("not working yet")
def test_save(tmp_path):
    g = nx.barbell_graph(6, 1)
    for add_capacity in g.nodes:
        g.nodes[add_capacity]["capacity"] = 1
    labeled, hierarchy = split_graph(g, 8)
    filename = tmp_path / "example.h5"
    save_pandas(labeled, hierarchy, filename)

    g2 = nx.from_pandas_adjacency(pd.read_hdf(str(filename), key="graph"))
    assert g2.nodes[3]["group"] in {2, 3}
    h2 = nx.from_pandas_adjacency(pd.read_hdf(str(filename), key="belonging"))
    assert len(h2) == 3
