import pybdsim
import os
import pytest
from pathlib import Path

# case, FIELD_TYPE, FIELD_FORMAT, FIELD_FILE, BEAM_ENERGY, FIELD_INTERPOLATOR,
# expected Sigma_x, Sigma_xp, mean_x, Sigma_y, Sigma_yp, mean_y
FIELD_INTERPOLATION_CASES = [
    ("1d_linear",    "bmap1d", "bdsim1d", "1dexample.dat", "1.0", "linear",
     0.005354202580646126, 0.001999076865966775, 0.009670783941715035,
     0.013084708676590241, 0.007202701938688855, -0.49687208319306375),
    ("1d_linearmag", "bmap1d", "bdsim1d", "1dexample.dat", "1.0", "linearmag",
     0.005360657975868763, 0.0020020719479500963, 0.009683479112656596,
     0.01307943167235869, 0.0072005010788836685, -0.49720062289237976),
    ("1d_nearest",   "bmap1d", "bdsim1d", "1dexample.dat", "1.0", "nearest",
     0.0018571098686965446, 0.0004469812469452971, 0.009439205919555388,
     0.01307691510397638, 0.007198931645154899, -0.49778312349915504),
    ("2d_linear",    "bmap2d", "bdsim2d", "2dexample.dat", "1.0", "linear",
     0.015804539022049573, 0.010316564235008652, 8.499772373153859e-05,
     0.0021579719729259575, 0.0023403134007770198, 1.8904866732009396e-05),
    ("2d_linearmag", "bmap2d", "bdsim2d", "2dexample.dat", "1.0", "linearmag",
     0.01969824900808272, 0.013199531233735034, 0.00010222111806351676,
     0.0038697662117538945, 0.004129952429779972, 4.843972614912673e-06),
    ("2d_nearest",   "bmap2d", "bdsim2d", "2dexample.dat", "1.0", "nearest",
     0.003369653184855525, 0.0017251188722198771, 3.561127408404445e-05,
     0.021222188911178278, 0.021194220357673686, -0.00018837782195287218),
    ("2d_cubic",     "bmap2d", "bdsim2d", "2dexample.dat", "1.0", "cubic",
     0.018419807674184555, 0.012275748730702854, 0.00010576244183662311,
     0.0028903558879167703, 0.0032919311481443892, 1.0439962574434957e-05),
    ("3d_linear",    "bmap3d", "bdsim3d", "3dexample.dat", "10.0", "linear",
     0.014324369577942097, 0.007515015279365734, 0.5660426369667053,
     0.0044860079849747825, 0.002270031791075037, 0.22305434429049492),
    ("3d_linearmag", "bmap3d", "bdsim3d", "3dexample.dat", "10.0", "linearmag",
     0.014327077885869297, 0.007516079445364859, 0.5661105772137642,
     0.004486432469495695, 0.002270183744965747, 0.22307491642832755),
    ("3d_nearest",   "bmap3d", "bdsim3d", "3dexample.dat", "10.0", "nearest",
     0.015180510433518032, 0.007908333993363166, 0.5767620910525322,
     0.00595327484532122, 0.003382907443600101, 0.22346383558809757),
    ("3d_cubic",     "bmap3d", "bdsim3d", "3dexample.dat", "10.0", "cubic",
     0.014271013981376675, 0.007416345178360901, 0.5799057118058205,
     0.004409168245179408, 0.002207146467824476, 0.226743698656559),
    ("4d_linear",    "bmap4d", "bdsim4d", "4dexample.dat", "1.0", "linear",
     0.0017761945113131978, 0.00035136689967708905, 1.3215959309269466e-05,
     0.0017857934386989697, 0.0003543900315124393, -2.1371774069270798e-05),
    ("4d_linearmag", "bmap4d", "bdsim4d", "4dexample.dat", "1.0", "linearmag",
     0.0017761945113131978, 0.00035136689967708905, 1.3215959309269466e-05,
     0.0017857934386989697, 0.0003543900315124393, -2.1371774069270798e-05),
    ("4d_nearest",   "bmap4d", "bdsim4d", "4dexample.dat", "1.0", "nearest",
     0.0017761945113131978, 0.00035136689967708905, 1.3215959309269466e-05,
     0.0017857934386989697, 0.0003543900315124393, -2.1371774069270798e-05),
    # values below are valid for Geant4 >= 11.2.0 - see G4_PRE_11_2_OVERRIDES
    ("4d_cubic",     "bmap4d", "bdsim4d", "4dexample.dat", "1.0", "cubic",
     0.0017761945113131978, 0.00035136689967708905, 1.3215959309269466e-05,
     0.0017857934386989697, 0.0003543900315124393, -2.1371774069270798e-05),
]

