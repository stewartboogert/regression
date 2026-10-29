! need to make t1 rcol target horizontalWidth small to avoid angular dip going through large amount target

d1: drift, l={{ DRIFT_LENGTH }}*m;
t1: rcol, l={{ TARGET_LENGTH }}*m, material="{{ TARGET_MATERIAL }}", horizontalWidth={{ TARGET_LENGTH }};
l0 : line = (d1, t1, d1);

use, period=l0;

s0: samplerplacement, samplerType="sphere", aper1=100*cm, x=0*cm, y=0*cm,
                      s={{ DRIFT_LENGTH }}*m +{{ TARGET_LENGTH }}/2*m;

beam, particle="e+",
      energy={{ BEAM_ENERGY }}*GeV,
      distrType="reference";

option, physicsList = "em em_extra",
        worldMaterial="G4_Galactic",
        beampipeMaterial="G4_Galactic",
        physicsVerbose=1;

