import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv
import design_space as ds

# constants
g = 32.174
CD0 = cv.CD0
AR = cv.AR_w
e_cr = cv.e_cr
k_cr = 1 / (np.pi * AR * e_cr)

R = 53.35

mid_wf = 0.7792324662696907
dash_wf = mid_wf
man_wf = mid_wf


# dash at 

def dash_TW(WS, mach):
    rho, a, p, T = ds.atmo_vals(30000)
    v = mach * a
    q = 0.5 * rho * v**2
    T_ratio = ds.Tratio(30000)
    T_Wcr = (q * CD0) / (WS*dash_wf) + (k_cr * WS*dash_wf) / (q)
    return T_Wcr * dash_wf / T_ratio


def maneuver_TW(WS, psi_deg):
    rho, a, p, T = ds.atmo_vals(20000)
    v = 0.85 * a
    psi = psi_deg * np.pi/180
    n = np.sqrt((psi*v/g)**2 + 1)
    q = 0.5 * rho * v**2
    T_ratio = ds.Tratio(20000)
    TW = (q*CD0)/(WS*man_wf) + (k_cr*n**2*WS*man_wf)/q
    return TW * man_wf / T_ratio

#plot
WS_range = np.linspace(40, 100, 200)

mach_values = np.arange(1.6, 3.2, 0.1)
psi_values = np.arange(8, 12.5, 0.5)

plt.figure(figsize=(10,7))

# constant mach
for mach in mach_values:
    TW_vals = []

    for WS in WS_range:
        TW_vals.append(dash_TW(WS, mach))

    plt.plot(WS_range, TW_vals, 'b-')


# constant maneuver rate
for psi in psi_values:
    TW_vals = []

    for WS in WS_range:
        TW_vals.append(maneuver_TW(WS, psi))

    plt.plot(WS_range, TW_vals, 'r-')
    


# labels
plt.xlabel('W/S (lbf/ft²)')
plt.ylabel('T/W')
plt.title('Carpet Plot: Dash Mach and Maneuver Rate')


# plt.text(58, 0.3734, 'M = 1.6',color='blue',fontsize=9, ha='left',va='center',)
# plt.text(63.5, 0.3855, 'M = 1.7',color='blue',fontsize=9, ha='left',va='center',)
# plt.text(68.3, 0.4019, 'M = 1.8',color='blue',fontsize=9, ha='left',va='center',)
# plt.text(73.4, 0.4156, 'M = 1.9',color='blue',fontsize=9, ha='left',va='center',)
# plt.text(77.8, 0.4335, 'M = 2.0',color='blue',fontsize=9, ha='left',va='center',)


# plt.text(76.53,0.4525, 'ψ = 8.0°/s',color='red',fontsize=9,ha='left',va='center')
# plt.text(72.10, 0.4802, 'ψ = 8.5°/s',color='red',fontsize=9,ha='left',va='center')
# plt.text(68.5, 0.505, 'ψ = 9.0°/s',color='red',fontsize=9,ha='left',va='center')
# plt.text(64.8, 0.532, 'ψ = 9.5°/s',color='red',fontsize=9,ha='left',va='center')
# plt.text(61.2, 0.559, 'ψ = 10.0°/s',color='red',fontsize=9,ha='left',va='center')
# plt.text(58.4, 0.584, 'ψ = 10.5°/s',color='red',fontsize=9,ha='left',va='center')

plt.plot( (cv.W_TO/cv.S_w), (22000*2/cv.W_TO), marker='*', color='gold', markersize=15,  markeredgecolor='black', zorder=5, label='Design Point')
plt.plot( (cv.W_TO/600), (22000*2/cv.W_TO), marker='*', color='gold', markersize=15,  markeredgecolor='black', zorder=5, label='Design Point')

plt.grid(True)
plt.xlim(40,100)
plt.ylim(0.35,0.9)

plt.show()