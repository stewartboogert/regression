import pytest
import pybdsim
import os

def test() :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "drift"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"
    
    data = {
        'LENGTH': '1.0',
        'BEAM_ENERGY' : '1'
    }

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,100,1)
    pybdsim.Run.RebdsimOptics(root_name,optics_name)

    od = pybdsim.Data.Load(optics_name)

    Mean_x   = od.optics.GetColumn("Mean_x")
    Mean_y   = od.optics.GetColumn("Mean_y")
    Mean_t   = od.optics.GetColumn("Mean_t")
    Mean_E   = od.optics.GetColumn("Mean_E")
    Sigma_x  = od.optics.GetColumn("Sigma_x")
    Sigma_y  = od.optics.GetColumn("Sigma_y")
    Sigma_xp = od.optics.GetColumn("Sigma_xp")
    Sigma_yp = od.optics.GetColumn("Sigma_yp")
    
    print(Mean_x)
    print(Mean_y)
    print(Mean_t)
    print(Mean_E)
    print(Sigma_x)
    print(Sigma_y)
    print(Sigma_xp)
    print(Sigma_yp)

    rmat = pybdsim.Analysis.CalculateRMatrix(root_name,"Primary","t1.",size=6, average=True)    
    ref_rmat = [[1,2,0,0,0,0],
                [0,1,0,0,0,0],
                [0,0,1,2,0,0],
                [0,0,0,1,0,0],
                [0,0,0,0,1,0],
                [0,0,0,0,0,1]]
    print('rounded matrix',pybdsim.Testing.round_matrix(rmat))
    print('maximum matrix difference',pybdsim.Testing.max_matrix_diff(rmat,ref_rmat))    

    assert pybdsim.Testing.compare_matrix(rmat,ref_rmat)
    
