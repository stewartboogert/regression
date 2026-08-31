import pytest
import pybdsim
import os
from pathlib import Path


def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store) :

    os.chdir(Path(__file__).resolve().parent)
    
    base_name     = "laserwire_compton_multiStep"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    l  = 2.0 
    data = {
        'LASER_ENERGY': '150',
        'BEAM_ENERGY' : '1.3'
    }

    nprimary = testlength_primaries.get_nprimary(__file__,test_length)
    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,nprimary,1)

    data = pybdsim.DataPandas.BDSIMOutput(root_name)
    sampler_data = data.get_sampler('laser1.')
    partID = sampler_data['partID']
    Npho = 0

    for i in range(len(partID)):
        if partID[i] == 22:
            Npho += 1

    te = testdata_store.new_test_entry("22_processes/laserwire_compton_multiStep",__file__,nprimary,0)
    te.add_output_parameter("npho", Npho)
    ref_Npho=637



    assert (Npho==ref_Npho)