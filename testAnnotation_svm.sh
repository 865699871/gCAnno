python ./defineCellTypePipline_svm.py -o ./test_svm/ -d ./ref/embedding/02.embeddingDis.xls -q ./testData/test/expdata_normal.xls -rd ./testData/ref/expdata_normal.xls -rt ./testData/ref/cluster.xls -sg 65
python ./static.py ./test_svm/ ./testData/test/cluster.xls 
