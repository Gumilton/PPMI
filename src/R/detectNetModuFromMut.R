args <- commandArgs(trailingOnly = F) 
dir <- args[grep("--dir=", args)] 
dir <- substr(dir, 7, nchar(dir))#working directory
print(dir)
maf <- args[grep("--maf=", args)] 
maf <- substr(maf, 7, nchar(maf))#maf file name
print(maf)
method <- args[grep("--method=", args)]
method <- substr(method, 10, nchar(method))#method option, edgeBetweenness, fastgreedy, spinglass and walktrap
print(method)
outputPrefix <- args[grep("--outputPrefix=", args)] 
outputPrefix <- substr(outputPrefix, 16, nchar(outputPrefix))#output file prefix
print(outputPrefix)
plot <- args[grep("--plot=", args)] 
plot <- substr(plot, 8, nchar(plot))#plot option
print(plot)
#sample command line: 
#R CMD BATCH --dir=/working/directory/ --maf=test.maf --outputPrefix=prefix --plot=T extractSNPstoMAF.R


library(igraph)
mut <- read.delim(paste(dir, maf, sep = ""), header=FALSE, row.names=NULL)
#read mutations that cause amino acid change
bipartite <- data.frame(item = paste(mut[, 3], mut[, 2], mut[, 4], sep = ""), patient = mut[, 6])
bipartite <- graph.data.frame(bipartite, directed = F)
#build bipartite graph
modularity <- function(x, method){
  switch (method,
          edgeBetweenness = edge.betweenness.community(bipartite, weights = NULL),
          fastgreedy = fastgreedy.community(bipartite, weights = NULL),
          spinglass = spinglass.community(bipartite, weights = NULL),#conected graph only
          walktrap = walktrap.community(bipartite, weights = NULL))}
mod <- modularity(bipartite, method)
save(bipartite, mod, file = paste(dir, outputPrefix, ".rda", sep = ""))
#determine modularity
if (plot){
 pdf(paste(dir, outputPrefix, "Bipartite.pdf", sep = ""), width = 50, height = 50)
 keyMutation = c()#define subtype-feature mutations
 vertexColor <- mod$membership
 vertexColor[match(keyMutation, mod$names)] <- "Red"#color according to subtypes, keyMutation in red
 vertexSize <- rep(5, length(mod$names))
 vertexSize[match(keyMutation, mod$names)] <- 15
 vertexSize[grep("PPMI", mod$names)] <- 10#size, keyMutation > patient > mutation
 vertexShape <- rep("circle", length(mod$names))
 vertexShape[match(keyMutation, mod$names)] <- "square"#shape, keyMutation in suqare, anything else in circle
 vertexLabel <- character(length(mod$names))
 vertexLabel[match(keyMutation, mod$names)] <- keyMutation#only label keyMutation
 plot.igraph(bipartite, vertex.color = vertexColor, vertex.frame.color = NA,
             vertex.size = vertexSize, vertex.shape = vertexShape, vertex.label.cex = 1,
             vertex.label = vertexLabel, main = method)
 legend("topleft", legend = c("patient", "mut", "keyMut"), pch = c(19, 20, 15), border = NA, bty = "n")
 dev.off()
}
#plot bipartite graph

########
#Reference: Ciriello, Nature Genetics, 2013
########
