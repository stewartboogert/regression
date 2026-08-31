import pytest
import pybdsim
import os
from pathlib import Path
import numpy as np

def test():
    os.chdir(Path(__file__).resolve().parent)

    base_name = "laser_pulse"
    base_name_1 = "laser_pulse_1"
    base_name_2 = "laser_pulse_2"
    template_name = base_name + ".tpl"
    gmad_name_1 = base_name_1 + ".gmad"
    gmad_name_2 = base_name_2 + ".gmad"
    root_name_1 = base_name_1 + ".root"
    root_name_2 = base_name_2 + ".root"

    params_1 = {
        'PULSE': 'pulseDuration',
        'PULSEVALUE': '71.0'
    }

    FWHM = 2.0*np.sqrt(2.0*np.log(2)) * 71.0
    params_2 = {
        'PULSE': 'pulseFWHM',
        'PULSEVALUE': str(FWHM)
    }

    pybdsim.Run.RenderGmadJinjaTemplate(template_name, gmad_name_1, params_1)
    pybdsim.Run.Bdsim(gmad_name_1, base_name_1, 10000, 1)

    # TODO need to merge laser PR in BDSIM for rest of test to work
    #pybdsim.Run.RenderGmadJinjaTemplate(template_name, gmad_name_2, params_2)
    #pybdsim.Run.Bdsim(gmad_name_2, base_name_2, 10000, 1)

    data_1 = pybdsim.DataPandas.BDSIMOutput(root_name_1)
    sampler_data_1 = data_1.get_sampler('laser1.')
    weights_1 = sampler_data_1['weight']
    partID_1 = sampler_data_1['partID']
    wpho_1 = []

    #data_2 = pybdsim.DataPandas.BDSIMOutput(root_name_2)
    #sampler_data_2 = data_2.get_sampler('laser1.')
    #weights_2 = sampler_data_2['weight']
    #partID_2 = sampler_data_2['partID']
    #wpho_2 = []

    for i in range(len(partID_1)):
        if partID_1[i] == 22:
            wpho_1.append(weights_1[i])

    #for j in range(len(partID_2)):
    #    if partID_2[j] == 22:
    #        wpho_2.append(weights_2[j])

    Npho_1 = sum(wpho_1)
    #Npho_2 = sum(wpho_2)

    #assert (pytest.approx(Npho_1, abs=1e-3) == pytest.approx(Npho_2, abs=1e-3))