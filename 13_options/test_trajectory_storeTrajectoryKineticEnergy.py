import pytest
import pybdsim
import os
from pathlib import Path


def test() :

    os.chdir(Path(__file__).resolve().parent)
    
    base_name     = "trajectory_storeTrajectoryKineticEnergy"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"
    
    data = {
        'LENGTH': '1.0',
        'BEAM_ENERGY' : '1'
    }

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,100,1)
    pybdsim.Run.RebdsimOptics(root_name,optics_name)

