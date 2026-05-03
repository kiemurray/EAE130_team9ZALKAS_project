# this is for declaring variables that are used across multiple files, such as the T_S_iteration.py and design_space.py files. This way, we can avoid hardcoding values in multiple places and maintain consistency across our codebase.
import numpy as np

# constants
R=53.35     # gas constant in (ft*lbf/lbm*R)                                                         #ft*lbf/lbm-Rankine
g = 32.174  # gravitational constant (slug/lbm)   
c_f=0.0026
ra = 950             # nmi
E = 20 / 60         # min --> hr
WOD=15*1.68781                          # ft/s, Wind over deck (given in RFP)
CD0=0.01036                             # clean, used for cruise
num_pilot = 1
avg_wt_person = 200  #lb
aim_120c = 356 #lb
aim_9x = 188 #lb
mk_83jdam = 1000 #lb 
crew = 200 #lb
a2a_payload = 6*aim_120c + 2*aim_9x + crew
strike_payload = 2*aim_9x + 4*mk_83jdam + crew
W_crew = num_pilot*crew
W_payload = strike_payload
SFC = 1.85 # SFC at max thrust
K_mc = 1.45 # Mission Completion Required After Failure
W_urdr = 1221 # Uninstalled Radar Weight, lbf
W_uav = 2500 - W_urdr # Uninstalled Avionics Weight, lbf
S_fw = 45 # Firewall Surface Area, ft^2 (discuss estimation later)
W_en = 2445 # Engine Weight, each, lbf
M = 2.0 # Mach Number


# lift coefficients (updated after A2)
CLmax_TO = 1.5 # maximum lift coefficient for takeoff
CLmax_L = 1.8 # maximum lift coefficient for landing
CLmax_climb = 0.9 # maximum lift coefficient for climb, assumed clean


# stucture variables

x_cg =  23.8094      # aircraft center of gravity (ft) assumed
num_engines = 2 # Number of Engines
S_cs = 223 # Total Area of Flight Control Surfaces
N_s = 10 # Number of Flight Control Surfaces
N_c = 6 # Number of Functions Performed By Controls (4-7)
N_u = 10 # Number of Hydraulic Utility Functions (5-15)
W_dg = 56631 # Design Gross Weight (lbf)
n_z = 8.0 # limit load, desired by RFP
N_z = 1.5 * n_z # Ultimate Load Factor
n_z_negative = -5 #estimate for negative limit load




# wing (600 sq ft)
y_offset = 3 #ft
b_w = 37.458        # wing span tip-to-tip (ft)
b_w_total = b_w + 2*y_offset
c_w = 13.47       # wing chord (ft)
S_w = 560             # wing area (ft^2)
AR_w = 2.52
tc_root = 0.06 # t/c ratio at root chord
taper_ratio = 0.137 # Taper Ratio
wing_sweep = 50 # Wing Sweep at 25% MAC
lambda_w = 50   # Sweep angle of wing (degrees)

#Section 1 (root to change in back sweep)
c_root_1 = 29.34     #root chord (ft)
b_section_1 = 11.558   #section 1 span
b_section_1_total = (y_offset+b_section_1)*2
lambda_back_1 = 25      #desired back sweep (degrees)
c_tip_1 = c_root_1 - b_section_1*(np.tan(np.deg2rad(lambda_w))+np.tan(np.deg2rad(lambda_back_1))) 
#print("For",lambda_back_1,"degree back sweep, section 1 tip chord is:",c_tip_1,"ft")
#print("Total section 1 wingspan:",b_section_1_total,"ft")


#Section 2 (change in back sweep to tip)
c_root_2 = c_tip_1     #root chord (ft)
b_section_2 = (0.5*b_w) - b_section_1   #section 2 span
#print("Section 2 span:",b_section_2,"ft")
lambda_back_2 = 20      #desired back sweep (degrees)
c_tip_2 = c_root_2 - b_section_2*(np.tan(np.deg2rad(lambda_w))-np.tan(np.deg2rad(lambda_back_2))) 
#print("For",lambda_back_2,"degree back sweep, section 2 tip chord is:",c_tip_2,"ft")
#print("Taper ratio becomes:",c_tip_2/c_root_1)
#print("Aspect ratio becomes:",((b_w)**2)/S_w)

