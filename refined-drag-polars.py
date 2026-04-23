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

CD_miss = 0.18 + 0.15
CD_leak = 0.15
c = cv.c_w

CD0_land = CD_friction + CD_miss + CD_leak 

# CD = CDmin + K*(CL-CLmin)**2

CD0_takeoff_nogear = [0.00570, 0.00587, 0.00553, 0.00525, 0.00501, 0.00482, 
    0.00467, 0.00457, 0.00452, 0.00449, 0.00454, 0.00460, 
    0.00471, 0.00487, 0.00505]

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
CLtot_clean_transformed = [-x for x in reversed(CLtot_clean)]
CDtot_clean_transformed = [x for x in reversed(CDtot_clean)]

# CLtot_landing_gear_down = [
#     0.22654, 0.14697, 0.17999, 2.99231, 1.40966
# ]

# CDtot_landing_gear_down = [
#     1.81604, 1.50197, 1.67972, 6.02132, 9.36590
# ]
# CLtot_landing_gear_down_inv = [-x for x in reversed(CLtot_landing_gear_down)]
# CDtot_landing_gear_down_inv = [x for x in reversed(CDtot_landing_gear_down)]

CLwtot_takeoff_nogear = [
    -0.02448, 0.02076, 0.06574, 0.11041, 0.15465, 0.19827, 
    0.24107, 0.28280, 0.32354, 0.35864, 0.40365, 0.44283, 
    0.48113, 0.52130, 0.56114
]

CDwtot_takeoff_nogear = [
    0.00606, 0.00616, 0.00668, 0.00815, 0.01056, 0.01386, 
    0.01800, 0.02286, 0.02835, 0.03624, 0.04433, 0.05124, 
    0.06032, 0.07346, 0.08368
]
# coeffs_clean = np.polyfit(CDtot_clean, CLtot_clean, deg=2)
# coeffs_clean_inv = np.polyfit(CLtot_clean_transformed, CDtot_clean, deg=2)
# fit_clean = np.poly1d(coeffs_clean)
# fit_clean_inv = np.poly1d(coeffs_clean_inv)
# # print(f"Fit: {coeffs_clean[0]:.6f}*CD^2 + {coeffs_clean[1]:.6f}*CD + {coeffs_clean[2]:.6f}")
# coeffs_gear_down = np.polyfit(CDtot_landing_gear_down, CLtot_landing_gear_down, deg=2)
# fit_gear_down = np.poly1d(coeffs_gear_down)
# coeffs_landing = np.polyfit(CDtot_avg_landing_nogear,CLtot_avg_landing_nogear, deg=2)
# fit_gear_up = np.poly1d(coeffs_landing)
# CD_arr = np.linspace(-0.01, 0.1, 100)

# clean = fit_clean(CD_arr) 
# clean_inv = fit_clean_inv(CD_arr)
# gear_up = fit_gear_up(CD_arr) + delta_CD_elevons + delta_CD_ailerons + delta_CD_slats_inboard + delta_CD_slats_outboard
# gear_down = fit_gear_down(CD_arr) + delta_CD_elevons + delta_CD_ailerons + delta_CD_slats_inboard + delta_CD_slats_outboard

CL_clean = np.array(CLtot_clean)
CL_clean_inv = np.array(CLtot_clean_transformed)
# CL_clean = np.append(CL_clean_inv, CL_clean)
CD_clean = np.array(CDtot_clean)
CD_clean_inv = np.array(CDtot_clean_transformed)
# CD_clean = np.append(CD_clean_inv, CD_clean)
# CL_gear_down = np.array(CLtot_landing_gear_down)
# # CL_gear_down_inv = np.array(CLtot_landing_gear_down_inv)
# # CL_gear_down = np.append(CL_gear_down_inv, CL_gear_down)
# CD_gear_down = np.array(CDtot_landing_gear_down)
# CD_gear_down_inv = np.array(CDtot_landing_gear_down_inv)
# CD_gear_down = np.append(CD_gear_down_inv, CD_gear_down)
CL_gear_up = np.array(CLwtot_takeoff_nogear) 
CD_gear_up = np.array(CDwtot_takeoff_nogear)+ CD0_land


coeffs_clean = np.polyfit(CL_clean, CD_clean, deg=2)
poly_func = np.poly1d(coeffs_clean)

x_smooth = np.linspace(-1, 2, 100)
y_smooth = poly_func(x_smooth)

# coeffs_gear_down = np.polyfit(CL_gear_down, CD_gear_down, deg=2)
# poly_func_gear_down = np.poly1d(coeffs_gear_down)+ CD0_land
# x_smooth_gear_down = np.linspace(-1, 2, 100)
# y_smooth_gear_down = poly_func_gear_down(x_smooth_gear_down) 
coeffs_gear_up = np.polyfit(CL_gear_up, CD_gear_up, deg=2)
poly_func_gear_up = np.poly1d(coeffs_gear_up)
x_smooth_gear_up = np.linspace(-1, 2, 100)
y_smooth_gear_up = poly_func_gear_up(x_smooth_gear_up)

plt.plot(y_smooth, x_smooth, label="Clean Fit", color='blue') 
# plt.plot(y_smooth_gear_down, x_smooth_gear_down, label="Landing Gear Down", color='orange')
plt.plot(y_smooth_gear_up, x_smooth_gear_up, label="Landing Gear Up", color='green')
plt.ylabel("Lift Coefficient (CL)")
plt.xlabel("Drag Coefficient (CD)")
plt.title("Drag Polar Fit")
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.legend()
plt.xlim(0, 1)
# plt.ylim(-1, 1)
plt.grid(True)
plt.show()
# # plt.plot(CDtot_clean, CLtot_clean)
# plt.plot(CDtot_clean, CLtot_clean, label="Clean", color='lightgreen')
# plt.plot(CDtot_clean, CLtot_clean_transformed, label="Clean Inverted", color='green')
# # plt.plot(CDtot_landing_gear_down, CLtot_landing_gear_down, label='Landing Gear Down')
# plt.plot(CDtot_landing_gear_down,CLtot_landing_gear_down, label="Takeoff Gear Down", color='orange')
# plt.plot(CDtot_avg_landing_nogear, CLtot_avg_landing_nogear, label="Takeoff Gear Up", color= 'blue')
# plt.ylabel('CL')
# plt.xlabel('CD')

# plt.ylim(-0.25,0.25)

# plt.title('CL vs CD with Quadratic Fit')
# plt.legend()
# plt.grid(True)
# plt.show()
