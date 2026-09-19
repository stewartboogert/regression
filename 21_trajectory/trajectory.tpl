d1: drift, l=1*m;
c1: rcol, l=5*cm, xsize=0, ysize=0, material="G4_Fe";
d2: drift, l=1*m;

l0 : line = (d1,c1,d2);

use, period=l0;

{{ SAMPLER_SETTING }}

beam, particle="e-",
      energy=10*GeV,
      X0=0.0*m,
      Xp0=0.0,
      Y0=0.0*m,
      Yp0=0.0,
      distrType="reference";

option, {{ PHYSICS_LISTS }}
        seed=1,
        storeTrajectory=1,
        storeTrajectoryDepth=-1,
        storeTrajectoryAllVariables=1,
        storeEloss=1,
        storeElossLinks=1;