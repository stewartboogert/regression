import pytest
import pybdsim
import os
from pathlib import Path
import cross_section_analysis

@pytest.mark.parametrize("material, energy, nprimary, pname", [
    ('G4_Be', "1", "5e4", "G4_Be_p01"),
    ('G4_Be', "2", "5e4", "G4_Be_p02"),
    ('G4_Be', "3", "5e4", "G4_Be_p03"),
    ('G4_Be', "4", "5e4", "G4_Be_p04"),
    ('G4_Be', "5", "5e4", "G4_Be_p05"),
    ('G4_Be', "6", "5e4", "G4_Be_p06"),
    ('G4_Be', "7", "5e4", "G4_Be_p07"),
    ('G4_Al', "1", "5e4", "G4_Al_p01"),
    ('G4_Al', "2", "5e4", "G4_Al_p02"),
    ('G4_Al', "3", "5e4", "G4_Al_p03"),
    ('G4_Al', "4", "5e4", "G4_Al_p04"),
    ('G4_Al', "5", "5e4", "G4_Al_p05"),
    ('G4_Al', "6", "5e4", "G4_Al_p06"),
    ('G4_Al', "7", "5e4", "G4_Al_p07"),
    ('G4_Fe', "1", "5e4", "G4_Fe_p01"),
    ('G4_Fe', "2",  "5e4", "G4_Fe_p02"),
    ('G4_Fe', "3",  "5e4", "G4_Fe_p03"),
    ('G4_Fe', "4", "5e4", "G4_Fe_p04"),
    ('G4_Fe', "5", "5e4", "G4_Fe_p05"),
    ('G4_Fe', "6", "5e4", "G4_Fe_p06"),
    ('G4_Fe', "7", "5e4", "G4_Fe_p07"),
    ('G4_Cu', "1", "5e4", "G4_Cu_p01"),
    ('G4_Cu', "2", "5e4", "G4_Cu_p02"),
    ('G4_Cu', "3", "5e4", "G4_Cu_p03"),
    ('G4_Cu', "4", "5e4", "G4_Cu_p04"),
    ('G4_Cu', "5", "5e4", "G4_Cu_p05"),
    ('G4_Cu', "6", "5e4", "G4_Cu_p06"),
    ('G4_Cu', "7", "5e4", "G4_Cu_p07"),
    ('G4_Pb', "1", "5e4", "G4_Pb_p01"),
    ('G4_Pb', "2", "5e4", "G4_Pb_p02"),
    ('G4_Pb', "3", "5e4", "G4_Pb_p03"),
    ('G4_Pb', "4", "5e4", "G4_Pb_p04"),
    ('G4_Pb', "5", "5e4", "G4_Pb_p05"),
    ('G4_Pb', "6", "5e4", "G4_Pb_p06"),
    ('G4_Pb', "7", "5e4", "G4_Pb_p07")
])
def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store,
         material, energy, nprimary, pname) :

    os.chdir(Path(__file__).resolve().parent)

    base_name = "lead"
    template_name = base_name + ".tpl"
    param_name = base_name + "_" + material + "_" + energy
    gmad_name = param_name + ".gmad"
    root_name = param_name+".root"
    json_name = param_name+".json"
    stdout_file = param_name+".stdout"
    stderr_file = param_name+".stderr"

    params = {
        'DRIFT_LENGTH': '1',
        'BEAM_ENERGY' : str(float(energy)*82), # Z of lead
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
    te = testdata_store.new_test_entry("22_processes/electron_" + pname, __file__, nprimary, timing)
    te.add_input_parameter_dict(params)
    te.add_output_file(os.path.dirname(__file__)+"/"+json_name,"json")
    te.add_output_file(os.path.dirname(__file__)+"/"+stdout_file,"stdout")
    te.add_output_file(os.path.dirname(__file__)+"/"+stderr_file,"stderr")