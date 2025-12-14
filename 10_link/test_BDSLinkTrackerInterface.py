import bdsim
import os

def constructor() :

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")
    tracker_l.Reset()

    return 0

def accessLinkObjects() :

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")
    bdsim_l   = tracker_l.GetBDSIMLink()
    bunch_l   = tracker_l.GetBunchLink()
    tracker_l2 = tracker_l.GetInstance()

    return 0

def accessors():

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")

    assert tracker_l.GetBDSIMConfigFile() == "./trackerInterface.gmad"
    assert tracker_l.GetReferenceParticlePDG() == 11
    assert tracker_l.GetReferenceParticleKineticEnergy() == 100
    assert tracker_l.GetRelativeEnergyCut() == 0.01
    assert tracker_l.GetReferenceIonCharge() == 1
    assert tracker_l.GetSeed() == 1234
    assert tracker_l.GetBatchMode() == True
    assert tracker_l.GetMinimumKineticEnergy() == tracker_l.GetReferenceParticleKineticEnergy() * tracker_l.GetRelativeEnergyCut()

    return 0

def noNeutralParticles():

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")

    # default is true
    assert tracker_l.GetNoNeutralParticles() == True

    # change to false and assert
    tracker_l.SetNoNeutralParticles(False)
    assert tracker_l.GetNoNeutralParticles() == False

    return 0

def referenceParticle():

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")
    rpd = tracker_l.GetReferenceParticleDefinition() # (r)eference (p)article (d)efinition

    assert rpd.Name() == "e-"
    assert rpd.PDGID() == 11
    assert rpd.KineticEnergy() == 100

    return 0

def addParticleXSuite():
    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")
    bunch_l = tracker_l.GetBunchLink()

    # reference particle like
    tracker_l.AddParticle(0,0, 0,0, 0,0, 1,1, 0, 0, 11)
    bunch_l.ClearParticles()

    # position/angles
    tracker_l.AddParticle(1,2, 3,4, 0,0, 1,1, 0, 0, 11)
    bunch_l.ClearParticles()

    # momentum deviation and ct

    # s?

    # particle id

    tracker_l.Reset()


def addParticleMomentum():
    pass

def test_constructor(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :

    code = make_bdsim_test_code(constructor, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    result = run_bdsim_test_code_as_subprocess(code)

def test_accessLinkObjects(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :

    code = make_bdsim_test_code(accessLinkObjects, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    result = run_bdsim_test_code_as_subprocess(code)

def test_accessors(make_bdsim_test_code, run_bdsim_test_code_as_subprocess):

    code = make_bdsim_test_code(accessors, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    result = run_bdsim_test_code_as_subprocess(code)

def test_noNeutralParticles(make_bdsim_test_code, run_bdsim_test_code_as_subprocess):

    code = make_bdsim_test_code(noNeutralParticles, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    result = run_bdsim_test_code_as_subprocess(code)

def test_referenceParticle(make_bdsim_test_code, run_bdsim_test_code_as_subprocess):

    code = make_bdsim_test_code(referenceParticle, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    result = run_bdsim_test_code_as_subprocess(code)
