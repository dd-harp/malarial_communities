import logging

import networkx as nx
from networkx.algorithms.flow import shortest_augmenting_path

LOGGER = logging.getLogger(__name__)


def _set_group(graph, nodes, parent_id):
    for n in nodes:
        graph.nodes[n]["group"] = parent_id


def split_graph(flow_graph, maximum_node_count):
    """
    Given a graph, splits it hierarchically until every piece
    is smaller than the given maximum node count.
    This uses an algorithm from networkx called "minimum edge cut."
    It uses a depth-first search for subgraphs.

    Args:
        flow_graph (nx.Graph): Has flows on edges.
        maximum_node_count (int): No subgraph should be larger than this.

    Returns:
        (nx.Graph, nx.DiGraph): The original graph, marking which nodes belong
                                to which subgraphs, and a tree of which
                                subgraphs have which parents.

    """
    work = list()
    belonging_tree = nx.DiGraph()
    group_cnt = 1
    for parent_component in nx.connected_components(flow_graph):
        belonging_tree.add_node(group_cnt)
        _set_group(flow_graph, parent_component, group_cnt)
        work.append([parent_component, group_cnt])
        group_cnt += 1
    if len(work) > 1:
        LOGGER.info(f"There are {len(work)} connected components at the start.")

    while work:
        parent_component, parent_id = work.pop()
        parent_graph = nx.Graph(flow_graph.subgraph(parent_component))
        remove_edges = nx.minimum_edge_cut(
            parent_graph,
            flow_func=shortest_augmenting_path,
        )
        parent_graph.remove_edges_from(remove_edges)

        for child_component in nx.connected_components(parent_graph):
            _set_group(flow_graph, child_component, group_cnt)
            belonging_tree.add_edge(group_cnt, parent_id)
            if len(child_component) > maximum_node_count:
                work.append([child_component, group_cnt])
            group_cnt += 1
    return flow_graph, belonging_tree


def save_pandas(graph, hierarchy, output_file):
    df = nx.to_pandas_adjacency(graph)
    df.to_hdf(str(output_file), "graph", mode="a", format="fixed")
    tree = nx.to_pandas_adjacency(hierarchy)
    tree.to_hdf(str(output_file), "belonging", mode="a", format="fixed")
