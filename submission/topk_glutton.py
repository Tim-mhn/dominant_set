"""
A smarter glutton algorithm for dominant with strict comparison between next node to add
Eg: if there are several nodes that connect as many new connections, search deeper into each node and find what is the best path (recursive)
"""

import sys, os, time
import networkx as nx
import itertools
import logging
KTOP = 6 # Pick the ktop best new nodes and search deeper
MAX_DEPTH = 0
LOG_LEVEL = logging.INFO

logging.basicConfig(format='%(message)s',level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def topk_glutton(g):
    """
        A Faire:
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

    """
    empty_D = list()

    D_subsets = [empty_D] # List of tuples (u,v) where u=subset, v = number of isolated nodes

    dominant = _find_dominant(D_subsets, g)
    while not dominant:
        top_candidates = list()
        for D in D_subsets:
            # Get k best subset from D. Add them to list of all subsets
            logger.debug(f"Topk candidates called in main function. D={D}")
            top_candidates += _topk_candidates(D, g)

        # Sort subsets by number of isolated nodes (ascending order)
        top_candidates = sorted(top_candidates, key=lambda tup: tup[1])

        top_candidates = top_candidates[:KTOP]
        D_subsets = list(map(lambda s: list(s[0]), top_candidates))
        dominant = _find_dominant(D_subsets, g)

    return dominant

def _find_dominant(list_D, g):
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

def _topk_candidates(D, g, depth=0, max_depth=MAX_DEPTH):
    """
    From a subset D, get the list of candidates=(subset, iso_nodes_count).
    If they are even candidates, allow to look deeper in graph w.r.t MAX_DEPTH
    """
    logger.debug(f"_topk_subsets: depth={depth}, D={D}")
    notin_D = set(g.nodes) - set(D)
    # Subset candidates created from D
    D_candidates = list(map(lambda n : D + [n], notin_D))
    # List of tuples (u,v) with u: subset candidate / v: number of iso nodes
    D_candidates = list(map(lambda D_cand: (D_cand, len(get_iso_nodes(D_cand, g))), D_candidates))
    # Sort and keep KTOP best candidates
    D_candidates = _keep_topk(D_candidates, g, depth, max_depth)
    return D_candidates

def _keep_topk(D_candidates, g, depth=0, max_depth=MAX_DEPTH):
    """
    Keep only KTOP best subset candidates.
    If there are equal candidates on the edge of KTOP, go deeper to find best candidates
    """
    D_candidates = sorted(D_candidates, key=lambda tup: tup[1])
    # If we have less or equal candidates as KTOP, return all candidates
    try:
        edge_score = D_candidates[KTOP][1]
    except IndexError:
        return D_candidates

    if edge_score == D_candidates[KTOP-1][1] and depth<max_depth:
        logger.debug(f"_keep_top called. Lookup deeper with d={depth} and max_depth={max_depth}")
        # First candidate with same edge_score
        first = next((cand for cand in D_candidates if cand[1] == edge_score))

        first_index, equal_candidates = _equal_score_candidates(edge_score, D_candidates)

        logger.debug(f" {len(equal_candidates)} even candidates: {equal_candidates}")

        deeper_candidates = list()
        for cand in equal_candidates:
            # Transform candidate (subset, #iso) into subset
            subset = cand[0]
            topk_candidates = _topk_candidates(subset, g, depth+1, max_depth)
            deeper_candidates.append(topk_candidates[0])

        available_spots = KTOP - first_index
        # Sort by Isolated nodes value
        deeper_candidates = sorted(deeper_candidates, key=lambda tup: tup[1])
        deeper_candidates = deeper_candidates[:available_spots]
        deeper_candidates = list(map(lambda c: list(c), deeper_candidates))

        # Remove the last node that we added (since we looked-up one level deeper to decide)
        for deeper_cand in deeper_candidates:
            deeper_cand[0].pop()

        # Top subsets are the first ones + some among the even candidates
        topk_subsets = D_candidates[:first_index] + deeper_candidates
        return topk_subsets

    else:
        logger.debug(f"_keep_topk entered ELSE part with {D_candidates}")
        toreturn = D_candidates[:KTOP]
        logger.debug(f"returning {toreturn}")
        return toreturn


def _equal_score_candidates(edge_score, D_candidates):
    # Get candidates with score = edge_score 
    # D_candidates is already sorted
    equal_candidates =  list()
    first_index = None
    for idx, cand in enumerate(D_candidates):
        if cand[1] == edge_score:
            equal_candidates.append(cand)
            # Index of first matching candidate
            first_index = idx if not first_index else first_index

        elif cand[1] > edge_score:
            # As soon as we  find candidate with superior score, we return list as weve found all equal candidaates (sorted list)
            return first_index, equal_candidates
    return first_index, equal_candidates


def is_dominant(D, g):
    """ Returns if D is dominant-subset of g """
    for n in set(g.nodes) - set(D):
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

    for n in set(g.nodes) - set(D):
        new_nodes = count_new_nodes(n, g, iso_nodes)

        if new_nodes > max_new_nodes:
            new_node = n

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