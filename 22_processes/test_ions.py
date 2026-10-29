import pytest
import pybdsim
import os
from pathlib import Path
import cross_section_analysis

NATURAL_ISOTOPE_MASS_NUMBERS = {
    1: (1, 2),
    2: (3, 4),
    3: (6, 7),
    4: (9,),
    5: (10, 11),
    6: (12, 13),
    7: (14, 15),
    8: (16, 17, 18),
    9: (19,),
    10: (20, 21, 22),
    11: (23,),
    12: (24, 25, 26),
    13: (27,),
    14: (28, 29, 30),
    15: (31,),
    16: (32, 33, 34, 36),
    17: (35, 37),
    18: (36, 38, 40),
    19: (39, 40, 41),
    20: (40, 42, 43, 44, 46, 48),
    21: (45,),
    22: (46, 47, 48, 49, 50),
    23: (50, 51),
    24: (50, 52, 53, 54),
    25: (55,),
    26: (54, 56, 57, 58),
    27: (59,),
    28: (58, 60, 61, 62, 64),
    29: (63, 65),
    30: (64, 66, 67, 68, 70),
    31: (69, 71),
    32: (70, 72, 73, 74, 76),
    33: (75,),
    34: (74, 76, 77, 78, 80, 82),
    35: (79, 81),
    36: (78, 80, 82, 83, 84, 86),
    37: (85, 87),
    38: (84, 86, 87, 88),
    39: (89,),
    40: (90, 91, 92, 94, 96),
    41: (93,),
    42: (92, 94, 95, 96, 97, 98, 100),
    44: (96, 98, 99, 100, 101, 102, 104),
    45: (103,),
    46: (102, 104, 105, 106, 108, 110),
    47: (107, 109),
    48: (106, 108, 110, 111, 112, 113, 114, 116),
    49: (113, 115),
    50: (112, 114, 115, 116, 117, 118, 119, 120, 122, 124),
    51: (121, 123),
    52: (120, 122, 123, 124, 125, 126, 128, 130),
    53: (127,),
    54: (124, 126, 128, 129, 130, 131, 132, 134, 136),
    55: (133,),
    56: (130, 132, 134, 135, 136, 137, 138),
    57: (138, 139),
    58: (136, 138, 140, 142),
    59: (141,),
    60: (142, 143, 144, 145, 146, 148, 150),
    62: (144, 147, 148, 149, 150, 152, 154),
    63: (151, 153),
    64: (152, 154, 155, 156, 157, 158, 160),
    65: (159,),
    66: (156, 158, 160, 161, 162, 163, 164),
    67: (165,),
    68: (162, 164, 166, 167, 168, 170),
    69: (169,),
    70: (168, 170, 171, 172, 173, 174, 176),
    71: (175, 176),
    72: (174, 176, 177, 178, 179, 180),
    73: (180, 181),
    74: (180, 182, 183, 184, 186),
    75: (185, 187),
    76: (184, 186, 187, 188, 189, 190, 192),
    77: (191, 193),
    78: (190, 192, 194, 195, 196, 198),
    79: (197,),
    80: (196, 198, 199, 200, 201, 202, 204),
    81: (203, 205),
    82: (204, 206, 207, 208),
    83: (209,),
    90: (230, 232),
    91: (231,),
    92: (234, 235, 238),
}

param_list = [
    (
        'G4_Cu',
        "1000",
        "5e4",
        f"{atomic_number}",
        f"{mass_number}",
        f"G4_ion_{atomic_number}_{mass_number}",
    )
    for atomic_number, mass_numbers in NATURAL_ISOTOPE_MASS_NUMBERS.items()
    for mass_number in mass_numbers
]

@pytest.mark.parametrize("material, energy, nprimary, Z, A, pname", param_list)
def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store,
         material, energy, nprimary, Z, A, pname) :

    os.chdir(Path(__file__).resolve().parent)

    base_name = "ions"
    template_name = base_name + ".tpl"
    param_name = base_name + "_" + f"{int(Z):02d}" + "_" + f"{int(A):02d}" + "_" + energy
    gmad_name = param_name + ".gmad"
    root_name = param_name+".root"
    json_name = param_name+".json"
    stdout_file = param_name+".stdout"
    stderr_file = param_name+".stderr"
    params = {
        'DRIFT_LENGTH': '1',
        'BEAM_ENERGY' : energy,
        'TARGET_LENGTH' : '1e-3',
        'TARGET_MATERIAL' : material,
        'ION_AZ' : A +" "+ Z
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
    te = testdata_store.new_test_entry("22_processes/ions_" + pname, __file__, nprimary, timing)
    te.add_input_parameter_dict(params)
    te.add_output_file(os.path.dirname(__file__)+"/"+json_name,"json")
    te.add_output_file(os.path.dirname(__file__)+"/"+stdout_file,"stdout")
    te.add_output_file(os.path.dirname(__file__)+"/"+stderr_file,"stderr")