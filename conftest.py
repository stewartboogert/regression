import pytest

import sys
import os
import subprocess
import inspect
import json
from pathlib import Path

def pytest_addoption(parser):
    parser.addoption("--length", action="store", default="short")

@pytest.fixture
def test_length(request):
    return request.config.getoption("--length")

def get_testname(testpath) :
    p = Path(testpath)
    stem = str(p.stem)
    base = str(p.parent).split('/')[-1]
    return base+"/"+stem

def get_testpath(testpath) :
    p = Path(testpath)
    return str(p.parent)

class test_nprimary :
    def __init__(self):
        self.nprimary = {"01_element/test_drift":{"short":2500,"medium":10000,"long":50000},
                         "01_element/test_quadrupole":{"short":2500,"medium":10000,"long":50000},
                         "01_element/test_rbend":{"short":2500,"medium":10000,"long":50000},
                         "01_element/test_sbend":{"short":2500,"medium":10000,"long":50000},
                         "01_element/test_sextupole":{"short":2500,"medium":10000,"long":50000}}

    def get_nprimary(self,testpath, length) :
        testname = get_testname(testpath)
        return self.nprimary[testname][length]

_test_nprimary = test_nprimary()

@pytest.fixture
def testlength_primaries():
    return _test_nprimary

class testdata_store :
    '''Class to store pytest output files for regression testing'''
    def __init__(self):
        self.testname = []
        self.testfile = []
        self.testfilepath = []
        self.testfiletype = []
        self.testnprimary = []

    def addtestoutput(self, testpath, filename, type, nprimary):
        testname = get_testname(testpath)
        path = get_testpath(testpath)
        self.testname.append(testname)
        self.testfile.append(filename)
        self.testfilepath.append(path)
        self.testfiletype.append(type)
        self.testnprimary.append(nprimary)

    def write(self):

        with open("testdata_store.dat","w") as f:
            json.dump({"testname":self.testname,
                       "testfile":self.testfile,
                       "testfilepath":self.testfilepath,
                       "testtfiletype":self.testfiletype,
                       "testnprimary":self.testnprimary}, f)

# Store that is persistent
_testdata_store = testdata_store()

@pytest.fixture
def testdata_store() :
    return _testdata_store

def pytest_sessionfinish(session, exitstatus):
    '''Write testdata_store to file'''
    _testdata_store.write()


@pytest.fixture
def make_bdsim_test_code() :
    return make_bdsim_test_code_func

def make_bdsim_test_code_func(func, args = "", dir="", functions=[]) :
    func_name = func.__name__

    code_to_run  = "import bdsim\n"
    code_to_run += "import pytest\n"
    code_to_run += "import sys\n"
    code_to_run += "import os\n"
    if dir != "" :
        code_to_run += 'os.chdir("' + dir + '")\n'
    for f in functions :
        code_to_run += inspect.getsource(func)
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

@pytest.fixture
def running_under_pytest() :
    return running_under_pytest_func

def running_under_pytest_func():
    return "PYTEST_CURRENT_TEST" in os.environ

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