eta_w = 0.97      # difference factor between the theoretical section lift curve slope for the wing
S_csw = 103 # Wing Mounted Control Surface Area ft^2
K_dwf = 0.774 # For Non-Delta Wing Aircraft
K_vs = 1.0 # non-variable sweep
S_wet_wing = 692.402

#flaps info updated May 1st (B3.17)
#25 percent chord
#b_range_flaps (0.15 - 0.6315 inboard) (0.632 - 1.0 outboard)
#print("b_f:",(0.6315 - 0.150) *b_w,"ft")
#print("c_f_inner:",0.25*c_tip_1,"ft")
#print("c_f_outer:",0.25*c_root_1,"ft")
b_f = 18.03 #feet (both sides)
c_f_inner = 2.544 #feet (inner chord)
c_f_outer = 7.335 #feet (outer chord)
S_flap = 178.11 #ft^2
#print("inboard flap area:",(0.25*(c_root_1+c_tip_1))*(b_f),"ft^2")




#inboard slats (0.1 * c_wing)
c_slat_inboard_i = 2.118 #feet
c_slat_inboard_o = 0.909 #feet 
b_slat_inboard = (0.6797 - 0.226) * b_w

#slats (0.1 * c_wing)
c_slat_outboard_i = 0.909 #feet
c_slat_outboard_o = 0.449 #feet 
b_slat_outboard = (1 - 0.670732) * b_w


# fuselage
S_wet_fuselage = 528.140 
K_f = 0.344      # empirical factor
L_f = 47.5         # fuselage length (ft)
D_f = 6.4 # Fuselage Depth, ft
W_f = 14.6   # maximum width of fuselage (ft)
K_dw = 0.768
K_vg = 1.62 # Variable Inlet Geometry
R_kva = 160 # System Electrical Rating, kV * A
L_a = 35 # Electrical Routing Distance, ft
L_d = 11.23 # Duct Length, ft
K_d = 2.6 # Duct Constant
L_s = 11.23 # Single Duct Length, ft
D_e = 6.68 # Engine Diameter, ft
L_tp = 2.5 # Length of Tailpipe, ft
L_sh = 12.83 # Length of Engine Shroud, ft
L_ec = 21.6 # Length From Engine Front to Cockpit, ft
T_e = 22000 # Thrust per Engine, lbf
K_cb = 1.0 # Non Cross Beam
K_tpg = 1.0 # Non-Tripod Landing Gear
W_l = 34000 # Landing Gross Weight, lbf
N_gear = 3.8 # Landing Limit Load (Raymer Assumption)
N_l = 1.5 * N_gear # Ultimate Landing Load Factor
L_m = 48 # Length of Landing Gear, in.
L_n = 48 # Length of Nose Gear, in.
N_nw = 2 # Number of Nose Wheels


# vertical tail
c_vt = 0.094 # vertical tail volume coefficient (Raymer Section 6.5.3)
print("Vertical tail arm:",0.40 * L_f,"ft")
L_vt = 19 # vertical tail moment arm (ft) (Should be 45-50% of the fuselage length according to Raymer 6.5.3) (Updated May 1)
H_v = 4.5 # Vertical Tail Height Above Fuselage (this gets cancelled out anyways)
AR_vt = 1.85 # Vertical Tail Aspect Ratio
cr_c = 0.30 #rudder chord fraction (Raymer 6.5.3)
S_r = 120 # Rudder Area ft^2
taper_ratio_vt = 0.3 # Vertical Tail Taper Ratio
sweep_vt = 50 # Vertical Tail Sweep
n_zv = 3.0 # Vertical Tail Limit Load (estimated)
N_zv = 1.5 * n_zv # Vertical Tail Limit Load
S_vt = c_vt*b_w*S_w/L_vt #vertical tail area (Eq 6.28 Raymer)
#S_vt = 161 ft (As of )
print("Vertical Tail Area:",S_vt,"ft")
L_t = 10.78 # Tail Length
#S_vt = 145 # Vertical Tail Area [ft]
#S_vt = 66 #Vertical Tail Area (ft^2) from Assignment 5
c_t = 8.24676 #stabilator MAC (not updated)

