# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 09:08:13 2016

@author: JH Sun
"""
"""
 Different Matrices with 100 feature dimensions preprocessed with differet ways will be passed to you.
 You may subset it with the first (Because the more important the feature is, the smaller its index will be) 
   several features (eg. 10 or 30 or 50) locally before passing it to the Learner.
"""

# common packages.
import numpy as np
import matplotlib.pylab as plt
import scipy
import sklearn
from sklearn import cluster

def outlier_handler():
# for combine learner labels and outlier labels
    pass

def LabelReader(LabelsAddress):
    with open(LabelsAddress, 'r') as f:
        Labels = f.read().splitlines()
    for i in xrange(len(Labels)):
        Labels[i] = (Labels[i].split('\t'))
        Labels[i] = [float(j) for j in Labels[i]]

    Labels = np.array(Labels)  
def tinker(Matrix):
    TinkerSet = (356, 421)
    #TinkerSet = ()
    Matrix = np.delete(Matrix, TinkerSet, axis = 0)
    return Matrix

def MatrixReader(MatrixAddress):
    import numpy as np    
    with open(MatrixAddress, 'r') as f:
        Matrix = f.read().splitlines()
        
    for i in xrange(len(Matrix)):
        Matrix[i] = (Matrix[i].split('\t'))
        Matrix[i] = [float(j) for j in Matrix[i]]

    Matrix = np.array(Matrix)
    #Matrix = tinker(Matrix)
    return Matrix
    
def WardAgglLearner(Matrix, option = {}):    # Matrix is a numpy.ndarray, dtype = float, shape = (PatientNum, FeatureNum).

    clustering = cluster.AgglomerativeClustering(linkage='ward', n_clusters=5)
    clustering.fit(Matrix)
    return np.asarray(zip(range(len(clustering.labels_)),clustering.labels_ + 1))

def AverageAgglLearner(Matrix, option = {}):    # Matrix is a numpy.ndarray, dtype = float, shape = (PatientNum, FeatureNum).

    clustering = cluster.AgglomerativeClustering(linkage='average', n_clusters=3)
    clustering.fit(Matrix)
    return np.asarray(zip(range(len(clustering.labels_)),clustering.labels_ + 1))

def CompAggLearner(Matrix, option = {}):    # Matrix is a numpy.ndarray, dtype = float, shape = (PatientNum, FeatureNum).

    clustering = cluster.AgglomerativeClustering(linkage='complete', n_clusters=3)
    clustering.fit(Matrix)
    return np.asarray(zip(range(len(clustering.labels_)),clustering.labels_ + 1))

def DBSCANLearner(Matrix, option = {}):    # Matrix is a numpy.ndarray, dtype = float, shape = (PatientNum, FeatureNum).

    dbscan = cluster.DBSCAN(eps=.3)
    dbscan.fit(Matrix)
    return np.asarray(zip(range(len(dbscan.labels_)),dbscan.labels_ + 1))

def Visualization(MatrixAddress, Learner, Labels, dim):     #dim = 2 or 3
    """
    Visualization method
    """
    import matplotlib.pylab as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    # Parameters:
    s = 35
    alpha = 0.5
    
    
    Matrix = MatrixReader(MatrixAddress)[:,0:dim]
    
    if dim == 2:
        fig = plt.figure()
        plt.scatter(Matrix[:,0], Matrix[:,1], s=s, c=Labels[:,1]/float(Labels[:,1].max()), marker='o', cmap='prism', norm=None, vmin=None, vmax=None, alpha=alpha, linewidths=None, verts=None, edgecolors=None, hold=None, data=None)
        # plt.savefig('Ward_slice100_nc5.png', dpi=200)
        plt.show()

    elif dim == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(Matrix[:,0], Matrix[:,1], Matrix[:,2], s = s, c=Labels[:,1]/float(Labels[:,1].max()), marker='o', cmap='prism', norm=None, vmin=None, vmax=None, alpha=alpha)
        plt.show()

def Labeler(Learner, MatrixAddress):    # MatrixAddress is the address of reducted feature matrix .txt file
    Matrix = MatrixReader(MatrixAddress)    
    PatientNum = Matrix.shape[0]
    FeatureNum = Matrix.shape[1]
    
    SliceNum = FeatureNum   # May be changed to subset features!
    Matrix = Matrix[:,0:SliceNum]
    Labels = Learner(Matrix)
    # print(Labels)
    extra_information = "-"     # Necessary extra information for labeling and clustering, such as clustering parameters, etc.
    with open(Learner.__name__ + "_" + extra_information + "_" + "slice" + str(SliceNum) + ".txt","w") as f:
        for i in xrange(len(Labels)):
            f.write(str(Labels[i][0]))
            f.write('\t')
            f.write(str(Labels[i][1]))
            f.write('\n')
    return Labels

   
if __name__ == "__main__":
    MatrixAddress = "../Mat_Mannual_1_645_100.txt"
    Labels = Labeler(WardAgglLearner, MatrixAddress)
    Visualization(MatrixAddress, WardAgglLearner, Labels, 2)

"""
 Alternative way to get labels:
"""
# LabelsAddress = " "
# Labels = LabelReader(LabelsAddress)

