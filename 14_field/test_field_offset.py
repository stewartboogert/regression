import pybdsim
import os
import pytest
from pathlib import Path

# case, FIELD_X_OFFSET, FIELD_Y_OFFSET, FIELD_Z_OFFSET,
# expected Sigma_x, Sigma_xp, mean_x, Sigma_y, Sigma_yp, mean_y
FIELD_OFFSET_CASES = [
    ("x_offset", "0.1", "0.0", "0.0",
     0.013835341613313606, 0.0072268511635527445, 0.568285196685791,
     0.00478033296891485, 0.0023960091258065264, 0.23385638386309146),
    ("y_offset", "0.0", "0.1", "0.0",
     0.01438563542490261, 0.007424089790444462, 0.577986688876152,
     0.005241687258850288, 0.002609618738995901, 0.25584089472591875),
    ("z_offset", "0.0", "0.0", "0.1",
     0.013459971494015222, 0.007452970502992219, 0.5479260095000267,
     0.004177156229900975, 0.002217752745742983, 0.2142822514116764),
]


@pytest.mark.parametrize(
    "case, x_offset, y_offset, z_offset,"
    " expected_Sigma_x, expected_Sigma_xp, expected_mean_x,"
    " expected_Sigma_y, expected_Sigma_yp, expected_mean_y",
    FIELD_OFFSET_CASES
)
def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store,
         case, x_offset, y_offset, z_offset,
         expected_Sigma_x, expected_Sigma_xp, expected_mean_x,
         expected_Sigma_y, expected_Sigma_yp, expected_mean_y):

    os.chdir(Path(__file__).resolve().parent)

    base_name     = f"field_offset_{case}"
    template_name = "field_map_offset.tpl"
    gmad_name     = base_name + ".gmad"
    root_name     = base_name + ".root"

    params = {
        'FIELD_TYPE': 'bmap3d',
        'FIELD_FORMAT': 'bdsim3d',
        'FIELD_FILE': '3dexample.dat',
        'FIELD_LENGTH': '1.0',
        'BEAM_ENERGY': '10.0',
        'FIELD_X_OFFSET': x_offset,
        'FIELD_Y_OFFSET': y_offset,
        'FIELD_Z_OFFSET': z_offset,
    }

    nprimary = testlength_primaries.get_nprimary(__file__, test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name, gmad_name, params)
    pybdsim.Run.Bdsim(gmad_name, base_name, nprimary, 1)

    data = pybdsim.DataPandas.BDSIMOutput(root_name)
    sampler_data = data.get_sampler("d2.")

    sampler_Sigma_x  = sampler_data['x'].std()
    sampler_Sigma_xp = sampler_data['xp'].std()
    sampler_mean_x   = sampler_data['x'].mean()
    sampler_Sigma_y  = sampler_data['y'].std()
    sampler_Sigma_yp = sampler_data['yp'].std()
    sampler_mean_y   = sampler_data['y'].mean()

    assert pytest.approx(sampler_Sigma_x, rel=1e-3)  == expected_Sigma_x
    assert pytest.approx(sampler_Sigma_xp, rel=1e-3) == expected_Sigma_xp
    assert pytest.approx(sampler_mean_x, rel=1e-3)   == expected_mean_x
    assert pytest.approx(sampler_Sigma_y, rel=1e-3)  == expected_Sigma_y
    assert pytest.approx(sampler_Sigma_yp, rel=1e-3) == expected_Sigma_yp
    assert pytest.approx(sampler_mean_y, rel=1e-3)   == expected_mean_y

    te = testdata_store.new_test_entry("14_field/field_offset_" + case, __file__, nprimary, 0)
    te.add_input_parameter_dict(params)
    te.add_output_file(os.path.dirname(__file__)+"/"+root_name, "root")
    te.add_output_parameter("Sigma_x", sampler_Sigma_x)
    te.add_output_parameter("Sigma_xp", sampler_Sigma_xp)
    te.add_output_parameter("mean_x", sampler_mean_x)
    te.add_output_parameter("Sigma_y", sampler_Sigma_y)
    te.add_output_parameter("Sigma_yp", sampler_Sigma_yp)
    te.add_output_parameter("mean_y", sampler_mean_y)
