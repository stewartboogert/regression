import pytest
import pybdsim
import os
from pathlib import Path

def test() :

    os.chdir(Path(__file__).resolve().parent)
    
    base_name     = "placement_sampler"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"
    combine_name  = base_name+"_combine.root"
    
    params = {
        'LENGTH': '1.0',
        'BEAM_ENERGY' : '1'
    }

    ngenerate = 500

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,params)
    pybdsim.Run.Bdsim(gmad_name,base_name,ngenerate,1)
    data = pybdsim.DataPandas.BDSIMOutput(root_name)
    sampler_data = data.get_sampler("s1.")

    # extract the relevant data
    sampler_number = len(sampler_data)
    sampler_x = sampler_data['x']
    sampler_xp = sampler_data['xp']
    sampler_y = sampler_data['y']
    sampler_yp = sampler_data['yp']
    sampler_energy = sampler_data['energy']

    # calculate values that should remain consistent with every run
    sampler_x_sigma = sampler_x.std()
    sampler_x_mean = sampler_x.mean()
    sampler_xp_sigma = sampler_xp.std()
    sampler_xp_mean = sampler_xp.mean()

    sampler_y_sigma = sampler_y.std()
    sampler_y_mean = sampler_y.mean()
    sampler_yp_sigma = sampler_yp.std()
    sampler_yp_mean = sampler_yp.mean()

    sampler_energy_sigma = sampler_energy.std()
    sampler_energy_mean = sampler_energy.mean()
