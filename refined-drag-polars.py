import numpy as np
import code_variables as cv
import matplotlib.pyplot as plt

M = 0.2
rho_TO_land = cv.rho_sl
a_TO_land = cv.a_SL
mu_TO_land = 3.737e-7 #Dynamic viscosity of air at sea level in kg/(m*s)
k = 0.7e-5 #Surface roughness for smooth molded composite in ft (raymer)
x_tc = 0.4 #Location of max thickness as a fraction of chord (NACA 64-206)
S_elevons = 40.005
S_ailerons =  30.043
S_slats_inboard =  104.272 
S_slats_outboard =  12.359
S_wing_wet =  1487.536

def Reynolds_number(rho, V, c, mu):
    return (rho * V * c) / mu

Re_TO_land_w = Reynolds_number(rho_TO_land, cv.V_TO, cv.c_w, mu_TO_land)
Re_TO_land_fuselage = Reynolds_number(rho_TO_land, cv.V_TO, cv.L_f, mu_TO_land)
Re_TO_land_tail = Reynolds_number(rho_TO_land, cv.V_TO, cv.c_t, mu_TO_land)

def Re_cutoff_subsonic(l,k):
    return 38.21*(l/k)**1.053

def Re_cutoff_transonic(l,k,M):
    return 44.62*(l/k)**1.053 *M**1.16

Re_cutoff_fuselage_land = Re_cutoff_subsonic(cv.L_f,k)
Re_cutoff_wing_land = Re_cutoff_subsonic(cv.c_w,k)
Re_cutoff_tail_land = Re_cutoff_subsonic(cv.c_t,k)

if Re_TO_land_fuselage < Re_cutoff_fuselage_land:
    Cf_fuse= 1.328/Re_TO_land_fuselage**0.5
else:
    Cf_fuse = 0.455/((np.log10(Re_TO_land_fuselage)**2.58)*(1+(0.144*M**2))**0.65)

if Re_TO_land_w < Re_cutoff_wing_land:
    Cf_wing = 1.328/Re_TO_land_w**0.5
else:
    Cf_wing = 0.455/((np.log10(Re_TO_land_w)**2.58)*(1+(0.144*M**2))**0.65)

if Re_TO_land_tail < Re_cutoff_tail_land:
    Cf_tail = 1.328/Re_TO_land_tail**0.5
else:
    Cf_tail = 0.455/((np.log10(Re_TO_land_tail)**2.58)*(1+(0.144*M**2))**0.65)


FF_wing = (1 + (0.6/x_tc)*(cv.tc_root) + 100*(cv.tc_root)**4)*(1.34*M**0.18*(cv.lambda_w)**0.28)
FF_tail = (1 + (0.6/x_tc)*(cv.t_t/cv.c_t) + 100*(cv.t_t/cv.c_t)**4)*(1.34*M**0.18*(cv.sweep_vt)**0.28)
FF_fuselage = (0.9+(5/(cv.L_f/cv.W_f)**1.5)+(cv.L_f/cv.W_f)/400)

friction_wing = Cf_wing*FF_wing*cv.S_wet_wing
friction_tail = Cf_tail*FF_tail*cv.S_wet_tail*1.03
friction_fuselage = Cf_fuse*FF_fuselage*cv.S_wet_fuselage
CD_friction = (friction_wing + friction_tail + friction_fuselage)/cv.S_wingtest
print("CD_friction =", CD_friction)

CD_miss = 0.18+0.15
CD_leak = 0.15
c = cv.c_w

CD0_land = CD_friction + CD_miss + CD_leak 

# CD = CDmin + K*(CL-CLmin)**2

def delta_CD_flaps(delta_flap, c_f, c, S_f, S_wing_wet):
    return 1.7*(c_f/c)**(1.38)*(S_f/S_wing_wet)*(np.sin(delta_flap))**2 #plain and split flap
delta_CD_elevons = delta_CD_flaps(15,0.25,cv.c_w,S_elevons,S_wing_wet) #plain and split flap
delta_CD_ailerons = delta_CD_flaps(20,0.25,cv.c_w,S_ailerons,S_wing_wet) #plain and split flap
delta_CD_slats_inboard = delta_CD_flaps(20,0.1,cv.c_w,S_slats_inboard,S_wing_wet) #plain and split flap
delta_CD_slats_outboard = delta_CD_flaps(20,0.1,cv.c_w,S_slats_outboard,S_wing_wet) #plain and split flap

