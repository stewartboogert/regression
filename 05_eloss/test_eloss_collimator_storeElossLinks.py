import pytest
import pybdsim
import os

def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store) :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "eloss_collimator_storeElossLinks"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"
    
    data = {
        'LENGTH': '1.0',
        'BEAM_ENERGY' : '1'
    }

    # get number of primaries to simulate
    nprimary = testlength_primaries.get_nprimary(__file__,test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,500,1)

    te = testdata_store.new_test_entry("05_eloss/eloss_collimator_storeElossLinks", __file__, nprimary, 0)
