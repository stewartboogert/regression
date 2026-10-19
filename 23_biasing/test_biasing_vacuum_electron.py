import pytest
import pybdsim
import os
from pathlib import Path
import biasing_vacuum_electron_analysis

@pytest.mark.parametrize("process, bias, nprimary, pname", [
    ('eIoni', "1e06", "1e3", "eIoni_p01"),
    ('eIoni', "1e07", "1e3", "eIoni_p02"),
    ('eIoni', "1e08", "1e3", "eIoni_p03"),
    ('eIoni', "1e09", "1e3", "eIoni_p04"),
    ('eIoni', "1e10", "1e3", "eIoni_p05"),
    ('eIoni', "1e11", "1e3", "eIoni_p06"),
    ('eIoni', "1e12", "1e3", "eIoni_p07"),
    ('eBrem', "1e08", "1e3", "eBrem_p01"),
    ('eBrem', "1e09", "1e3", "eBrem_p02"),
    ('eBrem', "1e10", "1e3", "eBrem_p03"),
    ('eBrem', "1e11", "1e3", "eBrem_p04"),
    ('eBrem', "5e11", "1e3", "eBrem_p05"),
    ('eBrem', "1e12", "1e3", "eBrem_p06"),
    ('eBrem', "5e12", "1e3", "eBrem_p07"),
    ('eBrem', "1e13", "1e3", "eBrem_p08"),
    ('eBrem', "1e14", "1e3", "eBrem_p09"),
    ('eBrem', "1e15", "1e3", "eBrem_p10"),
    ('CoulombScat', "1e12", "1e3", 'CoulombScat_p01'),
    ('CoulombScat', "1e13", "1e3", 'CoulombScat_p02'),
    ('CoulombScat', "1e14", "1e3", 'CoulombScat_p03'),
    ('CoulombScat', "1e15", "1e3", 'CoulombScat_p04'),
    ('CoulombScat', "1e16", "1e3", 'CoulombScat_p05'),
    ('CoulombScat', "1e17", "1e3", 'CoulombScat_p06'),
    ('CoulombScat', "1e18", "1e3", 'CoulombScat_p07'),
    ('CoulombScat', "1e19", "1e3", 'CoulombScat_p08'),
    ('CoulombScat', "1e20", "1e3", 'CoulombScat_p09'),
    ('CoulombScat', "1e21", "1e3", 'CoulombScat_p10'),
    ('electronNuclear', "1e12", "1e3", 'electronNuclear_p01'),
    ('electronNuclear', "1e13", "1e3", 'electronNuclear_p02'),
    ('electronNuclear', "1e14", "1e3", 'electronNuclear_p03'),
    ('electronNuclear', "1e15", "1e3", 'electronNuclear_p04'),
    ('electronNuclear', "1e16", "1e3", 'electronNuclear_p05'),
    ('electronNuclear', "1e17", "1e3", 'electronNuclear_p06'),
    ('electronNuclear', "1e18", "1e3", 'electronNuclear_p07'),
    ('electronNuclear', "1e19", "1e3", 'electronNuclear_p08'),
    ('electronNuclear', "1e20", "1e3", 'electronNuclear_p09'),
    ('electronNuclear', "1e21", "1e3", 'electronNuclear_p10'),
])
def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store,
         process, bias, nprimary, pname) :

    os.chdir(Path(__file__).resolve().parent)

    base_name = "biasing_vacuum_electron"
    template_name = base_name + ".tpl"
    gmad_name = base_name + "_"+process+"_"+bias+ ".gmad"
    out_name  = base_name + "_"+process+"_"+bias
    root_name = out_name+".root"
    json_name = out_name+".json"

    params = {
        'BIAS_PROCESS': process,
        'BIAS_FACTOR' : bias,
        'DRIFT_NUMBER': 10,
        'DRIFT_LENGTH': '1',
        'BEAM_ENERGY' : '50'
    }

    # get number of primaries to simulate
    # from parameters

    # render and run
    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,params)
    sproc, timing = pybdsim.Run.Bdsim(gmad_name,out_name,int(float(nprimary)),1,returnTiming=True)

    # analysis
    ac = biasing_vacuum_electron_analysis.analysis(root_name)
    ac.write_persistent_data(json_name)

    # store test output
    te = testdata_store.new_test_entry("23_biasing/biasing_vacuum_electron_" + pname, __file__, nprimary, timing)
    te.add_input_parameter_dict(params)
    te.add_output_file(os.path.dirname(__file__)+"/"+json_name, "json")
    te.add_output_parameter("npfh", ac.get_persistent_data()['npfh'])
