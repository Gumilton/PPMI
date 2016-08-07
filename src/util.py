
# This is to compare two .maf files
# the input takes two .maf files, with format as "Chrom\tPosition\tRef\tAlt\tGene\tPatient"
# output are lists of 1) unique in first file, 2) unique in second file and 3) common

def compareMAF(maf1, maf2):
    m1 = []
    m2 = []
    with open(maf1) as f:
        m1 = [l for l in f]

    with open(maf2) as f:
        m2 = [l for l in f]

    return list(set(m1) - set(m2)), list(set(m2) - set(m2)), list(set(m1) & set(m2))





