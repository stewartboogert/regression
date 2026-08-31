import pybdsim

import pytest
import os
from pathlib import Path

def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

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

    te = testdata_store.new_test_entry("02_elements/drift", __file__, nprimary, 0)
    te.add_output_file(os.path.dirname(__file__)+"/"+root_name, "root")
    te.add_output_file(os.path.dirname(__file__)+"/"+optics_name, "optics")
    te.add_output_parameter("rmat",rmat.tolist())
