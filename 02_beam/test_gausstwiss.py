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
    
    base_name     = "gausstwiss"
    template_name = base_name+".tpl"
    gmad_name     = base_name+".gmad"
    root_name     = base_name+".root"

    l  = 2.0 
    params = {
        'BETX': '4',
        'BETY' : '4',
        'EMITX' : '5e-7',
        'EMITY' : '5e-7'
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

    cov_xxp = np.cov(primary_x,primary_xp)
    cov_yyp = np.cov(primary_y,primary_yp)


    sigma_x_generated = np.sqrt(cov_xxp[0][0])
    sigma_y_generated = np.sqrt(cov_yyp[0][0])
    sigma_x_calculated = np.sqrt(float(params['BETX'])*float(params['EMITX']))
    sigma_y_calculated = np.sqrt(float(params['BETY'])*float(params['EMITY']))
    
    emittance_x_generated = np.sqrt(cov_xxp[0][0]*cov_xxp[1][1]-cov_xxp[0][1]*cov_xxp[1][0])
    emittance_y_generated = np.sqrt(cov_yyp[0][0]*cov_yyp[1][1]-cov_yyp[0][1]*cov_yyp[1][0])
    emittance_x_input = float(params['EMITX'])
    emittance_y_input = float(params['EMITY'])
    
    courant_synder_gamma_x = 1/float(params['BETX']) # if alphax == 0
    courant_synder_gamma_y = 1/float(params['BETY']) # if alphay == 0
    
    sigma_xp_generated = np.sqrt(cov_xxp[1][1])
    sigma_yp_generated = np.sqrt(cov_yyp[1][1])
    sigma_xp_calculated = (emittance_x_input/np.pi-sigma_x_calculated*courant_synder_gamma_x)/float(params['BETX'])
    sigma_yp_calculated = (emittance_y_input/np.pi-sigma_y_calculated*courant_synder_gamma_y)/float(params['BETY'])

    assert(number_particles == nprimary)
    assert(sigma_x_calculated == pytest.approx(sigma_x_generated,abs=1e-3))
    assert(sigma_y_calculated == pytest.approx(sigma_x_generated,abs=1e-3))
    assert(sigma_xp_calculated == pytest.approx(sigma_xp_generated,abs=1e-3))
    assert(sigma_yp_calculated == pytest.approx(sigma_xp_generated,abs=1e-3))
    assert(emittance_x_input == pytest.approx(emittance_x_generated,abs=1e-3))
    assert(emittance_y_input == pytest.approx(emittance_y_generated,abs=1e-3))

    te = testdata_store.new_test_entry("02_beam/guasstwiss"+"_"+pname, __file__, nprimary, 0)
    te.add_input_parameter_dict(params)




    



