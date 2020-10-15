# from utils import is_dominant, edge_node_graph
import networkx as nx
import time
import sys
MAX_STEP = 750
step = 0
FORCE_STOP = False ## force stop after max steps even if no dominant found
GLOUTON_MAX_STEP_RATIO = .3

def dfs_ft_glouton_dominant(g):
    print(f"Starting DFS+Glouton Dominant")
    global step
    step = 0
    start = time.time()
    all_nodes = list(map(lambda node_str: int(node_str), g.nodes))
    # all_nodes = glouton_sort(g, [], all_nodes, all_nodes)

    glouton_subset = get_glouton_subset(g)
    best = sys.maxsize
    best_dominant = None
    candidate_subsets = [[n] for n in all_nodes]
    best, best_dominant = find_best_dominant(g, candidate_subsets, best, best_dominant, all_nodes)
    end = time.time()

    # test is_dominant
    # candidat = [49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 3, 2, 1, 0]
    # print(is_dominant(candidat, g, all_nodes))


    print(f"Finished DFS. Took {end-start} s to complete")
    print(f"New best = {best} with {best_dominant}")
    best_dominant = list(map(lambda node_int: str(node_int), best_dominant))
    return best_dominant

def find_best_dominant(g, candidate_subsets, best, best_dominant, all_nodes):
    """
    g : non oriented graph
    candidates : list of subsets of g (list of sets)
    """
    global step
    step += 1
    
    if step > MAX_STEP and (best_dominant or FORCE_STOP):
        return best, best_dominant
    for i, subset in enumerate(candidate_subsets):
        to_print = False

        # If subset has more elements than best current dominant, it's not worth looking into it => it won't be the best dominant
        if len(subset) < best:
            t0 = time.time()
            if is_dominant(subset, g, all_nodes):
                # If it's dominant, we update the current best values (minimum number of nodes for a dominant subset)
                if to_print:
                    print(f"[is_dominant]  step {step}: {time.time() - t0}")
                best = len(subset)
                best_dominant = subset
                print(f"New best : {best} {best_dominant}")

            else:
                # Otherwise we create a new list of candidates by adding nodes to the subset
                # Recursively, we find the best dominant among these new candidate subsets
                t0 = time.time()
                nodes_can_add  = get_next_nodes(g, subset, all_nodes)
                nodes_can_add = glouton_sort(g, subset, nodes_can_add, all_nodes)
                if to_print:
                    print(f"Subset: {subset} -- Potential new nodes: {nodes_can_add}")
                    print(f"[get_next_nodes]: {time.time() - t0}")

                if len(nodes_can_add) > 0:
                    # If there no nodes that can be added to subset, stop recursion (eg if subset = g.nodes we can't add anymore node)
                    next_subsets = [ subset + [n] for n in nodes_can_add]
                    t0 = time.time()
                    best, best_dominant = find_best_dominant(g, next_subsets, best, best_dominant, all_nodes)
                    if to_print:
                        print(f"[find_best_dominant]  step {step}: {time.time() - t0}")

    return best, best_dominant
def get_next_nodes(g, subset, all_nodes):
    """ we only add nodes that are inferior to last node of subset """
    # last_node = subset[-1]
    # return list(filter(lambda n: n < last_node, all_nodes))
    return set(all_nodes) - set(subset)


def is_dominant(subset, g, all_nodes):
    for n in list(set(all_nodes) - set(subset)):
        if not edge_node_graph(n, subset, g):
            return False
    return True

def edge_node_graph(n, subset, g):
    """Checks whether there is an edge between subgraph D of g and node n"""
    for subset_node in subset:
        n = str(n)
        subset_node = str(subset_node)
        if g.has_edge(subset_node, n):
            return True
    return False

def glouton_sort(g, subset, nodes_can_add, all_nodes):
    """
    Sort potential new nodes by comparing how many new connections they add
    """
    iso_nodes = get_iso_nodes(g, subset, all_nodes)
    max_new_nodes = 0
    new_node = None

    node_new_conn_dic = dict()

    for n in set(all_nodes) - set(subset):
        new_nodes = count_new_nodes(n, g, iso_nodes)

        # if new_nodes > max_new_nodes:
        #     new_node = n
        node_new_conn_dic[n] = new_nodes

    sorted_nodes = [node for (node, new_conn) in sorted(node_new_conn_dic.items(), key=lambda x: x[1], reverse=True)]
    return sorted_nodes

def get_iso_nodes(g, subset, all_nodes):
    """
    Get list of isolated nodes from sub-ensemble D of graph g
    """
    iso_nodes = set()

    for n in set(all_nodes) - set(subset):
        connected = False
        for D_node in all_nodes:
            if g.has_edge(str(n), str(D_node)):
                connected = True
                break

        if not connected:
            iso_nodes.add(n)

    return iso_nodes

def count_new_nodes(root, g, nodes):
    """ Count number of nodes connected to node n in g"""
    new_connections = 0
    for n in nodes:
        if g.has_edge(str(n), str(root)):
            new_connections += 1
    return new_connections


# def get_glouton_subset(g):
#     """ 
#     Step #1 of algo: get an initial subset with glouton algo with a limited size
#     If it's not dominant, DFS will be used to make a dominant one starting from this
