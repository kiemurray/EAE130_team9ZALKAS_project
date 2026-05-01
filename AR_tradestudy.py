import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv
import design_space as ds

# constants
g = 32.174
CD0 = cv.CD0
e_cr = cv.e_cr


R = 53.35

mid_wf = 0.7792324662696907
dash_wf = mid_wf
man_wf = mid_wf

def maneuver_TW(WS, AR, psi_deg = 10):
    rho, a, p, T = ds.atmo_vals(20000)
    v = 0.85 * a
    k_cr = 1 / (np.pi * AR * e_cr)
    psi = psi_deg * np.pi/180
    n = np.sqrt((psi*v/g)**2 + 1)
    q = 0.5 * rho * v**2
    T_ratio = ds.Tratio(20000)
    TW = (q*CD0)/(WS*man_wf) + (k_cr*n**2*WS*man_wf)/q
    return TW * man_wf / T_ratio

#plot
WS_range = np.linspace(40, 120, 200)

AR_values = np.arange(2, 3.6, 0.25)

plt.figure(figsize=(10,7))

# constant maneuver rate
for AR in AR_values:
    TW_vals = []

    for WS in WS_range:
        TW_vals.append(maneuver_TW(WS, AR, psi_deg = 10))

    plt.plot(WS_range, TW_vals, 'r-')
    plt.text(WS+1, TW_vals[-1], f'AR={AR}', fontsize=9, color='blue')

# labels
plt.xlabel('W/S (lbf/ft²)')
plt.ylabel('T/W')
plt.title('AR Effect on 10.0°/s Maneuver Constraint')


#plt.plot( (cv.W_TO/cv.S_w), (22000*2/cv.W_TO), marker='*', color='gold', markersize=15,  markeredgecolor='black', zorder=5, label='Design Point')
#plt.plot( (cv.W_TO/600), (22000*2/cv.W_TO), marker='*', color='gold', markersize=15,  markeredgecolor='black', zorder=5, label='Design Point')

plt.grid(True)
plt.xlim(40,120)
plt.ylim(0.35,1.1)

plt.show()