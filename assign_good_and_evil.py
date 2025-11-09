'''
from dsc40graph import UndirectedGraph
from collections import deque

def assign_good_and_evil(graph):
    """
    Determines if a graph can be 2-colored ('good' and 'evil') such that
    no two adjacent nodes have the same color.
    
    If possible, returns a dictionary mapping nodes to 'good' or 'evil'.
    If not possible (i.e., the graph is not bipartite), returns None.
    """
    
    # This dictionary will store the label ('good' or 'evil') for each node
    # It also serves as our "visited" set.
    labels = {}
    
    # We must loop through all nodes in the graph to handle
    # disconnected components (like 'UCSD' in the example).
    for start_node in graph.nodes:
        
        # If this node hasn't been labeled, it's part of a new component
        if start_node not in labels:
            
            # Start a new BFS for this component
            # Label the first node 'good' (this choice is arbitrary)
            labels[start_node] = 'good'
            queue = deque([start_node])
            
            while queue:
                u = queue.popleft()
                current_label = labels[u]
                
                # Determine the opposite label for neighbors
                opposite_label = 'evil' if current_label == 'good' else 'good'
                
                for v in graph[u]:
                    if v not in labels:
                        # If neighbor is unvisited, label it and add to queue
                        labels[v] = opposite_label
                        queue.append(v)
                    else:
                        # If neighbor is already labeled, check for a conflict
                        # A conflict means two adjacent nodes have the same label
                        if labels[v] == current_label:
                            # This means the graph has an odd-length cycle
                            # and is not bipartite.
                            return None # [cite: 537, 556]
                            
    # If the loop finishes with no conflicts, the labeling is successful
    return labels
'''

from collections import deque
def assign_good_and_evil(graph):
    label = {}
    status = {node: 'undiscovered' for node in graph.nodes}
    for node in graph.nodes:
        if status[node] == 'undiscovered':
            possible = good_and_evil_bfs(graph, node, status, label)
            if not possible:
                return None
    return label
def good_and_evil_bfs(graph, source, status, label):
    status[source] = 'pending'
    label[source] = 'good'
    pending = deque([source])
    # while there are still pending nodes
    while pending:
        u = pending.popleft()
        for v in graph.neighbors(u):
            # explore edge (u,v)
            if status[v] == 'undiscovered':
                status[v] = 'pending'
                if label[u] == 'good':
                    label[v] = 'evil'
                else:
                    label[v] = 'good'
                # append to right
                pending.append(v)
            elif label[u] == label[v]:
                return False
        status[u] = 'visited'
    return True