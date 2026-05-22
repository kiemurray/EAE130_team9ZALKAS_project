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
    0.046681069603, 0.073009672552, 0.099535072052, 0.12548459176, 0.1515544098, 0.18077073488, 0.20775764846, 0.23638703411, 0.26349966102, 0.2918053677,
    0.31878553545, 0.3521905836, 0.37760990325, 0.40325916355, 0.42948837322, 0.46012329863, 0.49153959438, 0.51364851847, 0.54290735495, 0.56690792301
]
CDtot_clean = [
    0.0050477512, 0.005861487079, 0.007169495645, 0.008747104313, 0.010758237927, 0.013400034246, 0.016103098907, 0.019479703572, 0.023288634508, 0.027327813863,
    0.031692986598, 0.038149888989, 0.041945538071, 0.047667128572, 0.052843351147, 0.060685133852, 0.068347362461, 0.073824515237, 0.081881366957, 0.0902087781
]
CDi_clean = [
    0.000687683903, 0.001474666388, 0.002746316916, 0.004277024207, 0.00623223055, 0.008808558576, 0.011436223364, 0.014726950075, 0.018441319466,0.022377324902,
    0.026630627366, 0.032957614267, 0.036611268459, 0.042199820704, 0.047226541486, 0.054883513318, 0.062405080965, 0.067711751679, 0.075602614322, 0.083727499465
]
CD0_clean = [
    0.004360067297, 0.004386820691, 0.004423178728, 0.004470080106, 0.004526007376, 0.00459147567, 0.004666875543, 0.004752753497, 0.004847315041, 0.004950488961,
    0.005062359232, 0.005192274722, 0.005334269613, 0.005467307868, 0.005616809661, 0.005801620534, 0.005942281496, 0.006112763559, 0.006278752635, 0.006481278635
]

CLtot_gearup_TO = [
    0.082789269, 0.108040001, 0.13328844, 0.158196507, 0.184358162, 0.210417072, 0.235470898, 0.260850016, 0.285702691, 0.313340893, 
    0.340318233, 0.369617482, 0.393920027, 0.420883526, 0.441494259, 0.463048402, 0.497348487, 0.516151923, 0.550667955, 0.570237441
]
CDtot_gearup_TO = [
    0.00808581, 0.009326177, 0.010861297, 0.012941373, 0.014989415, 0.017289204, 0.020411001, 0.023812936, 0.026849512, 0.031168856, 
    0.036096648, 0.040691645, 0.044822192, 0.0510363, 0.056321619, 0.062268962, 0.070373573, 0.073359842, 0.086070731, 0.089391048
]
CDi_gearup_TO = [
    0.003327538, 0.00454283, 0.006043964, 0.008081831, 0.010077741, 0.012318008, 0.015374058, 0.018692723, 0.021651448, 0.02587149, 
    0.030703803, 0.035183184, 0.039177056, 0.045261898, 0.050434782, 0.056235799, 0.064198979, 0.067065006, 0.079581511, 0.082745655
]
CDo_gearup = [
    0.004758272, 0.004783347, 0.004817332, 0.004859542, 0.004911674, 0.004971196, 0.005036944, 0.005120213, 0.005198064, 0.005297366, 
    0.005392845, 0.005508461, 0.005645136, 0.005774402, 0.005886837, 0.006033163, 0.006174594, 0.006294836, 0.00648922, 0.006645392
]


CLtot_gearup_landing = [
    0.049113681, 0.081255422, 0.113024368, 0.145261373, 0.176918958, 0.211494736,
    0.241757704, 0.275208681, 0.310700094, 0.342560593, 0.37628135, 0.414789751
]
CDtot_gearup_landing = [
    0.006787083, 0.007893677, 0.009443661, 0.011573466, 0.014110161, 0.017255395,
    0.020843447, 0.025414853, 0.030800636, 0.036343135, 0.041316912, 0.049981519
]
CDi_gearup_landing = [
    0.002057671, 0.00314431, 0.004661632, 0.006744097, 0.009220031, 0.012288954,
    0.015794089, 0.020258075, 0.02551929, 0.030938278, 0.035775034, 0.04426899
]
CDo_gearup_landing = [
    0.004729413, 0.004749367, 0.004782029, 0.004829369, 0.00489013, 0.004966441, 
    0.005049358, 0.005156778, 0.005281346, 0.005404857, 0.005541877, 0.005712529
]



CLtot_geardown_TO = [
    0.082789269, 0.108040001, 0.13328844, 0.158196507, 0.184358162, 0.210417072, 0.235470898, 0.260850016, 0.285702691, 0.313340893, 
    0.340318233, 0.369617482, 0.393920027, 0.420883526, 0.441494259, 0.463048402, 0.497348487, 0.516151923, 0.550667955, 0.570237441
]
CDtot_geardown_TO = [
    0.01616435464, 0.01740472164, 0.01893984164, 0.02101991764, 0.02306795964, 0.02536774864, 0.02848954564, 0.03189148064, 0.03492805664, 0.03924740064,
    0.04417519264, 0.04877018964, 0.05290073664, 0.05911484464, 0.06440016364, 0.07034750664, 0.07845211764, 0.08143838664, 0.09414927564, 0.09746959264
]
CDi_geardown_TO = [
    0.01140608264, 0.01262137464, 0.01412250864, 0.01616037564, 0.01815628564, 0.02039655264, 0.02345260264, 0.02677126764, 0.02972999264, 0.03395003464,
    0.03878234764, 0.04326172864, 0.04725560064, 0.05334044264, 0.05851332664, 0.06431434364, 0.07227752364, 0.07514355064, 0.08766005564, 0.09082419964
]
CDo_geardown = [
    0.01283681664, 0.01286189164, 0.01289587664, 0.01293808664, 0.01299021864, 0.01304974064, 0.01311548864, 0.01319875764, 0.01327660864, 0.01337591064,
    0.01347138964, 0.01358700564, 0.01372368064, 0.01385294664, 0.01396538164, 0.01411170764, 0.01425313864, 0.01437338064, 0.01456776464, 0.01472393664
]

CLtot_geardown_landing = [
    0.049113681, 0.081255422, 0.113024368, 0.145261373, 0.176918958, 0.211494736,
    0.241757704, 0.275208681, 0.310700094, 0.342560593, 0.37628135, 0.414789751
]
CDtot_geardown_landing = [
    0.01486562764, 0.01597222164, 0.01752220564, 0.01965201064, 0.02218870564, 0.02533393964,
    0.02892199164, 0.03349339764, 0.03887918064, 0.04442167964, 0.04939545664, 0.05806006364
]
CDi_geardown_landing = [
    0.01013621564, 0.01122285464, 0.01274017664, 0.01482264164, 0.01729857564, 0.02036749864,
    0.02387263364, 0.02833661964, 0.03359783464, 0.03901682264, 0.04385357864, 0.05234753464
]
CDo_geardown_landing = [
    0.01280795764, 0.01282791164, 0.01286057364, 0.01290791364, 0.01296867464, 0.01304498564,
    0.01312790264, 0.01323532264, 0.01335989064, 0.01348340164, 0.01362042164, 0.01379107364
]


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
e_cl = 0.71
e_tk = 0.63 
e_lnd = 0.50

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
