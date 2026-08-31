! Notes
! Large sigmaT for cutting timing on scorer
! mesh0 for different scorers
! mesh1 for scorer options (depositeddose)
! mesh2_XXX for mesh options (depoisteddose)

d1: drift, l=0.4*m, apertureType="circularvacuum", beampipeMaterial="G4_Galactic";

blueish: newcolour, red=0, green=128, blue=255, alpha=0.3;

waterBlock: rcol, l=20*cm, material="water", colour="blueish";
! waterBlock: rcol, l=20*cm, material="G4_Galactic", colour="blueish";

l1: line=(d1, waterBlock, d1);
use, l1;

cellcharge: scorer, type="cellcharge";
cellflux: scorer, type="cellflux";
cellfluxscaled: scorer, type="cellfluxscaled", conversionFactorFile="conversion_factors/electrons.dat";
cellfluxscaledperparticle: scorer, type="cellfluxscaledperparticle", conversionFactorPath="conversion_factors";
ddose: scorer, type="depositeddose";
denergy: scorer, type="depositedenergy";
cellpopulation: scorer, type="population";

mesh0: scorermesh, nx=25, ny=25, nz=50,
       scoreQuantity="cellcharge cellflux cellfluxscaled cellfluxscaledperparticle ddose denergy cellpopulation ",
       xsize=25*cm, ysize=25*cm, zsize=100*cm, referenceElement="waterBlock";

!!!!!!!!!!!!!!!!!!!!!!!
! Options on scorer
!!!!!!!!!!!!!!!!!!!!!!!
ddose_g4name: scorer, type="depositeddose", particleName="e-";
ddose_pdgid: scorer, type="depositeddose", particlePDGID=-11;
ddose_emin: scorer, type="depositeddose", minimumKineticEnergy = 1*GeV;
ddose_emax: scorer, type="depositeddose", maximumKineticEnergy = 1*GeV;
ddose_tmin: scorer, type="depositeddose", minimumTime=-100*s;
ddose_tmax: scorer, type="depositeddose", maximumTime=-100*s;
ddose_materialinc: scorer, type="depositeddose", materialToInclude="water";
ddose_materialexc: scorer, type="depositeddose", materialToExclude="water";
ddose_world: scorer, type="depositeddose", scoreWorldVolumeOnly=1;
ddose_primary: scorer, type="depositeddose", scorePrimariesOnly=1;

mesh1: scorermesh, nx=25, ny=25, nz=50,
      scoreQuantity="ddose_g4name ddose_pdgid ddose_emin ddose_emax ddose_tmin ddose_tmax ddose_materialinc ddose_materialexc ddose_world ddose_primary",
      xsize=25*cm, ysize=25*cm, zsize=100*cm, referenceElement="waterBlock";

!!!!!!!!!!!!!!!!!!!!!!!
! Options on mesh
!!!!!!!!!!!!!!!!!!!!!!!

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