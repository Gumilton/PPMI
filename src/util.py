
# This is to compare two .maf files
# the input takes two .maf files, with format as "Chrom\tPosition\tRef\tAlt\tGene\tPatient"
# output are lists of 1) unique in first file, 2) unique in second file and 3) common

def compareMAF(maf1, maf2, fileToWrite):
    m1 = set()
    m2 = []
    print("reading file 1")
    c = 0
    with open(maf1) as f:
        for l in f:
            c+= 1
            if c%100000 == 0:
                print(c)
            if l[0] != "#":
                l = str.split(l, "\t")
                m1.add((l[0], l[1], l[2], l[3], l[5]))

    print("reading file 2")
    c = 0
    f= open(maf2)
    writeFile = open(fileToWrite, "a")
    for l in f:
        c+= 1
        if c%100000 == 0:
            print(c)
        if l[0] != "#":
            l = str.split(l, "\t")
            if (l[0], l[1], l[2], l[3], l[5]) in m1:
                writeFile.write("\t".join(l))

    print ("Done")
    f.close()
    writeFile.close()


if __name__ == "__main__":
    compareMAF("../noquote_SNPA.maf", "../ppmi_av_exonic_variant.maf", fileToWrite="../intersect.maf")





