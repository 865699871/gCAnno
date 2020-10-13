from model.node2vec import Node2Vec
import os
import networkx as nx
import pandas as pd
import numpy as np


def embeddingGraph(graphFile, outdir,
                   walk_length=10, num_walks=80,
                   p=0.25, q=4, workers=1,
                   window_size=5, iter=3):
    """
    graph embedding
    :param graphFile: graph file
    :param outdir: file output location
    :param walk_length: (default 10)
    :param num_walks: (default 80)
    :param p: (default 0.25)
    :param q: (default 4)
    :param workers: (default 1)
    :param window_size: (default 5)
    :param iter: (default 3)
    :return:
    """
    G = nx.read_edgelist(graphFile, create_using=nx.DiGraph(), nodetype=None, data=[('weight', float)])
    model = Node2Vec(G, walk_length=walk_length, num_walks=num_walks, p=p, q=q, workers=workers)
    model.train(window_size=window_size, iter=iter)
    embeddings = model.get_embeddings()
    nodes = []
    data = []
    for i in embeddings.keys():
        nodes.append(i)
        data.append(embeddings[i])
    data = pd.DataFrame(data)
    data.index = nodes
    data.to_csv(outdir + '02.embeddingVector.xls', sep='\t')
    return data


def distanceMatrix(outdir, clusterFile):
    """
    calculate the distance between cell type vector and gene vector
    output distance matrix
    :param outdir: file output location
    :param clusterFile: cellType file
    """
    embeddingFile = outdir + '02.embeddingVector.xls'
    embeddingVector = pd.read_csv(embeddingFile, sep='\t', index_col=0)
    cluster = pd.read_csv(clusterFile, sep='\t')
    cellType = cluster['cluster'].unique()
    newcellType = []
    for i in cellType:
        newcellType.append(str(i))
    cev = embeddingVector.T[newcellType].T
    gev = embeddingVector.loc[~embeddingVector.index.isin(newcellType)]
    cells = cev.index.tolist()
    genes = gev.index.tolist()
    cev = np.asarray(cev)
    gev = np.asarray(gev)
    distanceM = []
    for i in gev:
        item = []
        for j in cev:
            euclide = np.linalg.norm(np.asarray(i) - np.asarray(j))
            item.append(euclide)
        distanceM.append(item)
    distanceM = pd.DataFrame(distanceM, columns=cells, index=genes)
    distanceM.to_csv(outdir + '02.embeddingDis.xls', sep='\t')

