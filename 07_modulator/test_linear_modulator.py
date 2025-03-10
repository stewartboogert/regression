import pybdsim
import numpy as np


def scaling_factor(t, t0=-0.51, t1=0.51, amplitudeScale=2.0, amplitudeOffset=2.0):
    if t0 <= t <= t1:
        return amplitudeScale * t + amplitudeOffset
    else:
        return 0.0
    
def write_beamfile(particle_times):
    with open('beam.dat', 'w') as f:
        for t in particle_times:
            f.write('0.0\t' + str(t) + '\n')


def test():
    momentum = '50.0'
    magnet_length = '1.0'
    t0 = '-0.51'
    t1 = '0.51'
    scale = '2.0'
    offset = '2.0'

    particle_times = np.array([-1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 1.0])
    write_beamfile(particle_times)

    #B-Field is defined as uniform [0, 1, 0]
    b_fields = np.array([scaling_factor(t, float(t0), float(t1), float(scale), float(offset)) for t in particle_times])
    deflection_angles = -0.299792458 * b_fields * float(magnet_length) / float(momentum)

    base_name = "linear_modulator"
    template_name = base_name + ".tpl"
    gmad_name = base_name + ".gmad"
    root_name = base_name + ".root"

    data = {
        'T0': t0,
        'T1': t1,
        'SCALE': scale,
        'OFFSET': offset,
        'LENGTH': magnet_length,
        'MOMENTUM': momentum
    }

    pybdsim.Run.RenderGmadJinjaTemplate(template_name, gmad_name, data)
    pybdsim.Run.Bdsim(gmad_name, base_name, 7)
    d = pybdsim.Data.Load(root_name)

    results = [np.abs(event.d1.xp[0] - deflection_angles[i]) < 1e-6 for i, event in enumerate(d.GetEventTree())]

    assert np.all(results)
