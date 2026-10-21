import pybdsim
import numpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

class AnalysisClass(pybdsim.RootEventAnalysis.RootEventAnalyser) :
    def __init__(self) :
        super().__init__()

    def init(self):
        self.process_data = {}

    def process(self) :
        pfh = self.event.PrimaryFirstHit
        s   = self.event.GetSamplerS("s0.")

        if pfh.n == 0 :
            return

        processType = pfh.postStepProcessType[0]
        processSubType = pfh.postStepProcessSubType[0]

        if processType not in self.process_data :
            self.process_data[processType] = {}

        if processSubType not in self.process_data[processType] :
            self.process_data[processType][processSubType] = {}
            self.process_data[processType][processSubType]['n'] = 0
            self.process_data[processType][processSubType]['totalEnergy'] = []
            self.process_data[processType][processSubType]['theta'] = []
            self.process_data[processType][processSubType]['partID'] = []

        process_data = self.process_data[processType][processSubType]
        process_data['n'] += 1

        for i in range(1,s.n) :
            self.process_data[processType][processSubType]['totalEnergy'].append(s.totalEnergy[i])
            self.process_data[processType][processSubType]['theta'].append(s.theta[i])
            self.process_data[processType][processSubType]['partID'].append(s.partID[i])

    def terminate(self):
        self.add_persistent_data("process", self.process_data)

    def plot(self):
        pass

    def plot(self):
        pass

def analysis(file_name  = None) :
    a = pybdsim.RootEventAnalysis.RootEventAnalysis(file_name)
    ac = AnalysisClass()
    a.analysis(ac)
    return ac
