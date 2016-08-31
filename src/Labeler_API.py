# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 02:16:22 2016

@author: JH Sun
"""
# Different Matrices with 100 feature dimensions preprocessed with differet ways will be passed to you.
# You may subset it with the first (Because the more important the feature is, the smaller its index will be) 
#   several features (eg. 10 or 30 or 50) locally before passing it to the Learner.


def Learner(Matrix):    # Matrix is a numpy.ndarray, dtype = float, shape = (PatientNum, FeatureNum).
    import numpy as np    
    PatientNum = Matrix.shape[0]
    FeatureNum = Matrix.shape[1]
    
    # We may encounter outlier issues. In this case, the outliers that may be put aside will be labeled 0.
    return Labels   # Labels  is a numpy.ndarray,shape = (PatientNum, 2), dtype = int. label = (0),1,2,3,...

def Labeler(Learner, MatrixAddress):    # MatrixAddress is the address of reducted feature matrix .txt file
    import numpy as np    
    with open(MatrixAddress, 'r') as f:
        Matrix = f.read().splitlines()
        
    for i in xrange(len(Matrix)):
        Matrix[i] = (Matrix[i].split('\t'))
        Matrix[i] = [float(j) for j in Matrix[i]]

    Matrix = np.array(Matrix)
    PatientNum = Matrix.shape[0]
    FeatureNum = Matrix.shape[1]
    
    Labels = Learner(Matrix)
    
    with open(Learner.__name__ + "_extra information_" + ".txt","w") as f:
        for i in xrange(len(Labels)):
            f.write(str(Labels[i][0]))
            f.write('\t')
            f.write(str(Labels[i][1]))
            f.write('\n')
            
    return Labels

MatrixAddress = "Your .txt Matrix Address"
Labels = Labeler(Learner, MatrixAddress)
