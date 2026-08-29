import pybdsim
import numpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

class AnalysisClass(pybdsim.RootEventAnalysis.RootEventAnalyser) :
    def __init__(self) :
        super().__init__()

    def init(self):
        self.photon_energy = []
        self.photon_angle  = []

    def process(self) :
        for itraj in range(0, self.event.Trajectory.n, 1):
            pxpypz0 = self.event.Trajectory.pxpypz[itraj][0]  # first step momentum
            kineticEnergy = self.event.Trajectory.kineticEnergy[itraj][0]  # first step KE
            if self.event.Trajectory.parentID[itraj] != 0:
                self.photon_energy.append(kineticEnergy)
                self.photon_angle.append(pxpypz0[1] / pxpypz0[2])

    def terminate(self):
        self.photon_energy = numpy.array(self.photon_energy)
        self.photon_angle = numpy.array(self.photon_angle)/1e-3
        self.plot()

    def plot(self):
        xbins = numpy.logspace(numpy.log10(self.photon_energy.min()),numpy.log10(self.photon_energy.max()), 50)
        ybins = numpy.linspace(self.photon_angle.min(), self.photon_angle.max(), 50)
        counts, xedges, yedges = numpy.histogram2d(self.photon_energy, self.photon_angle, bins=[xbins,ybins])  # angle in mrad

        ax = plt.figure(figsize=(7, 7))

        plt.subplot(2,2,1)
        plt.pcolormesh(xedges, yedges, counts.T, cmap='viridis', norm=LogNorm())
        plt.gca().set_xscale('log')
        plt.xlabel('energy/GeV')
        plt.ylabel('angle/mrad')

        plt.subplot(2,2,2)
        plt.hist(self.photon_angle,50,range=(self.photon_angle.min(), self.photon_angle.max()), orientation='horizontal')

        plt.subplot(2,2,3)
        plt.hist(self.photon_energy,50,range=(self.photon_energy.min(), self.photon_energy.max()))

        self.add_persistent_data("photon_energy_angle", {"contents": counts,
                                                         "xedges": xedges,
                                                         "yedges": yedges})

        plt.show()

def analysis(file_name  = None) :
    a = pybdsim.RootEventAnalysis.RootEventAnalysis(file_name)
    ac = AnalysisClass()
    a.analysis(ac)
    return ac
