d1: drift, l=1*m;
t1: rcol, l={{ LENGTH }}*m, material="G4_Fe", xsize=0, ysize=0;
d2: drift, l=1*m;

l0 : line = (d1,t1,d2);

use, period=l0;

sample, all;

beam, particle="e-",
      energy={{ BEAM_ENERGY }}*GeV,
      X0=0.0*m,
      Xp0=0.0,
      Y0=0.0*m,
      Yp0=0.0, 
      alfx=0,
      alfy=0,
      betx=4*m,
      bety=4*m,
      dispx=0.0*m,
      dispxp=0.0,
      dispy=0.0*m,
      dispyp=0.0,
      distrType="gausstwiss",
      emitx=5e-7*m,
      emity=5e-7*m,
      sigmaE=0.02,
      sigmaT=1e-11;

option, physicsList = "em";

s1: samplerplacement, referenceElement="t1",
                      referenceElementNumber=0,
		      samplerType="cylinder",
                      x=0*cm, y=0*cm, s=0*cm,
                      axisAngle=0, axisY=0, angle=0,
                      aper1=0.5*m, aper2={{ LENGTH }}/2*m;