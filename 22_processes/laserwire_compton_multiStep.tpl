
lb1: laserflux, wavelength=532.0*nm,
m2=1.2,
pulseDuration=71.0*ps,
pulseEnergy={{ LASER_ENERGY }}*mJ,
w0=2.3*um;

laser1: laserwire, l=0.01*m, wireLength=0.1*m, laserOffsetTheta=-pi/2, laserOffsetPhi=0,laserOffsetY=0.0*m, laserOffsetZ=0*m, laserOffsetX=0, laserBeam="lb1";

lat : line=(laser1);
use, lat;

beam, particle="e-",
      energy={{ BEAM_ENERGY }}*GeV,
      X0=0.0*m,
      Xp0=0.0,
      Y0=0.0*m,
      Yp0=0.0, 
      distrType="gauss",
      sigmaX=119*um,
      sigmaY=1.07*um,
      sigmaE=0,
      sigmaT=0;
option, 
physicsList="laser_compton_scattering", scaleFactorLaser=1000;

sample, range=laser1;
