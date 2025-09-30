d1: drift, l=1*m;

AlBlock: rcol, l=10*m, material="G4_Al";

l1: line=(d1, AlBlock);
use, l1;

beam, particle="millicharged",
      kineticEnergy=10*GeV;

option, enableMillicharge=1,
        millichargeName="millicharged",
        millichargeMass={{ MASS }}*GeV,
        millichargeCharge={{ CHARGE }},
        millichargeID=411000;

sampler: samplerplacement, z=11*m, aper1=10*m, aper2=10*m, shape="rectangular", partID={411000};