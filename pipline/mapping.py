import pandas as pd
import numpy as np
import os
from sklearn.naive_bayes import BernoulliNB


def mapping(distanceFile, testdataFile, outDir, selectGenenum=65):
    """
    using distance between cell type vector and gene vector
    to select genes and build Naive bayes model for annotation
    output annotation result

    :param distanceFile: embedding distance file location
    :param testdataFile: query datasets file
    :param outDir: output path
    :param selectGenenum: (default 65)
    """
    distance = pd.read_csv(distanceFile, sep='\t', index_col=0)
    selectgene = {}
    for i in distance.columns:
        celltype = i
        item = distance[i].sort_values()
        # 65
        topgenes = item.index.tolist()[:selectGenenum]
        selectgene[celltype] = topgenes

    featureList = []
    for i in selectgene.keys():
        for j in selectgene[i]:
            if j not in featureList:
                featureList.append(j)
    featureMatrix = []
    for i in selectgene.keys():
        item = []
        typeGene = selectgene[i]
        for j in featureList:
            if j in typeGene:
                item.append(1)
            else:
                item.append(0)
        featureMatrix.append(item)
    featureMatrix = pd.DataFrame(featureMatrix, columns=featureList, index=selectgene.keys())
    Xtrain = np.asarray(featureMatrix)
    Ytrain = featureMatrix.index.tolist()

    bnb = BernoulliNB()
    bnb.fit(Xtrain, Ytrain)

    testData = pd.read_csv(testdataFile, sep='\t', index_col=0).T
    testGene = testData.columns.tolist()
    addgene = []
    for i in featureList:
        if i not in testGene:
            addgene.append(i)
    for i in addgene:
        testData[i] = 0

    testData = testData[featureList]

    Xtest = []
    nptestData = np.asarray(testData)

    for i in nptestData:
        item = []
        for j in i:
            if j != 0:
                item.append(1)
            else:
                item.append(0)
        Xtest.append(item)

    y_predict = bnb.predict(Xtest)
    y_proba = bnb.predict_proba(Xtest)
    normal_proba = []
    for i in y_proba:
        newvalue = []
        sum = 0
        for j in i:
            sum += j
        for j in range(len(i)):
            if i[j]/ sum > 0.1:
                newvalue.append([bnb.classes_[j],i[j]/ sum])
        normal_proba.append(newvalue)

    prob_file = outDir + 'out_predict_proba.txt'
    prob_file = open(prob_file,'w')
    for i in range(len(normal_proba)):
        prob_file.write(testData.index[i] + '\t')
        for j in normal_proba[i]:
            prob_file.write(j[0] +'\t'+ str(j[1])+'\t')
        prob_file.write('\n')
    prob_file.close()
    y_predict = pd.DataFrame(y_predict, index=testData.index, columns=['pridect'])
    y_predict.to_csv(outDir + 'out_predict_cluster.xls', sep='\t')
