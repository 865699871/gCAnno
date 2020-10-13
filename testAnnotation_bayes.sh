python ./defineCellTypePipline_bayes.py -o ./test_bayes/ -d ./ref/embedding/02.embeddingDis.xls -q ./testData/test/expdata_normal.xls -sg 65
python ./static.py ./test_bayes/ ./testData/test/cluster.xls 
