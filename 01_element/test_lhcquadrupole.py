import pytest
import pybdsim
import os

def test() :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "lhcquadrupole"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    # check field along diagonal in primary aperture,
    # secondary aperture and outside of the secondary aperture (yoke)
    listX0 = [1,20.4,23.4]
    listY0 = [1,1,4]
    listXoffset = [-0.0198441,0.1741561,0.2050054]

    for i in range(len(listXoffset)):

        X0,Y0,Xoffset = listX0[i],listY0[i],listXoffset[i]

        data = {
            'X0': str(X0),
            'Y0': str(Y0),
        }

        pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
        pybdsim.Run.Bdsim(gmad_name,base_name,ngenerate=1,seed=1)

        d = pybdsim.DataPandas.BDSIMOutput(root_name)
        s = d.get_sampler("sampler.")

        assert(s['x'][0] == pytest.approx(Xoffset, rel=1e-4))