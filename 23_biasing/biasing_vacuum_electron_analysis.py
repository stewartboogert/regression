import pybdsim

class AnalysisClass(pybdsim.RootEventAnalysis.RootEventAnalyser) :
    def __init__(self) :
        super().__init__()

    def init(self):
        self.npfh = 0
        self.pfh_S = []
        self.pfh_weight = []

    def process(self) :
        pfh_e = self.event.PrimaryFirstHit
        self.npfh += pfh_e.n
        for i, S in enumerate(pfh_e.S):
            self.pfh_S.append(S)
            self.pfh_weight.append(pfh_e.weight[i])

    def terminate(self):
        self.add_persistent_data("npfh", self.npfh)

    def plot(self):
        pass

def analysis(file_name  = None) :
    a = pybdsim.RootEventAnalysis.RootEventAnalysis(file_name)
    ac = AnalysisClass()
    a.analysis(ac)
    return ac