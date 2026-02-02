import numpy as np
import matplotlib.pyplot as plt

#question: use strike mission TOGW? or use mission weights depending on where the req comes from?
#add ideal and necessary dashes and manuevers to see

#constants (come back)
g = 32.174        # ft/s^2
ks = 0.0            # idk how to find this 
CD0 = 0.0          # use OpenVSP
AR = 0.0              # use OpenVSP
e = 0.0             # ???
k = 1 / (np.pi * AR * e)

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
W_S = np.linspace(20, 200, 500)  #lbf/ft^2

# Takeoff constraint
s_to = 	306 + 9/12               # C-13-2 catapult stroke length (ft)
CLmax_TO = 0.0
T_W_takeoff = ks**2 * W_S / (rho_to * g * CLmax_TO * s_to)

# Catapult Constraints
#
#
#

# Landing constraint 
s_lg = 349         # ft
l_wf = 0.0         # landing weight fraction (find from weight code later)
CLmax_L = 0.0
W_S_landing = s_lg * rho_to * CLmax_L / 80
W_S_landing = W_S_landing / (l_wf)

# Cruise and Dash Constraints
def cr_dash_constraint(v, rho, wf, T_dash_ratio):
    q = 0.5 * rho * v**2
    return (q * CD0) / (wf * T_dash_ratio * W_S) + (k * T_dash_ratio * W_S) / (wf * q)

mach_cruise = 0.85
v_cr = mach_cruise * a_40    # ft/s Ma 0.8-0.85 at 40,000ft
cr_wf = 0.0                  # cruise weight fraction (find from weight code later, figure out if we need cruise 1 or cruise 2)
Tcr_Tto = 0.0                # cruise thrust / take off thrust?
T_W_cruise = cr_dash_constraint(v_cr, rho_40, cr_wf, Tcr_Tto)

mach_dashSL = 0.85
v_dashSL = mach_dashSL * a_SL       # Ma 0.85-0.9 at SL
mid_wf = 0.0                           # use weight code
Tdashsl_Tto = 0.0 
T_W_dashSL = cr_dash_constraint(v_dashSL, rho_sl, mid_wf, Tdashsl_Tto)

mach_dash30 = 1.6     # 1.6-2.0 at 30kft
v_dash30 = mach_dash30 * a_30          
dash30_wf = 0.0       # weight fraction (find from weight code later, figure out what part of mission)
Tdash30_Tto = 0.0     
T_W_dashSL = cr_dash_constraint(v_dash30, rho_30, dash30_wf, Tdash30_Tto)

# Ceiling constraint
ROC_ceiling = 100 / 60    # ft/s (service ceiling from slides)
T_W_ceiling = 0.0 #add eq

# Maneuvering constraint
psi = 0.0              # rad/s (8.0-10.0 deg/sec at 20,000 ft mid mission fuel weight)
v_maneuver = 0.0       # idk yet
T20_Tto = 0.0          # midmission thrust / take off thrust
man_wf = mid_wf
def manuever_constraint (v, rho, wf, T_man_ratio, psi):
    q = 0.5 * rho * v**2
    n = np.sqrt((psi * v / g) + 1)
    return ((q * CD0) / (T_man_ratio * wf * W_S) + (k * n**2 * mid_wf * W_S) / (T_man_ratio * q))
T_W_maneuver = manuever_constraint(v_maneuver, rho_20, man_wf, T20_Tto, psi)

# Plot
#
#
#