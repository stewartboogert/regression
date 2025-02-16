import pybdsim
from numpy import pi 
import os

def test() :

    os.path.dirname(__file__)
    
    base_name     = "sbend"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"
    
    data = {
        'LENGTH': '1.0',
        'ANGLE': 5/180*pi,
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

    rmat = pybdsim.Analysis.CalculateRMatrix(root_name,"d1.","t1.",size=6, average=True)

    print(rmat)
