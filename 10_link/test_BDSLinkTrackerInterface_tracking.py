# pip install pytest-xdist
# pytest -n auto
import pytest
import bdsim
from pathlib import Path

def addLinkElement() :
    import bdsim
    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad", 2212, 5*bdsim.clhep.TeV, 0.01, 1234, 1, 1)

    # create element
    e = bdsim.Element()
    e.name = "drift1"
    e.type = bdsim.elementtype.ElementType.DRIFT
    e.l = 1.0

    # add element
    bdsim_l = tracker_l.GetBDSIMLink()
    bdsim_l.AddLinkElement(e)

    # select element
    bdsim_l.SelectLinkElement("drift1")

    # reference particle
    rp = tracker_l.GetReferenceParticleDefinition()

    # add particle
    tracker_l.AddParticle(0,  0,  0,  0,  rp.Momentum(), 0.,  0.,  0, 2212)  # pdgid;
    tracker_l.Reset()

    return 0

@pytest.mark.skip(reason="Not implemented yet")
def test_addLinkElement(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code = make_bdsim_test_code(construct)
    result = run_bdsim_test_code_as_subprocess(code)

def referenceParticle(simple_bdslink) :
    tracker_l = simple_bdslink(gmadFile = str(Path(__file__).parent / "trackerInterface.gmad"))
    bdsim_l = tracker_l.GetBDSIMLink()
    bdsim_l.Reset()

    return 0

@pytest.mark.skip(reason="Not implemented yet")
def test_referenceParticle(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code = make_bdsim_test_code(referenceParticle)
    result = run_bdsim_test_code_as_subprocess(code)

def beamOn(simple_bdslink) :
    tracker_l = simple_bdslink(gmadFile = str(Path(__file__).parent / "trackerInterface.gmad"))
    bdsim_l = tracker_l.GetBDSIMLink()
    bdsim_l.BeamOn(1)
    tracker_l.Reset()
    return 0

@pytest.mark.skip(reason="Not implemented yet")
def test_beamOn(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code = make_bdsim_test_code(beamOn)
    result = run_bdsim_test_code_as_subprocess(code)