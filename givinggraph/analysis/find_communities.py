import community
import networkx as nx

edges_list = [("123", "345", 0.5), ("345", "456", 0.7),
              ("345", "1", 0.1), ("1", "123", 0.3)]


def compute_communities(edges_list):
    G = nx.Graph()
    for edge in edges_list:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    partition = community.best_partition(G)
    return partition

print compute_communities(edges_list)