alpha_values = [0.0, 0.29167, 0.58333, 0.875, 1.16667, 1.45833, 1.75, 2.04167, 2.33333,
                2.625, 2.91667, 3.20833, 3.5, 3.79167, 4.08333, 4.375, 4.66667, 4.95833,
                5.25, 5.54167, 5.83333, 6.125, 6.41667, 6.70833, 7.0]

CDtot_clean = [
    0.02050, 0.02087, 0.02130, 0.02214, 0.02299, 0.02386, 0.02468, 0.02592, 0.02702,
    0.02797, 0.02926, 0.03068, 0.03278, 0.03411, 0.03570, 0.03730, 0.03910, 0.04091,
    0.04281, 0.04484, 0.04600, 0.04725, 0.04901, 0.05041, 0.05228
]
CLtot_clean = [
    0.00879, 0.01770, 0.02659, 0.03525, 0.04411, 0.05338, 0.06253, 0.07167, 0.08105,
    0.08919, 0.09800, 0.10718, 0.11752, 0.12581, 0.13410, 0.14229, 0.15025, 0.15867,
    0.16645, 0.17450, 0.18261, 0.19056, 0.19859, 0.20670, 0.21429
]
CDtot_landing_gear_down = [
    0.02063, 0.02096, 0.02140, 0.02226, 0.02311, 0.02387, 0.02464, 0.02607, 0.02714,
    0.02800, 0.02933, 0.03073, 0.03258, 0.03340, 0.03574, 0.03733, 0.03922, 0.04120,
    0.04297, 0.04476, 0.04606, 0.04732, 0.04909, 0.05058, 0.05236
]

CLtot_landing_gear_down = [
    0.00907, 0.01803, 0.02691, 0.03550, 0.04440, 0.05381, 0.06284, 0.07164, 0.08125,
    0.08952, 0.09924, 0.10771, 0.11776, 0.12645, 0.13421, 0.14267, 0.15047, 0.15885,
    0.16702, 0.17451, 0.18251, 0.19092, 0.19876, 0.20702, 0.21480
]
CDtot_avg_landing_nogear    = [0.08020773, 0.08544009, 0.09509525, 0.15400723, 0.13648854, 0.11906174, 0.12084928, 0.19870452, 0.13373305, 0.13229621, 0.11678673, -1.26150724, -0.88158880, 0.02666942, 0.10797449]
CLtot_avg_landing_nogear    = [0.16997004, 0.19070988, 0.17689464, 0.21609493, 0.19947138, 0.27931094, 0.29297851, 0.32184035, 0.32669529, 0.29666088, 0.04678969, -3.45295521, -2.21213341, -0.12624830, 0.07915005]
coeffs_clean = np.polyfit(CDtot_clean, CLtot_clean, deg=2)
fit_clean = np.poly1d(coeffs_clean)
# print(f"Fit: {coeffs_clean[0]:.6f}*CD^2 + {coeffs_clean[1]:.6f}*CD + {coeffs_clean[2]:.6f}")
coeffs_gear_down = np.polyfit(CDtot_landing_gear_down, CLtot_landing_gear_down, deg=2)
fit_gear_down = np.poly1d(coeffs_gear_down)
coeffs_landing = np.polyfit(CDtot_avg_landing_nogear,CLtot_avg_landing_nogear, deg=2)
fit_gear_up = np.poly1d(coeffs_landing)
CD_arr = np.linspace(-0.01, 0.1, 100)

clean = fit_clean(CD_arr) 
gear_up = fit_gear_up(CD_arr)
gear_down = fit_gear_down(CD_arr) + delta_CD_elevons + delta_CD_ailerons + delta_CD_slats_inboard + delta_CD_slats_outboard

# plt.plot(CDtot_clean, CLtot_clean)
plt.plot(CD_arr, clean, label="Clean", color='green')
# plt.plot(CDtot_landing_gear_down, CLtot_landing_gear_down, label='Landing Gear Down')
plt.plot(CD_arr, gear_down, label="Takeoff Gear Down", color='orange')
plt.plot(CD_arr, gear_up, label="Takeoff Gear Up", color= 'blue')
plt.ylabel('CL')
plt.xlabel('CD')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.ylim(-0.25,0.25)
plt.title('CL vs CD with Quadratic Fit')
plt.legend()
plt.grid(True)
plt.show()
