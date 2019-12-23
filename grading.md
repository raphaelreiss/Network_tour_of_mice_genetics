## Genetics
By Benjamin

This dataset contains genes, protein expressions and phenotypes of a "family" of mice.
It is a subset of the open dataset available at <http://www.genenetwork.org>.
The goal is to explore the data using graphs and discover connections between genes, protein expression, and phenotypes.
This data has been collected by different laboratories all over the world during several decades.
The [EPFL's LISP](https://www.epfl.ch/labs/auwerx-lab) is part of the group.
More details about the project and dataset can be found on this [EPFL mediacom article](https://actu.epfl.ch/news/a-big-data-tool-begins-new-era-for-biology-and-per/).

This dataset is a collection of matrices.
Each column is a single BXD strain (a mouse) whose genome is a unique combination of the C57BL/6J and DBA/2J parental strains.
They have been saved as CSV files (with a `txt` extension).
The `genotype_BXD.txt` file is a binary matrix that describes the contribution of each of the parental strains for a list of selected genes (rows).
Each row of the genotype data indicates whether a certain position in the genome is inherited from the C57BL/6J or DBA/2J parent.
Phenotype data contained in `Phenotype.txt` are also matrices indicating the values of each phenotype for each strain.
In addition, multiomic molecular phenotypes from different mouse organs are represented as one matrix per organ (e.g., brain, bone, muscle, liver, etc.), in the `expression_data` folder.

It is important to note that protein or phenotype information is not available for all the mice.
Depending on the research team gathering the data or the protocols, only a subset of mice have been tested for each phenotype, or different organs have been analyzed.
Hence, the combination of several matrices will result in missing entries.
These missing entries, along with the variety of the data, are a real challenge for a data science approach, but mimic the real life situation encountered with human medical records.

The dataset for the NTDS project can be found [here](https://drive.switch.ch/index.php/s/mtQ2F0dYc7dHOtQ).
The students are expected to:
* use the different matrices of data to build one or more graphs (for example a graph of mice),
* explore these graphs,
* associate values to the nodes of the graphs using the other matrices,
* apply graph signal processing approaches,
* discover new relations between the genome, protein expressions in tissues and phenotypes (optional but that would be great!).

|          | Description                                                  |         Amount |
| -------- | ------------------------------------------------------------ | -------------: |
| nodes    | mice                                                         |      100 - 200 |
| edges    | similar genes, protein expressions, or phenotypes            | O(10) per node |
| features | genes, protein expressions in tissues, or phenotypes         |          1000s |
| labels   | depends: a particular gene, phenotype, or protein expression |            N/A |

Resources:
* [EPFL mediacom article](https://actu.epfl.ch/news/a-big-data-tool-begins-new-era-for-biology-and-per/)
* [Info on the BXD mice](https://www.biorxiv.org/content/10.1101/672097v3.full)
* [Official dataset website](http://www.genenetwork.org/)
* [Subset for NTDS](https://drive.switch.ch/index.php/s/mtQ2F0dYc7dHOtQ)





# NTDS'19 projects grading

Below is a detailed description of the five criteria on which projects will be evaluated.
Bonus points can be attributed in each category for going the extra mile.

### 1. Story (20 points)

* motivation: why study this question or develop that product?
* relevance of chosen data and tools
	* Can the data answer the question or support the product?
	* Are the chosen tools relevant?

### 2. Acquisition (10 points)

* proper data: it has a graph structure, and nodes have attributes (e.g., features, labels, time series)
* example bonus: collection, processing, and cleaning of primary or complementary data (e.g., using a web API, combining datasets, designing a scheme to weight the edges)

### 3. Exploration (20 points)

* some properties of the graph (e.g., connected components, sparsity, diameter, clusters, degree distribution, spectrum)
* identify the type of graph (e.g., power law, small world, regular, sampled manifold)
* some properties of the nodes (e.g., clustering coefficient, modularity, centrality)
* some analysis of the attributes (e.g., their distribution, smoothness, graph Fourier transform)
* a vizualization of the network
* a reflection on the insights

### 4. Exploitation (30 points)

* at least one of the following tools, seen during the lectures, is used:
	* clustering (spectral clustering, k-means)
	* graph Fourier transform
	* regularization (graph Tikhonov, graph total variation)
	* dimensionality reduction (PCA, MDS, LLE, ISOMAP, Laplacian eigenmaps, t-SNE)
	* graph filters (Chebyshev, ARMA)
	* graph neural networks
* critical evaluation of the results
	* subjective or objective (baseline, existing work)
	* state the limitations: to what extent did you answer the question or provide a good product
* example bonus: use multiple relevant tools, or tools beyond what was seen in class

### 5. Communication (20 points)

* report:
	* structure
	* content: be explicit about what you did in acquisition, exploration, exploitation. It should be precise enough for another team to replicate your work. Results should be supported by figures, tables, etc.
	* well written: clarity, conciseness
* oral: presentation skills (organization, clarity)
* github repository: README, LICENSE, documented, organization (notebooks and python modules), reproducible, good coding practice (comments, docstrings)
* example bonus: published interactive visualization
