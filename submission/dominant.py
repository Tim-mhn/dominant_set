import sys, os, time
import networkx as nx
import logging
from dfs_dominant import dfs_dominant
from dominant_glouton import dominant_glouton
from topk_glutton import topk_glutton

LOG_LEVEL = logging.INFO

logging.basicConfig(format='%(message)s',level=LOG_LEVEL)
logger = logging.getLogger(__name__)



# def arg_max_new_connections(D, g):

#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__=="__main__":
    total_count = 0
    start = time.time()
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])

    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
	    print(input_dir, "doesn't exist")
	    exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
	    print(input_dir, "doesn't exist")
	    exit() 

    # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))             
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    for i, graph_filename in enumerate(sorted(os.listdir(input_dir))):
        print(f"------------------ {graph_filename}-------------------- \r\n\r\n")
        graph_start = time.time()
        # importer le graphe
        g = nx.read_adjlist(os.path.join(input_dir, graph_filename))
        # calcul du dominant
        D = sorted(topk_glutton(g), key=lambda x: int(x))
        print(f"Result: {len(D)}  |  D={D}")

        if "100" in graph_filename:
            total_count += len(D)

        # ajout au rapport
        output_file.write(graph_filename)
        for node in D:
            output_file.write(' {}'.format(node))
        output_file.write('\n')
        graph_dur = time.time() - graph_start
        logger.info(f"Graph {i+1} completed in {graph_dur}s\r\n\r\n")

    end = time.time()
    print(f"Total count: {total_count} Total time : {end-start} s")
    output_file.close()
