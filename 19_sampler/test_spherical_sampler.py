import pytest
import pybdsim
import os
from pathlib import Path

def test() :

    os.chdir(Path(__file__).resolve().parent)
    
    base_name     = "spherical_sampler"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"
    combine_name  = base_name+"_combine.root"
    
    params = {
        'LENGTH': '1e-3',
        'BEAM_ENERGY' : '1'
    }

    ngenerate = 500

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,params)
    pybdsim.Run.Bdsim(gmad_name,base_name,ngenerate,1)
    data = pybdsim.DataPandas.BDSIMOutput(root_name)
    sampler_data = data.get_ssampler("s1.")

    sampler_number = len(sampler_data)
    sampler_theta = sampler_data['theta']
    sampler_thetap = sampler_data['thetap']
    sampler_phi = sampler_data['phi']
    sampler_phip = sampler_data['phip']
    sampler_energy = sampler_data['totalEnergy']

    sampler_theta_sigma = sampler_theta.std()
    sampler_theta_mean = sampler_theta.mean()
    sampler_thetap_sigma = sampler_thetap.std()
    sampler_thetap_mean = sampler_thetap.mean()

    sampler_phi_sigma = sampler_phi.std()
    sampler_phi_mean = sampler_phi.mean()
    sampler_phip_sigma = sampler_phip.std()
    sampler_phip_mean = sampler_phip.mean()

    sampler_energy_sigma = sampler_energy.std()
    sampler_energy_mean = sampler_energy.mean()

