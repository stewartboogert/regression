import pytest
import pybdsim

def test(test_length, testlength_primaries, testdata_store) :

    os.chdir(os.path.dirname(__file__))

    base_name     = "atf2"
    gmad_name     = "./01_atf2/linsige.gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"
    
    nprimary = testlength_primaries.get_nprimary(__file__,test_length)

    pybdsim.Run.Bdsim(gmad_name,base_name,nprimary,nprimary)
    pybdsim.Run.RebdsimOptics(root_name,optics_name)

    testdata_store.add_test_output(__file__,optics_name,"optics", nprimary)
