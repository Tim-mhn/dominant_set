"""
A smarter glutton algorithm for dominant with strict comparison between next node to add
Eg: if there are several nodes that connect as many new connections, search deeper into each node and find what is the best path (recursive)
"""

import sys, os, time
import networkx as nx
import itertools
KTOP = 5 # Pick the ktop best new nodes and search deeper

def topk_glutton(g):
    """
        A Faire:         
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

    """
    empty_D = list()

    list_D = [empty_D] # List of tuples (u,v) where u=subset, v = number of isolated nodes

    dominant = find_dominant(list_D, g)
    while not dominant:
        subsets = list()
        for D in list_D:
            # Get k best subset from D. Add them to list of all subsets
            subsets += _topk_subsets(D, g)
            # #print(f"Subsets: {subsets}")
            #print(f"{len(subsets)} Subsets: {subsets}")

        # Sort subsets by number of isolated nodes (ascending order)
        try:
            subsets = sorted(subsets, key=lambda tup: tup[1])
        except Exception:
            #print(f"Subsets: {subsets}")
            raise ValueError("e")
        # Keep the TOPK best subsets (with least number of isolated nodes)
        subsets = subsets[:KTOP]
        list_D = list(map(lambda s: list(s[0]), subsets))
        dominant = find_dominant(list_D, g)

    # #print(f"Finished with {len(D)} with {D}")
    return dominant

def find_dominant(list_D, g):
    """
    Check if one of the subset in list_D is dominant.
    Return first dominant if it exists
    Return false otherwise
    """
    #print(f"List_D: {list_D}")
    for D in list_D:
        if is_dominant(D, g):
            return D
    return False

def _topk_subsets(D, g):
    notin_D = set(g.nodes) - set(D)
    #print(f"Ntin D : {notin_D}")
    # Subset candidates created from D
    D_candidates = list(map(lambda n : D + [n], notin_D))
    #print(f"D_candidates : {list(D_candidates)}")
    # List of tuples (u,v) with u: subset candidate / v: number of iso nodes
    D_candidates = list(map(lambda D_cand: (D_cand, len(get_iso_nodes(D_cand, g))), D_candidates))
    # # #print(f"D_candidates : {list(D_candidates)}")
    # Sort and keep KTOP best subsets
    D_candidates = sorted(D_candidates, key=lambda tup: tup[1])
    topk_subsets = D_candidates[:KTOP]
    #print(f"topk_subsets {topk_subsets}")
    # Return only 1st element of tuple = subset (and not number of iso nodes)
    return topk_subsets

def is_dominant(D, g):
    try:
        for n in set(g.nodes) - set(D):
            if not edge_node_graph(n, D, g):
                return False
    except TypeError:
        #print(f"Error caused by D : {D}")
        raise ValueError("error")
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

    for n in set(g.nodes) - set(D):
        new_nodes = count_new_nodes(n, g, iso_nodes)

        if new_nodes > max_new_nodes:
            new_node = n
        # elif new_nodes == max_new_nodes:
            # #print(f"Same new connections for {n} and {new_node}")

    return new_node

def get_iso_nodes(D, g):
    """
    Get list of isolated nodes from sub-ensemble D of graph g
    """
    iso_nodes = list()

    for n in set(g.nodes) - set(D):
        connected = False
        for D_node in D:
            if g.has_edge(n, D_node):
                connected = True
                break

        if not connected:
            iso_nodes.append(n)

    return iso_nodes

def count_new_nodes(root, g, nodes):
    """ Count number of nodes connected to node n in g"""
    new_connections = 0
    for n in nodes:
        if g.has_edge(n, root):
            new_connections += 1
    return new_connections