import pytest
import pybdsim
import os
from pathlib import Path


def test(testdata_store) :

    os.chdir(Path(__file__).resolve().parent)
    
    base_name     = "laserwire_photodetachment_multiStep"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    data = {
        'LASER_ENERGY': '67.4',
        'BEAM_ENERGY' : '0.942022+0.003'
    }

    # TODO fixture nprimary
    nprimary = 10000

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,nprimary,1)

    data = pybdsim.DataPandas.BDSIMOutput(root_name)
    sampler_data = data.get_sampler('laser1.')
    partID = sampler_data['partID']
    Ne = 0

    for i in range(len(partID)):
        if partID[i] == 11:
            Ne += 1

    ref_Ne = 6852

    assert (Ne==ref_Ne)

    te = testdata_store.new_test_entry("08_processes/laserwire_photodetachment_multiStep",__file__,nprimary,0)
    te.add_output_parameter("ne", Ne)