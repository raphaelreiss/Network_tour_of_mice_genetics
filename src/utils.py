import scipy
import numpy as np
import collections
import networkx as nx
from tabulate import tabulate
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

### Adjacency matrix building ###
def distance_scipy_spatial(z, k=4, metric='euclidean'):
    """Compute exact pairwise distances. *Crédits to M. Defferrard*"""
    d = scipy.spatial.distance.pdist(z, metric)
    d = scipy.spatial.distance.squareform(d)
    # k-NN graph.
    idx = np.argsort(d)[:, 1:k+1]
    d.sort()
    d = d[:, 1:k+1]
    return d, idx

def adjacency(dist, idx):
    """Return the adjacency matrix of a kNN graph. *Crédits to M. Defferrard*"""
    M, k = dist.shape
    assert M, k == idx.shape
    assert dist.min() >= 0

    # Weights.
    sigma2 = np.mean(dist[:, -1])**2
    dist = np.exp(- dist**2 / sigma2)

    # Weight matrix.
    I = np.arange(0, M).repeat(k)
    J = idx.reshape(M*k)
    V = dist.reshape(M*k)
    W = scipy.sparse.coo_matrix((V, (I, J)), shape=(M, M))

    # No self-connections.
    W.setdiag(0)

    # Non-directed graph.
    bigger = W.T > W
    W = W - W.multiply(bigger) + W.T.multiply(bigger)

    assert W.nnz % 2 == 0
    assert np.abs(W - W.T).mean() < 1e-10
    assert type(W) is scipy.sparse.csr.csr_matrix
    return W

def adjacency_subset(genotype_df, strains, metric, k=4):
    """ Build adjacency matrix using whole data filtered by the strains name"""

    filtered_df = genotype_df.loc[strains].copy(deep=True)
    filtered_df.sort_index(inplace=True)
    genetic_distance, idx = distance_scipy_spatial(filtered_df.values, k, metric=metric)
    return adjacency(genetic_distance, idx)

### Graph stats ###

def graph_moment(G, order=1):
    """Compute the moments of of the graph"""
    assert isinstance(G, nx.Graph)

    # Build degree counter
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg_cnt = zip(*degreeCount.items())

    return sum(map(lambda x: x[0] ** order * x[1], degreeCount.items())) / len(degree_sequence)

def plot_degree_histogram(G, ax):
    """Plot the histogram of the edge degree for the graph G"""
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    ax.bar(deg, cnt, label='Histogram')

def print_remaining_data(adjacency):
    """Print the percentage of data that is non zero"""
    print("{:0.2f} % of the original data is kept"\
          .format(adjacency[adjacency.nonzero()].size / adjacency.size * 100))

def plot_distrib(adjacency):
    """ Plot the density of kerneled distances

    Args:
        adjacency (np.ndarray): adjacency matrix

    """
    assert isinstance(adjacency, np.ndarray)

    non_zero = adjacency[adjacency > 0.]
    plt.plot(np.sort(non_zero)[::-1])

def graph_basic_stats(G):
    """ Print basic stats for a nx.Graph()"""
    assert isinstance(G, nx.Graph)

    nodes_number = G.number_of_nodes()
    edges_number = G.number_of_edges()


    tab = [
        ["Number of nodes", nodes_number],
        ["Number of edges", edges_number],
        ["Graph density", round(nx.classes.function.density(G) * 100, 2)],
        ["Number of connected components", nx.number_connected_components(G)],
        ["Average clustering coefficient", round(nx.average_clustering(G), 2)],
        ["Diameter of the network (longest shortest path)", nx.diameter(G)]
    ]
    print(tabulate(tab, tablefmt='fancy_grid'))
