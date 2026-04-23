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

CD_miss = 0.15
CD_leak = 0.15
c = cv.c_w

CD0_land = CD_friction + CD_miss + CD_leak 

# CD = CDmin + K*(CL-CLmin)**2


CLtot_clean = [
    0.15381, 0.20066, 0.24783, 0.29529, 0.34285, 0.39005, 0.43571, 
    0.48184, 0.52909, 0.57288, 0.61497, 0.65640, 0.69926, 0.74278, 0.78682
]

CDtot_clean = [
    0.00446, 0.00424, 0.00407, 0.00394, 0.00386, 0.00383, 0.00385,
    0.00391, 0.00401, 0.00416, 0.00435, 0.00458, 0.00484, 0.00515, 0.00550
]
CDi_clean = [
    0.00315, 0.00936, 0.01664, 0.02523, 0.03517, 0.04446, 0.05425, 
    0.06598, 0.07930, 0.09369, 0.10537, 0.12138, 0.13166, 0.15371, 0.17343
]
CD0_clean = [
    0.00446, 0.00424, 0.00407, 0.00394, 0.00386, 0.00383, 0.00385,
    0.00391, 0.00401, 0.00416, 0.00435, 0.00458, 0.00484, 0.00515, 0.00550
]
CLtot_gearup_TO = [
    0.20925, 0.25794, 0.30684, 0.35597, 0.40494, 0.45287, 0.50011, 0.54841,
    0.59744, 0.64630, 0.69829, 0.74086, 0.79244, 0.88400, 0.98651, 1.02510
]

CDtot_gearup_TO = [
    0.00468, 0.00443, 0.00424, 0.00412, 0.00408, 0.00411, 0.00416, 0.00427, 0.00443, 0.00465, 0.00493, 0.00544, 0.00644, 0.00790, 0.00948, 0.01189]


CDi_gearup_TO = [
    0.00317, 0.00615, 0.00990, 0.01397, 0.01821, 0.02275, 0.02796, 0.03327,
    0.03774, 0.04392, 0.04785, 0.05478, 0.05465, 0.05701, 0.06924, 0.07517
]

CDo_gearup = [0.00468, 0.00443, 0.00424, 0.00412, 0.00408, 0.00411, 0.00416, 0.00427, 0.00443, 0.00465, 0.00493, 0.00544, 0.00644, 0.00790, 0.00948, 0.01189]

CLtot_gearup_landing = [
    0.43165, 0.46415, 0.51703, 0.57222, 0.61084, 0.66977, 0.72607, 0.79323,
    0.88072, 0.99417, 1.04692, 1.14142
]

CDtot_gearup_landing = [
    0.00444, 0.00443, 0.00447, 0.00456, 0.00468, 0.00481, 0.00496, 0.00514, 0.00535, 0.00560, 0.00586, 0.00615]

CDi_gearup_landing = [
    0.01186, 0.01574, 0.02018, 0.02528, 0.03083, 0.03689, 0.04292, 0.05177,
    0.06022, 0.06980, 0.07600, 0.08415
]
CDo_gearup_landing = [0.00444, 0.00443, 0.00447, 0.00456, 0.00468, 0.00481, 0.00496, 0.00514, 0.00535, 0.00560, 0.00586, 0.00615]
CLtot_geardown_TO = [
    0.20781, 0.25637, 0.30536, 0.35559, 0.40409, 0.45235, 0.50067, 0.54933,
    0.59855, 0.64850, 0.69799, 0.75163, 0.80162, 0.89268, 0.96665, 1.04471
]

CDtot_geardown_TO = [
    0.00472, 0.00449, 0.00432, 0.00422, 0.00421, 0.00424, 0.00430, 0.00441, 0.00458, 0.00480, 0.00513, 0.00581, 0.00684, 0.00861, 0.00945, 0.01330]

CDi_geardown_TO = [
    0.00419, 0.00744, 0.01137, 0.01561, 0.01993, 0.02466, 0.02995, 0.03493,
    0.04084, 0.04580, 0.04987, 0.05653, 0.05703, 0.05947, 0.07289, 0.06821
]
CDo_geardown = [0.00472, 0.00449, 0.00432, 0.00422, 0.00421, 0.00424, 0.00430, 0.00441, 0.00458, 0.00480, 0.00513, 0.00581, 0.00684, 0.00861, 0.00945, 0.01330]

CLtot_geardown_landing = [
    0.44934, 0.49284, 0.51304, 0.57142, 0.62303, 0.69125, 0.72300, 0.76826,
    0.84160, 0.89831, 1.06883, 1.16525
]

CDtot_geardown_landing = [
    0.00448, 0.00447, 0.00451, 0.00460, 0.00471, 0.00484, 0.00499, 0.00517, 0.00538, 0.00563, 0.00588, 0.00618]

CDi_geardown_landing = [
    0.01176, 0.01563, 0.02009, 0.02510, 0.03066, 0.03665, 0.04300, 0.05139,
    0.06033, 0.06731, 0.07664, 0.08462
]
CDo_geardown_landing = [0.00448, 0.00447, 0.00451, 0.00460, 0.00471, 0.00484, 0.00499, 0.00517, 0.00538, 0.00563, 0.00588, 0.00618]


