import pytest
import pybdsim
import os

def test() :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "laserwire_photodetachment_cumulative"
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
    weights=samplerData.data.get("weight")
    we=[]
    for i in range(len(weights)):
        if i%2==0:
            we.append(weights[i+1])
    Ne=sum(we)
    ref_Ne=5.843840659450507
    
    print('test ', Ne)
    print('ref ', ref_Ne)
    assert pybdsim.Testing.compare_matrix(Ne,ref_Ne)