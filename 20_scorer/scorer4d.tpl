

d1: drift, l=0.4*m, apertureType="circularvacuum", beampipeMaterial="G4_Galactic";

blueish: newcolour, red=0, green=128, blue=255, alpha=0.3;

waterBlock: rcol, l=20*cm, material="water", colour="blueish";
! waterBlock: rcol, l=20*cm, material="G4_Galactic", colour="blueish";

l1: line=(d1, waterBlock, d1);
use, l1;

cellflux4d: scorer, type="cellflux4d";

mesh0: scorermesh, nx=25, ny=25, nz=50, ne=25,
       scoreQuantity="cellflux4d",
       xsize=25*cm, ysize=25*cm, zsize=100*cm, referenceElement="waterBlock",
       eLow=1e-12*GeV,eHigh=1*GeV;

beam, particle="e-",
      distrType = "gauss",
      energy=1*GeV,
      sigmaT=1*s;

option, physicsList="em",
        storeMinimalData=1,
        storePerEventHistos=0,
        worldMaterial="G4_Galactic";

! For debugging and determining parameters
!sample,all;
!option, physicsList="em",
!        storeMinimalData=0,
!        storePerEventHistos=0,
!        storeElossTime=1,
!        worldMaterial="G4_Galactic";