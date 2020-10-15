import sys, os, time
import networkx as nx
from dfs_dominant import dfs_dominant
from dominant_glouton import dominant_glouton





# def arg_max_new_connections(D, g):

#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__=="__main__":
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
        if i > -1:
            # break
            print(f"------------------ {graph_filename}-------------------- \r\n\r\n")
            # importer le graphe
            g = nx.read_adjlist(os.path.join(input_dir, graph_filename))
            
            # calcul du dominant
            D = sorted(dominant_glouton(g), key=lambda x: int(x))

            # ajout au rapport
            output_file.write(graph_filename)
            for node in D:
                output_file.write(' {}'.format(node))
            output_file.write('\n')
            print(f"------------------ END OF Step {i+1}-------------------- \r\n\r\n")

        # if i > 15:
        #     break
    end = time.time()
    print(f"Total time : {end-start} s")
    output_file.close()
