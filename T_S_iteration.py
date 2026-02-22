import numpy as np
import matplotlib.pyplot as plt
import design_space
import constraint_coeff


#change to our numbers
AR = 2.06
s = 46 
s_ref = 955

#drag polar (change to our numbers)
S_wet = 2500
c_f = 0.0026
def calculate_zero_lift_drag_coefficient(c_f, S_wet, s_ref):
    return c_f * (S_wet / s_ref)

#C_D_0 = calculate_zero_lift_drag_coefficient(c_f, S_wet, s_ref)
C_D_0 = 0.01166
print("Zero-lift drag coefficient C_D_0:", C_D_0)

##---configurations------
# Adjust C_Lmax for each flight configuration
cL_clean = np.linspace(-0.9,0.9,100)
cL_takeoff = np.linspace(-2,2,100)
cL_landing = np.linspace(-2.6,2.6,100)

# Clean configuration
#def calculate_induced_drag_coefficient(AR, e):
#    return 1/(np.pi*AR*e)
#e_clean = 0.820
#coef_clean = calculate_induced_drag_coefficient(AR, e_clean)
#print("Induced drag coefficient for clean configuration:", coef_clean)
#clean = C_D_0 + coef_clean*cL_clean*cL_clean

# Takeoff configuration
#e_takeoff = 0.75
#delta_CD0_takeoff = 0.01 # additional drag due to takeoff flaps
#coef_takeoff = calculate_induced_drag_coefficient(AR, e_takeoff)
#print("Induced drag coefficient for takeoff configuration:", coef_takeoff)
#takeoff = C_D_0 + delta_CD0_takeoff + coef_takeoff*cL_takeoff*cL_takeoff 

# Landing configuration
#e_landing = 0.7
#delta_CD0_landing = 0.055 # additional drag due to landing flaps and gear
#coef_landing = calculate_induced_drag_coefficient(AR, e_landing)
#print("Induced drag coefficient for landing configuration:", coef_landing)
#landing_flaps = C_D_0 + delta_CD0_landing + coef_landing*cL_landing*cL_landing

# Additional drag due to landing gear only
#e_gear = e_clean # Assuming landing gear does not affect the efficiency factor
#delta_CD0_gear = 0.015 # additional drag due to landing gear
#coef_gear = calculate_induced_drag_coefficient(AR, e_gear)
#landing_gear = C_D_0 + delta_CD0_gear + coef_gear*cL_landing*cL_landing


#plt.figure(figsize=(16,9))
#plt.title('Drag Polars')
#plt.xlabel("$C_D$")
#plt.ylabel("$C_L$")
#plt.plot(clean, cL_clean, label='Clean', linestyle='-', linewidth=2)
#plt.plot(takeoff, cL_takeoff, label='w. Takeoff flaps', linestyle='-', linewidth=2)
#plt.plot(landing_flaps, cL_landing, label='w. Landing flaps', linestyle='-', linewidth=2)
#plt.plot(landing_gear, cL_landing, label='w. Landing gear', linestyle='-', linewidth=2)
#plt.legend(loc='best')
#plt.show()


##----T/W and W/S Diagram-----
#
#
#
#



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
print("W_payload: " + str(W_payload) + " lb")


##----Inner loop-----
def calculate_engine_weight(T_0):
    W_eng_dry = 0.521 * T_0**0.9
    W_eng_oil = 0.082 * T_0**0.65
    W_eng_rev = 0.034 * T_0
    W_eng_control = 0.26 * T_0**0.5
    W_eng_start = 9.33 * (W_eng_dry/1000) ** 1.078
    W_eng = W_eng_dry + W_eng_oil + W_eng_rev + W_eng_control + W_eng_start
    W_eng = 3826 # actual F100 weight (from https://www.rtx.com/en/prattwhitney/products/military-engines/f100)
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

