beamgasBias: xsecBias, xsecfact={1e11}, particle="e-", flag={2}, proc="eBrem";

d1: drift, l={{ DRIFT_LENGTH }} *m;
t1: rcol, l={{ RCOL_LENGTH }}*m, material="G4_Fe", xsize=0, ysize=0;
d2: drift, l=0.1*m;
b1: sbend, l={{ SBEND_LENGTH }}*m, angle=0.01;
q1: quadrupole, l={{ QUAD_LENGTH }}*m, k1=0.025;
q2: quadrupole, l={{ QUAD_LENGTH }}*m, k1=-0.025;

l0 : line = (d1,q1,d2,q2,d2,q1,d2,q2,d2,q1,d2,q2);

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

option, physicsList = "em em_extra",
        defaultBiasVacuum="beamgasBias",
        physicsVerbose=1;
