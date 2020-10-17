# dominant_set
Algorithms to find a dominant set from a graph (using Python Networkx)
https://networkx.github.io/documentation/stable/index.html

### Pick your algorithm
Pick either regular glutton, topk_glutton or dfs_glutton by changing line 47 of dominant.py file

- dominant_glutton: at each step, add node that brings the most new connections
- topk_glutton: same as previous but select the K best candidates at each step. Possibility to look-up deeper if they are even candidates on the edge of selection
- dfs_glutton: Depth-first search (only runnable for small graphs, < 20 nodes)


### Run a test : sh run.sh
