args <- commandArgs(trailingOnly = F) 
dir <- args[grep("--dir=", args)] 
dir <- substr(dir, 7, nchar(dir))#working directory
print(dir)
mat <- args[grep("--mat=", args)] 
mat <- substr(mat, 7, nchar(mat))#feature matrix file name
print(mat)
dist <- args[grep("--dist=", args)] 
dist <- substr(dist, 8, nchar(dist))#dist methods, NegDist, ExpSim, LinSim, CorSim, LinKernel
print(dist)
outputPrefix <- args[grep("--outputPrefix=", args)] 
outputPrefix <- substr(outputPrefix, 16, nchar(outputPrefix))#output file prefix
print(outputPrefix)
#sample command line: 
#R CMD BATCH --no-save --dir=/working/directory/ --mat=test.txt --dist=NegDist --outputPrefix=prefix apClust.R

library(apcluster)
mat <- as.matrix(read.delim(paste(dir, mat, sep = ""), header=FALSE, row.names=NULL))
#read features
apClust <- function(x, dist){
  switch (dist,
          NegDist = apcluster(negDistMat(r=2), x, details = T),
          ExpSim = apcluster(expSimMat, x, details = T),
          LinSim = apcluster(linSimMat, x, details = T),
          CorSim = apcluster(corSimMat, x, details = T),
          LinKernel = apcluster(linKernel, x, details = T))}
ap <- apClust(mat, dist)
#compute distance matrix
sink(paste(dir, outputPrefix, dist, "AP.txt", sep = ""))
show(ap)
dev.off()
#plot clustering result