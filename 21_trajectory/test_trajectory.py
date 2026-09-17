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
    data = pybdsim.DataPandas.BDSIMOutput(root_name)

    # event structure
    e = data.get_events()
    ntraj = e.iloc[0]['ntraj']

    # find primary trajectory
    trajectories = data.get_trajectories(0)
    iprimary = trajectories[trajectories['parentID'] == 0].index.tolist()[0]

    # assert on primary trajectory
    t, ids = data.get_trajectory(0, iprimary)

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
        
    # store output parameters for regression testing
    te = testdata_store.new_test_entry("21_trajectory/trajectory"+"_"+pname, __file__, ngenerate, 0)
    te.add_input_parameter_dict(params)
    te.add_output_parameter("ntraj", int(ntraj))
    te.add_output_parameter("len(trajectory)",len(t))