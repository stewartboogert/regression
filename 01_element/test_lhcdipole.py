import pytest
import pybdsim
import os

def test() :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "lhcdipole"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    # check field in primary aperture,
    # secondary aperture and outside of the secondary aperture (yoke)
    listX0 = [0,19.4,19.4]
    listY0 = [0,0,4]
    listAssert = [1.9062219,-0.1165236,-0.1521038]

    for i in range(len(listAssert)):

        X0,Y0,assertion = listX0[i],listY0[i],listAssert[i]

        data = {
            'X0': str(X0),
            'Y0': str(Y0),
        }

        pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
        pybdsim.Run.Bdsim(gmad_name,base_name,ngenerate=1,seed=1)

        d = pybdsim.DataPandas.BDSIMOutput(root_name)
        s = d.get_sampler("sampler.")

        assert(s['x'][0] == pytest.approx(assertion))