# Geant4 v11.2.0 changed G4PropagatorInField step-size handling (new
# fMaxStepSizeMultiplier/fMinBigDistance parameters - see G4 v11.2.0 release
# notes), which shifts exactly where BDSIM's cubic 4D field interpolator
# samples the field map. Confirmed identical on Geant4 10.7.4/11.0.4/11.1.3;
# confirmed matching FIELD_INTERPOLATION_CASES' 4d_cubic values on 11.2+
# (and identical to test_field_tracking.py's "4d" case, since cubic is
# BDSIM's default 4D interpolator).
G4_PRE_11_2_OVERRIDES = {
    "4d_cubic": (0.0016556805394320657, 0.0002906922050868294, 0.00022163846734898129,
                 0.0018062131083373385, 0.00038040219503206527, 8.285922579478395e-05),
}


def _g4_pre_11_2(geant4_version):
    major, minor = (int(x) for x in geant4_version.split(".")[:2])
    return (major, minor) < (11, 2)


@pytest.mark.parametrize(
    "case, field_type, field_format, field_file, beam_energy, interpolator,"
    " expected_Sigma_x, expected_Sigma_xp, expected_mean_x,"
    " expected_Sigma_y, expected_Sigma_yp, expected_mean_y",
    FIELD_INTERPOLATION_CASES
)
def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store,
         case, field_type, field_format, field_file, beam_energy, interpolator,
         expected_Sigma_x, expected_Sigma_xp, expected_mean_x,
         expected_Sigma_y, expected_Sigma_yp, expected_mean_y):

    os.chdir(Path(__file__).resolve().parent)

    base_name     = f"field_interpolation_{case}"
    template_name = "field_map_interpolator.tpl"
    gmad_name     = base_name + ".gmad"
    root_name     = base_name + ".root"

    params = {
        'FIELD_TYPE': field_type,
        'FIELD_FORMAT': field_format,
        'FIELD_FILE': field_file,
        'FIELD_LENGTH': '1.0',
        'BEAM_ENERGY': beam_energy,
        'FIELD_INTERPOLATOR': interpolator,
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

    if case in G4_PRE_11_2_OVERRIDES and _g4_pre_11_2(geant4_version):
        (expected_Sigma_x, expected_Sigma_xp, expected_mean_x,
         expected_Sigma_y, expected_Sigma_yp, expected_mean_y) = G4_PRE_11_2_OVERRIDES[case]

    assert pytest.approx(sampler_Sigma_x, rel=1e-3)  == expected_Sigma_x
    assert pytest.approx(sampler_Sigma_xp, rel=1e-3) == expected_Sigma_xp
    assert pytest.approx(sampler_mean_x, rel=1e-3)   == expected_mean_x
    assert pytest.approx(sampler_Sigma_y, rel=1e-3)  == expected_Sigma_y
    assert pytest.approx(sampler_Sigma_yp, rel=1e-3) == expected_Sigma_yp
    assert pytest.approx(sampler_mean_y, rel=1e-3)   == expected_mean_y

    te = testdata_store.new_test_entry("14_field/field_interpolation_" + case, __file__, nprimary, 0)
    te.add_input_parameter_dict(params)
    te.add_output_file(os.path.dirname(__file__)+"/"+root_name, "root")
    te.add_output_parameter("Sigma_x", sampler_Sigma_x)
    te.add_output_parameter("Sigma_xp", sampler_Sigma_xp)
    te.add_output_parameter("mean_x", sampler_mean_x)
    te.add_output_parameter("Sigma_y", sampler_Sigma_y)
    te.add_output_parameter("Sigma_yp", sampler_Sigma_yp)
    te.add_output_parameter("mean_y", sampler_mean_y)