#Algorithm 3 in Metabook
def calculate_weight_fraction(L_D_max, R, E, ct_cruise, ct_dash, v_cruise, v_dash):
    """This function calculates the weight fractions for cruise and loiter/descent phases based on the Breguet range and endurance equations, and also other terms.
    Args:
        L_D_max (float): Maximum lift-to-drag ratio of the aircraft.
        R (float): Combat range in nautical miles.
        E (float): Endurance in hours.
        ct (float): Specific fuel consumption in lb/(lbf hr).
        V (float): Velocity in knots."""
    
    L_D = 0.94 * L_D_max
    warmup = 0.99
    taxi = 0.99
    takeoff = 0.99
    climb = 0.96 
    dash_ingress = np.exp((-50*ct_dash) / (v_dash*L_D))
    dash_egress = dash_ingress
    descent = 0.99
    midmission_descent = 0.995
    midmission_climb = 0.98
    landing = 0.995
    cruise = np.exp((-R*ct_cruise) / (v_cruise*L_D))
    loiter = np.exp((-E*ct_cruise) / (L_D))

    weight_fraction = warmup*taxi*takeoff*climb*cruise*midmission_descent*dash_ingress*dash_egress*midmission_climb*cruise*descent*loiter*landing 

    Wf_W0 = (1 - weight_fraction) * 1.06    # compute fuel fraction
    print("Total Fuel Fraction Wf/W0: {:.3f}".format(Wf_W0))

    return Wf_W0

#Algorithm 2 in Metabook 
def inner_loop_weight(TOGW_guess, S_wing, S_ht, S_vt, S_wet_fuselage,
    num_engines, w_crew, w_payload, T_0, err=1e-6, max_iter=200):
    
    W0_history = []
    delta = np.inf
    it = 0

    while delta > err and it < max_iter:
        # 1) fuel fraction (could be constant or updated)
        Wf_W0 = calculate_weight_fraction(L_D_max, R, E, ct_cruise, ct_dash, v_cruise, v_dash)
        W_fuel = Wf_W0 * TOGW_guess

        # 2) empty weight based on current TOGW guess + geometry + thrust
        W_empty = calculate_empty_weight(
            S_wing, S_ht, S_vt, S_wet_fuselage,
            TOGW_guess, T_0, num_engines)
        print(f"Empty Weight: {W_empty} lbs")

        # 3) new gross weight
        W0_new = W_empty + w_crew + w_payload + W_fuel
        W0_history.append(W0_new)

        # 4) convergence check
        delta = abs(W0_new - TOGW_guess) / max(abs(W0_new), 1e-9)

        # 5) update
        TOGW_guess = W0_new
        it += 1

    converged = (delta <= err)
    return TOGW_guess, converged, it, np.array(W0_history)

# Fixed parameters for weight estimation
L_D_max = 10
R = 950            # nmi
E = 20 / 60         # min --> hr
ct_cruise = 0.7     # lb/(lbf hr)
ct_dash = 0.7
v_cruise = 490      # knots
v_dash = 560        # knots
S_ht = 0
S_vt = 45
S_wet_fuselage = 700
num_engines = 2  # Example number of engines

# The value we can adjust by the constraint curve. For example, if we want to be on the takeoff constraint curve, we can find the corresponding W/S and then calculate the TOGW based on that W/S and the wing area.
S_wing = 946 #based on vsp design v5
T_0 = 23930  # Example value for thrust per engine

TOGW_guess = 55000  # Initial guess for Takeoff Gross Weight in pounds
final_TOGW, converged, iterations, W0_history = inner_loop_weight(
    TOGW_guess, S_wing, S_ht, S_vt, S_wet_fuselage,
    num_engines, W_crew, W_payload, T_0)

# plot the convergence history
plt.figure(figsize=(10,6))
plt.plot(W0_history, marker='o')
plt.title('Convergence of TOGW Estimate')
plt.xlabel('Iteration')
plt.ylabel('Estimated TOGW (lb)')
plt.grid()
plt.show()
print("Final estimated TOGW:", final_TOGW, "lb")


