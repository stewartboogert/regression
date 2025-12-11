# Author (Institute): Stewart Boogert (Cockcroft)
# Start date: 9/11/2025
# Issue number: None

import pytest
import pybdsim
import os

def test():
    os.chdir(os.path.dirname(__file__))

    # versions
    version = pybdsim.Run.Versions()

    # build gmad files and output paths
    base_name = "template"
    template_name = base_name + ".tpl"
    gmad_name = base_name + ".gmad"
    root_name = base_name + ".root"
    optics_name = base_name + "_optics.root"

    l = 2.0
    data = {
        'LENGTH': str(l),
        'BEAM_ENERGY': '1'
    }

    # Run analysis
    pybdsim.Run.RenderGmadJinjaTemplate(template_name, gmad_name, data)
    pybdsim.Run.Bdsim(gmad_name, base_name, 2500, 1)
    pybdsim.Run.RebdsimOptics(root_name, optics_name)

    do = pybdsim.DataPandas.REBDSIMOptics(optics_name)
    do_df = do.get_optics()
    print(do_df)

    rmat = pybdsim.Analysis.CalculateRMatrix(root_name, "d1.", "t1.", size=6, average=True)
    ref_rmat = [[1, l, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 0, 1, l, 0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1]]

    assert pybdsim.Testing.compare_matrix(rmat, ref_rmat)