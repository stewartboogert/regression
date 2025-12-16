# pip install pytest-xdist
# pytest -n auto

import os

def drift_proton_5TeV() :
    import bdsim
    import numpy as np

    def polarToCartesianMomenta(theta, phi, momentum):
        px = momentum*np.sin(theta)*np.cos(phi)
        py = momentum*np.sin(theta)*np.sin(phi)
        pz = momentum*np.cos(theta)

        return [float(px), float(py), float(pz)]

    tracker_l = bdsim.BDSLinkTrackerInterface.GetInstance("./trackerInterface.gmad", 2212, 5*bdsim.clhep.TeV, 0.01, 1234, 1, 1)
    bdsim_l = tracker_l.GetBDSIMLink()

    # create element
    e = bdsim.Element()
    e.name = "drift1"
    e.type = bdsim.elementtype.ElementType.DRIFT
    e.l = 1.0

    # add element
    bdsim_l = tracker_l.GetBDSIMLink()
    bdsim_l.AddLinkElement(e)

    # select element
    bdsim_l.SelectLinkElement("drift1")

    # reference particle
    rp = tracker_l.GetReferenceParticleDefinition()

    # number of particles
    ngenerate = 1000

    # add particle
    theta = np.random.uniform(0, 0.01, ngenerate)
    phi = np.random.uniform(0, 2*np.pi,ngenerate)
    xmm = np.random.uniform(-1, 1, ngenerate)
    ymm = np.random.uniform(-1, 1, ngenerate)
    for i, [t,p,x,y] in enumerate(zip(theta, phi, xmm,ymm)) :
        mom = polarToCartesianMomenta(t, p, rp.Momentum())
        tracker_l.AddParticle(x, y,  *mom , 0.,0.,  i,2212)  # pdgid;

    # beam on
    bdsim_l.BeamOn(ngenerate)

    # get sampler data
    sh = bdsim_l.SamplerHits()

    if "PYTEST_CURRENT_TEST" in os.environ:
        tracker_l.Reset()
        return 0
    else :
        return tracker_l

def test_proton_5TeV(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code = make_bdsim_test_code(drift_proton_5TeV, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    result = run_bdsim_test_code_as_subprocess(code)
