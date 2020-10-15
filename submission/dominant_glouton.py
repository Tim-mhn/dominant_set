import sys, os, time
import networkx as nx

def dominant_glouton(g):
    """
        A Faire:         
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

    """
    D = set()

    while not is_dominant(D, g):
        n = min_isolated_nodes(D, g)
        D.add(n)

    print(f"Finished with {len(D)} with {D}")
    return D

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

def min_isolated_nodes(D, g):
    """
    Returns next node to add to D to minimize number of isolated nodes from D
    """
    iso_nodes = get_iso_nodes(D, g)
    max_new_nodes = 0
    new_node = None

    for n in set(g.nodes) - D:
        new_nodes = count_new_nodes(n, g, iso_nodes)

        if new_nodes > max_new_nodes:
            new_node = n

    return new_node

def get_iso_nodes(D, g):
    """
    Get list of isolated nodes from sub-ensemble D of graph g
    """
    iso_nodes = set()

    for n in set(g.nodes - D):
        connected = False
        for D_node in D:
            if g.has_edge(n, D_node):
                connected = True
                break

        if not connected:
            iso_nodes.add(n)

    return iso_nodes

def count_new_nodes(root, g, nodes):
    """ Count number of nodes connected to node n in g"""
    new_connections = 0
    for n in nodes:
        if g.has_edge(n, root):
            new_connections += 1
    return new_connections