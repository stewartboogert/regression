beamgasBias: xsecBias, xsecfact={ {{ BIAS_FACTOR }} }, particle="e-", flag={2}, proc="{{ BIAS_PROCESS }}";

d1: drift, l={{ DRIFT_LENGTH }} *m;

l0 : line = ( {{ DRIFT_NUMBER }}*d1);

use, period=l0;

sample, all;

beam, particle="e-",
      energy={{ BEAM_ENERGY }}*GeV,
      distrType="reference";

option, physicsList = "em em_extra",
        worldMaterial="G4_Galactic",
        defaultBiasVacuum="beamgasBias",
        physicsVerbose=1;
