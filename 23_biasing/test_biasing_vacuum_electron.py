import pytest
import pybdsim
import os
from pathlib import Path
import biasing_vacuum_electron_analysis

@pytest.mark.parametrize("process, bias, nprimary, pname", [
    ('eBrem', "1e08", "1e3", "eBrem_p1"),
    ('eBrem', "1e09", "1e3", "eBrem_p2"),
    ('eBrem', "1e10", "1e3", "eBrem_p3"),
    ('eBrem', "1e11", "1e3", "eBrem_p4"),
    ('eBrem', "1e12", "1e3", "eBrem_p5"),
    ('eBrem', "1e13", "1e3", "eBrem_p6"),
    ('eBrem', "1e14", "1e3", "eBrem_p7"),
    ('eBrem', "1e15", "1e3", "eBrem_p8"),

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