# horizontal tail
c_ht = 0.4        # horizontal tail volume coefficient (Raymer Section 6.5.3)
L_ht = L_vt       # horizontal tail moment arm (ft)
AR_h = 3.5       # aspect ratio of horizontal stabilizer (empenage slide 54)
K_rht = 1.047 # Rolling Tail (Stabilators)
lambda_h = lambda_w +5   # Sweep angle of horizontal tail (degrees) (Raymer 4.5.4 syas add 5 degrees)
H_t = 0 # Horizontal Tail Height Above Fuselage
K_vsh = 1.0 # Non-Variable Sweep Wing
eta_h = 0.9      # difference factor between the theoretical section lift curve slope for the horizontal tail
t_t = 0.05 # tail thickness, estimated based on t/c ratios of other aircraft and the fact that the tail is thinner than the wing
print("Horizontal Tail Area:",c_ht*c_w*S_w/L_ht,"ft")
S_wet_tail = 151.715
S_ht = 173
#assignment 5 has horizontal tail area at 197.4 ft^2

#fuel volume things
rho_jp5 = 51.1              #lb/ft^3   
packing_factor_shallow_fuselage = 0.8
packing_factor_deep_fuselage = 0.85
packing_factor_wing = 0.75
V_t = 3127 # Total Fuel Volume, gal
V_i = 0.75 * V_t # Integral Fuel Tank Volume, gal
V_p = 0.25 * V_t # Self-Sealing Wing Tank Volume, gal
N_t = 10 # Number of Tanks
tank_1_v = 106 # ft^3
tank_2_v = 99.6 # ft^3
tank_34_v = 22.0 # ft^3
tank_5_v = 60.4 # ft^3
tank_6_v = 79.7 # ft^3
tank_78_v = 45.3 # ft^3
wing_tank_v = 71.0 # ft^3

# mission segment variables
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

# takeoff parameters
V_TO = 160 * 1.68781                    # takeoff speed in ft/s, assuming 160 knots for takeoff
W_TO = 54747
e_to = 0.775                            #takeoff
k_to = 1 / (np.pi * AR_w * e_to)          #takeoff
S_wingtest = 600 #based on vsp design B3.16
T_0 = 23930  # Example value for thrust per engine
T_0_mil = 13000

# climb parameters
ks = 1.2 # climb ratio (climb speed over stall speed)

# cruise parameters
ct_cruise = 0.7     # lb/(lbf hr)
v_cruise = 490      # knots
ct_cruise = 0.724 #lb/(lbf hr)
ct_AB = 1.85 #lb/(lbf hr)
M_cruise = 0.85
e_cr = 0.82                             #cruise
e_cr_estimate = 4.61*(1-0.045*AR_w**0.68)*(np.cos(lambda_w*np.pi/180)**0.15)-3.1 #Raymer equation 12.49
k_cr = 1 / (np.pi * AR_w * e_cr)          #cruise

# dash parameters
v_dash = 560        # knots 
ct_dash = 0.7       # lb/(lbf hr) for dash, assumed to be the same as cruise
M_dashSL = 0.85
M_dashSLideal= 0.9
M_dash30= 1.6
M_dash30ideal = 2.0

# maneuvering parameters
V_stall=145/1.1                         # stall speed in knots, divided by 1.1 to get a margin for climb speed
V_stall *= 1.68781                      # convert stall speed to ft/s

# Landing Parameters
s_L = 5000 # total landing distance 
s_a = 450 # ground clearance distance, taken from STOL requirements
s_L_G = 349 # carrier ground roll distance for landing, assumed to be 349 ft
F_hook = 120000
V_engage_56lb = 145 * 1.68781           # ft/s, speed at which 56 lb of thrust is required for maneuvering constraint    
V_landing= V_engage_56lb+WOD            # ft/s, landing speed, sum of engage speed and wind over deck
V_engage= 130 * 1.68781                 # ft/s, speed at which arrestor is engaged, assuming 130 knots
e_land = 0.725  
k_land = 1 / (np.pi * AR_w * e_land)      #landing# this is for declaring variables that are used across multiple files, such as the T_S_iteration.py and design_space.py files. This way, we can avoid hardcoding values in multiple places and maintain consistency across our codebase.

# functions
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

# thrust ratio at altitude
def Tratio(height):
    return atmo_vals(height)[2]/atmo_vals(0)[2] * np.sqrt(atmo_vals(0)[3]/atmo_vals(height)[3])

