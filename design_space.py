import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv

#constants 
g = 32.174                                                            # ft/s^2
CD0 = 0.01166                                                         # clean, used for cruise, dashes, ceiling, manuever
W_TO = 55700
AR = 2.066       
n_eng = 2 
e_to = 0.775           
e_cr = 0.82
e_land = 0.725
k_to = 1 / (np.pi * AR * e_to)
k_cr = 1 / (np.pi * AR * e_cr)
k_land = 1 / (np.pi * AR * e_land)
ks = 1.2
R = 53.35                                                              #ft*lbf/lbm-Rankine

CLmax_TO = 1.7
CLmax_L = 2.1
CLmax_climb = CLmax_TO

# Weight Fractions
cr_wf = 0.93148704          
wf_climb =  0.970299
mid_wf = 0.7792324662696907                
dash30_wf = mid_wf         
man_wf = mid_wf
wf_landing = 0.6227770873721522

# Density and Temp Formulas
#Returns an array, with [density, speed of sound] at the given altitude
def atmo_vals(height):
    if height < 36152:                                                 #feet
        T_alt = 59 -0.00356*height                                     #Fahrenheit
        p_alt = 2116 * ((T_alt+459.7)/518.6)**(5.256)                  #lbf/ft^2
    elif height > 82345:
        T_alt = -205.5 + 0.00164*height
        p_alt = 51.97 * ((T_alt+459.7)/389.98)**(-11.388)
    else:
        T_alt = -70
        p_alt = 473.1 * np.exp(1.73 - 0.000048*height)
    rho_alt = p_alt / (1718 * (T_alt+459.7))                       #slugs/ft^3
    a_alt = (1.4*R*32.17*(T_alt+459.7))**(1/2)                     # ft/s
    T_alt += 459.67                                                #converts to rankine
    return [rho_alt,a_alt,p_alt,T_alt]


rho_40, a_40 = atmo_vals(40000)[:2]
rho_30, a_30 = atmo_vals(30000)[:2]
rho_20, a_20 = atmo_vals(20000)[:2]
rho_sl, a_SL = atmo_vals(0)[:2]
rho_to = 0.00224392                                                     # slug/ft^3 (sea level but 89.8F)

def Tratio(height):
    return (atmo_vals(height)[0]/atmo_vals(0)[0])**0.6

# Wing loading range
W_S = np.linspace(0, 200, 500)                                          #lbf/ft^2

# Stall
v_stall = 145/1.1                                                       #knots
v_stall *= 1.68781                                                      #ft/s
W_S_stall = 0.5 * rho_sl * v_stall**2 * CLmax_L

# Takeoff 
v_to = 160 #knotsF
v_to *= 1.68781 #conversion to ft/s
W_S_takeoff = 0.5 * rho_to * v_to**2 * CLmax_TO 

# Climb
SEROC_launch = 200/60                                                    #ft/s (200ft/min)
#G = 0.024                                                                #2.4% for FAR25
#T_W_climb = ks**2*CD0/CLmax_climb + CLmax_climb*k_to/(ks**2) + G
def tw_climb(WS):
    T_W_climb = SEROC_launch*(CD0/k_cr)**(1/4)*(rho_to/2)**(1/2)*(WS*wf_climb)**(-1/2)+2*(k_cr*CD0)**(1/2)
    T_W_climb = (1/0.8)*(1/0.94)*(n_eng/(n_eng-1))*(wf_climb)*T_W_climb     #converts back to TO condition
    return T_W_climb
T_W_climb = tw_climb(W_S)

# Cruise and Dash 
def cr_dash_constraint(v, rho, wf, T_ratio, WS):
    q = 0.5 * rho * v**2
    T_Wcr = (q * CD0) / (WS*wf) + (k_cr * WS*wf) / (q)
    return T_Wcr * wf / T_ratio

