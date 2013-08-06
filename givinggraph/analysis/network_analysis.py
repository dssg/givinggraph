import community
import networkx as nx

edges_list = [("123", "345", 0.5), ("345", "456", 0.7),
              ("345", "1", 0.1), ("1", "123", 0.3)]


def compute_communities(edges_list, directed=False, weighted=True):
    """For the given weighted edges, find the communities for each node."""
    G = nx.DiGraph() if directed else nx.Graph()
    if weighted:
        G.add_weighted_edges_from(edges_list)
    else:
        G.add_edges_from(edges_list)

    partition = community.best_partition(G)
    return partition


def compute_hubs_authorities(edges_list, directed=False, weighted=True):
    """For the given weighted edges, compute hubs and authorities values for each node"""
    G = nx.DiGraph() if directed else nx.Graph()
    if weighted:
        G.add_weighted_edges_from(edges_list)
    else:
        G.add_edges_from(edges_list)

    hits = nx.hits(G, max_iter=500)
    hubs = hits[0]
    authorities = hits[1]
    return hubs, authorities

# print compute_hubs_authorities(edges_list)[0]
# print compute_hubs_authorities(edges_list)[1]
print compute_communities(edges_list)
