import pytest
import pybdsim
import os

def test() :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "laserwire_photodetachment_multiStep"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    data = {
        'LASER_ENERGY': '67.4',
        'BEAM_ENERGY' : '0.942022+0.003'
    }

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,10000,1)

    d = pybdsim.Data.Load(root_name)
    samplerData = pybdsim.Data.SamplerData(d,'laser1') 
    partid=samplerData.data.get('partID')
    Ne=0
    for i in range(len(partid)):
        if partid[i]==11:
            Ne+=1

    ref_Ne=6852
    

    assert (Ne==ref_Ne)