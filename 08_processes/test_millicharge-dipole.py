import pytest
import pybdsim
import os

def test() :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "millicharge-dipole"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"

    pybdsim.Run.Bdsim(gmad_name,base_name,ngenerate=1,seed=1)


    d = pybdsim.DataPandas.BDSIMOutput(root_name)
    s = d.get_sampler("sampler.")

    assert(s['x'][0] == pytest.approx(-3.466564))
    
