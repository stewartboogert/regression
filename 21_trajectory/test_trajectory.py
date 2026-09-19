import pytest
import pybdsim
import os
from pathlib import Path

@pytest.mark.parametrize("param, value, pname", [
    ('SAMPLER_SETTING', '', 'samplenone'),
    ('SAMPLER_SETTING', 'sample, all;','sampleall'),
    ('PHYSICS_LISTS', 'physicsList="em",','physicsList_em')
])
def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store,
         param, value, pname) :

    os.chdir(Path(__file__).resolve().parent)

    base_name     = "trajectory"+"_"+pname
    template_name = "trajectory.tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    ngenerate = 1

    params = {'SAMPLER_SETTING':'',
              'PHYSICS_LISTS':''}

    # set parametrised value
    params[param] = value

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,params)
    pybdsim.Run.Bdsim(gmad_name,base_name,ngenerate,1)
    dataPandas = pybdsim.DataPandas.BDSIMOutput(root_name)

    # event structure
    e = dataPandas.get_events()
    ntraj = e.iloc[0]['ntraj']

    # find primary trajectory
    trajectories = dataPandas.get_trajectories(0)
    iprimary = trajectories[trajectories['parentID'] == 0].index.tolist()[0]

    # assert on primary trajectory
    t, ids = dataPandas.get_trajectory(0, iprimary)

    if pname == "samplenone" :
        assert(ntraj == 1)
        assert(len(t) == 14)
    elif pname == "sampleall" :
        assert(ntraj == 1)
        assert(len(t) == 20)
    elif pname == "physicsList_em" :
        if geant4_version == '11.4.2' :
            assert(ntraj == 4044)
            assert(len(t) == 72)
        # TOOD other geant4 versions

    data = pybdsim.Data.Load(root_name)
    et = data.GetEventTree()
    e = data.GetEvent()
    et.GetEntry(0)

    debug_file_name = "temp_"+pname+".dat"
    v,h = pybdsim.Analysis.Trajectory.traverse_trajectories(e.Trajectory, None)

    if pname == "samplenone" :
        assert(h.hex() == "eb99b05bbd61e978982a5d6e92524a564a0f4d30869cc57b3da10f8429f67faf")
    elif pname == "sampleall" :
        assert(h.hex() == "d2bef3e58a40be42e99fa0105245437c289e7ff47199d8062d7105649977fe01")
    elif pname == "physicsList_em" :
        assert(h.hex() == "3abba719eb35b4f71dd067e9f502def078cbf0fbc2e195f9d6f1cbc44f82039d")

    # store output parameters for regression testing
    te = testdata_store.new_test_entry("21_trajectory/trajectory"+"_"+pname, __file__, ngenerate, 0)
    te.add_input_parameter_dict(params)
    te.add_output_parameter("ntraj", int(ntraj))
    te.add_output_parameter("len(trajectory)",len(t))
    te.add_output_parameter("hash(trajectory)",h.hex())