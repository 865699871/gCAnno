import pandas as pd
import numpy as np
import os
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

def mapping(distanceFile, testdataFile,refdataFile,reftypeFile, outDir, selectGenenum=65):
    """
    using distance between cell type vector and gene vector
    to select genes and build svm model for annotation
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

    Xtrain = pd.read_csv(refdataFile, sep='\t', index_col=0).T[featureList]
    Xtrain = np.asarray(Xtrain)
    Ytrain = pd.read_csv(reftypeFile, sep='\t')['cluster'].tolist()
    Classifier = LinearSVC()
    clf = CalibratedClassifierCV(Classifier)

    clf.fit(Xtrain, Ytrain)
    testData = pd.read_csv(testdataFile, sep='\t', index_col=0).T
    testGene = testData.columns.tolist()
    addgene = []
    for i in featureList:
        if i not in testGene:
            addgene.append(i)
    for i in addgene:
        testData[i] = 0

    testData = testData[featureList]
    y_predict = clf.predict(testData)
    y_proba = clf.predict_proba(testData)
    normal_proba = []
    for i in y_proba:
        newvalue = []
        sum = 0
        for j in i:
            sum += j
        for j in range(len(i)):
            if i[j] / sum > 0.1:
                newvalue.append([clf.classes_[j],i[j]/ sum])
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

