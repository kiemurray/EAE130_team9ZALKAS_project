import numpy as np
import matplotlib.pyplot as plt

#constants 
g = 32.174          # ft/s^2
CD0 = 0.01111       # clean, used for cruise and dashes
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
R = 53.35           #ft*lbf/lbm-Rankine

CLmax_TO = 1.7
CLmax_L = 2.1
CLmax_climb = 1.9 # REVISIT


# Density and Temp Formulas
#Returns an array, with [density, speed of sound] at the given altitude
def atmo_vals(height):
    if height < 36152:                              #feet
        T_alt = 59 -0.00356*height                  #Fahrenheit
        p_alt = 2116 * ((T_alt+459.7)/518.6)**(5.256)   #lbf/ft^2
    elif height > 82345:
        T_alt = -205.5 + 0.00164*height
        p_alt = 51.97 * ((T_alt+459.7)/389.98)**(-11.388)
    else:
        T_alt = -70
        p_alt = 473.1 * np.exp(1.73 - 0.000048*height)
    rho_alt = p_alt / (1718 * (T_alt+459.7))            #slugs/ft^3
    a_alt = (1.4*R*32.17*(T_alt+459.7))**(1/2)
    T_alt += 459.67 #converts to rankine
    return [rho_alt,a_alt,p_alt,T_alt]


rho_40 = 0.000585189         # slug/ft^3 (cruise 40k ft)
a_40 = 968.076               # ft/s
rho_30 = 0.000889378
a_30 = 994.664
rho_20 = 0.00126659
a_20 = 1036.85
rho_sl = 0.00237717          
a_SL = 1116.45
rho_to = 0.00224392          # slug/ft^3 (sea level but 89.8F)
def Tratio(height):
    return atmo_vals(height)[2]/atmo_vals(0)[2] * np.sqrt(atmo_vals(0)[3]/atmo_vals(height)[3])

# Wing loading range
W_S = np.linspace(0, 200, 500)  #lbf/ft^2

# Stall (DONE)
v_stall = 145/1.1   #knots
v_stall *= 1.68781  #ft/s
W_S_stall = 0.5 * rho_sl * v_stall**2 * CLmax_L

# Takeoff constraint
v_to = 160 #knots
v_to *= 1.68781 #conversion to ft/s
W_S_takeoff = 0.5 * rho_to * v_to**2 * CLmax_TO

# climb
SEROC_launch = 200/60  #ft/s (200ft/min)
wf_climb =  0.93148704 
G = SEROC_launch / (ks * np.sqrt(2 * W_S / (rho_to * CLmax_climb)))     #seroc/v_climb or set to 1.2% for FAR25
T_W_climb = ks**2*CD0/CLmax_climb + CLmax_climb*k_to/(ks**2) + G
T_W_climb = (1/0.8)*(1/0.94)*(n_eng/(n_eng-1))*(wf_climb)*T_W_climb     #converts back to TO condition


# Cruise and Dash Constraints
def cr_dash_constraint(v, rho, wf, T_dash_ratio):
    q = 0.5 * rho * v**2
    T_Wcr = (q * CD0) / (wf * W_S) + (k_cr * wf * W_S) / (q)
    return T_Wcr * wf / T_dash_ratio

mach_cruise = 0.85
v_cr = mach_cruise * a_40              # ft/s Ma 0.8-0.85 at 40,000ft
cr_wf = 0.6443957522603523             # cruise weight fraction (find from weight code later, figure out if we need cruise 1 or cruise 2)
Tcr_Tto = Tratio(40000)              # cruise thrust / take off thrust?
T_W_cruise = cr_dash_constraint(v_cr, rho_40, cr_wf, Tcr_Tto)

mach_dashSL = 0.85
v_dashSL = mach_dashSL * a_SL       # Ma 0.85-0.9 at SL
mid_wf = 0.7806623694686121        
Tdashsl_Tto = 1
T_W_dashSL = cr_dash_constraint(v_dashSL, rho_sl, mid_wf, Tdashsl_Tto)

mach_dashSLideal = 0.9
v_dashSLideal = mach_dashSL * a_SL      
T_W_dashSLideal = cr_dash_constraint(v_dashSLideal, rho_sl, mid_wf, Tdashsl_Tto)


