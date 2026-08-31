import pytest
import pybdsim
import os
from pathlib import Path

def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store) :

    os.chdir(Path(__file__).resolve().parent)
    
    base_name     = "laserwire_compton_cumulative"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    data = {
        'LASER_ENERGY': '150',
        'BEAM_ENERGY' : '1.3'
    }

    nprimary = testlength_primaries.get_nprimary(__file__,test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,nprimary,1)

    d = pybdsim.Data.Load(root_name)
    samplerData = pybdsim.Data.SamplerData(d,'laser1') 
    weights=samplerData.data.get("weight")
    partid=samplerData.data.get("partID")
    wpho=[]

    for i in range(len(partid)):
        if partid[i]==22:
            wpho.append(weights[i])


    Npho=sum(wpho)
    ref_Npho=0.626774271968543

    te = testdata_store.new_test_entry("08_processes/laserwire_compton_cumulative",__file__,nprimary,0)
    te.add_output_parameter("npho", Npho)

    assert (Npho==pytest.approx(ref_Npho,abs=1e-3))