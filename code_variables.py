# if this synced message me on discord 
# this is for declaring variables that are used across multiple files, such as the T_S_iteration.py and design_space.py files. This way, we can avoid hardcoding values in multiple places and maintain consistency across our codebase.
import numpy as np
# constants
R=53.35     # gas constant in (ft*lbf/lbm*R)                                                         #ft*lbf/lbm-Rankine
g = 32.174  # gravitational constant (slug/lbm)                                                         # ft/s^2
c_f=0.0026

# lift coefficients
CLmax_TO = 1.7 # maximum lift coefficient for takeoff
CLmax_L = 2.1 # maximum lift coefficient for landing
CLmax_climb = CLmax_TO # maximum lift coefficient for climb, assumed to be the same as takeoff

# weight fractions
wf_cr = 0.93148704              # weight fraction for cruise
wf_climb =  0.970299            # weight fraction for climb
wf_midclimb = 0.98               # weight fraction for mid-climb
wf_midcruise = 0.7806623694686121     # weight fraction for mid-cruise
wf_dash30 = wf_midcruise              # weight fraction for 30,000ft dash, assumed to be the same as mid-cruise
wf_man = 0.7792324662696907     # weight fraction for maneuvering
wf_landing = 0.6227770873721522 # weight fraction for landing
wf_warmup= 0.99                 # weight fraction for engine warmup, assumed to be 0.99 (1% fuel burn during warmup)   
wf_taxi= 0.99
wf_takeoff= 0.99
wf_descent= 0.99
wf_middescent = 0.995


# weight estimation fixed parameters
L_D_max=10 
R = 700#950            # nmi
E = 20 / 60         # min --> hr
ct_cruise = 0.7     # lb/(lbf hr)
ct_dash = 0.7   # lb/(lbf hr) for dash, assumed to be the same as cruise
v_cruise = 490      # knots
v_dash = 560        # knots (are we sure these are knots?)
S_ht = 0
S_vt = 45
S_wet_fuselage = 700
S_ref = 955
num_engines = 2  # Example number of engines

# The value we can adjust by the constraint curve. For example, if we want to be on the takeoff constraint curve, we can find the corresponding W/S and then calculate the TOGW based on that W/S and the wing area.
S_wingtest = 946 #based on vsp design v5
T_0 = 23930  # Example value for thrust per engine

##-----weights-------
num_pilot = 1
avg_wt_person = 200  #lb
aim_120c = 356 #lb
aim_9x = 188 #lb
mk_83jdam = 1000 #lb 
crew = 200 #lb
#a2a_payload = 6*aim_120c + 2*aim_9x + crew
strike_payload = 2*aim_9x + 4*mk_83jdam + crew
W_crew = num_pilot*crew
W_payload = strike_payload


# mach numbers 
M_cruise = 0.85
M_dashSL = 0.85
M_dashSLideal= 0.9
M_dash30= 1.6
M_dash30ideal = 2.0

# velocities
WOD=15*1.68781                          # ft/s, Wind over deck (given in RFP)
V_stall=145/1.1                         # stall speed in knots, divided by 1.1 to get a margin for climb speed
V_stall *= 1.68781                      # convert stall speed to ft/s
V_TO = 160 * 1.68781                    # takeoff speed in ft/s, assuming 160 knots for takeoff

                         # ft/s
V_engage_56lb = 145 * 1.68781           # ft/s, speed at which 56 lb of thrust is required for maneuvering constraint    
V_landing= V_engage_56lb+WOD            # ft/s, landing speed, sum of engage speed and wind over deck
V_engage= 130 * 1.68781                 # ft/s, speed at which arrestor is engaged, assuming 130 knots


# drag coefficients and factors
CD0=0.01166                             # clean, used for cruise

W_TO = 55700
AR = 2.066
n_eng = 2

# oswald efficiency factors for different configurations
e_to = 0.775                            #takeoff
e_cr = 0.82                             #cruise
e_land = 0.725                          #landing

# induced drag factors for different configurations
k_to = 1 / (np.pi * AR * e_to)          #takeoff
k_cr = 1 / (np.pi * AR * e_cr)          #cruise
k_land = 1 / (np.pi * AR * e_land)      #landing

