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

# 2/25 Lab Code Variables
# geometric variables

# empennage sizing
# vertical tail
c_vt = 0.094        # vertical tail volume coefficient
L_vt = 14.4         # vertical tail moment arm (ft)

# wing
b_w = 41.026226        # wing span tip-to-tip (ft)
c_w = 19.918018        # wing chord (ft)
S_w = 685             # wing area (ft^2)

# horizontal tail
c_ht = 0.3        # horizontal tail volume coefficient
L_ht = 15.4       # horizontal tail moment arm (ft)

lambda_w = 40   # Sweep angle of wing (degrees)
lambda_h = 45   # Sweep angle of horizontal tail (degrees)

eta_w = 0.97      # difference factor between the theoretical section lift curve slope for the wing
eta_h = 0.9      # difference factor between the theoretical section lift curve slope for the horizontal tail

Kf = 0.344      # empirical factor
Lf = 45         # fuselage length (ft)
Wid_fuse = 14.6   # maximum width of fuselage (ft)

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

# Landing Parameters
s_L = 5000 # total landing distance 
s_a = 450 # ground clearance distance, taken from STOL requirements
s_L_G = 349 # carrier ground roll distance for landing, assumed to be 349 ft
F_hook = 120000

# weight estimation fixed parameters
L_D_max=10 
R = 950             # nmi
E = 20 / 60         # min --> hr
ct_cruise = 0.7     # lb/(lbf hr)
ct_dash = 0.7       # lb/(lbf hr) for dash, assumed to be the same as cruise
v_cruise = 490      # knots
v_dash = 560        # knots (are we sure these are knots?)
S_t_plan = 177      # V-tail area based on Raymer approximation
S_ht = 109
S_vt = 66
S_wet_fuselage = 700
S_ref = 685
num_engines = 2  # Example number of engines

# The value we can adjust by the constraint curve. For example, if we want to be on the takeoff constraint curve, we can find the corresponding W/S and then calculate the TOGW based on that W/S and the wing area.
S_wingtest = 685 #based on vsp design v5
T_0 = 23930  # Example value for thrust per engine
T_0_mil = 13000
c_t_military = 0.724 #lb/(lbf hr)
c_t_AB = 1.85 #lb/(lbf hr)

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
CD0=0.01036                             # clean, used for cruise

W_TO = 55700
AR_w = 2.46
AR_h = 3.5       # aspect ratio of horizontal stabilizer (empenage slide 54)
n_eng = 2

# oswald efficiency factors for different configurations
e_to = 0.775                            #takeoff
e_cr = 0.82                             #cruise
e_cr_estimate = 4.61*(1-0.045*AR_w**0.68)*(np.cos(lambda_w*np.pi/180)**0.15)-3.1 #Raymer equation 12.49

print("e_cruise guess: ",e_cr,"\ne_cruiseEstimate: ",e_cr_estimate)
e_land = 0.725                          #landing

# induced drag factors for different configurations
k_to = 1 / (np.pi * AR_w * e_to)          #takeoff
k_cr = 1 / (np.pi * AR_w * e_cr)          #cruise
k_land = 1 / (np.pi * AR_w * e_land)      #landing

# climb ratio (climb speed over stall speed)
ks = 1.2

# functions

#knots to ft/s conversion
def knots_to_ft_per_s(knots):
    return knots * 1.68781

def ft_s_to_knots(ft_s):
    return ft_s / 1.68781

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
rho_10, a_10 = atmo_vals(10000)[:2]
rho_sl, a_SL = atmo_vals(0)[:2]
rho_to = 0.00224392    
rho_cruise = rho_40

#fuel volume things
rho_jp5 = 51.1              #lb/ft^3   
packing_factor_shallow_fuselage = 0.8
packing_factor_deep_fuselage = 0.85
packing_factor_wing= 0.75

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



x_cg =  23.8094      # aircraft center of gravity (ft) assumed

