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
    
    base_name     = "gaussmatrix"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    l  = 2.0 
    params = {
        'SIG11' : '0.002*0.002',
        'SIG22' : '0.09*0.005*0.09*0.005',
        'SIG33' : '0.002*0.002',
        'SIG44' : '0.09*0.005*0.09*0.005',
        'SIG55' : '1e-9*1e-9',
        'SIG66' : '1e-5*1e-5'
            }

    paramsValue = {
        'SIG11' : 0.002*0.002,
        'SIG22' : 0.09*0.005*0.09*0.005,
        'SIG33' : 0.002*0.002,
        'SIG44' : 0.09*0.005*0.09*0.005,
        'SIG55' : 1e-9*1e-9,
        'SIG66' : 1e-5*1e-5
            }

    # set parametrised value
    params[param] = value

    # get number of primaries to simulate
    nprimary = testlength_primaries.get_nprimary(__file__,test_length)

    pybdsim.Run.RenderGmadJinjaTemplate(template_name,gmad_name,params)
    pybdsim.Run.Bdsim(gmad_name,base_name,nprimary,1)

    data = pybdsim.DataPandas.BDSIMOutput(root_name)
    primary_data = data.get_primary()
    
    primary_x = primary_data['x']
    primary_xp = primary_data['xp']
    primary_y = primary_data['y']
    primary_yp = primary_data['yp']  
    primary_t = primary_data['T']
    primary_energy = primary_data['energy']
    number_particles=len(primary_x)

    sigma_x_generated = np.std(primary_x)
    sigma_xp_generated = np.std(primary_xp)
    sigma_y_generated = np.std(primary_y)
    sigma_yp_generated = np.std(primary_yp)
    sigma_t_generated = np.std(primary_t)*1e-9 # convert from nano seconds to seconds for gmad to geant root output
    sigma_energy_generated = np.std(primary_energy)
    print(sigma_t_generated/1e9)
    sigma_x_input = np.sqrt(float(paramsValue['SIG11']))
    sigma_xp_input = np.sqrt(float(paramsValue['SIG22']))
    sigma_y_input = np.sqrt(float(paramsValue['SIG33']))
    sigma_yp_input = np.sqrt(float(paramsValue['SIG44']))
    sigma_t_input = np.sqrt(float(paramsValue['SIG55']))
    sigma_energy_input = np.sqrt(float(paramsValue['SIG66']))

    assert(number_particles == nprimary)
    assert(sigma_x_input == pytest.approx(sigma_x_generated,abs=1e-3))
    assert(sigma_xp_input == pytest.approx(sigma_xp_generated,abs=1e-3))
    assert(sigma_y_input == pytest.approx(sigma_x_generated,abs=1e-3))
    assert(sigma_yp_input == pytest.approx(sigma_xp_generated,abs=1e-3))
    assert(sigma_t_input == pytest.approx(sigma_t_generated,abs=1e-1))
    assert(sigma_energy_input == pytest.approx(sigma_energy_generated,abs=1e-3))

    te = testdata_store.new_test_entry("02_beam/guassmatrix"+"_"+pname, __file__, nprimary, 0)
    te.add_input_parameter_dict(params)




    



