import pytest
import pybdsim
import os
from pathlib import Path
import platform


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

    params = {'SAMPLER_SETTING':'sample, all;',
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
            assert(ntraj == 8899)
            assert(len(t) == 38)
        # TOOD other geant4 versions

    data = pybdsim.Data.Load(root_name)
    et = data.GetEventTree()
    e = data.GetEvent()
    et.GetEntry(0)

    debug_file_name = "temp_"+pname+".dat"
    v,h = pybdsim.Analysis.Trajectory.traverse_trajectories(e.Trajectory, None)

    system = platform.system()
    if system == 'Linux' :
        if pname == "samplenone":
            if geant4_version == '11.0.4' or geant4_version == '10.7.4':
                assert(h.hex() == "ceb52bc2651e899f0ee1e3288afe01a20a22af65989b81236fb8883cc8750a64")
            else :
                assert (h.hex() == "eb99b05bbd61e978982a5d6e92524a564a0f4d30869cc57b3da10f8429f67faf")
        elif pname == "sampleall":
            assert (h.hex() == "d2bef3e58a40be42e99fa0105245437c289e7ff47199d8062d7105649977fe01")
        elif pname == "physicsList_em" :
            if geant4_version == '11.4.2' :
                assert(h.hex() == "e9f00c17e00380ffa3374403d07b5e6765686405f932fef82ef1e8333da60372")
            elif geant4_version == '11.3.2' :
                assert(h.hex() == "37f6ebd9cb5874442c8430cbc5b12b0af3c657308b57cce024418ed6b1c44525")
            elif geant4_version == '11.2.2' :
                assert(h.hex() == "d677ddd9b91c505054cfe5d8240b37d44d8fb0a13c931ec63c277fe136570fc9")
            elif geant4_version == '11.1.3' :
                assert(h.hex() == "5dd262fe7fa142b48b3cda948ea4be38ab5a68a3d04881d660d6fbefdd2789a1")
            elif geant4_version == '11.0.4' :
                assert(h.hex() == "3da5858fdfb7c9f1a8cf78e855a2c75bed32a1cc34a495d16e231e70ca8d39fb")
            elif geant4_version == '10.7.4' :
                assert(h.hex() == "eac9bb2be02613edcfa24251947e1b46e78269aa40414211e574cc0c38bc30a0")

    # store output parameters for regression testing
    te = testdata_store.new_test_entry("21_trajectory/trajectory"+"_"+pname, __file__, ngenerate, 0)
    te.add_input_parameter_dict(params)
    te.add_output_parameter("ntraj", int(ntraj))
    te.add_output_parameter("len(trajectory)",len(t))
    te.add_output_parameter("hash(trajectory)",h.hex())