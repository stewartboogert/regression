import pytest

import sys
import subprocess
import inspect

@pytest.fixture
def make_bdsim_test_code() :
    return make_bdsim_test_code_func

def make_bdsim_test_code_func(func, args = "", dir="") :
    func_name = func.__name__

    code_to_run  = "import bdsim\n"
    code_to_run += "import pytest\n"
    code_to_run += "import sys\n"
    code_to_run += "import os\n"
    if dir != "" :
        code_to_run += 'os.chdir("' + dir + '")\n'
    code_to_run += inspect.getsource(func)
    code_to_run += "ret ="+func_name+"("+args+")\n"
    code_to_run += "sys.exit(ret)"

    return code_to_run

@pytest.fixture
def run_bdsim_test_code_as_subprocess():
    return run_bdsim_test_code_as_subprocess_func

def run_bdsim_test_code_as_subprocess_func(code) :
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

@pytest.fixture
def simple_bdslink() :
    return simple_bdslink_code

def simple_bdslink_code(gmadFile = "./trackerInterface.gmad",
                        pdgID = 2212,
                        kineticEnergy = 5e6,
                        relativeEnergyCutIn = 0.01,
                        seed=1234,
                        referenceIonCharge=1,
                        batchMode=True) :

    import bdsim
    bds_ti = bdsim.BDSLinkTrackerInterface.GetInstance(gmadFile,
                                                       pdgID,
                                                       kineticEnergy,
                                                       relativeEnergyCutIn,
                                                       seed,
                                                       referenceIonCharge,
                                                       batchMode)

    # create element
    e = bdsim.Element()
    e.name = "drift1"
    e.type = bdsim.elementtype.ElementType.DRIFT
    e.l = 1.0

    # add element
    l = bds_ti.GetBDSIMLink()
    l.AddLinkElement(e)

    # select element
    l.SelectLinkElement("drift1")

    # reference particle
    rp = bds_ti.GetReferenceParticleDefinition()

    # add particle
    bds_ti.AddParticle(0, # x
                       0, # y
                       0, # px
                       0, # py
                       rp.Momentum(), # pz
                       0., # t
                       0., # s
                       0, # trackid
                       2212) # pdgid;

    return bds_ti