import subprocess
import util

class Model():

    def __init__(self):
        pass


    def extractMAF(self, path_to_file, filename, output_prefix):
        subprocess.call(["Rscript", "--vanilla", path_to_file, filename, output_prefix])

    def compareMAF(self, maf1, maf2):
        m1_uni, m2_uni, common = util.compareMAF(maf1, maf2)