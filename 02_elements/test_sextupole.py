import pytest
import pybdsim
import os
import numpy as np
from pathlib import Path

def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    np.set_printoptions(linewidth=200)

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

    te = testdata_store.new_test_entry("02_elements/sextupole", __file__, nprimary, 0)
    te.add_output_file(os.path.dirname(__file__)+"/"+root_name, "root")
    te.add_output_file(os.path.dirname(__file__)+"/"+optics_name, "optics")