mach_cruise = 0.85
v_cr = mach_cruise * a_40     
Tcr_Tto = Tratio(40000)   
def tw_cruise (WS):
     cruiseTW = cr_dash_constraint(v_cr, rho_40, cr_wf, Tcr_Tto, WS)
     return  cruiseTW                                              
T_W_cruise = tw_cruise(W_S)

mach_dashSL = 0.85
v_dashSL = mach_dashSL * a_SL                                             # Ma 0.85-0.9 at SL
Tdashsl_Tto = 1
def tw_SLdash (WS):
     SLdashTW = cr_dash_constraint(v_dashSL, rho_sl, mid_wf, Tdashsl_Tto, WS)
     return  SLdashTW 
T_W_dashSL = tw_SLdash(W_S)

mach_dashSLideal = 0.9
v_dashSLideal = mach_dashSL * a_SL   
def tw_SLdashideal (WS):
     SLdashidealTW = cr_dash_constraint(v_dashSLideal, rho_sl, mid_wf, Tdashsl_Tto, WS)
     return  SLdashidealTW    
T_W_dashSLideal = tw_SLdashideal(W_S)

mach_dash30 = 1.6                                                          # 1.6-2.0 at 30kft
v_dash30 = mach_dash30 * a_30          
Tdash30_Tto = Tratio(30000)  
def tw_30dash(WS):
     h30dashTW = cr_dash_constraint(v_dash30, rho_30, dash30_wf, Tdash30_Tto, WS)
     return  h30dashTW    
T_W_dash30 = tw_30dash(W_S)

mach_dash30ideal = 2.0                    
v_dash30ideal = mach_dash30ideal * a_30    
def tw_30dashideal(WS):
     h30dashidealTW = cr_dash_constraint(v_dash30ideal, rho_30, dash30_wf, Tdash30_Tto, WS)
     return  h30dashidealTW    
T_W_dash30ideal = tw_30dashideal(W_S) 

# Service Ceiling
ROC_ceiling = 100 / 60                                                     #ft/s (service ceiling from slides)
ceiling_alt = 50000                                                        #ft chose reasonable value
Tceiling_ratio = Tratio(ceiling_alt)
def tw_ceiling(WS):
    TW_ceiling = ROC_ceiling*(CD0/k_cr)**(1/4)*((atmo_vals(ceiling_alt))[0]/2)**(1/2)*((WS* mid_wf))**(-1/2) + 2*(k_cr*CD0)**(1/2) 
    TW_ceiling *= mid_wf / Tceiling_ratio
    return TW_ceiling
T_W_ceiling = tw_ceiling(W_S)

# Maneuvering 
def manuever_constraint (v, rho, wf, T_ratio, psi, WS):
    q = 0.5 * rho * v**2
    n = np.sqrt((psi * v / g)**2 + 1)
    T_Wman = ((q * CD0) / (WS*wf) + (k_cr * n**2 * WS*wf) / (q))
    return T_Wman * wf / T_ratio


psi = 8 * np.pi/180                                                         # rad/s (8.0-10.0 deg/sec at 20,000 ft mid mission fuel weight)
v_maneuver = v_cr    #ft/s
T20_Tto = Tratio(20000)   
def tw_maneuver(WS):
    maneuverTW = manuever_constraint(v_maneuver, rho_20, man_wf, T20_Tto, psi, WS)
    return maneuverTW                                                 # 20kft thrust / take off thrust
T_W_maneuver = tw_maneuver(W_S)

psi_ideal = 10 * np.pi/180    # rad/s (8.0-10.0 deg/sec at 20,000 ft mid mission fuel weight)
def tw_maneuverideal(WS):
    maneuveridealTW = manuever_constraint(v_maneuver, rho_20, man_wf, T20_Tto, psi_ideal, WS)
    return maneuveridealTW      
T_W_maneuver_ideal = tw_maneuverideal(W_S)


