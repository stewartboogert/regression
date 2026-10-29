import pybdsim
import os
import pytest
from pathlib import Path
from typing import Any, Optional

# case, FIELD_TYPE, FIELD_FORMAT, FIELD_FILE, E_SCALING, B_SCALING, T0
# E_SCALING and B_SCALINg are neccessary to prevent either field from dominating
# expected Sigma_x, Sigma_xp, mean_x, Sigma_y, Sigma_yp, mean_y, mean_dE
# mean_dE is the mean energy gain in MeV from the sampler before to the one after the field.
FIELD_EM_CASES = [
    ("emap_1d", "emap1d", "bdsim1d", "1dexample.dat", "1e6", None, "0",
     0.0017803453103012264, 0.0003603543511468917, -0.005994415771191416,
     0.001786320550804256, 0.00035479668576939537, -6.434119632660895e-06, -0.5841668009758383),
    ("ebmap_1d", "ebmap1d", "bdsim1d", "1dexample.dat", "1e6", "0.002", "0",
     0.0018043585188031459, 0.0003664727420890056, -0.006002826991910843,
     0.0017867188549562693, 0.00035791966218459297, -0.003609459846706295, -0.5841798067093285),
    ("emap_2d", "emap2d", "bdsim2d", "2dexample.dat", "1e6", None, "0",
     0.0017808560922912844, 0.000359030828461541, 1.418676564414909e-05,
     0.0017871023818352577, 0.00035546108018698786, -2.1692428283415665e-05, -2.9999024152755904),
    ("ebmap_2d", "ebmap2d", "bdsim2d", "2dexample.dat", "1e6", "0.002", "0",
     0.001799358867831519, 0.0003636765826122359, 1.4375907227329065e-05,
     0.0017312555799670756, 0.00034341415705282615, -2.111175043076514e-05, -2.999902141094246),
    ("emap_3d", "emap3d", "bdsim3d", "3dexample.dat", "1e6", None, "0",
     0.0017809298453082575, 0.00035671939256067366, 0.00651370110327116,
     0.0017984152897977843, 0.00036366771242359047, -0.012750011442229151, 2.605745756626199),
    ("ebmap_3d", "ebmap3d", "bdsim3d", "3dexample.dat", "1e6", "0.002", "0",
     0.0018121811349968635, 0.0003701731745198828, 0.014106991355959326,
     0.0017510580380473827, 0.0003499364565116011, -0.008933986345445738, 2.6097755432128444),
    ("emap_4d", "emap4d", "bdsim4d", "4dexample.dat", "1e6", None, "-5",
     0.0018004518045887307, 0.00039581939701401265, -0.01427978038424626,
     0.0018851422728214213, 0.0005042518668551149, 0.028468481404706834, -2.087845885753614),
    ("ebmap_4d", "ebmap4d", "bdsim4d", "4dexample.dat", "1e6", "0.002", "-5",
     0.0018862623929632096, 0.0005299124315819688, -0.03137310663461685,
     0.0018438110204553613, 0.0004338458919581707, 0.019884576276130973, -2.0877945661544883),
]


@pytest.mark.parametrize(
    "case, field_type, field_format, field_file, e_scaling, b_scaling, t0,"
    " expected_Sigma_x, expected_Sigma_xp, expected_mean_x,"
    " expected_Sigma_y, expected_Sigma_yp, expected_mean_y, expected_mean_dE",
    FIELD_EM_CASES
)
def test(geant4_version: str, bdsim_version: str,
         test_length: str, testlength_primaries: Any, testdata_store: Any,
         case: str, field_type: str, field_format: str, field_file: str,
         e_scaling: str, b_scaling: Optional[str], t0: str,
         expected_Sigma_x: float, expected_Sigma_xp: float, expected_mean_x: float,
         expected_Sigma_y: float, expected_Sigma_yp: float, expected_mean_y: float,
         expected_mean_dE: float) -> None:

    os.chdir(Path(__file__).resolve().parent)

    base_name     = f"field_em_tracking_{case}"
    template_name = "field_map_em.tpl"
    gmad_name     = base_name + ".gmad"
    root_name     = base_name + ".root"

    params = {
        'FIELD_TYPE': field_type,
        'FIELD_FORMAT': field_format,
        'FIELD_FILE': field_file,
        'FIELD_LENGTH': '1.0',
        'BEAM_ENERGY': '1.0',
        'T0': t0,
        'E_SCALING': e_scaling,
    }
    if b_scaling is not None:
        params['B_SCALING'] = b_scaling

    nprimary = testlength_primaries.get_nprimary(__file__, test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name, gmad_name, params)
    sproc, timing = pybdsim.Run.Bdsim(gmad_name, base_name, nprimary, seed=1, returnTiming=True)

    data = pybdsim.DataPandas.BDSIMOutput(root_name)
    sampler_before = data.get_sampler("d1.")
    sampler_after  = data.get_sampler("d2.")

    sampler_Sigma_x  = sampler_after['x'].std()
    sampler_Sigma_xp = sampler_after['xp'].std()
    sampler_mean_x   = sampler_after['x'].mean()
    sampler_Sigma_y  = sampler_after['y'].std()
    sampler_Sigma_yp = sampler_after['yp'].std()
    sampler_mean_y   = sampler_after['y'].mean()
    sampler_mean_dE  = (sampler_after['energy'].mean() - sampler_before['energy'].mean()) * 1e3

    assert pytest.approx(sampler_Sigma_x, rel=1e-3)  == expected_Sigma_x
    assert pytest.approx(sampler_Sigma_xp, rel=1e-3) == expected_Sigma_xp
    assert pytest.approx(sampler_mean_x, rel=1e-3)   == expected_mean_x
    assert pytest.approx(sampler_Sigma_y, rel=1e-3)  == expected_Sigma_y
    assert pytest.approx(sampler_Sigma_yp, rel=1e-3) == expected_Sigma_yp
    assert pytest.approx(sampler_mean_y, rel=1e-3)   == expected_mean_y
    assert pytest.approx(sampler_mean_dE, rel=1e-3)  == expected_mean_dE

    te = testdata_store.new_test_entry("14_field/field_em_tracking_" + case, __file__, nprimary, timing)
    te.add_input_parameter_dict(params)
    te.add_output_file(os.path.dirname(__file__)+"/"+root_name, "root")
    te.add_output_parameter("Sigma_x", sampler_Sigma_x)
    te.add_output_parameter("Sigma_xp", sampler_Sigma_xp)
    te.add_output_parameter("mean_x", sampler_mean_x)
    te.add_output_parameter("Sigma_y", sampler_Sigma_y)
    te.add_output_parameter("Sigma_yp", sampler_Sigma_yp)
    te.add_output_parameter("mean_y", sampler_mean_y)
    te.add_output_parameter("mean_dE", sampler_mean_dE)
