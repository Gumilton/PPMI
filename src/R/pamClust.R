args <- commandArgs(trailingOnly = F) 
dir <- args[grep("--dir=", args)] 
dir <- substr(dir, 7, nchar(dir))#working directory
print(dir)
mat <- args[grep("--mat=", args)] 
mat <- substr(mat, 7, nchar(mat))#feature matrix file name
print(mat)
k <- args[grep("--k=", args)] 
k <- substr(k, 5, nchar(k))#k clusters
print(k)
dist <- args[grep("--dist=", args)] 
dist <- substr(dist, 8, nchar(dist))#dist methods, Pearson, Spearman, and Euclidean
print(dist)
consensus <- args[grep("--consensus=", args)]
consensus <- substr(consensus, 13, nchar(consensus))#method option, kmeans, pam
print(consensus)
outputPrefix <- args[grep("--outputPrefix=", args)] 
outputPrefix <- substr(outputPrefix, 16, nchar(outputPrefix))#output file prefix
print(outputPrefix)
#sample command line: 
#R CMD BATCH --no-save --dir=/working/directory/ --mat=test.txt --k=10 --dist=pearson --consensus=T --outputPrefix=prefix pamClust.R

library(cluster)
library(ConsensusClusterPlus)
mat <- as.matrix(read.delim(paste(dir, mat, sep = ""), header=FALSE, row.names=NULL))
#read features
if (consensus){
  pdf(paste(dir, outputPrefix, dist, "ConsensusPam.pdf", sep = ""))
  ConsensusClusterPlus(mat, maxK = k, reps = 500, clusterAlg = "pam", distance = tolower(dist))
  dev.off()
}else{
  distance <- function(x, dist){
    switch (dist,
            Pearson = cor(t(x), use = "everything", method = "pearson"),
            Spearman = cor(t(x), use = "everything", method = "spearman"),
            Euclidean = dist(x, method = "euclidean"))}
  d <- distance(mat, dist)
  #compute distance matrix
  pdf(paste(dir, outputPrefix, dist, "Pam.pdf", sep = ""), width = 20, height = 20)
  par(mfrow = c(4, 4))
  for (i in 2:k){
    plot(pam(d, i))
  }
  dev.off()
}