# Traditional Runway Landing
v_engage56lb = 145                                                          # knots 
WOD = 15
v_landing = v_engage56lb + WOD
v_landing *= 1.68781                                                     #ft/s

W_S_landing_runway = ((cv.s_L - cv.s_a) * (cv.rho_10/cv.rho_sl) * cv.CLmax_L) / 80
W_S_landing_runway /= cv.wf_landing

# Arrestor Landing (will be check for later, probably not on the constraint diagram)
F_hook = 120000                                                           #lbf
s_lg = 349                                                                #ft, assumed length of landing runway w/ arresting wire
S_wet = 2500                                                              #ft^2, assumed wetted area of the aircraft
v_engage = 130 * 1.68781                                                  #ft/s, assumed engagement speed of the arresting hook (115 knots)

W_S_landing56lb = 0.5 * rho_sl * v_engage**2 * CLmax_L
W_S_landing56lb /= wf_landing


#W_S_landing = (s_lg * g * rho_sl * S_wet * CD0) / (np.log(1 + (0.5*rho_sl*S_wet*v_eng**2*CD0)/0.8*F_hook))




# # PLOTS
# plt.figure(figsize=(12, 8))
# plt.axvline(W_S_landing_runway, color='magenta', linewidth=2, label='Landing')
# plt.axvline(W_S_takeoff, color='black', linewidth=2, label='Takeoff (Catapult)')
# #plt.axvline(W_S_landing_runway, color='magenta', linestyle='--', linewidth=2, label='Landing (3000ft Runway)')
# plt.plot(W_S, T_W_climb, color='orange', linewidth=2, label='Climb (SEROC)')
# plt.plot(W_S, T_W_cruise, color='blue', linewidth=2, label='Cruise (40k ft, M0.85)')
# plt.plot(W_S, T_W_dashSL, color='cyan', linewidth=2, label='Dash SL (M0.85)')
# plt.plot(W_S, T_W_dashSLideal, color='cyan', linestyle='--', linewidth=2, label='Dash SL Ideal (M0.9)')
# plt.plot(W_S, T_W_dash30, color='limegreen',  linewidth=2, label='Dash 30k ft (M1.6)')
# plt.plot(W_S, T_W_dash30ideal, color='limegreen', linestyle='--', linewidth=1.8, label='Dash 30k ft Ideal (M2.0)')
# plt.plot(W_S, T_W_maneuver, color='red', linewidth=2, label='Maneuver (8 deg/s)')
# plt.plot(W_S, T_W_maneuver_ideal, color='red', linestyle='--', linewidth=2.2, label='Maneuver Ideal (10 deg/s)')
# diff = np.abs(T_W_dash30ideal - T_W_maneuver_ideal)
# plt.plot( (56411.39/675), (22000*2/56411.39), marker='*', color='gold', markersize=15,  markeredgecolor='black', zorder=5, label='Design Point')
# plt.axvline(W_S_stall, color='purple', linewidth=2, label='Stall')
# plt.plot(W_S, T_W_ceiling, color='darkgreen', linewidth=2, label='Service Ceiling (50,000 ft)')
# design_envelope = np.maximum.reduce([T_W_climb * np.ones_like(W_S), T_W_maneuver, T_W_dash30])

# plt.fill_between(W_S, design_envelope, 2.0,  # 2.0 is a safe upper Y-limit
#                  where=(W_S <= W_S_stall), 
#                  color='yellow', 
#                  alpha=0.3, 
#                  zorder=1,
#                  label='Design Window')
# plt.xlabel('Wing Loading W/S (lbf/ft²)', fontsize=18)
# plt.ylabel('Thrust-to-Weight Ratio T/W', fontsize=18)
# plt.title('Aircraft Constraint Diagram', fontsize=20)
# plt.grid(True, alpha=0.4)
# plt.legend(fontsize=14, loc='upper right')


# plt.xlim(0, 200)
# plt.ylim(0, 2.0)  

# plt.show()