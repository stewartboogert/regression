# pip install pytest-xdist
# pytest -n auto
import pytest
import bdsim
from pathlib import Path

def test(simple_bdslink) :
    tracker_l = simple_bdslink(gmadFile = str(Path(__file__).parent / "trackerInterface.gmad"))

def test_referenceParticle(simple_bdslink) :
    tracker_l = simple_bdslink(gmadFile = str(Path(__file__).parent / "trackerInterface.gmad"))
    bdsim_l = tracker_l.GetBDSIMLink()

def beamOn(simple_bdslink) :
    tracker_l = simple_bdslink(gmadFile = str(Path(__file__).parent / "trackerInterface.gmad"))
    bdsim_l = tracker_l.GetBDSIMLink()
    bdsim_l.BeamOn(1)
    tracker_l.Reset()

def test_beamOn(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code = make_bdsim_test_code(beamOn)
    result = run_bdsim_test_code_as_subprocess(code)