import subprocess
import util

class Model():

    def __init__(self):
        pass


    def extractMAF(self, path_to_file, filename, output_prefix):
        subprocess.call(["Rscript", "--vanilla", path_to_file, filename, output_prefix])

    def compareMAF(self, maf1, maf2):
        m1_uni, m2_uni, common = util.compareMAF(maf1, maf2)

    def ANNOVAR1(self, path_to_software, path_to_file, output_prefix):
        subprocess.call(["perl", path_to_software, "convert2annovar.pl", "-format", "vcf4", path_to_file, "-outfile", output_prefix, "-allsample", '-include', '-withfreq', '--comment', "--includeinfo"])

    def ANNOVAR2(self, path_to_software, path_to_file):
        subprocess.call(["perl", path_to_software, "annotate_variation.pl", "-geneanno", "-buildver", "hg19", path_to_file, path_to_software+"/humandb/", "--comment", "--includeInfo"])

    def annova2maf(self, path_to_file, path_to_header, mafFileName, patientIndexStart= 20):

        maf = open(mafFileName, "a")
        h = str.split(open(path_to_header).readline())
        k = 0
        for l in open(path_to_file):
            l = str.split(l, '\t')
            # "Chrom\tPosition\tRef\tAlt\tGene\tPatient"
            if k%1000 == 0:
                print("Processing " + str(k))

            if l[17] != "PASS":
                continue
            id = "\t".join([l[3],l[4],l[6],l[7],l[2]])
            for p in range(patientIndexStart, 665):
                gt = str.split(l[p], ":")[0]
                if gt != "0/0" and gt != "./.":
                    maf.write(id+"\t"+h[p]+"\n")
            k += 1

        maf.close()


    def writeMaf(self, maf, filename):
        print("Write into maf")
        f = open(filename, "w")
        f.write("\n".join(maf))



if __name__ == "__main__":
    m = Model()
    m.annova2maf(path_to_file="../ppmi.feb.1.2015.avinput.exonic_variant_function", path_to_header= "../av_header.txt", mafFileName="../ppmi_av_exonic_variant.maf")