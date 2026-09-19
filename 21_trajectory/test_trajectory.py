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

    if pname == "samplenone":
        if geant4_version == '11.0.2' or geant4_version == '10.7.4 ':
            assert(h.hex() == "ceb52bc2651e899f0ee1e3288afe01a20a22af65989b81236fb8883cc8750a64")
        else :
            assert (h.hex() == "eb99b05bbd61e978982a5d6e92524a564a0f4d30869cc57b3da10f8429f67faf")
    elif pname == "sampleall":
        assert (h.hex() == "d2bef3e58a40be42e99fa0105245437c289e7ff47199d8062d7105649977fe01")
    elif pname == "physicsList_em" :
        if geant4_version == '11.4.2' :
            assert(h.hex() == "174bab89f013c6080003187e1240a29a5489a1a1a6c61eb02b3a9f9b9851ad65")
        elif geant4_version == '11.3.2' :
            assert(h.hex() == "a0b5ab9e21cb085d91cb7fb5f7a780219448b180dc69ceabed5442d2144d5fc1")
        elif geant4_version == '11.2.2' :
            assert(h.hex() == "f82167e60c03c0a96d6e9a56dcb1de9290913415b8513fd7c38bc1beb08ac6ff")
        elif geant4_version == '11.1.3' :
            assert(h.hex() == "ea08287c5bcc7157bf56a259874c396d79e4988cf5e30be58834d6dd08aa5e13")
        elif geant4_version == '11.0.4' :
            assert(h.hex() == "b8cd47157fe14e8cc981d67dcce0739efc8e33ac5c8fc4fed3b4cadd2a7f742d")
        elif geant4_version == '10.7.4' :
            assert(h.hex() == "6ee466468653fc1c267c16bfeabf7b8017a186a269869e6d57204b4e022971f7")

    # store output parameters for regression testing
    te = testdata_store.new_test_entry("21_trajectory/trajectory"+"_"+pname, __file__, ngenerate, 0)
    te.add_input_parameter_dict(params)
    te.add_output_parameter("ntraj", int(ntraj))
    te.add_output_parameter("len(trajectory)",len(t))
    te.add_output_parameter("hash(trajectory)",h.hex())