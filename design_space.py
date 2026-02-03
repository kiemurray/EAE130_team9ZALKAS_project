import numpy as np
import matplotlib.pyplot as plt

#add ideal and necessary dashes and manuevers to see

#constants (come back)
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

CLmax_TO = 1.7
CLmax_L = 2.1
CLmax_climb = np.sqrt(CD0/k_cr) 


rho_40 = 0.000585189         # slug/ft^3 (cruise 40k ft)
a_40 = 968.076               # ft/s
rho_30 = 0.000889378
a_30 = 994.664
rho_20 = 0.00126659
a_20 = 1036.85
rho_sl = 0.00237717          
a_SL = 1116.45
rho_to = 0.00224392          # slug/ft^3 (sea level but 89.8F)

# Wing loading range
W_S = np.linspace(0, 200, 500)  #lbf/ft^2

# Stall
v_stall = 145/1.1
W_S_stall = 0.5 * rho_sl * v_stall**2 * CLmax_L

# Takeoff constraint
s_to = 	306 + 9/12               # C-13-2 catapult stroke length (ft)
T_W_takeoff = ks**2 * W_S / (rho_to * g * CLmax_TO * s_to)

# Catapult Constraints
#
#
#

# climb
SEROC_launch = 200/60  #ft/s (200ft/min)
G = SEROC_launch / (ks * np.sqrt(2 * W_S / (rho_sl * CLmax_climb)))
wf_climb =  0.9314870399999999

T_W_climb = ks**2*CD0/CLmax_climb + CLmax_climb*k_to/(ks**2) + G
T_W_climb = (1/0.8)*(1/0.94)*(n_eng/(n_eng-1))*(wf_climb)*T_W_climb

# Landing constraint 
s_lg = 349                 # ft (COME BACK TO THIS)
l_wf = 0.6196632019352915        # landing weight fraction (find from weight code later)
W_S_landing = s_lg * rho_to/rho_sl * CLmax_L / (80 * l_wf)
print(f"ws landing = {W_S_landing}")

# Cruise and Dash Constraints
def cr_dash_constraint(v, rho, wf, T_dash_ratio):
    q = 0.5 * rho * v**2
    return (q * CD0) / (wf * T_dash_ratio * W_S) + (k_cr * T_dash_ratio * W_S) / (wf * q)

mach_cruise = 0.85
v_cr = mach_cruise * a_40    # ft/s Ma 0.8-0.85 at 40,000ft
cr_wf = 0.6443957522603523  # cruise weight fraction (find from weight code later, figure out if we need cruise 1 or cruise 2)
Tcr_Tto = rho_40/rho_sl                # cruise thrust / take off thrust?
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
Tdash30_Tto = rho_30/rho_sl     
T_W_dash30 = cr_dash_constraint(v_dash30, rho_30, dash30_wf, Tdash30_Tto)

mach_dash30ideal = 2.0     # 1.6-2.0 at 30kft
v_dash30ideal = mach_dash30ideal * a_30          
T_W_dash30ideal = cr_dash_constraint(v_dash30ideal, rho_30, dash30_wf, Tdash30_Tto)

# Ceiling constraint
ROC_ceiling = 100 / 60    # ft/s (service ceiling from slides)
T_W_ceiling = 0.0 #add eq

# Maneuvering constraint
def manuever_constraint (v, rho, wf, T_man_ratio, psi):
    q = 0.5 * rho * v**2
    n = np.sqrt((psi * v / g)**2 + 1)
    return ((q * CD0) / (T_man_ratio * wf * W_S) + (k_cr * n**2 * wf * W_S) / (T_man_ratio * q))

psi = 8 * np.pi/180    # rad/s (8.0-10.0 deg/sec at 20,000 ft mid mission fuel weight)
v_maneuver = v_cr      # idk yet
T20_Tto = rho_20/rho_sl          # 20kft thrust / take off thrust
man_wf = mid_wf
T_W_maneuver = manuever_constraint(v_maneuver, rho_20, man_wf, T20_Tto, psi)

psi_ideal = 10 * np.pi/180    # rad/s (8.0-10.0 deg/sec at 20,000 ft mid mission fuel weight)
T_W_maneuver_ideal = manuever_constraint(v_maneuver, rho_20, man_wf, T20_Tto, psi_ideal)



# PLOTS
plt.figure(figsize=(12, 8))


plt.plot(W_S, T_W_takeoff, color='black', linewidth=2.5, label='Takeoff (Catapult)')

plt.plot(W_S, T_W_climb, color='tab:orange', linewidth=2.5, label='Climb (SEROC)')

plt.plot(W_S, T_W_cruise, color='tab:blue', linewidth=2.2, label='Cruise (40k ft, M0.85)')

plt.plot(W_S, T_W_dashSL, color='tab:blue', linestyle='--', linewidth=1.8, label='Dash SL (M0.85)')
#plt.plot(W_S, T_W_dashSLideal, color='tab:blue', linestyle=':', linewidth=1.8, label='Dash SL Ideal (M0.9)')

plt.plot(W_S, T_W_dash30, color='tab:green', linestyle='--', linewidth=1.8, label='Dash 30k ft (M1.6)')
#plt.plot(W_S, T_W_dash30ideal, color='tab:green', linestyle=':', linewidth=1.8, label='Dash 30k ft Ideal (M2.0)')

plt.plot(W_S, T_W_maneuver, color='tab:red', linewidth=2.5, label='Maneuver (8 deg/s)')
#plt.plot(W_S, T_W_maneuver_ideal, color='tab:red', linestyle='--', linewidth=2.2, label='Maneuver Ideal (10 deg/s)')

plt.axvline(W_S_landing, color='magenta', linestyle='-.', linewidth=2, label='Landing')
plt.axvline(W_S_stall, color='purple', linestyle=':', linewidth=2, label='Stall')


# Formatting
plt.xlabel('Wing Loading W/S (lbf/ft²)', fontsize=14)
plt.ylabel('Thrust-to-Weight Ratio T/W', fontsize=14)
plt.title('Aircraft Constraint Diagram', fontsize=16)
plt.grid(True, alpha=0.4)
plt.legend(fontsize=10, loc='upper right')

plt.xlim(0, 200)
plt.ylim(0, 2.0)  # Adjust this if needed

plt.show()
