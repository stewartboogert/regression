import pybdsim
from numpy import pi
from numpy import sin
from numpy import cos
import os

def test() :

    os.path.dirname(__file__)
    
    base_name     = "sbend"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"

    length = 1.0
    angle = 10/180*pi
    rho = length/angle
    data = {
        'LENGTH': length,
        'ANGLE': angle,
        'BEAM_ENERGY' : '1'
    }

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,3000,1)
    pybdsim.Run.RebdsimOptics(root_name,optics_name)

    rmat = pybdsim.Analysis.CalculateRMatrix(root_name,"d1.","t1.",size=6, average=True)
    ref_rmat = [[ cos(angle)      ,  rho*sin(angle),   0.,      0.,   0.,   0  ],
                [-1/rho*sin(angle),      cos(angle),   0.,      0.,   0.,   0  ],
                [               0.,              0.,   1.,  length,   0.,   0. ],
                [               0.,              0.,   0.,      1.,   0.,   0. ],
                [               0.,              0.,   0.,      0.,   1.,   0. ],
                [               0.,              0.,   0.,      0.,   0.,   0. ]]
    print(pybdsim.Testing.round_matrix(rmat,3))
    print(pybdsim.Testing.round_matrix(ref_rmat,3))
    print(pybdsim.Testing.max_matrix_diff(rmat,ref_rmat))
    
    assert pybdsim.Testing.compare_matrix(rmat,ref_rmat)
