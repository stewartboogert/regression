import pytest
import pybdsim
import os
from pathlib import Path

def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store) :

    os.chdir(Path(__file__).resolve().parent)

    base_name = "biasing_thin"
    template_name = base_name + ".tpl"
    gmad_name = base_name + ".gmad"
    root_name = base_name + ".root"

    data = {
        'DRIFT_LENGTH': '10',
        'RCOL_LENGTH': '0.1',
        'BEAM_ENERGY' : '50',
        'SBEND_LENGTH': '1.0',
        'QUAD_LENGTH': 0.25
    }

    # get number of primaries to simulate
    nprimary = 1000

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
