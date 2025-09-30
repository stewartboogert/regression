import pytest
import pybdsim
import os

def test() :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "millicharge-scatter"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    # mass [GeV], charge [e+], resulting x-offset [m]
    assertions = [[0.1,1,0.03022],[1,0.5,-0.04656],[5,0.1,-0.00668]]

    for assertion in assertions:

        mass,charge,xoffset = assertion

        # make gmad from template
        data = {'CHARGE': charge,'MASS': mass,}
        pybdsim.Run.RenderGmadJinjaTemplate(template_name, gmad_name, data)

        # run job
        pybdsim.Run.Bdsim(gmad_name,base_name,ngenerate=1,seed=1)

        # extract x-offset from output
        d = pybdsim.DataPandas.BDSIMOutput(root_name)
        s = d.get_sampler("sampler.")
        xoffset_out = s['x'][0]

        # compare result
        assert(xoffset_out == pytest.approx(xoffset,abs=1e-3))
    
