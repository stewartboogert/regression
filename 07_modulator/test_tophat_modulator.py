import pybdsim
import numpy as np


def modulator(t, t0, t1, amplitudeScale):
    if t0 <= t <= t1:
        return amplitudeScale
    else:
        return 0


def test():
    momentum = '50.0'
    magnet_length = '1.0'
    t0 = '-0.5'
    t1 = '0.5'
    scale = '2.0'

    particle_times = np.array([-1, -0.25, 0, 0.25, 1])
    coordinates = [[0, t] for t in particle_times]
    beamfilename = 'beam_tophat_modulator.dat.gz'
    pybdsim.Beam.WriteUserFile(beamfilename, coordinates)

    #B-Field is defined as uniform [0, 1, 0]
    b_fields = np.array([modulator(t, float(t0), float(t1), float(scale)) for t in particle_times])
    deflection_angles = -0.299792458 * b_fields * float(magnet_length) / float(momentum)

    base_name = "tophat_modulator"
    template_name = base_name + ".tpl"
    gmad_name = base_name + ".gmad"
    root_name = base_name + ".root"

    data = {
        'T0': t0,
        'T1': t1,
        'SCALE': scale,
        'LENGTH': magnet_length,
        'MOMENTUM': momentum,
        'BEAMFILENAME': beamfilename
    }

    pybdsim.Run.RenderGmadJinjaTemplate(template_name, gmad_name, data)
    pybdsim.Run.Bdsim(gmad_name, base_name, len(particle_times))
    d = pybdsim.Data.Load(root_name)

    assert np.all(np.array([np.abs(event.d1.xp[0] - deflection_angles[i]) < 1e-6 for i, event in enumerate(d.GetEventTree())]))
