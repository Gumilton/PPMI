library(VariantAnnotation)
library(TxDb.Hsapiens.UCSC.hg19.knownGene)
library(BSgenome.Hsapiens.UCSC.hg19)

txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene

SNPs <- function(txdb, vcf, species){
  samples = samples(scanVcfHeader(vcf))#record sample names
  SNP = lapply(1:length(samples), function(i){
    print(i)
    print(samples[i])
    vcf <- readVcf(vcf, species, ScanVcfParam(samples=samples[i]))
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
    write.table(VAR, file = paste(samples[i], "txt", sep = "."), row.names = F)
  })
  names(SNP) = samples
  SNP
}

SNP <- SNPs(txdb, "ppmi.feb.1.2015.vcf", "hg19")
save(SNP, file = "SNP.rda")
