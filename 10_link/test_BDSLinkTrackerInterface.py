import bdsim

def constructors() :
    bds_ti = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad")
    bds_l   = bds_ti.GetBDSIMLink()
    bds_b   = bds_ti.GetBunchLink()
    bds_ti2 = bds_ti.GetInstance()

def test_constructors(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code = make_bdsim_test_code(constructors)
    result = run_bdsim_test_code_as_subprocess(code)

