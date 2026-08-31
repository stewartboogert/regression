lb1: laserflux, wavelength=1064.0*nm,
m2=1.2,
pulseDuration=106.0*ns,
pulseEnergy={{ LASER_ENERGY }}*mJ,
w0=50*mm;

laser1: laserwire, l=0.01*m, wireLength=0.1*m, laserOffsetTheta=-pi/2, laserOffsetPhi=0,laserOffsetY=0.0*m, laserOffsetZ=0*m, laserOffsetX=0, laserBeam="lb1";

lat : line=(laser1);
use, lat;

beam, particle="ion 1 1 -1",
      energy={{ BEAM_ENERGY }}*MeV,
      X0=0.0*m,
      Xp0=0.0,
      Y0=0.0*m,
      Yp0=0.0, 
      distrType="gauss",
      sigmaX=2*mm,
      sigmaY=4*mm,
      sigmaE=0,
      sigmaT=0;
option, 
physicsList="laser_photo_detachment", scaleFactorLaser=1000;

sample, range=laser1;