##---outer loop---
#T/W stuff ONLY
#DO NOT FUCKING PUT LANDING AND TAKEOFF HERE
def outer_loop_thrust_for_one_constraint(
    S_wing_grid,
    TOGW_guess_init,
    T_total_guess_init,      # total thrust guess (all engines), lbf
    num_engines,
    S_ht, S_vt, S_wet_fuselage,
    W_crew, W_payload,
    coef_1_cruise_constraint, coef_2_cruise_constraint,
    tol_T_rel=1e-3,          
    max_iter_T=50,
    relax=1.0                # optional damping: 0.3~1.0 (use <1 if oscillation)
):
    
    T_total_converged = []
    W0_converged = []
    iter_counts = []
    T_total_history_allS = []  # list of arrays (one per S)

    for S_wing in S_wing_grid:

        # Initialize outer loop for this S
        T_total = T_total_guess_init
        T_hist = []

        for k in range(max_iter_T):
            # Convert total thrust to per-engine thrust for the weight model
            T_0 = T_total / num_engines

            # Inner loop: converge weight for (S, T_0)
            W0, wconv, it_w, W0_hist = inner_loop_weight(
                TOGW_guess_init,
                S_wing, S_ht, S_vt, S_wet_fuselage,
                num_engines, W_crew, W_payload, T_0
            )

            # Wing loading from converged weight
            WS = W0 / S_wing

            # Constraint: compute required T/W from W/S
            # For cruise as example:
            TW_req = coef_1_cruise_constraint/WS + coef_2_cruise_constraint*WS
            # For takeoff as example:
            # TW_req = coef_takeoff_constraint*WS

            # Required total thrust
            T_req = TW_req * W0

            # Store history
            T_hist.append(T_total)

            # Check outer convergence
            if abs(T_req - T_total) / max(abs(T_total), 1e-9) < tol_T_rel:
                T_total = T_req
                break

            # Update thrust (optionally relaxed damping)
            T_total = (1 - relax) * T_total + relax * T_req

        # Save results for this S
        T_total_converged.append(T_total)
        W0_converged.append(W0)
        iter_counts.append(k+1)
        T_total_history_allS.append(np.array(T_hist))

    return (np.array(T_total_converged),
            np.array(W0_converged),
            np.array(iter_counts),
            T_total_history_allS,
            W0, wconv, it_w, W0_hist)

#anthony is an idiot

#Takes thrust array and outputs S array
#ONLY TAKEOFF AND LANDING
#DONT YOU DARE PUT ANYTHING ELSE IN THIS SACRED FUNCTION
def outer_loop_W_S_curves(
            engine_array,               #similar to other outer loop for S
            TOGW_guess_init,
            S_wing_guess_init,          #Honestly just take a swing at it
            S_ht, 
            S_vt, 
            S_wet_fuselage,
            num_engines, 
            W_crew, 
            W_payload,
            FieldLength = 349
):
    tol_T_rel=1e-3,          
    max_iter_T=50
    S_wing_grid = []    #Storing final S Values
    T_grid = []         #Storing final Thrust values
    S_wing_guess=S_wing_guess_init #give us a starting value
    S_hist = []         #Shows iteration history
    

    for i in range(0,len(engine_array)): #basically just a linspace of possible thrust values
        T_0 = engine_array[i] #Take thrust value from the array
        S_hist.append(S_wing_guess)
        T_grid.append(T_0)
        
        for k in range(max_iter_T):

            #compute TOGW using inner loop code
            W0, wconv, it_w, W0_hist = inner_loop_weight(
                TOGW_guess_init, S_wing_guess_init, S_ht, S_vt, S_wet_fuselage,
                num_engines, W_crew, W_payload, T_0
            )

            #add constraint inputs here



            #constraint inputs to get (W_0/S)
            W_S_constraint = design_space.W_S_takeoff #constraint input


            S_wing_guess = W0/(W_S_constraint)
            if abs(S_wing_guess - S_hist[i])/abs(S_hist[i]) < tol_T_rel:
                break
            
        #now we have a converged S value for the thrust value from the array
        S_wing_grid.append(S_wing_guess)
        
    
    return(T_grid,S_wing_grid)

    c1_ceil, c2_ceil = calculate_ceiling_constraint_coefficient(rho, V_fps, C_D_0, AR, e_clean)
    print(f"Ceiling Constraints - Coef1: {c1_ceil:.4f}, Coef2: {c2_ceil:.6f}")

    TW_req_ceiling = (c1_ceil / WS_val) + (c2_ceil * WS_val) + G
    T_req_ceiling = TW_req_ceiling * W0
