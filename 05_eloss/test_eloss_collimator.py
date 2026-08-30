import pytest
import pybdsim
import os

import eloss_analysis

def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store) :

    os.chdir(os.path.dirname(__file__))
    
    base_name        = "eloss_collimator"
    template_name    = base_name+".tpl"
    gmad_name        = base_name+".gmad"
    root_name        = base_name+".root"
    rebdsimIn_name   = base_name+".txt"
    rebdsimOut_name  = base_name+"_rebdsim.root"
    analsisJson_name = base_name+"_analysis.json"
    
    data = {
        'LENGTH': '1.0',
        'BEAM_ENERGY' : '1'
    }

    # get number of primaries to simulate
    nprimary = testlength_primaries.get_nprimary(__file__,test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,nprimary,1)
    pybdsim.Run.Rebdsim(rebdsimIn_name, root_name, rebdsimOut_name),

    ac = eloss_analysis.analysis(root_name)
    ac.write_persistent_data(analsisJson_name)

    te = testdata_store.new_test_entry("05_eloss/eloss_collimator", __file__, nprimary, 0)
    te.add_output_file(os.path.dirname(__file__)+"/"+rebdsimOut_name, "rebdsim")