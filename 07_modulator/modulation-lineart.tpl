m1: modulator, type = "lineart", T0 = {{ T0 }}*s, T1 = {{ T1 }}*s, amplitudeScale = {{ SCALE }}, amplitudeOffset = {{ OFFSET }};
f1: field, type = "bmap2d", magneticFile = "bdsim2d:b-field.dat.gz", fieldModulator = "m1";
d1: drift, l = {{ LENGTH }}*m, aper1 = 1.0*m, fieldAll = "f1";

l1: line = (d1);
use, l1;

beam, particle = "proton",
	momentum = {{ MOMENTUM }}*GeV,
	distrType = "userfile",
	distrFile = "beam.dat",
	distrFileFormat = "z[m]:t[s]";

sample, all;