# Fixed parameters for weight estimation
L_D_max = 9
R = 1000            # nmi
E = 30 / 60         # min --> hr
c = 0.52            # lb/(lbf hr)
V = 291 * 1.94      # m/s --> knots
S_ht = 0
S_vt = 74
S_wet_fuselage = 700
num_engines = 2  # Example number of engines

# Set grid of wing areas to analyze
S_wing_grid = list(range(3000, 6000, 2))    # Example range of wing areas to analyze
# Set grid of thrust values to analyze
T_engine_grid = list(range(0,100000,10000))     # used for the W/S driven constraint plots


TOGW_guess_init = 55000  # Initial guess for Takeoff Gross Weight in pounds
T_total_guess_init = 24000 * num_engines  # Initial guess for total thrust in pounds-force

S_wing_guess=900

T_grid,S_W_S_array=outer_loop_W_S_curves(T_engine_grid,TOGW_guess_init,S_wing_guess,S_ht,S_vt,S_wet_fuselage,num_engines,W_crew,W_payload)

T_total_curve, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=num_engines,
    S_ht=S_ht, S_vt=S_vt, S_wet_fuselage=S_wet_fuselage,
    W_crew=W_crew, W_payload=W_payload,
    coef_1_cruise_constraint=constraint_coeff.coef_1_cruise_constraint,
    coef_2_cruise_constraint=constraint_coeff.coef_2_cruise_constraint,
    tol_T_rel=1e-6,
    max_iter_T=200,
    relax=1
)




# plot the convergence history
plt.figure(figsize=(10,6))
plt.plot(S_W_S_array,T_grid, marker='o')
plt.xlim(0, len(S_W_S_array))
plt.title('T_S Curve from W_S Curve ')
plt.xlabel('S (ft^2)')
plt.ylabel('T (lbf)')
plt.grid()
plt.show()

##---plot---
# Plot the resulting T vs S curve from the outer loop convergence

plt.figure(figsize=(16,9))
plt.title('Converged T vs S for Cruise Constraint')
plt.xlabel("Wing Area S (ft^2)")
plt.ylabel("Total Thrust T (lbf)")
plt.plot(S_wing_grid, T_total_curve, label='Converged T for Cruise Constraint', marker='o')
plt.legend(loc='best')
plt.grid()
plt.show()


#Comparable Aircraft T/S
T_J39C_dry=12000 #lbf
T_J39C_wet=18000 #lbf
S_J39C=320 #ft^2

T_Su33_dry=33400 #lbf
T_Su33_wet=56400 #lbf
S_Su33=730 #ft^2

#I didnt find dry thrust numbers for Su-34
T_Su34_wet=60000 #lbf
S_Su34=667.8 #ft^2

T_Typhoon_dry=27000 #lbf
T_Typhoon_wet=40400 #lbf
S_Typhoon=551.1 #ft^2

T_Rafale_M_dry=22500 #lbf
T_Rafale_M_wet=34000 #lbf
S_Rafale_M=492 #ft^2

T_F18_E_dry=26000 #lbf
T_F18_E_wet=44000 #lbf

S_F18_E_M=500 #ft^2


plt.figure(figsize=(16,9))
plt.title('Converged T vs S for Cruise Constraint')
plt.xlabel("Wing Area S (ft^2)")
plt.ylabel("Total Thrust T (lbf)")
plt.plot(S_wing_grid, T_cruise, label='Cruise')
plt.plot(S_wing_grid, T_SLdash, label='SL Dash')
plt.plot(S_wing_grid, T_SLdashideal, label='Ideal SL Dash')
plt.plot(S_wing_grid, T_30dash, label='30k ft Dash')
plt.plot(S_wing_grid, T_30dashideal, label='Ideal 30k ft Dash')
plt.plot(S_wing_grid, T_maneuver, label='Maneuver')
plt.plot(S_wing_grid, T_maneuverideal, label='Ideal Maneuver')
plt.plot(S_wing_grid, T_ceiling, label='Ceiling (50k ft)')
plt.plot(S_wing_grid, T_climb, label='SEROC Climb')
plt.plot(S_W_S_array_takeoff, T_grid, label = 'Takeoff')
plt.plot(S_W_S_array_landing, T_grid, label = 'Landing')
plt.plot(S_W_S_array_stall, T_grid, label = 'Stall')

