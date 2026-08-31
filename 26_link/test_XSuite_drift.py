import pytest

import numpy as np
import xtrack as xt

import os

pytestmark = pytest.mark.xfail(reason="requires bdsim")

def drift() :

    import bdsim

    d = xt.Drift(length=1)

    e = bdsim.Element()
    e.name = "d1"
    e.type = bdsim.elementtype.ElementType.DRIFT
    e['l'] = 1.0
    # xt_bdsimelement = bdsim.xsuite.BDSIMElement(e)

    line = xt.Line(elements=[d])
    line.particle_ref = xt.Particles(mass0=xt.PROTON_MASS_EV, q0=1, energy0=7e12)

    particles = line.build_particles(
        nemitt_x=2.5e-6, nemitt_y=1e-6,
        x=[-1, 0, 0.5], y=[0.3, -0.2, 0.2],
        px=[0.1, 0.2, 0.3], py=[0.5, 0.6, 0.8],
        zeta=[0, 0.1, -0.1], delta=[1e-4, 0., -1e-4])

    d.track(particles)

def test_drift(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    os.chdir(os.path.dirname(__file__))
    code = make_bdsim_test_code(drift)
    result = run_bdsim_test_code_as_subprocess(code)