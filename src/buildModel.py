import subprocess
import util

class Model():

    def __init__(self):
        pass


    def extractMAF(self):
        subprocess.call("Rscript")

    def compareMAF(self, maf1, maf2):
        m1_uni, m2_uni, common = util.compareMAF(maf1, maf2)