S_main = np.array(S_wing_grid)
T_top = 100000
T_lower_curve = np.array(T_maneuverideal)

# Sort landing data
idx = np.argsort(T_grid)
T_land_sorted = np.array(T_grid)[idx]
S_land_sorted = np.array(S_W_S_array_landing)[idx]

# Sort 30k dash ideal data
idx30 = np.argsort(T_30dashideal)
T_30_sorted = np.array(T_30dashideal)[idx30]
S_30_sorted = np.array(S_main)[idx30]

# Sort stall data
idx_stall = np.argsort(T_grid)
T_stall_sorted = np.array(T_grid)[idx_stall]
S_stall_sorted = np.array(S_W_S_array_stall)[idx_stall]

# Create mesh
S_mesh, T_mesh = np.meshgrid(S_main, np.linspace(0, T_top, 400))

# Interpolate landing S requirement at each T (left boundary)
S_landing_required = np.interp(T_mesh, T_land_sorted, S_land_sorted)

#interpolate stall S req
S_stall_required = np.interp(T_mesh, T_stall_sorted, S_stall_sorted)

# Interpolate 30k dash ideal S at each T (right boundary)
S_30_required = np.interp(T_mesh, T_30_sorted, S_30_sorted)

# Mask: above maneuver, right of landing, left of 30k dash ideal
mask = (
    (T_mesh >= np.interp(S_mesh, S_main, T_lower_curve)) &  # above maneuver
    (S_mesh >= np.maximum(S_landing_required, S_stall_required)) &  
    (S_mesh <= S_30_required)                               # left of 30k dash ideal
)



# Shade
plt.contourf(
    S_mesh,
    T_mesh,
    mask,
    levels=[0.5, 1],
    alpha=0.25,
    colors=['yellow']
)

#comparable aircraft points
aircraft_points = [
    (S_J39C, T_J39C_wet, "J39C"),
    (S_Su33, T_Su33_wet, "Su-33"),
    (S_Su34, T_Su34_wet, "Su-34"),
    (S_Typhoon, T_Typhoon_wet, "Typhoon"),
    (S_Rafale_M, T_Rafale_M_wet, "Rafale M"),
    (S_F18_E_M, T_F18_E_wet, "F/A-18E"),]
#plots and lables comparable aircraft
for S, T, name in aircraft_points:
    plt.plot(S, T, marker='^', markersize=5, color='black')
    plt.annotate(name, (S, T), xytext=(5,5), textcoords='offset points')


# Plot our aircraft point
f_100_thrust = 23930 
S_ZALKAS = 950 #ft^2
T_ZALKAS = f_100_thrust * num_engines
plt.plot(S_ZALKAS, T_ZALKAS, marker='*', color='gold', markersize=15,  markeredgecolor='black', zorder=5)
plt.annotate('ZALKAS Fighter', (S_ZALKAS, T_ZALKAS), xytext=(5,5), textcoords='offset points')

plt.legend(loc='upper right')
plt.ylim(0,100000)
plt.grid()
plt.show()

# print("Takeoff Array Length: "+ str(len(S_W_S_array_takeoff))+"\nTakeoff Array: " + str(S_W_S_array_takeoff))
# print("Landing Array Length: "+ str(len(S_W_S_array_landing))+"\nLanding Array: " + str(S_W_S_array_landing))

# #plot the convergence history
# plt.figure(figsize=(10,6))
# plt.plot(S_W_S_array_takeoff,T_grid, marker='o', color='orange')
# plt.plot(S_W_S_array_landing,T_grid, marker='x',color='blue')
# plt.title('T_S Curve from W_S Curve ')
# plt.xlabel('S (ft^2)')
# plt.ylabel('T (lbf)')
# plt.grid()
# plt.show()