# weight fraction calculation function 
def calculate_weight_fraction(L_D_max, ra, E, ct_cruise, ct_dash, v_cruise, v_dash):
    """This function calculates the weight fractions for cruise and loiter/descent phases based on the Breguet range and endurance equations, and also other terms.
    Args:
        L_D_max (float): Maximum lift-to-drag ratio of the aircraft.
        ra (float): Combat range in nautical miles.
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
    # print("Total Fuel Fraction Wf/W0: {:.3f}".format(Wf_W0))

    return Wf_W0


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

def get_V_MinThrust(Weight,Altitude,wingArea,K_induced,C_D_0): #also minimum drag
    rho, a = atmo_vals(Altitude)[:2] #grabbing density and speed of sound
    V_minThrust = np.sqrt((2*Weight/(rho*wingArea))*np.sqrt(K_induced/C_D_0))
    return V_minThrust

def get_C_L_MinThrust(C_D_0,K_induced):
    return np.sqrt(C_D_0/K_induced)

def get_C_D_Min(C_D_0):
    return 2*C_D_0 #It's literally that easy

#Range Optimization (Raymer 17.2.5)
def get_C_L_bestRange(C_D_0,K_induced):
    return np.sqrt(C_D_0/(3*K_induced))

def get_V_bestRange(Weight,Altitude,wingArea,K_induced,C_D_0):
    C_L_bestRange = get_C_L_bestRange(C_D_0,K_induced)
    rho, a = atmo_vals(Altitude)[:2] #grabbing density and speed of sound
    V_minThrust = np.sqrt((2*Weight/(rho*wingArea))/C_L_bestRange)
    return V_minThrust

def get_D_bestRange(C_D_0,V_bestRange,wingArea,Altitude):
    rho, a = atmo_vals(Altitude)[:2] #grabbing density and speed of sound
    return (((1/2)*rho*V_bestRange**2)*wingArea*(C_D_0*4/3))

#Updated Fuel Fractions (From Raymer Ch 19)
def fuelFraction(t,c_t,T_A_initial,W_initial): #time in hours
    #t is time during a mission segment (assume constant T/W)
    #Break up segments into small chunks to assume constant T/W

    return 1-t*c_t*(T_A_initial/W_initial)

#This assumes that (V/C)(L/D) does not vary with weight. This is untrue
#Use V_minThrust for range
T_idle = 0.05*T_0 #idle thrust

# function dependent variables
rho_40, a_40 = atmo_vals(40000)[:2]
rho_30, a_30 = atmo_vals(30000)[:2]
rho_20, a_20 = atmo_vals(20000)[:2]
rho_10, a_10 = atmo_vals(10000)[:2]
rho_sl, a_SL = atmo_vals(0)[:2]
rho_to = 0.00224392    
rho_cruise = rho_40

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

wf_takeoff = fuelFraction(5/60,ct_cruise,2*T_0_mil,W_TO)
W_cruise_i = W_TO*wf_warmup*wf_taxi*wf_climb

def get_cruisefuelFraction(numSegments,range_nm,W_topOfClimb,altitude,S_w,k_cr,C_D_0,C_cruise):
    #range in nm
    stepDistance=range_nm/numSegments
    # print("step distance: ",stepDistance,"nm")
    weightArray=[W_topOfClimb]
    velocityArray=[]
    for step in range(numSegments):
        V_cruise_step = get_V_bestRange(weightArray[step],altitude,S_w,k_cr,C_D_0)
        time = 6076.12 * stepDistance / V_cruise_step #convert distance in nm to feet
        print("time for step",step,": ",time,"sec")
        T_req = get_D_bestRange(C_D_0,V_cruise_step,S_w,altitude)
        print("Thrust Required",T_req,"lbf")
        W_fuel_burned = T_req*(time/3600)*C_cruise #need to convert to hours since specific fuel consumption in hours
        weightArray.append(weightArray[step]-W_fuel_burned)
        velocityArray.append(V_cruise_step)
    # print("length of weightarray: ",len(weightArray))
    # print("Weight Array:        Velocity Array")
    for i in range(len(velocityArray)):
        print(weightArray[i],"lbf       ",velocityArray[i],"ft/s")

CL_bestRange = get_C_L_bestRange(CD0,k_cr)
V_bestRange = get_V_bestRange(W_cruise_i,40000,S_w,k_cr,CD0) #ft/s
get_cruisefuelFraction(2,1000,W_cruise_i,40000,S_w,k_cr,CD0,ct_cruise)

# functions
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

# thrust ratio at altitude
def Tratio(height):
    return atmo_vals(height)[2]/atmo_vals(0)[2] * np.sqrt(atmo_vals(0)[3]/atmo_vals(height)[3])

# weight fraction calculation function 
def calculate_weight_fraction(L_D_max, ra, E, ct_cruise, ct_dash, v_cruise, v_dash):
    """This function calculates the weight fractions for cruise and loiter/descent phases based on the Breguet range and endurance equations, and also other terms.
    Args:
        L_D_max (float): Maximum lift-to-drag ratio of the aircraft.
        ra (float): Combat range in nautical miles.
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
    # print("Total Fuel Fraction Wf/W0: {:.3f}".format(Wf_W0))

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

