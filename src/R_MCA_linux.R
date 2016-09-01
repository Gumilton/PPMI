#!/usr/bin/env R
args = commandArgs(trailingOnly=TRUE)
ReductDim = as.integer(args[1])
Address = args[2] #.txt

"Begin!"
Mat <- read.delim(Address, header=FALSE,stringsAsFactors = TRUE)
#Mat = Mat[c(1:145,147:210,212:356,358:421,423:428,430:545,547:645),]  # Outlier: 357,422,146,546,211,429
library(FactoMineR)
X <- Mat
result = MCA(X, ncp = ReductDim, ind.sup = NULL, quanti.sup = NULL,
             quali.sup = NULL, excl=NULL, graph = TRUE,
             level.ventil = 0, axes = c(1,2), row.w = NULL,
             method="Indicator", na.method="NA", tab.disj=NULL)
coord = result$ind$coord
OutName = paste(paste(substr(Address,1,nchar(Address)-4),ReductDim,sep="_"),"txt",sep=".")
write.table(coord,OutName , sep="\t",row.names = FALSE,col.names = F) #.txt
"Finished!"