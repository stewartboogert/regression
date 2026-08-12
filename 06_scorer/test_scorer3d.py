import pybdsim

import pytest
import os

def test(test_length, testlength_primaries, testdata_store):
    os.chdir(os.path.dirname(__file__))

    base_name = "scorer3d"
    template_name = base_name+".tpl"
    gmad_name = base_name + ".gmad"
    root_name = base_name + ".root"

    data = {}

    nprimary = testlength_primaries.get_nprimary(__file__, test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name, base_name, nprimary, 1)

    testdata_store.add_test_output(__file__, root_name, "root", nprimary)
