import os
import pytest

pytestmark = pytest.mark.xfail(reason="requires bdsim")

def constructor() :
    import bdsim

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")
    tracker_l.Reset()

    return 0

def constructor_nofile() :
    import bdsim

    parser = bdsim.BDSParser()
    beam = parser.GetBeam()
    beam['energy'] = 1.0;
    beam['particleName'] = 'e-'

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance(parser)
    # tracker_l.Reset()

    return 0

def accessLinkObjects() :
    import bdsim

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")
    bdsim_l   = tracker_l.GetBDSIMLink()
    bunch_l   = tracker_l.GetBunchLink()
    tracker_l2 = tracker_l.GetInstance()

    return 0

def accessors():
    import bdsim

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
    import bdsim

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")

    # default is true
    assert tracker_l.GetNoNeutralParticles() == True

    # change to false and assert
    tracker_l.SetNoNeutralParticles(False)
    assert tracker_l.GetNoNeutralParticles() == False

    return 0

def referenceParticle():
    import bdsim

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")
    rpd = tracker_l.GetReferenceParticleDefinition() # (r)eference (p)article (d)efinition

    assert rpd.Name() == "e-"
    assert rpd.PDGID() == 11
    assert rpd.KineticEnergy() == 100

    return 0

def addParticleXSuite():
    import bdsim

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")
    bunch_l = tracker_l.GetBunchLink()

    # reference particle like
    tracker_l.AddParticle(0,0, 0,0, 0,0, 1,1, 0, 0, 11)
    p = bunch_l.GetNextParticleLocal()
    assert p.totalEnergy == pytest.approx(100.51099891)
    assert p.Position() == [0,0,0]
    assert p.Momentum() == [0,0,1]
    assert p.x == 0
    assert p.y == 0
    assert p.xp == 0
    assert p.yp == 0
    assert p.T == 0
    assert p.s == 0
    assert p.weight == 1
    bunch_l.ClearParticles()

    # position/angles
    tracker_l.AddParticle(1*bdsim.clhep.um, 2*bdsim.clhep.um, 3e-6,4e-6, 0,0, 1,1, 0, 0, 11)
    p = bunch_l.GetNextParticleLocal()
    assert p.totalEnergy == pytest.approx(100.51099891)
    assert p.Position() == [1e-3,2e-3,0]
    assert p.Momentum() == [3e-06, 4e-06, 0.9999999999875]
    assert p.x == 1e-3
    assert p.y == 2e-3
    assert p.xp == 3e-6
    assert p.yp == 4e-6
    assert p.T == 0
    assert p.s == 0
    assert p.weight == 1
    bunch_l.ClearParticles()

    # momentum deviation
    tracker_l.AddParticle(0,0, 0,0, 0, 0.05, 1,1, 0, 0, 11)
    p = bunch_l.GetNextParticleLocal()
    assert p.totalEnergy == pytest.approx(105.53642205201491)
    assert p.Position() == [0,0,0]
    assert p.Momentum() == [0,0,1]
    assert p.x == 0
    assert p.y == 0
    assert p.xp == 0
    assert p.yp == 0
    assert p.T == 0
    assert p.s == 0
    assert p.weight == 1
    bunch_l.ClearParticles()

    # ct
    tracker_l.AddParticle(0,0, 0,0, 1e-6, 0, 1,1, 0, 0, 11)
    p = bunch_l.GetNextParticleLocal()
    assert p.totalEnergy == pytest.approx(100.51099891)
    assert p.Position() == [0,0,0]
    assert p.Momentum() == [0,0,1]
    assert p.x == 0
    assert p.y == 0
    assert p.xp == 0
    assert p.yp == 0
    assert p.T == pytest.approx(-3.335684061233747e-06)
    assert p.s == 0
    assert p.weight == 1
    bunch_l.ClearParticles()

    # charge ratio
    tracker_l.AddParticle(0,0, 0,0, 0,0, 1,0.5, 0, 0, 11)
    p = bunch_l.GetNextParticleLocal()
    assert p.totalEnergy == pytest.approx(50.25744785985477)
    assert p.Position() == [0,0,0]
    assert p.Momentum() == [0,0,1]
    assert p.x == 0
    assert p.y == 0
    assert p.xp == 0
    assert p.yp == 0
    assert p.T == 0
    assert p.s == 0
    assert p.weight == 1
    bunch_l.ClearParticles()

    # chi
    tracker_l.AddParticle(0,0, 0,0, 0,0, 2,1, 0, 0, 11)
    p = bunch_l.GetNextParticleLocal()
    assert p.totalEnergy == pytest.approx(50.25744785985477)
    assert p.Position() == [0,0,0]
    assert p.Momentum() == [0,0,1]
    assert p.x == 0
    assert p.y == 0
    assert p.xp == 0
    assert p.yp == 0
    assert p.T == 0
    assert p.s == 0
    assert p.weight == 1
    bunch_l.ClearParticles()

    # particle id
    tracker_l.AddParticle(0,0, 0,0, 0,0, 1,1, 0, 0, 2212) # electron -> proton
    p = bunch_l.GetNextParticleLocal()
    assert p.totalEnergy == pytest.approx(943.6400638808593) # expect total energy to change
    assert p.Position() == [0,0,0]
    assert p.Momentum() == [0,0,1]
    assert p.x == 0
    assert p.y == 0
    assert p.xp == 0
    assert p.yp == 0
    assert p.T == 0
    assert p.s == 0
    assert p.weight == 1
    bunch_l.ClearParticles()
    tracker_l.Reset()

    return 0

