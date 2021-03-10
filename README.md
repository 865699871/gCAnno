# gCAnno-A tool for cell type annotation of single-cell transcriptome sequencing
Cell type annotation is essential for single cell data analysis.gCAnno can annotate cell types accurately.

## Dependencies
python 3.6.4
```Bash
conda create -n environment python=3.6.4
```
```Bash
conda install packge=version
```
packges  | version|
--------- | --------|
numpy  | 1.16.4 |
pandas  | 0.20.3 |
scipy  | 1.2.0 |
scikit-learn  | 0.21.3 |
matplotlib  | 3.0.3 |
networkx | 2.1 |
gensim | 3.4.0 |

## Usage
### example ([detail](https://github.com/865699871/gCAnno/wiki/Arguments-detail))
* build model
```Bash
python ./buildModelPipline.py -o ./ref/ -e ./testData/ref/expdata_normal.xls -c ./testData/ref/cluster.xls -fr 0.3

```
* cell type annotation--Bayes
```Bash
python ./defineCellTypePipline_bayes.py -o ./test_bayes/ -d ./ref/embedding/02.embeddingDis.xls -q ./testData/test/expdata_normal.xls -sg 65

```
* cell type annotation--SVM
```Bash
python ./defineCellTypePipline_svm.py -o ./test_svm/ -d ./ref/embedding/02.embeddingDis.xls -q ./testData/test/expdata_normal.xls -rd ./testData/ref/expdata_normal.xls -rt ./testData/ref/cluster.xls -sg 65

```

## Others
#### testData
We provide users a small dataset to test gCAnno. User can run `sh testref.sh` to build model and run `sh testAnnotation_bayes.sh` or `sh testAnnotation_svm.sh` to test model.


## Contact
****
|Author|Gao Shenghan|
|---|---
|E-mail|gaoxian15002970749@163.com|
****

