import pytest
import pybdsim
import os
import numpy as np

def test(test_length, testlength_primaries, testdata_store) :
    np.set_printoptions(linewidth=200)

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "sextupole"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"

    l  = 1.0
    k2 = -5.0
    data = {
        'LENGTH': l,
        'K2' : k2,
        'BEAM_ENERGY' : '1'
    }

    nprimary = testlength_primaries.get_nprimary(__file__,test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,nprimary,1)
    pybdsim.Run.RebdsimOptics(root_name,optics_name)

    do = pybdsim.DataPandas.REBDSIMOptics(optics_name)
    do_df = do.get_optics()

    
    rmat = pybdsim.Analysis.CalculateTaylorMapOrder2(root_name,"d1.","s1.", average=True)

    #ref_rmat = [[1,l,0,0,0,0],
    #            [0,1,0,0,0,0],
    #            [0,0,1,l,0,0],
    #            [0,0,0,1,0,0],
    #            [0,0,0,0,1,0],
    #            [0,0,0,0,0,1]]


    #print('maximum matrix difference',pybdsim.Testing.max_matrix_diff(rmat,ref_rmat))
    #assert pybdsim.Testing.compare_matrix(rmat,ref_rmat)
    
    testdata_store.addtestoutput(__file__,root_name,"root", nprimary)
    testdata_store.addtestoutput(__file__,optics_name,"optics", nprimary)