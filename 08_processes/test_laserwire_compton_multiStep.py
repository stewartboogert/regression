import pytest
import pybdsim
import os

def test() :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "laserwire_compton_multiStep"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    l  = 2.0 
    data = {
        'LASER_ENERGY': '150',
        'BEAM_ENERGY' : '1.3'
    }

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,10000,1)

    d = pybdsim.Data.Load(root_name)
    samplerData = pybdsim.Data.SamplerData(d,'laser1') 
    partid=samplerData.data.get('partID')
    Npho=0
    for i in range(len(partid)):
        if partid[i]==22:
            Npho+=1

    ref_Npho=637
    
    print('test ',Npho)
    print('ref ', ref_Npho)
    assert pybdsim.Testing.compare_matrix(Npho,ref_Npho)