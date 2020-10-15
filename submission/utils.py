import networkx as nx


def is_dominant(D, g):
    for n in list(set(g.nodes) - D):
        if not edge_node_graph(n, D, g):
            return False
    return True

def edge_node_graph(n, D, g):
    """Checks whether there is an edge between subgraph D of g and node n"""
    for D_node in D:
        if g.has_edge(n, D_node):
            return True
    return False
