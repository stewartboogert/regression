d1: drift, l=1*m;
t1: drift, l=2*m;
d2: drift, l=1*m;

l0 : line = (d1,t1,d2);

use, period=l0;

sample, all;

beam, particle="e-",
      energy=1*GeV,
      X0=0.0*m,
      Xp0=0.0,
      Y0=0.0*m,
      Yp0=0.0, 
      alfx=0,
      alfy=0,
      betx={{ BETX }}*m,
      bety={{ BETY }}*m,
      dispx=0.0*m,
      dispxp=0.0,
      dispy=0.0*m,
      dispyp=0.0,
      distrType="gausstwiss",
      emitx={{ EMITX }}*m,
      emity={{ EMITY}}*m,
      sigmaE=0.02,
      sigmaT=1e-11;
