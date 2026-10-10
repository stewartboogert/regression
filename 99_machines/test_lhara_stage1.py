import os
import pytest
import pybdsim
import subprocess
from pathlib import Path

def test(test_length, testlength_primaries, testdata_store):

    os.chdir(Path(__file__).resolve().parent)

    base_name   = "lhara_stage1"
    gmad_name   = "./04_lhara_stage1/LhARA_S1.gmad"
    root_name   = base_name + ".root"
    optics_name = base_name + "_optics.root"

    nprimary = testlength_primaries.get_nprimary(__file__, test_length)

    pybdsim.Run.Bdsim(gmad_name, base_name, nprimary, nprimary)
    subprocess.call(["rebdsimOptics",
                     root_name,
                     optics_name,
                     "--emittanceOnTheFly"],
                    stdout=open(os.devnull, "wb"))

    te = testdata_store.new_test_entry("99_machines/lhara_stage1", __file__, nprimary, 0)
    te.add_output_file(os.path.dirname(__file__)+"/"+optics_name, "optics")
