import os

def bdsimSetup() :
    import bdsim

    p = bdsim.BDSParser.Instance("trackerInterface.gmad")
    o = p.GetOptions()
    o.batch = 1

    b = bdsim.BDSIM(p)
    b.BeamOn(1)

    return 0

def bdsimAccessors() :
    import bdsim

    p = bdsim.BDSParser.Instance("trackerInterface.gmad")
    b = p.GetBeam()
    bl = p.GetBeamline()
    d1 = p.GetElement("d1")
    o = p.GetOptions()


def test_bdsimSetup(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimSetup, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetup(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimAccessors, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)