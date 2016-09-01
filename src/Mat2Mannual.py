#!/usr/bin/env python
import sys
args = sys.argv

MatAddress = args[1]    #.pickle
Mat_lower = int(args[2])
Mat_upper = int(args[3])

print "Parameters:",MatAddress, Mat_lower, Mat_upper
import pickle
import numpy as np

with open(MatAddress) as f:
    Mat = pickle.load(f)[0]

ColSum = Mat.sum(0)

Filter = []
for i in range(len(ColSum)):
    if (Mat_lower <= ColSum[i])and (ColSum[i] <= Mat_upper):
        Filter.append(i)

Mat_manual = Mat[:,Filter]   
print "Mat_manual.shape:", Mat_manual.shape

with open("Filter_"+str(Mat_lower)+'_'+str(Mat_upper)+'.txt',"w") as f:
    for i in Filter:
        f.write(str(i))
        f.write('\n')

PatientNum = Mat_manual.shape[0]
GeneNum = Mat_manual.shape[1]

with open('Mat_Mannual_'+str(Mat_lower)+'_'+str(Mat_upper)+'.txt','w') as f:
    for i in range(PatientNum):
        for j in range(GeneNum):
            if Mat[i,j] == 1:
                f.write('y')
            else:
                f.write('n')
            if j!= GeneNum-1:
                f.write('\t')
        f.write('\n')