def get_V_MinThrust(Weight,Altitude,wingArea,K_induced,C_D_0): #also minimum drag
    rho, a = atmo_vals(Altitude)[:2] #grabbing density and speed of sound
    V_minThrust = np.sqrt((2*Weight/(rho*wingArea))*np.sqrt(K_induced/C_D_0))
    return V_minThrust

def get_C_L_MinThrust(C_D_0,K_induced):
    return np.sqrt(C_D_0/K_induced)

def get_C_D_Min(C_D_0):
    return 2*C_D_0 #It's literally that easy

#Range Optimization (Raymer 17.2.5)
def get_C_L_bestRange(C_D_0,K_induced):
    return np.sqrt(C_D_0/(3*K_induced))

def get_V_bestRange(Weight,Altitude,wingArea,K_induced,C_D_0):
    C_L_bestRange = get_C_L_bestRange(C_D_0,K_induced)
    rho, a = atmo_vals(Altitude)[:2] #grabbing density and speed of sound
    V_minThrust = np.sqrt((2*Weight/(rho*wingArea))/C_L_bestRange)
    return V_minThrust

def get_D_bestRange(C_D_0,V_bestRange,wingArea,Altitude):
    rho, a = atmo_vals(Altitude)[:2] #grabbing density and speed of sound
    return (((1/2)*rho*V_bestRange**2)*wingArea*(C_D_0*4/3))

#Updated Fuel Fractions (From Raymer Ch 19)
def fuelFraction(t,c_t,T_A_initial,W_initial): #time in hours
    #t is time during a mission segment (assume constant T/W)
    #Break up segments into small chunks to assume constant T/W

    return 1-t*c_t*(T_A_initial/W_initial)

#This assumes that (V/C)(L/D) does not vary with weight. This is untrue
#Use V_minThrust for range
T_idle = 0.05*T_0 #idle thrust

# function dependent variables
rho_40, a_40 = atmo_vals(40000)[:2]
rho_30, a_30 = atmo_vals(30000)[:2]
rho_20, a_20 = atmo_vals(20000)[:2]
rho_10, a_10 = atmo_vals(10000)[:2]
rho_sl, a_SL = atmo_vals(0)[:2]
rho_to = 0.00224392    
rho_cruise = rho_40

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

wf_takeoff = fuelFraction(5/60,ct_cruise,2*T_0_mil,W_TO)
W_cruise_i = W_TO*wf_warmup*wf_taxi*wf_climb

def get_cruisefuelFraction(numSegments,range_nm,W_topOfClimb,altitude,S_w,k_cr,C_D_0,C_cruise):
    #range in nm
    stepDistance=range_nm/numSegments
    # print("step distance: ",stepDistance,"nm")
    weightArray=[W_topOfClimb]
    velocityArray=[]
    for step in range(numSegments):
        V_cruise_step = get_V_bestRange(weightArray[step],altitude,S_w,k_cr,C_D_0)
        time = 6076.12 * stepDistance / V_cruise_step #convert distance in nm to feet
        # print("time for step",step,": ",time,"sec")
        T_req = get_D_bestRange(C_D_0,V_cruise_step,S_w,altitude)
        # print("Thrust Required",T_req,"lbf")
        W_fuel_burned = T_req*(time/3600)*C_cruise #need to convert to hours since specific fuel consumption in hours
        weightArray.append(weightArray[step]-W_fuel_burned)
        velocityArray.append(V_cruise_step)
    # print("length of weightarray: ",len(weightArray))
    # print("Weight Array:        Velocity Array")
    for i in range(len(velocityArray)):
        # print(weightArray[i],"lbf       ",velocityArray[i],"ft/s")
        pass

CL_bestRange = get_C_L_bestRange(CD0,k_cr)
V_bestRange = get_V_bestRange(W_cruise_i,40000,S_w,k_cr,CD0) #ft/s
get_cruisefuelFraction(2,1000,W_cruise_i,40000,S_w,k_cr,CD0,ct_cruise)