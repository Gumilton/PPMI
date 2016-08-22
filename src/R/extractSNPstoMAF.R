args <- commandArgs(trailingOnly = F) 
dir <- args[grep("--dir=", args)] 
dir <- substr(dir, 7, nchar(dir))#working directory
print(dir)
vcf <- args[grep("--vcf=", args)] 
vcf <- substr(vcf, 7, nchar(vcf))#vcf file name
print(vcf)
mode <- args[grep("--mode=", args)]
mode <- substr(mode, 8, nchar(mode))#SNP option, C:coding change, A:AA change
print(mode)
outputPrefix <- args[grep("--outputPrefix=", args)] 
outputPrefix <- substr(outputPrefix, 16, nchar(outputPrefix))#output file prefix
print(outputPrefix)
#sample command line: 
#R CMD BATCH --dir=/working/directory/ --vcf=test.vcf --outputPrefix=prefix --SNP=A extractSNPstoMAF.R


library(VariantAnnotation)
library(TxDb.Hsapiens.UCSC.hg19.knownGene)
library(BSgenome.Hsapiens.UCSC.hg19)
txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene

setwd(dir)
samples = samples(scanVcfHeader(vcf))#record sample names
SNP <- lapply(1:length(samples), function(i, vcf, mode){
  print(samples[i])
  vcf <- readVcf(vcf, "hg19", ScanVcfParam(samples=samples[i]))
  print(table(geno(vcf)[["GT"]]))
  vcf = vcf[which(geno(vcf)[["GT"]]%in%c(".", "0/0", "0|0") == F)]#filter by genotype
  SNP = vcf[isSNV(vcf)]#select SNP
  SNP = SNP[which(mcols(SNP)$FILTER == "PASS")]#keep SNPs passed filter
  if (mode == "C"){
    SNP <- predictCoding(SNP, txdb, Hsapiens)#find amino acid coding changes for variants
  }else if(mode == "A"){
    SNP <- predictCoding(SNP, txdb, Hsapiens)#find amino acid coding changes for variants
    SNP = SNP[which(as.character(mcols(SNP)$REFAA) != as.character(mcols(SNP)$VARAA))]#keep aa-change SNP
  }
  VAR = data.frame(Chrom=as.character(seqnames(SNP)), Position=start(SNP),
                 Ref=as.character(SNP$REF), Alt=as.character(SNP$ALT@unlistData),
                 Gene=SNP$GENEID, Patient=samples[i])
  VAR = VAR[!duplicated(VAR), ]
  VAR
}, vcf=vcf, mode=mode)
SNP = do.call(rbind, SNP)
save(SNP, file = "SNP.rda")
write.table(SNP, file = paste(outputPrefix, ".maf", sep = ""), row.names = F, sep = "\t")
