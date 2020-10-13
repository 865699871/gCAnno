import os
import time

from pipline.buildGraph import buildGraph
from pipline.embedding import embeddingGraph, distanceMatrix


import argparse


def main():
    parser = argparse.ArgumentParser(description='gcAnno for model building')
    parser.add_argument('-o','--outdir')
    parser.add_argument('-e','--exp')
    parser.add_argument('-c','--celltype')
    parser.add_argument('-fr', '--filterRate', default=0.3, type=float)

    args = parser.parse_args()
    outdir = args.outdir
    expdataFile = args.exp
    clusterFile = args.celltype

    filterRate = args.filterRate

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    environment01 = outdir + 'buildGraph/'
    environment02 = outdir + 'embedding/'

    logfile = outdir + 'logembedding.txt'

    logfile = open(logfile, 'w')
    print('buildGraph....')
    logfile.write('buildGraph....\n')
    logfile.flush()
    time_start = time.time()
    if not os.path.exists(environment01):
        os.makedirs(environment01)
    print('start build Graph')
    logfile.write('start build Graph\n')
    logfile.flush()
    buildGraph(expdataFile, environment01, clusterFile,filterRate=filterRate)
    time_end = time.time()
    print('buildGraph cost', (time_end - time_start) / 60)
    print('-------------------------------------------------------------')
    logfile.write('buildGraph cost ' + str((time_end - time_start) / 60) + '\n')
    logfile.write('-------------------------------------------------------------\n')
    logfile.flush()

    print('embedding....')
    logfile.write('embedding....\n')
    logfile.flush()
    time_start = time.time()
    if not os.path.exists(environment02):
        os.makedirs(environment02)
    print('start embedding')
    logfile.write('start embedding\n')
    logfile.flush()
    embeddingGraph(environment01 + '01.graph.txt', environment02)
    distanceMatrix(environment02, clusterFile)
    time_end = time.time()
    print('embedding cost', (time_end - time_start) / 60)
    print('-------------------------------------------------------------')
    logfile.write('embedding cost ' + str((time_end - time_start) / 60) + '\n')
    logfile.write('-------------------------------------------------------------\n')
    logfile.flush()



if __name__ == '__main__':
    main()
