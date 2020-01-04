import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from tabulate import tabulate
import random

import networkx as nx
from pygsp import graphs, filters, plotting


#### Network
def gaussian_kernel(dist, sigma):
    return np.exp(-dist**2 / (2*sigma**2))

def get_adjacency(X: np.ndarray, dist_metric, sigma=1, epsilon=0):
    """ X (n x d): coordinates of the n data points in R^d.
        sigma (float): width of the kernel
        epsilon (float): threshold
        Return:
        adjacency (n x n ndarray): adjacency matrix of the graph.
    """
    dist = squareform(pdist(X, metric=dist_metric))
    adjacency = gaussian_kernel(dist,sigma)
    adjacency[adjacency < epsilon] = 0
    np.fill_diagonal(adjacency, 0)
    return adjacency

def graph_basic_stats(G):
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



#### GSP
def compute_laplacian(adjacency: np.ndarray, normalize: bool):
    """ Return:
        L (n x n ndarray): combinatorial or symmetric normalized Laplacian.
    """
    D = np.diag(np.sum(adjacency, 1)) # Degree matrix
    combinatorial = D - adjacency
    if normalize:
        D_norm = np.diag(np.clip(np.sum(adjacency, 1), 1, None)**(-1/2))
        return D_norm @ combinatorial @ D_norm
    else:
        return combinatorial

def spectral_decomposition(laplacian: np.ndarray):
    """ Return:
        lamb (np.array): eigenvalues of the Laplacian
        U (np.ndarray): corresponding eigenvectors.
    """
    return np.linalg.eigh(laplacian)

def fit_polynomial(lam: np.ndarray, order: int, spectral_response: np.ndarray):
    """ Return an array of polynomial coefficients of length 'order'."""
    A = np.vander(lam, order, increasing=True)
    coeff = np.linalg.lstsq(A, spectral_response, rcond=None)[0]
    return coeff

def polynomial_graph_filter(coeff: np.array, laplacian: np.ndarray):
    """ Return the laplacian polynomial with coefficients 'coeff'. """
    power = np.eye(laplacian.shape[0])
    filt = coeff[0] * power
    for n, c in enumerate(coeff[1:]):
        power = laplacian @ power
        filt += c * power
    return filt


#### GCNN
def get_masks(nb_nodes, test_ratio, seed=None):
    ''' Return the indices for the train and test sets
    '''
    if seed is not None:
        np.random.seed(seed)

    nb_test = int(nb_nodes*test_ratio)
    test_mask = np.sort(random.sample(range(0, nb_nodes), nb_test))
    train_mask = list(set(np.arange(0, nb_nodes))^set(test_mask))

    return train_mask, test_mask

def compute_accuracy(y, y_hat):
    assert(len(y)==len(y_hat)), 'y and y_hat must have the same length'
    return np.sum(y_hat == y) / (len(y) - int(pd.DataFrame(y).isna().sum())) # to deal with NaNs
