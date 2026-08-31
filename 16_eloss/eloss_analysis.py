import pybdsim
import numpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

class AnalysisClass(pybdsim.RootEventAnalysis.RootEventAnalyser) :
    def __init__(self) :
        super().__init__()

    def init(self):
        pass

    def process(self) :
        pass

    def terminate(self):
        self.plot()

    def plot(self):
        pass

def analysis(file_name  = None) :
    a = pybdsim.RootEventAnalysis.RootEventAnalysis(file_name)
    ac = AnalysisClass()
    a.analysis(ac)
    return ac
