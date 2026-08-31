d1: drift, l=1*m;
t1: drift, l=2*m;
d2: drift, l=1*m;

l0 : line = (d1,t1,d2);

use, period=l0;

sample, all;

beam,  particle = "e-",
       energy = 1.0*GeV,
       distrType = "gaussmatrix",
       sigma11 = {{ SIG11 }},
       sigma22 = {{ SIG22 }},
       sigma33 = {{ SIG33 }},
       sigma44 = {{ SIG44 }},
       sigma55 = {{ SIG55 }},          
       sigma66 = {{ SIG66 }};