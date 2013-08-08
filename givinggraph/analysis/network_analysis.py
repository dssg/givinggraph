from . import community
import networkx as nx

edges_list = [("123", "345", 0.5), ("345", "456", 0.7),
              ("345", "1", 0.1), ("1", "123", 0.3)]


# first create a Graph, then give the graph as a parameter to the other functions
def create_graph(edges_list, directed=False, weighted=True):
    """For the given weighted edges, create a graph object."""
    G = nx.DiGraph() if directed else nx.Graph()
    if weighted:
        G.add_weighted_edges_from(edges_list)
    else:
        G.add_edges_from(edges_list)
    return G


def compute_communities(G):
    """For the given graph, find the communities for each node.
    >>> p = compute_communities(create_graph(edges_list))
    >>> p['1'] == p['123']
    True
    >>> p['345'] == p['456']
    True
    """
    if isinstance(G, nx.DiGraph):
        G = G.to_undirected()
    partition = community.best_partition(G)
    return partition


def compute_hubs_authorities(G):
    """For the given graph, compute hubs and authorities values for each node"""
    hits = nx.hits(G, max_iter=500)
    hubs = hits[0]
    authorities = hits[1]
    return hubs, authorities


def export_graph(G, name='graph'):
    """exports the graph"""
    nx.write_gml(G, name + '.gml')


def compute_average_node_connectivity(G):
    """For the given graph, compute the average connectivity"""
    return nx.average_node_connectivity(G)


def compute_all_pairs_node_connectivity_matrix(G):
    """For the given graph, returns a numpy 2d ndarray with node connectivity between all pairs of nodes"""
    return nx.all_pairs_node_connectivity_matrix(G)


my_graph = create_graph(edges_list)
print compute_communities(my_graph)
