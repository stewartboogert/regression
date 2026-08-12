import pybdsim

import pytest
import os

def test(geant4_version, bdsim_version, test_length, testlength_primaries, testdata_store) :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "drift"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"

    l  = 2.0 
    data = {
        'LENGTH': str(l),
        'BEAM_ENERGY' : '1'
    }

    nprimary = testlength_primaries.get_nprimary(__file__,test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,nprimary,1)
    pybdsim.Run.RebdsimOptics(root_name,optics_name)

    do = pybdsim.DataPandas.REBDSIMOptics(optics_name)
    do_df = do.get_optics()
    print(do_df)
    
    rmat = pybdsim.Analysis.CalculateRMatrix(root_name,"d1.","t1.",size=6, average=True)
    ref_rmat = [[1,l,0,0,0,0],
                [0,1,0,0,0,0],
                [0,0,1,l,0,0],
                [0,0,0,1,0,0],
                [0,0,0,0,1,0],
                [0,0,0,0,0,1]]

    assert pybdsim.Testing.compare_matrix(rmat,ref_rmat)

    testdata_store.add_test_output(__file__,root_name,"root", nprimary)
    testdata_store.add_test_output(__file__,optics_name,"optics", nprimary)
    testdata_store.add_test_object(__file__,rmat.tolist(), "rmat", nprimary)