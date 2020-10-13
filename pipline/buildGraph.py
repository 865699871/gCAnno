import os
import pandas as pd
import numpy as np

def buildGraph(expdataFile, outdir,clusterFile,filterRate=0.3):
    """
    build cellType-gene network
    :param expdataFile: expression matrix file, row is gene and column is cell
    :param outdir: file output location
    :param clusterFile: cellType file
    :param filterRate:  gene nodes filter condition (default 0.3)
    """
    expdata = pd.read_csv(expdataFile, sep='\t', index_col=0)
    genes = expdata.index.tolist()

    cluster = pd.read_csv(clusterFile, sep='\t')
    listType = cluster['cluster'].unique()

    clusterDir = {}
    for i in listType:
        item = cluster.loc[cluster['cluster'] == i]['cell.name'].tolist()
        clusterDir[i] = item

    exppart = []

    weight = []
    count = 0
    for i in genes:
        count += 1
        if count % 1000 == 0:
            print(count)
        item = expdata.loc[expdata.index == i]
        addindex = 0
        weightItem = []
        # test
        exppartItem = []

        for j in clusterDir.keys():
            cells = clusterDir[j]
            cellexp = np.asarray(item[cells])[0]
            non0 = 0
            sum = 0
            for k in cellexp:
                if k != 0:
                    non0 += 1
                    sum += k
            expRate = non0 / len(cellexp)
            if non0 != 0:
                expMean = sum/non0
            else:
                expMean = 0
            if expRate > filterRate:
                addindex = 1
            weightItem.append([j,i,expRate * expMean])
            exppartItem.append([j,i,expRate, expMean])
        if addindex == 1:
            for j in weightItem:
                if j[2] != 0:
                    weight.append(j)
            for j in exppartItem:
                if j[2] != 0:
                    exppart.append(j)
    cellTGene = pd.DataFrame(weight,columns=['cellType','gene','w'])

    graphnum = {}
    graphnum['cellType_gene'] = len(cellTGene) * 2
    cellTGene = np.asarray(cellTGene)
    outfile = open(outdir + '01.graph.txt', 'w')
    print('edge type')
    print(graphnum)
    print('all Edge')
    print(len(cellTGene) * 2)
    for i in cellTGene:
        outfile.write(str(i[0]) + ' ' + i[1] + ' ' + str(i[2]) + '\n')
        outfile.write(i[1] + ' ' + str(i[0]) + ' ' + str(i[2]) + '\n')
    outfile.close()

