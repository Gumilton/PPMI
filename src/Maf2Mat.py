'''
#!/usr/bin/env python
import sys
args = sys.argv

MafAddress = args[1]
'''
"""
Maf format to design matrix
"""
import numpy as np

def DictReverse(m):
    return dict(map(lambda t:(t[1],t[0]), m.items()))
MafAddress = 'D:/data/PPMI/nogene_30000.txt'

print 'Start!'
with open(MafAddress, 'r') as myfile:
    Maf = myfile.read().splitlines()

for i in xrange(len(Maf)):
    Maf[i] = Maf[i].split('\t')
    Maf[i] = [int(Maf[i][1]),Maf[i][4]]

GeneDict = {}
PatientDict = {}
GeneCount = 0
PatientCount = 0
for i in Maf:
    GeneTemp = i[0]
    PatientTemp = i[1]
    if GeneTemp not in GeneDict:
        GeneDict[GeneTemp] = GeneCount
        GeneCount += 1
    if PatientTemp not in PatientDict:
        PatientDict[PatientTemp] = PatientCount
        PatientCount += 1
GeneDict_Reverse = DictReverse(GeneDict)
PatientDict_Reverse = DictReverse(PatientDict)
        
import pickle
# Saving the objects:
with open('Dict.pickle', 'w') as f:
    pickle.dump([GeneDict, PatientDict, GeneDict_Reverse, PatientDict_Reverse], f)

Mat = np.zeros((len(PatientDict), len(GeneDict)), dtype = int)
for i in Maf:
    GeneTemp = i[0]
    PatientTemp = i[1]
    Mat[PatientDict[PatientTemp], GeneDict[GeneTemp]] = 1
    
with open('Mat.pickle', 'w') as f:
    pickle.dump([Mat], f)

print 'Finished!'

