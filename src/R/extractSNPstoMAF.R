args <- commandArgs(trailingOnly = F)
dir <- args[grep("--dir=", args)]
dir <- substr(dir, 7, nchar(dir))#working directory
vcf <- args[grep("--vcf=", args)]
vcf <- substr(vcf, 7, nchar(vcf))#vcf file name
outputPrefix <- args[grep("--outputPrefix=", args)]
outputPrefix <- substr(outputPrefix, 16, nchar(outputPrefix))#output file prefix
#sample command line:
#R CMD BATCH --dir=/working/directory/ --vcf=test.vcf --outputPrefix=prefix extractSNPstoMAF.R.R

library(TxDb.Hsapiens.UCSC.hg19.knownGene)
library(BSgenome.Hsapiens.UCSC.hg19)
txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene

setwd(dir)
samples = samples(scanVcfHeader(vcf))#record sample names

SNP <- lapply(1:length(samples), function(i){
  print(i)
  print(samples[i])
  vcf <- readVcf(vcf, "hg19", ScanVcfParam(samples=samples[i]))
  print(table(geno(vcf)[["GT"]]))
  vcf = vcf[which(geno(vcf)[["GT"]]%in%c(".", "0/0") == F)]#filter by genotype
  SNV = vcf[isSNV(vcf)]#select SNV
  cSNV <- predictCoding(SNV, txdb, Hsapiens)#find amino acid coding changes for variants
  cSNV = cSNV[which(cSNV$FILTER == "PASS")]#keep SNVs passed filter
  cSNV = cSNV[which(cSNV$REFAA != cSNV$VARAA)]#keep aa-change SNV
  cSNV = as.data.frame(mcols(cSNV))
  VAR = paste(cSNV$GENEID, paste(cSNV$REFAA, cSNV$PROTEINLOC, cSNV$VARAA, sep = ""), sep = "_")
  dup = which(duplicated(VAR))
  na = grep("NA", VAR)
  ind = unique(c(dup, na))
  VAR[-1*ind]
  VAR = data.frame(GENEID = cSNV$GENEID, REFAA = cSNV$REFAA, PROTEINLOC = cSNV$PROTEINLOC, VARAA = cSNV$VARAA)
  VAR = VAR[-1*ind, ]
  write.table(VAR, file = paste(outputPrefix, "_", samples[i], ".txt", sep = ""), row.names = F)
})
names(SNP) = samples
save(SNP, file = paste(outputPrefix, ".rda", sep = ""))