# climb ratio (climb speed over stall speed)
ks = 1.2

# functions

#knots to ft/s conversion
def knots_to_ft_per_s(knots):
    return knots * 1.68781

# values at atmospheric conditions
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
rho_to = 0.00224392         

# thrust ratio at altitude
def Tratio(height):
    return atmo_vals(height)[2]/atmo_vals(0)[2] * np.sqrt(atmo_vals(0)[3]/atmo_vals(height)[3])

# weight fraction calculation function 
def calculate_weight_fraction(L_D_max, R, E, ct_cruise, ct_dash, v_cruise, v_dash):
    """This function calculates the weight fractions for cruise and loiter/descent phases based on the Breguet range and endurance equations, and also other terms.
    Args:
        L_D_max (float): Maximum lift-to-drag ratio of the aircraft.
        R (float): Combat range in nautical miles.
        E (float): Endurance in hours.
        ct (float): Specific fuel consumption in lb/(lbf hr).
        V (float): Velocity in knots."""
    
    L_D = 0.94 * L_D_max
    warmup = wf_warmup
    taxi = wf_taxi
    takeoff = wf_takeoff
    climb = wf_climb 
    dash_ingress = np.exp((-50*ct_dash) / (v_dash*L_D))
    dash_egress = dash_ingress
    descent = wf_descent
    midmission_descent = wf_middescent
    midmission_climb = wf_midclimb
    landing = 0.995 #this seems a little high for landing weight fraction
    cruise = np.exp((-R*ct_cruise) / (v_cruise*L_D))
    loiter = np.exp((-E*ct_cruise) / (L_D))

    weight_fraction = warmup*taxi*takeoff*climb*cruise*midmission_descent*dash_ingress*dash_egress*midmission_climb*cruise*descent*loiter*landing 

    Wf_W0 = (1 - weight_fraction) * 1.06    # compute fuel fraction
    print("Total Fuel Fraction Wf/W0: {:.3f}".format(Wf_W0))

    return Wf_W0

def calculate_zero_lift_drag_coefficient(c_f, S_wet, S_ref):
    return c_f * (S_wet / S_ref)

def calculate_engine_weight(T_0):
    W_eng_dry = 0.521 * T_0**0.9
    W_eng_oil = 0.082 * T_0**0.65
    W_eng_rev = 0.034 * T_0
    W_eng_control = 0.26 * T_0**0.5
    W_eng_start = 9.33 * (W_eng_dry/1000) ** 1.078
    W_eng = W_eng_dry + W_eng_oil + W_eng_rev + W_eng_control + W_eng_start
    #W_eng = 3826 # actual F100 weight (from https://www.rtx.com/en/prattwhitney/products/military-engines/f100)
    W_eng= 4000
    return W_eng


def calculate_empty_weight(S_wing, S_ht, S_vt, S_wet_fuselage, TOGW, T_0 , num_engines):
    W_wing = S_wing * 9
    W_ht = S_ht * 4
    W_vt = S_vt * 5.3
    W_fuselage = S_wet_fuselage * 4.8
    W_landing_gear = 0.045 * TOGW
    Engine_weight = calculate_engine_weight(T_0)
    W_engines = Engine_weight * num_engines * 1.3
    W_all_else = 0.17 * TOGW
    W_empty = W_wing + W_ht + W_vt + W_fuselage + W_landing_gear + W_engines + W_all_else
    return W_empty


V_dashSL = M_dashSL *a_SL               # ft/s
V_cruise = M_cruise * a_40              # ft/s
V_dashSLideal = M_dashSLideal * a_SL    # ft/s
V_dash30 = M_dash30 * a_30              # ft/s
V_dash30ideal = M_dash30ideal * a_30    # ft/s
V_man=V_cruise 

# W_S fractions
W_S_stall = 0.5 * rho_sl * V_stall**2 * CLmax_L  # wing loading at stall
W_S_TO = 0.5 * rho_sl * V_TO**2 * CLmax_TO       # wing loading at takeoff
W_S_landing_56lb= 0.5 * rho_sl * V_landing**2 * CLmax_L/wf_landing   # wing loading at speed where 56 lb of thrust is required for maneuvering constraint