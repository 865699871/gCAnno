import os
import time

from pipline.mapping_svm import mapping
import argparse


def main():
    parser = argparse.ArgumentParser(description='gcAnno for cell type annotation using svm')
    parser.add_argument('-o', '--outdir')
    parser.add_argument('-d', '--distanceFile')
    parser.add_argument('-q', '--testinput')
    parser.add_argument('-rd', '--refinput')
    parser.add_argument('-rt', '--reftype')

    parser.add_argument('-sg', '--selectGenenum', default=65, type=int)

    args = parser.parse_args()
    outdir = args.outdir
    distanceFile = args.distanceFile
    testinput = args.testinput
    refinput = args.refinput
    reftype = args.reftype
    selectGenenum = args.selectGenenum

    if not os.path.exists(outdir):
        os.makedirs(outdir)
    logfile = outdir + 'logmodel.txt'

    logfile = open(logfile, 'w')
    print('prdict....')
    logfile.write('prdict....\n')
    logfile.flush()
    time_start = time.time()

    mapping(distanceFile, testinput, refinput, reftype, outdir,selectGenenum)

    time_end = time.time()
    print('prdict', (time_end - time_start) / 60)
    print('-------------------------------------------------------------')
    logfile.write('prdict ' + str((time_end - time_start) / 60) + '\n')
    logfile.write('-------------------------------------------------------------\n')
    logfile.flush()


if __name__ == '__main__':
    main()
