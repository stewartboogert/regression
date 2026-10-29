import pytest
import pybdsim
import os
from pathlib import Path
import cross_section_analysis

@pytest.mark.parametrize("material, energy, nprimary, pname", [
    ('G4_Be', "1", "5e4", "G4_Be_p01"),
    ('G4_Be', "5", "5e4", "G4_Be_p02"),
    ('G4_Be', "10", "5e4", "G4_Be_p03"),
    ('G4_Be', "50", "5e4", "G4_Be_p04"),
    ('G4_Be', "100", "5e4", "G4_Be_p05"),
    ('G4_Be', "500", "5e4", "G4_Be_p06"),
    ('G4_Al', "1", "5e4", "G4_Al_p01"),
    ('G4_Al', "5", "5e4", "G4_Al_p02"),
    ('G4_Al', "10", "5e4", "G4_Al_p03"),
    ('G4_Al', "50", "5e4", "G4_Al_p04"),
    ('G4_Al', "100", "5e4", "G4_Al_p05"),
    ('G4_Al', "500", "5e4", "G4_Al_p06"),
    ('G4_Fe', "1",  "5e4", "G4_Fe_p01"),
    ('G4_Fe', "5",  "5e4", "G4_Fe_p02"),
    ('G4_Fe', "10", "5e4", "G4_Fe_p03"),
    ('G4_Fe', "50", "5e4", "G4_Fe_p04"),
    ('G4_Fe', "100", "5e4", "G4_Fe_p05"),
    ('G4_Fe', "500", "5e4", "G4_Fe_p06"),
    ('G4_Cu', "1", "5e4", "G4_Cu_p01"),
    ('G4_Cu', "5", "5e4", "G4_Cu_p02"),
    ('G4_Cu', "10", "5e4", "G4_Cu_p03"),
    ('G4_Cu', "50", "5e4", "G4_Cu_p04"),
    ('G4_Cu', "100", "5e4", "G4_Cu_p05"),
    ('G4_Cu', "500", "5e4", "G4_Cu_p06"),
    ('G4_Pb', "1", "5e4", "G4_Pb_p01"),
    ('G4_Pb', "5", "5e4", "G4_Pb_p02"),
    ('G4_Pb', "10", "5e4", "G4_Pb_p03"),
    ('G4_Pb', "50", "5e4", "G4_Pb_p04"),
    ('G4_Pb', "100", "5e4", "G4_Pb_p05"),
    ('G4_Pb', "500", "5e4", "G4_Pb_p06")
])
def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store,
         material, energy, nprimary, pname) :

    os.chdir(Path(__file__).resolve().parent)

    base_name = "photon"
    template_name = base_name + ".tpl"
    param_name = base_name + "_" + material + "_" + energy
    gmad_name = param_name + ".gmad"
    root_name = param_name+".root"
    json_name = param_name+".json"
    stdout_file = param_name+".stdout"
    stderr_file = param_name+".stderr"

    params = {
        'DRIFT_LENGTH': '1',
        'BEAM_ENERGY' : energy,
        'TARGET_LENGTH' : '1e-3',
        'TARGET_MATERIAL' : material
    }

    # get number of primaries to simulate
    # from parameters

    # render and run
    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,params)
    sproc, timing = pybdsim.Run.Bdsim(gmad_name,param_name,int(float(nprimary)),1,returnTiming=True)

    # write log files
    with open(stdout_file,"w") as stdout_f :
        stdout_f.write(sproc.stdout)
    with open(stderr_file,"w") as stderr_f :
        stderr_f.write(sproc.stderr)

    # analysis
    ac = cross_section_analysis.analysis(root_name)
    ac.write_persistent_data(json_name)

    # delete root files
    # Path(root_name).unlink()

    # store test output
    te = testdata_store.new_test_entry("22_processes/photon_" + pname, __file__, nprimary, timing)
    te.add_input_parameter_dict(params)
    te.add_output_file(os.path.dirname(__file__)+"/"+json_name,"json")
    te.add_output_file(os.path.dirname(__file__)+"/"+stdout_file,"stdout")
    te.add_output_file(os.path.dirname(__file__)+"/"+stderr_file,"stderr")