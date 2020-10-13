import pandas as pd
import numpy as np
import os
import argparse
import matplotlib.pyplot as plt

def staticlabel(truelabelFile,resultFile,outdir):
    truelabel = np.asarray(pd.read_csv(truelabelFile,sep='\t'))
    result = pd.read_csv(resultFile,sep='\t',index_col=0)
    print(truelabel)
    print(result)
    static = []
    for i in truelabel:
        predict = np.asarray(result.loc[result.index == i[0]])[0]
        item = list(i)
        for j in predict:
            item.append(j)
        static.append(item)
    static = pd.DataFrame(static,columns=['cell.name','truelabel','predict'])
    static.to_csv(outdir + 'staticinput.xls',sep='\t',index=None)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('outdir')
    parser.add_argument('truelabelFile')

    args = parser.parse_args()
    outdir = args.outdir
    truelabelFile = args.truelabelFile


    if not os.path.exists(outdir):
        os.makedirs(outdir)

    resultFile = outdir + 'out_predict_cluster.xls'

    staticlabel(truelabelFile, resultFile, outdir)

    staticInputFile = outdir + 'staticinput.xls'

    result = pd.read_csv(staticInputFile, sep='\t')[['truelabel', 'predict']]

    listType = result['truelabel'].unique()
    staticresult = []
    sum = 0
    for i in listType:
        split = result.loc[result['truelabel'] == i]
        error = split.loc[split['truelabel'] != split['predict']]
        sum += len(split)
        staticresult.append([i, len(error), len(split)])
    print(sum)

    sumerror = 0
    sumtotal = 0
    for i in staticresult:
        sumerror += i[1]
        sumtotal += i[2]
    staticresult.append(['sum', sumerror, sumtotal])
    print(len(staticresult))
    outData = pd.DataFrame(staticresult, columns=['cluster', 'error', 'total'])
    print(outData)

    outData.to_csv(outdir + 'staticout.xls', sep='\t', index=None)

    # 生成数据
    labels = ['error', '']
    share = [float(sumerror) / sumtotal,
             float(sumtotal - sumerror) / sumtotal]
    # 设置分裂属性
    explode = [0.1, 0]

    # 分裂饼图
    plt.figure()
    plt.pie(share, explode=explode,
            labels=labels, autopct='%3.1f%%', shadow=True,
            colors=['#FF3B30', '#C3CFE8'])

    # 标题
    plt.title('acc OUR')
    plt.savefig(outdir + 'staticout.png')
    plt.close()

if __name__ == '__main__':
    main()