CL_clean = np.array(CLtot_clean)
CD_clean = np.array(CD0_clean) + 0.075*(np.abs(np.array(CDi_clean))) 
CD_gear_up_TO = np.abs(np.array(CDtot_gearup_TO)) + 0.075*(np.abs(np.array(CDi_gearup_TO)))
CL_gear_up_TO = np.array(CLtot_gearup_TO)
CL_landing_gearup = np.array(CLtot_gearup_landing)
CD_landing_gearup = np.abs(np.array(CDtot_gearup_landing)) + 0.075*(np.abs((np.array(CDi_gearup_landing))))
CL_gear_down_TO = np.array(CLtot_geardown_TO)
CD_gear_down_TO = np.abs(np.array(CDtot_geardown_TO)) + 0.075*(np.array(CDi_geardown_TO))
CL_landing_geardown = np.array(CLtot_geardown_landing)
CD_landing_geardown = np.abs(np.array(CDtot_geardown_landing)) + 0.075*(np.abs((np.array(CDi_geardown_landing)))) 
def calc_CD(CL,CL_min, CD0,e,AR,CDi):
    CD = CD0 + (1/((3.14)*(e)*(AR)))*np.square(CL-CL_min) + 0.075*(np.abs(CDi))
    return CD
e_cl = 0.820
e_tk = 0.775
e_lnd = 0.725

# CD_clean = calc_CD(CL_clean, min(CL_clean), CD0_clean, e_cl, cv.AR_w, CDi_clean) + CD_friction
CD_gear_down_TO = calc_CD(CL_gear_down_TO, min(CL_gear_down_TO), CDo_geardown, e_tk, cv.AR_w, CDi_geardown_TO) + CD_friction
CD_gear_up_TO = calc_CD(CL_gear_up_TO, min(CL_gear_up_TO), CDo_gearup, e_tk, cv.AR_w, CDi_gearup_TO) + CD_friction
CD_landing_gearup = calc_CD(CL_landing_gearup, min(CL_landing_gearup), CDo_gearup_landing, e_lnd, cv.AR_w, CDi_gearup_landing) + CD_friction
CD_landing_geardown = calc_CD(CL_landing_geardown, min(CL_landing_geardown), CDo_geardown_landing, e_lnd, cv.AR_w, CDi_geardown_landing) + CD_friction

coeffs_clean = np.polyfit(CL_clean, CD_clean, deg=2)
poly_func = np.poly1d(coeffs_clean) 
x_smooth = np.linspace(-1.2, 1.36, 100) 
y_smooth = poly_func(x_smooth)

coeffs_gear_down_TO = np.polyfit(CL_gear_down_TO, CD_gear_down_TO, deg=2)
poly_func_gear_down_TO = np.poly1d(coeffs_gear_down_TO) + CD_miss
x_smooth_gear_down_TO = np.linspace(-0.9, 1.5, 100)
y_smooth_gear_down_TO = poly_func_gear_down_TO(x_smooth_gear_down_TO) 

coeffs_gear_up_TO = np.polyfit(CL_gear_up_TO, CD_gear_up_TO, deg=2)
poly_func_gear_up = np.poly1d(coeffs_gear_up_TO)
x_smooth_gear_up_TO = np.linspace(-0.95, 1.5, 100)
y_smooth_gear_up_TO = poly_func_gear_up(x_smooth_gear_up_TO)

coeffs_gear_up_LA = np.polyfit(CL_landing_gearup, CD_landing_gearup, deg=2)
poly_func_gear_up_LA = np.poly1d(coeffs_gear_up_LA)
x_smooth_gear_up_LA = np.linspace(-2, 1.8, 100)
y_smooth_gear_up_LA = poly_func_gear_up_LA(x_smooth_gear_up_LA)

coeffs_gear_down_LA = np.polyfit(CL_landing_geardown, CD_landing_geardown, deg=2)
poly_func_gear_down_LA = np.poly1d(coeffs_gear_down_LA) + CD_miss
x_smooth_gear_down_LA = np.linspace(-2, 1.8, 100)
y_smooth_gear_down_LA = poly_func_gear_down_LA(x_smooth_gear_down_LA)

plt.figure(figsize=(10, 8))
plt.plot(y_smooth, x_smooth, label="Clean", color='blue') 
plt.plot(y_smooth_gear_down_TO, x_smooth_gear_down_TO, label="Takeoff Gear Down", color='orange')
plt.plot(y_smooth_gear_up_TO, x_smooth_gear_up_TO, label="Takeoff Gear Up", color='green')
plt.plot(y_smooth_gear_up_LA, x_smooth_gear_up_LA, label="Landing Gear Up", color='red')
plt.plot(y_smooth_gear_down_LA, x_smooth_gear_down_LA, label="Landing Gear Down", color='purple')
plt.ylabel("Lift Coefficient ($C_L$)", font="Times New Roman", fontsize=12)
plt.xlabel("Drag Coefficient ($C_D$)", font="Times New Roman", fontsize=12)
plt.title("Drag Polar", font="Times New Roman", fontsize=14)
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.legend(loc='upper right', fontsize=10)
plt.xlim(0, 0.2)
plt.ylim(-1, 1.8)
plt.grid(True)
plt.show()
