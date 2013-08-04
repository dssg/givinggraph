import community
import networkx as nx

edges_list = [("123", "345", 0.5), ("345", "456", 0.7),
              ("345", "1", 0.1), ("1", "123", 0.3)]


def compute_communities(edges_list):
    """For the given weighted edges, find the communities for each node."""
    G = nx.Graph()
    G.add_weighted_edges_from(edges_list)
    partition = community.best_partition(G)
    return partition

print compute_communities(edges_list)
