import os
import pytest
import pybdsim
from pathlib import Path

def test(test_length, testlength_primaries, testdata_store) :

    os.chdir(Path(__file__).resolve().parent)

    base_name     = "atf2"
    gmad_name     = "./01_atf2/linsige.gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"
    
    nprimary = testlength_primaries.get_nprimary(__file__,test_length)

    pybdsim.Run.Bdsim(gmad_name,base_name,nprimary,nprimary)
    pybdsim.Run.RebdsimOptics(root_name,optics_name)

    te = testdata_store.new_test_entry("99_machines/atf2",__file__,nprimary,0)
    te.add_output_file(os.path.dirname(__file__)+"/"+optics_name, "optics")