def addParticleMomentum():
    import bdsim
    import numpy as np

    def polarToCartesianMomenta(theta, phi, momentum):
        px = momentum*np.sin(theta)*np.cos(phi)
        py = momentum*np.sin(theta)*np.sin(phi)
        pz = momentum*np.cos(theta)

        return [float(px), float(py), float(pz)]

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")
    bunch_l = tracker_l.GetBunchLink()
    rp = tracker_l.GetReferenceParticleDefinition()

    # reference particle like
    tracker_l.AddParticle(0,0,  0,0,rp.Momentum(),  0,0,  0,11)
    p = bunch_l.GetNextParticleLocal()
    assert p.totalEnergy == pytest.approx(100.51099891)
    assert p.Position() == [0,0,0]
    assert p.Momentum() == [0,0,1]
    assert p.x == 0
    assert p.y == 0
    assert p.xp == 0
    assert p.yp == 0
    assert p.T == 0
    assert p.s == 0
    assert p.weight == 1
    bunch_l.ClearParticles()

    # position
    tracker_l.AddParticle(1*bdsim.clhep.um, 2*bdsim.clhep.um,
                          0,0,rp.Momentum(),
                          0,0,
                          0,11)
    p = bunch_l.GetNextParticleLocal()
    assert p.totalEnergy == pytest.approx(100.51099891)
    assert p.Position() == [1e-3,2e-3,0]
    assert p.Momentum() == [0,0,1]
    assert p.x == 1e-3
    assert p.y == 2e-3
    assert p.xp == 0
    assert p.yp == 0
    assert p.T == 0
    assert p.s == 0
    assert p.weight == 1
    bunch_l.ClearParticles()

    # momentum
    mom = polarToCartesianMomenta(0.01, 0, rp.Momentum())
    tracker_l.AddParticle(0,0,  *mom,  0,0,  0,11)
    p = bunch_l.GetNextParticleLocal()
    assert p.totalEnergy == pytest.approx(100.51099891)
    assert p.Position() == [0,0,0]
    assert p.Momentum() == pytest.approx([0.009999833334166664, 0.0, 0.9999500004166654])
    assert p.x == 0
    assert p.y == 0
    assert p.xp == 0.009999833334166664
    assert p.yp == 0
    assert p.T == 0
    assert p.s == 0
    assert p.weight == 1
    bunch_l.ClearParticles()

    # time
    tracker_l.AddParticle(0,0,  0,0,rp.Momentum(),  1e-8,0,  0,11)
    p = bunch_l.GetNextParticleLocal()
    assert p.totalEnergy == pytest.approx(100.51099891)
    assert p.Position() == [0,0,0]
    assert p.Momentum() == [0.0, 0.0, 1]
    assert p.x == 0
    assert p.y == 0
    assert p.xp == 0
    assert p.yp == 0
    assert p.T == 1e-8
    assert p.s == 0
    assert p.weight == 1
    bunch_l.ClearParticles()

    tracker_l.Reset()
    return 0

def pdgAccessors() :
    import bdsim

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")

    assert tracker_l.GetMassRatio(2212) == pytest.approx(1836.1526700712534)
    assert tracker_l.GetChargeRatio(2212) == -1
    assert tracker_l.GetChi(2212) == pytest.approx(-0.0005446170224838625)

    return 0

def test_constructor(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :


    code = make_bdsim_test_code(constructor, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    result = run_bdsim_test_code_as_subprocess(code)

def test_constructor_nofile(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :

    code = make_bdsim_test_code(constructor_nofile, args="", dir=os.path.dirname(os.path.abspath(__file__)))
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

def test_addParticleXSuite(make_bdsim_test_code, run_bdsim_test_code_as_subprocess):

    code = make_bdsim_test_code(addParticleXSuite, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    result = run_bdsim_test_code_as_subprocess(code)

def test_addParticleMomentum(make_bdsim_test_code, run_bdsim_test_code_as_subprocess):

    code = make_bdsim_test_code(addParticleMomentum, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    result = run_bdsim_test_code_as_subprocess(code)

def test_pdgAccessors(make_bdsim_test_code, run_bdsim_test_code_as_subprocess):

    code = make_bdsim_test_code(pdgAccessors, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    result = run_bdsim_test_code_as_subprocess(code)