mach_dash30 = 1.6     # 1.6-2.0 at 30kft
v_dash30 = mach_dash30 * a_30          
dash30_wf = mid_wf      #maybe change?
Tdash30_Tto = Tratio(30000)     
T_W_dash30 = cr_dash_constraint(v_dash30, rho_30, dash30_wf, Tdash30_Tto)

mach_dash30ideal = 2.0                    # 1.6-2.0 at 30kft
v_dash30ideal = mach_dash30ideal * a_30          
T_W_dash30ideal = cr_dash_constraint(v_dash30ideal, rho_30, dash30_wf, Tdash30_Tto)

# Ceiling constraint
ROC_ceiling = 100 / 60    # ft/s (service ceiling from slides)

#this doesn't convert to takeoff T_W;
T_W_ceiling = ROC_ceiling*(CD0/k_cr)**(1/4)*((atmo_vals(30000))[0]/2)**(1/2)*((W_S_takeoff * wf_climb))**(-1/2) + 2*(k_cr*CD0)**(1/2) #Lec 7 Slide 32


# Maneuvering constraint
def manuever_constraint (v, rho, wf, T_man_ratio, psi):
    q = 0.5 * rho * v**2
    n = np.sqrt((psi * v / g)**2 + 1)
    T_Wman = ((q * CD0) / (wf * W_S) + (k_cr * n**2 * wf * W_S) / (q))
    return T_Wman * wf / T_man_ratio
psi = 8 * np.pi/180    # rad/s (8.0-10.0 deg/sec at 20,000 ft mid mission fuel weight)
v_maneuver = v_cr    # idk yet
T20_Tto = Tratio(20000)          # 20kft thrust / take off thrust
man_wf = mid_wf
T_W_maneuver = manuever_constraint(v_maneuver, rho_20, man_wf, T20_Tto, psi)

psi_ideal = 10 * np.pi/180    # rad/s (8.0-10.0 deg/sec at 20,000 ft mid mission fuel weight)
T_W_maneuver_ideal = manuever_constraint(v_maneuver, rho_20, man_wf, T20_Tto, psi_ideal)

# Landing constraint 
v_engage56lb = 145      #knots based on graph and landing weight of 34513
v_engage56lb += 15      # accounts for WOD
v_engage56lb *= 1.68781 #ft/s
W_S_landing56lb = 0.5 * rho_sl * v_engage56lb**2 * CLmax_L

# PLOTS
plt.figure(figsize=(12, 8))


plt.axvline(W_S_takeoff, color='black', linewidth=2, label='Takeoff (Catapult)')

plt.plot(W_S, T_W_climb, color='orange', linewidth=2, label='Climb (SEROC)')
#plt.axhline(T_W_climb, color='tab:orange', linewidth=2, label='Climb (SEROC)')

plt.plot(W_S, T_W_cruise, color='blue', linewidth=2, label='Cruise (40k ft, M0.85)')

plt.plot(W_S, T_W_dashSL, color='cyan', linewidth=2, label='Dash SL (M0.85)')
plt.plot(W_S, T_W_dashSLideal, color='cyan', linestyle='--', linewidth=2, label='Dash SL Ideal (M0.9)')

plt.plot(W_S, T_W_dash30, color='green',  linewidth=2, label='Dash 30k ft (M1.6)')
plt.plot(W_S, T_W_dash30ideal, color='green', linestyle='--', linewidth=1.8, label='Dash 30k ft Ideal (M2.0)')

plt.plot(W_S, T_W_maneuver, color='red', linewidth=2, label='Maneuver (8 deg/s)')
plt.plot(W_S, T_W_maneuver_ideal, color='red', linestyle='--', linewidth=2.2, label='Maneuver Ideal (10 deg/s)')

plt.axvline(W_S_landing56lb, color='magenta',  linewidth=2, label='Landing')
plt.axvline(W_S_stall, color='purple', linewidth=2, label='Stall')
plt.axhline(T_W_ceiling, color='darkgreen', linewidth=2, label='Ceiling (at 60000 feet)')

# Formatting
plt.xlabel('Wing Loading W/S (lbf/ft²)', fontsize=14)
plt.ylabel('Thrust-to-Weight Ratio T/W', fontsize=14)
plt.title('Aircraft Constraint Diagram', fontsize=16)
plt.grid(True, alpha=0.4)
plt.legend(fontsize=10, loc='upper right')

plt.xlim(0, 200)
plt.ylim(0, 2.0)  

plt.show()
