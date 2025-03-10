import pybdsim
import numpy as np


def modulator(t, t0, t1, amplitudeScale, amplitudeOffset):
    if t0 <= t <= t1:
        return amplitudeScale * t + amplitudeOffset
    else:
        return 0


def test():
    momentum = '50.0'
    magnet_length = '1.0'
    t0 = '-0.51'
    t1 = '0.51'
    scale = '2.0'
    offset = '2.0'

    particle_times = np.array([-1, -0.5, -0.25, 0, 0.25, 0.5, 1])
    coordinates = [[0, t] for t in particle_times]
    beamfilename = 'beam.dat.gz'
    pybdsim.Beam.WriteUserFile(beamfilename, coordinates)

    #B-Field is defined as uniform [0, 1, 0]
    b_fields = np.array([modulator(t, float(t0), float(t1), float(scale), float(offset)) for t in particle_times])
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
        'MOMENTUM': momentum,
        'BEAMFILENAME': beamfilename
    }

    pybdsim.Run.RenderGmadJinjaTemplate(template_name, gmad_name, data)
    pybdsim.Run.Bdsim(gmad_name, base_name, 7)
    d = pybdsim.Data.Load(root_name)

    results = np.array([np.abs(event.d1.xp[0] - deflection_angles[i]) < 1e-6 for i, event in enumerate(d.GetEventTree())])

    assert np.all(results)
