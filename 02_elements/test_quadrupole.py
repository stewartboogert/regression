import pytest
import pybdsim
import os
from pathlib import Path
from numpy import sin, cos, sinh, cosh, sqrt

def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    base_name     = "quadrupole"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"
    optics_name   = base_name+"_optics.root"

    l  = 1.0
    k1 = -1.0
    data = {
        'LENGTH': str(l),
        'k1': str(k1),
        'BEAM_ENERGY' : '1'
    }

    nprimary = testlength_primaries.get_nprimary(__file__, test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,data)
    pybdsim.Run.Bdsim(gmad_name,base_name,nprimary,1)
    pybdsim.Run.RebdsimOptics(root_name,optics_name)

    do = pybdsim.DataPandas.REBDSIMOptics(optics_name)
    do_df = do.get_optics()
    print(do_df)
    
    rmat = pybdsim.Analysis.CalculateRMatrix(root_name,"d1.","q1.",size=6, average=True)
    a = sqrt(abs(k1)) * l
    if k1 > 0 :

        ref_rmat = [[cosh(a)              , 1/sqrt(abs(k1))*sinh(a),                    0,                      0,0,0],
                    [sqrt(abs(k1))*sinh(a),                 cosh(a),                    0,                      0,0,0],
                    [                    0,                       0,               cos(a), 1/sqrt(abs(k1))*sin(a),0,0],
                    [                    0,                       0,-sqrt(abs(k1))*sin(a),                 cos(a),0,0],
                    [                    0,                       0,                    0,                      0,1,0],
                    [                    0,                       0,                    0,                      0,0,0]]
    else :
        ref_rmat = [[               cos(a), 1/sqrt(abs(k1))*sin(a),                     0,                       0,0,0],
                    [-sqrt(abs(k1))*sin(a),                 cos(a),                     0,                       0,0,0],
                    [                    0,                      0,               cosh(a), 1/sqrt(abs(k1))*sinh(a),0,0],
                    [                    0,                      0, sqrt(abs(k1))*sinh(a),                 cosh(a),0,0],
                    [                    0,                      0,                     0,                       0,1,0],
                    [                    0,                      0,                     0,                       0,0,0]]
    print(pybdsim.Testing.round_matrix(rmat,3))
    print(pybdsim.Testing.round_matrix(ref_rmat,3))

    assert pybdsim.Testing.compare_matrix(rmat,ref_rmat)

    te = testdata_store.new_test_entry("02_elements/quadrupole", __file__, nprimary, 0)
    te.add_output_file(os.path.dirname(__file__)+"/"+root_name, "root")
    te.add_output_file(os.path.dirname(__file__)+"/"+optics_name, "optics")
    te.add_output_parameter("rmat",rmat.tolist())
