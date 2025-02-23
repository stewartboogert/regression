import pybdsim
from numpy import pi
import os

def test() :

    os.path.dirname(__file__)
    
    base_name     = "rbend"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"
    
    data = {
        'LENGTH': '1',
        'ANGLE': 10/180*pi,
        'BEAM_ENERGY' : '1'
    }

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,1000,1)
    pybdsim.Run.RebdsimOptics(root_name,optics_name)

    do = pybdsim.DataPandas.REBDSIMOptics(optics_name)
    do_df = do.get_optics()
    print(do_df)

    rmat = pybdsim.Analysis.CalculateRMatrix(root_name,"d1.","t1.",size=6, average=True)
    ref_rmat = [[ 1.,   1.,   0.,   0.,   0.,   0.1],
                [-0.,   1.,   0.,   0.,   0.,   0.2],
                [-0.,   0.,   1.,   1.,   0.,   0. ],
                [-0.,   0.,  -0.,   1.,   0.,   0. ],
                [ 0.,   0.,  -0.,  -0.,   1.,   0. ],
                [-0.,   0.,   0.,  -0.,  -0.,   1. ]]
    print('rounded matrix')
    print(pybdsim.Testing.round_matrix(rmat))
    print('maximum matrix difference')
    print(pybdsim.Testing.max_matrix_diff(rmat,ref_rmat))

    assert pybdsim.Testing.compare_matrix(rmat,ref_rmat)
