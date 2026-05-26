import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv

g = cv.g
WL = 49738          #landing weight
wt = 22             #ft/s sink rate of carrier aircraft
Ns = 2              # num of struts
Pm = 20944.72       # max static load per main gear strut

shock_type = 'oleo-pneumatic'
if shock_type == 'air':
    ns = 0.63
elif shock_type == 'metal':
    ns = 0.7
elif shock_type == 'liquid':
    ns = 0.8
elif shock_type == 'oleo-pneumatic':
    ns = 0.8
else:
    ns = 0.5 #cantilever spring
    
nt = 0.47           # tire energy absorption efficiency
Ng = 8.0            # landing gear load factor (3.0-8.0)
st = 34.5 - 2*14.85 #D0 of tire - 2*loaded radius
ss = ((0.5*(WL/g)*(wt**2)/(Ns * Pm *Ng))-nt*st)/ns + 1/12 # shock absorber length
print(f"ss = {ss}")


Et = 0.5 * WL/g *wt**2
print(f"E_t = {Et}")

Et = Ns * Pm * Ng * (nt*st + ns*ss)
print(f"Et = {Et}")

Ds = 0.041 + 0.0025* Pm**0.5
print(Ds)



# nose gear
Ns = 1
Pn = 7355.71 * 2 #max dyn load per wheel x2
Pn_static = 4962.39*2
Ng = Ng
ns = 1.0
st = 22.2 - 9.35*2
Et = Ns * Pn * Ng * (nt*st + ns*ss)
ss = ((0.5*(Pn_static/g)*(wt**2)/(Ns * Pm *Ng))-nt*st)/ns + 1/12
print(f"ss nose = {ss}")

Ds = 0.041 + 0.0025* Pn**0.5
print(Ds)