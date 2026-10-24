import pybdsim
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

class AnalysisClass(pybdsim.RootEventAnalysis.RootEventAnalyser) :
    def __init__(self) :
        super().__init__()

    def init(self):
        self.process_data = {}
        self.histograms = {}

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
        for processType in self.process_data :
            for processSubType in self.process_data[processType] :
                # Total energy histogram
                counts, xedges = np.histogram(self.process_data[processType][processSubType]['totalEnergy'],bins=50)
                self.histograms[str(processType)+"_"+str(processSubType)+'_totalEnergy'] = {"type": "histo1d",
                                                                                            "contents": counts,
                                                                                            "xedges": xedges,
                                                                                            "xlabel": "total energy GeV",
                                                                                            "yscale": "log"}
                self.process_data[processType][processSubType].pop('totalEnergy')

                # Polar angle histogram
                counts, xedges = np.histogram(self.process_data[processType][processSubType]['theta'],bins=50, range=(0,np.pi))
                self.histograms[str(processType)+"_"+str(processSubType)+'_theta'] = {"type": "histo1d",
                                                                                      "contents": counts,
                                                                                      "xedges": xedges,
                                                                                      "xlabel": "theta",
                                                                                      "yscale": "log"}
                self.process_data[processType][processSubType].pop('theta')

                # Particle ID histogram
                partIDHist = {}
                for partID in  self.process_data[processType][processSubType]['partID'] :
                    if partID not in partIDHist :
                        partIDHist[partID] = 0

                    partIDHist[partID] += 1

                self.histograms[str(processType)+"_"+str(processSubType)+'_partID'] = {"type": "bar1d",
                                                                                       "contents": list(partIDHist.values()),
                                                                                       "xcentres": list(partIDHist.keys()),
                                                                                       "xlabel": "part ID"}
                self.process_data[processType][processSubType].pop('partID')

        self.add_persistent_data("process", self.process_data)
        self.add_persistent_data("histograms", self.histograms)

    def plot(self):
        pass

def analysis(file_name  = None) :
    a = pybdsim.RootEventAnalysis.RootEventAnalysis(file_name)
    ac = AnalysisClass()
    a.analysis(ac)
    return ac
