import pytest
import pybdsim
import numpy as np
import os

@pytest.mark.parametrize("param, value, pname", [
    ('X0', "0.1*cm","p1"),
    ('Y0', "0.1*cm","p2"),
    ('Xp0', "0.1", "p3"),
    ('Yp0',"0.1", "p4")
])
def test(geant4_version, bdsim_version,
         test_length, testlength_primaries, testdata_store,
         param, value, pname) :

    os.chdir(os.path.dirname(__file__))
    
    base_name     = "reference"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    # default values for test
    l  = 2.0
    params = {'ENERGY': '1',
              'DRIFT_LENGTH': '2',
              'X0' : 0,
              'Y0' : 0,
              'Xp0' : 0,
              'Yp0' : 0,
    }

    # set parametrised value
    params[param] = value

    # get number of primaries to simulate
    nprimary = testlength_primaries.get_nprimary(__file__,test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,params)
    pybdsim.Run.Bdsim(gmad_name,base_name,nprimary,1)

    data = pybdsim.DataPandas.BDSIMOutput(root_name)
    primary_data = data.get_primary()
    sampler_data=data.get_sampler('t1.')    

    primary_x = primary_data['x']
    primary_xp = primary_data['xp']
    primary_y = primary_data['y']
    primary_yp = primary_data['yp']  
    primary_t = primary_data['T']
    primary_energy = primary_data['energy']
    number_particles=len(primary_x)

    cov_xxp = np.cov(primary_x,primary_xp)
    cov_yyp = np.cov(primary_y,primary_yp)

    sigma_x_generated = np.sqrt(cov_xxp[0][0])
    sigma_xp_generated = np.sqrt(cov_xxp[1][1])
    sigma_y_generated = np.sqrt(cov_yyp[0][0])
    sigma_yp_generated = np.sqrt(cov_yyp[1][1])
    
    emittance_x_generated = np.sqrt(cov_xxp[0][0]*cov_xxp[1][1]-cov_xxp[0][1]*cov_xxp[1][0])
    emittance_y_generated = np.sqrt(cov_yyp[0][0]*cov_yyp[1][1]-cov_yyp[0][1]*cov_yyp[1][0])

    sampler_number = len(sampler_data)
    sampler_x = sampler_data['x']
    sampler_xp = sampler_data['xp']
    sampler_y = sampler_data['y']
    sampler_yp = sampler_data['yp']
    sampler_energy = sampler_data['energy']

    sampler_cov_xxp = np.cov(sampler_x,sampler_xp)
    sampler_cov_yyp = np.cov(sampler_y,sampler_yp)

    sigma_x_sampler = np.sqrt(sampler_cov_xxp[0][0])
    sigma_xp_sampler = np.sqrt(sampler_cov_xxp[1][1])
    sigma_y_sampler = np.sqrt(sampler_cov_yyp[0][0])
    sigma_yp_sampler = np.sqrt(sampler_cov_yyp[1][1])

    emittance_x_sampler = np.sqrt(sampler_cov_xxp[0][0]*sampler_cov_xxp[1][1]-sampler_cov_xxp[0][1]*sampler_cov_xxp[1][0])
    emittance_y_sampler = np.sqrt(sampler_cov_yyp[0][0]*sampler_cov_yyp[1][1]-sampler_cov_yyp[0][1]*sampler_cov_yyp[1][0])

    assert(number_particles == nprimary)
    assert(0 == pytest.approx(sigma_x_generated,abs=1e-3))
    assert(0 == pytest.approx(sigma_x_generated,abs=1e-3))
    assert(0 == pytest.approx(emittance_x_generated,abs=1e-3))
    assert(0 == pytest.approx(emittance_y_generated,abs=1e-3))
    assert(0 == pytest.approx(sigma_xp_generated,abs=1e-3))
    assert(0 == pytest.approx(sigma_yp_generated,abs=1e-3))

    assert(sampler_number == nprimary)
    assert(0 == pytest.approx(sigma_x_sampler,abs=1e-3))
    assert(0 == pytest.approx(sigma_x_sampler,abs=1e-3))
    assert(0 == pytest.approx(emittance_x_sampler,abs=1e-3))
    assert(0 == pytest.approx(emittance_y_sampler,abs=1e-3))
    assert(0 == pytest.approx(sigma_xp_sampler,abs=1e-3))
    assert(0 == pytest.approx(sigma_yp_sampler,abs=1e-3))

    # store output parameters for regression testing
    te = testdata_store.new_test_entry("02_beam/reference"+"_"+pname, __file__, nprimary, 0)
    te.add_input_parameter_dict(params)
    te.add_output_parameter("x_sigma_generated",sigma_x_generated)
    te.add_output_parameter("y_sigma_generated",sigma_y_generated)
    te.add_output_parameter("xp_sigma_generated",sigma_xp_generated)
    te.add_output_parameter("yp_sigma_generated",sigma_yp_generated)
    te.add_output_parameter("x_emittance_generated", emittance_x_generated)
    te.add_output_parameter("y_emittance_generated", emittance_y_generated)

    te.add_output_parameter("x_sigma_sampler",sigma_x_sampler)
    te.add_output_parameter("y_sigma_sampler",sigma_y_sampler)
    te.add_output_parameter("xp_sigma_sampler",sigma_xp_sampler)
    te.add_output_parameter("yp_sigma_sampler",sigma_yp_sampler)
    te.add_output_parameter("x_emittance_sampler", emittance_x_sampler)
    te.add_output_parameter("y_emittance_sampler", emittance_y_sampler)


    



