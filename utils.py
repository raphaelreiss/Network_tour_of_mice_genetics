import numpy as np
import networkx as nx
from tabulate import tabulate
from scipy.spatial.distance import pdist, squareform


### Adjacency matrix building ###

def epsilon_similarity_graph(X: np.ndarray, metric='euclidean', sigma=1, epsilon=0):
    """ X (n x d): coordinates of the n data points in R^d.
        sigma (float): width of the kernel
        epsilon (float): threshold
        Return:
        adjacency (n x n ndarray): adjacency matrix of the graph.
    """
    Dists = squareform(pdist(X,metric = "euclidean"))
    Dists = np.exp(-Dists**2/(2 * sigma**2))
    Dists[Dists <= epsilon] = 0
    np.fill_diagonal(Dists,0)
    return Dists


def build_adj_from_strain(genotype_df, strains, metric, sigma, epsilon):
    """ Build adjacency matrix using whole data filtered by the strains parameter """

    filtered_df = genotype_df[genotype_df.index.isin(strains)].copy()
    filtered_df.sort_index(inplace=True)
    adj = epsilon_similarity_graph(filtered_df.values, \
                                   metric=metric, sigma=sigma, epsilon=epsilon)
    return adj


### Graph stats ###


def graph_basic_stats(G):
    """ Print basic stats for a nx.Graph()"""
    nodes_number = G.number_of_nodes()
    edges_number = G.number_of_edges()

    g_degree = G.degree()
    sum_degree = sum(dict(g_degree).values())
    average_degree = sum_degree / nodes_number

    tab = [
        ["Number of nodes", nodes_number],
        ["Number of edges", edges_number],
        ["Graph density", round(nx.classes.function.density(G) * 100, 2)],
        ["Average degree", round(average_degree, 2)],
        ["Number of connected components", nx.number_connected_components(G)],
        ["Average clustering coefficient", round(nx.average_clustering(G), 2)],
        ["Diameter of the network (longest shortest path)", nx.diameter(G)]
    ]
    print(tabulate(tab, tablefmt='fancy_grid'))
