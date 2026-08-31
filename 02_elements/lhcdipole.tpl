d1: drift, l=1*m, aper1=3*cm;
b1: sbend, magnetGeometryType="lhcleft", l=1*m, aper1=3*cm, angle=-0.5;
d2: drift, l=1*m, aper1=3*cm;

l0 : line = (d1,b1,d2);

use, period=l0;

sample, all;

beam, particle="proton",
      energy=7*TeV,
      X0={{ X0 }}*cm,
      Y0={{ Y0 }}*cm;

sampler: samplerplacement, z=5*m, aper1=5*m, aper2=5*m, shape="rectangular", partID={2212};
