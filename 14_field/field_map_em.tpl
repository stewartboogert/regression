d1: drift, l=1*m;
f1: field, type="{{ FIELD_TYPE }}"{% if E_SCALING %}, electricFile="{{ FIELD_FORMAT }}:{{ FIELD_FILE }}", eScaling={{ E_SCALING }}{% endif %}{% if B_SCALING %}, magneticFile="{{ FIELD_FORMAT }}:{{ FIELD_FILE }}", bScaling={{ B_SCALING }}{% endif %};
d_field: drift, l={{ FIELD_LENGTH }}*m, fieldAll="f1";
d2: drift, l=1*m;

l0: line = (d1, d_field, d2);
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
      T0={{ T0 }}*ns,
      sigmaT=1e-11;
