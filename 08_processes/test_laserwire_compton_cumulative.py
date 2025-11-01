import pytest
import pybdsim
import os

def test() :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "laserwire_compton_cumulative"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    data = {
        'LASER_ENERGY': '150',
        'BEAM_ENERGY' : '1.3'
    }

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,10000,1)

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
    

    assert (Npho==pytest.approx(ref_Npho,abs=1e-3))