## variables from Weight Class 2 Estimation
V_t = 3127 # Total Fuel Volume, gal
V_i = 0.75 * V_t # Integral Fuel Tank Volume, gal
V_p = 0.25 * V_t # Self-Sealing Wing Tank Volume, gal
N_t = 10 # Number of Tanks
SFC = 1.85 # SFC at max thrust
S_cs = 223 # Total Area of Flight Control Surfaces
N_s = 10 # Number of Flight Control Surfaces
N_c = 6 # Number of Functions Performed By Controls (4-7)
K_vsh = 1.0 # Non-Variable Sweep Wing
N_u = 10 # Number of Hydraulic Utility Functions (5-15)
K_mc = 1.45 # Mission Completion Required After Failure
R_kva = 160 # System Electrical Rating, kV * A
L_a = 35 # Electrical Routing Distance, ft
W_urdr = 1221 # Uninstalled Radar Weight, lbf
W_uav = 2500 - W_urdr # Uninstalled Avionics Weight, lbf
S_fw = 45 # Firewall Surface Area, ft^2 (discuss estimation later)
W_en = 2445 # Engine Weight, each, lbf
K_vg = 1.62 # Variable Inlet Geometry
L_d = 11.23 # Duct Length, ft
K_d = 2.6 # Duct Constant
L_s = 11.23 # Single Duct Length, ft
D_e = 6.68 # Engine Diameter, ft
L_tp = 2.5 # Length of Tailpipe, ft
L_sh = 12.83 # Length of Engine Shroud, ft
L_ec = 21.6 # Length From Engine Front to Cockpit, ft
T_e = 22000 # Thrust per Engine, lbf
tc_root = 0.06 # t/c ratio at root chord
taper_ratio = 0.295 # Taper Ratio
wing_sweep = 45 # Wing Sweep at 25% MAC
S_csw = 103 # Wing Mounted Control Surface Area ft^2
K_rht = 1.047 # Rolling Tail (Stabilators)
H_t = 0 # Horizontal Tail Height Above Fuselage
H_v = 4.5 # Vertical Tail Height Above Fuselage (this gets cancelled out anyways)
M = 2.0 # Mach Number
L_t = 10.78 # Tail Length
S_r = 120 # Rudder Area ft^2
AR_vt = 1.85 # Vertical Tail Aspect Ratio
taper_ratio_vt = 0.3 # Vertical Tail Taper Ratio
sweep_vt = 50 # Vertical Tail Sweep
K_dwf = 1 # For Non-Delta Wing Aircraft
L_f = 47.5 # Fuselage Length, ft
D_f = 6.4 # Fuselage Depth, ft
W_f = 14.6 # Fuselage Width, ft
K_cb = 1.0 # Non Cross Beam
K_tpg = 1.0 # Non-Tripod Landing Gear
W_l = 34000 # Landing Gross Weight, lbf
N_gear = 3.8 # Landing Limit Load (Raymer Assumption)
N_l = 1.5 * N_gear # Ultimate Landing Load Factor
L_m = 48 # Length of Landing Gear, in.
L_n = 48 # Length of Nose Gear, in.
N_nw = 2 # Number of Nose Wheels
K_dw = 1 # Non-Delta Wing
K_vs = 1.0 # non-variable sweep
W_dg = 56631 # Design Gross Weight (lbf)
n_z = 8.0 # limit load, desired by RFP
N_z = 1.5 * n_z # Ultimate Load Factor
n_zv = 3.0 # Vertical Tail Limit Load (estimated)
N_zv = 1.5 * n_zv # Vertical Tail Limit Load
S_w = 685 # Trapezoidal Wing Area ft^2


## -------- Updated Fuel Fractions -------- ##

#Sam is messing with fuel fractions
#If this works properly I will move to another file :)

#GE F414 Specs

T_idle = 0.05*T_0 #idle thrust



#Updated Fuel Fractions (From Raymer Ch 19)
def fuelFraction(t,c_t,T_A_initial,W_initial): #time in hours
    #t is time during a mission segment (assume constant T/W)
    #Break up segments into small chunks to assume constant T/W

    return 1-t*c_t*(T_A_initial/W_initial)

#wf_warmup = fuelFraction(0.25,c_t_military,T_idle,W_TO)
#wf_taxi = 1 #warmup includes warmup and taxi
wf_takeoff = fuelFraction(5/60,c_t_military,2*T_0_mil,W_TO)
#wf_climb = np.exp()
W_cruise_i = W_TO*wf_warmup*wf_taxi*wf_climb
print("W_cruise_initial: ",W_cruise_i,"lbf")
print("Air density at 40,000 ft: ",rho_cruise,"slugs/ft^3")
print("Cruise induced drag coefficient: ",k_cr)
CL_bestRange = np.sqrt(CD0/(3*k_cr))
print("C_L_bestRange: ",CL_bestRange)
V_bestRange = np.sqrt((2*W_cruise_i/(rho_cruise*S_w*CL_bestRange))) #ft/s
print("V_bestRange:",V_bestRange,"ft/s\nV_bestRange: ",V_bestRange/1.688,"kts = Mach",(V_bestRange/968),"Wf_takeoff",wf_takeoff)


## ---------------------------------------- ##
