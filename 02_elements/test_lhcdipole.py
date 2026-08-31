import pytest
import pybdsim
import os
from pathlib import Path


def test(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    base_name     = "lhcdipole"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    # TODO turn in pytest parametrize
    # check field in primary aperture,
    # secondary aperture and outside of the secondary aperture (yoke)
    # TODO turn in pytest parametrize
    listX0 = [0,19.4,19.4]
    listY0 = [0,0,4]
    listXoffset = [1.9062219,-0.1165236,-0.1521038]

    nprimary = 1

    for i in range(len(listXoffset)):

        X0,Y0,Xoffset = listX0[i],listY0[i],listXoffset[i]

        data = {
            'X0': str(X0),
            'Y0': str(Y0),
        }

        pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
        pybdsim.Run.Bdsim(gmad_name,base_name,ngenerate=nprimary,seed=1)

        d = pybdsim.DataPandas.BDSIMOutput(root_name)
        s = d.get_sampler("sampler.")

        assert(s['x'][0] == pytest.approx(Xoffset, rel=1e-4))

    te = testdata_store.new_test_entry("02_elements/lhcdipole", __file__, nprimary, 0)
    te.add_output_file(os.path.dirname(__file__)+"/"+root_name, "root")
