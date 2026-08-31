import pybdsim

import pytest
import os
from pathlib import Path


def test(test_length, testlength_primaries, testdata_store):
    os.chdir(Path(__file__).resolve().parent)

    base_name = "scorer3d"
    template_name = base_name+".tpl"
    gmad_name = base_name + ".gmad"
    root_name = base_name + ".root"

    data = {}

    nprimary = testlength_primaries.get_nprimary(__file__, test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name, base_name, nprimary, 1)

    te = testdata_store.new_test_entry("20_scorer/scorer3d", __file__, nprimary, 0)
    te.add_output_file(os.path.dirname(__file__)+"/"+root_name, "root")
