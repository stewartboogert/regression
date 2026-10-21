import pytest
import pybdsim
import os
from pathlib import Path
import cross_section_analysis

@pytest.mark.parametrize("material, energy, nprimary, pname", [
    ('G4_Be', "1", "1e5", "G4_Be_p01"),
    ('G4_Be', "5", "1e5", "G4_Be_p02"),
    ('G4_Be', "10", "1e5", "G4_Be_p03"),
    ('G4_Be', "50", "1e5", "G4_Be_p04"),
    ('G4_Be', "100", "1e5", "G4_Be_p05"),
    ('G4_Be', "500", "1e5", "G4_Be_p06"),
    ('G4_Al', "1", "1e5", "G4_Al_p01"),
    ('G4_Al', "5", "1e5", "G4_Al_p02"),
    ('G4_Al', "10", "1e5", "G4_Al_p03"),
    ('G4_Al', "50", "1e5", "G4_Al_p04"),
    ('G4_Al', "100", "1e5", "G4_Al_p05"),
    ('G4_Al', "500", "1e5", "G4_Al_p06"),
    ('G4_Fe', "1",  "1e5", "G4_Fe_p01"),
    ('G4_Fe', "5",  "1e5", "G4_Fe_p02"),
    ('G4_Fe', "10", "1e5", "G4_Fe_p03"),
    ('G4_Fe', "50", "1e5", "G4_Fe_p04"),
    ('G4_Fe', "100", "1e5", "G4_Fe_p05"),
    ('G4_Fe', "500", "1e5", "G4_Fe_p06"),
    ('G4_Cu', "1", "1e5", "G4_Cu_p01"),
    ('G4_Cu', "5", "1e5", "G4_Cu_p02"),
    ('G4_Cu', "10", "1e5", "G4_Cu_p03"),
    ('G4_Cu', "50", "1e5", "G4_Cu_p04"),
    ('G4_Cu', "100", "1e5", "G4_Cu_p05"),
    ('G4_Cu', "500", "1e5", "G4_Cu_p06"),
    ('G4_Pb', "1", "1e5", "G4_Pb_p01"),
    ('G4_Pb', "5", "1e5", "G4_Pb_p02"),
    ('G4_Pb', "10", "1e5", "G4_Pb_p03"),
    ('G4_Pb', "50", "1e5", "G4_Pb_p04"),
    ('G4_Pb', "100", "1e5", "G4_Pb_p05"),
    ('G4_Pb', "500", "1e5", "G4_Pb_p06")
])
def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store,
         material, energy, nprimary, pname) :

    os.chdir(Path(__file__).resolve().parent)

    base_name = "electron"
    template_name = base_name + ".tpl"
    param_name = base_name + "_" + material + "_" + energy
    gmad_name = param_name + ".gmad"
    root_name = param_name+".root"
    json_name = param_name+".json"

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

    # analysis
    ac = cross_section_analysis.analysis(root_name)
    # ac.write_persistent_data(json_name)

    # store test output
    te = testdata_store.new_test_entry("22_processes/electron_" + pname, __file__, nprimary, timing)
    te.add_input_parameter_dict(params)