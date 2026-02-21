# the goal of this code is to replicate the T_S_iteration code we have been using but with the 
# integration of the code variables file to ensure unit consistency and to avoid hardcoding values across multiple files.
# This will allow us to maintain a more organized and efficient codebase while performing the same calculations for the T-S iteration process.

import numpy as np
import matplotlib.pyplot as plt
import design_space as ds
import code_variables as cv
import constraint_coeff as cc

##---configurations------
# Adjust C_Lmax for each flight configuration
cL_clean = np.linspace(-0.9,0.9,100)
cL_takeoff = np.linspace(-2,2,100)
cL_landing = np.linspace(-2.6,2.6,100)

#calculating zero lift drag coefficent
C_D_0=cv.calculate_zero_lift_drag_coefficient(cv.c_f, ds.S_wet, cv.S_ref)

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
        #print("TOGW Guess: "+str(TOGW_guess)+"\nS_wing: "+str(S_wing)+"\nT_0: " + str(T_0))
        # 1) fuel fraction (could be constant or updated)
        Wf_W0 = cv.calculate_weight_fraction(cv.L_D_max, cv.R, cv.E, cv.ct_cruise, cv.ct_dash, cv.v_cruise, cv.v_dash)
        W_fuel = Wf_W0 * TOGW_guess

        # 2) empty weight based on current TOGW guess + geometry + thrust
        W_empty = cv.calculate_empty_weight(
            S_wing, S_ht, S_vt, S_wet_fuselage,
            TOGW_guess, T_0, num_engines)

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

TOGW_guess = 55000  # Initial guess for Takeoff Gross Weight in pounds
final_TOGW, converged, iterations, W0_history = inner_loop_weight(
    TOGW_guess, cv.S_wingtest, cv.S_ht, cv.S_vt, cv.S_wet_fuselage,
    cv.num_engines, cv.W_crew, cv.W_payload, cv.T_0)

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
#DO NOT PUT LANDING AND TAKEOFF HERE
def outer_loop_thrust_for_one_constraint(
    S_wing_grid,
    TOGW_guess_init,
    T_total_guess_init,      # total thrust guess (all engines), lbf
    num_engines,
    S_ht, S_vt, S_wet_fuselage,
    W_crew, W_payload,
    TWfunc,
    tol_T_rel=1e-3,          
    max_iter_T=50,
    relax=1.0                # optional damping: 0.3~1.0 (use <1 if oscillation)
):
    
    T_total_converged = []
    W0_converged = []
    iter_counts = []
    T_total_history_allS = []  # list of arrays (one per S)

    for S_wing in S_wing_grid:

        T_total = T_total_guess_init
        T_hist = []

        for k in range(max_iter_T):
            # Convert total thrust to per-engine thrust for the weight model
            T_0 = T_total / num_engines

            #get the weight (W0(S_wing))
            W0, wconv, it_w, W0_hist = inner_loop_weight(
                TOGW_guess_init, S_wing, S_ht, S_vt, S_wet_fuselage,
                num_engines, W_crew, W_payload, T_0)

            #computer W0/S0
            WS = W0 / S_wing

            #find TW
            TW_req = TWfunc(WS)

            #Required total thrust
            T_req = TW_req * W0

            # Store history
            T_hist.append(T_total)

            # Check outer convergence
            if abs(T_req - T_total) / max(abs(T_total), 1e-9) < tol_T_rel:
                T_total = T_req
                break

            #update thrust to converge
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


#anthony is an idiot!!!

#Takes thrust array and outputs S array
#ONLY TAKEOFF AND LANDING
#DONT YOU DARE PUT ANYTHING ELSE IN THIS SACRED FUNCTION
def outer_loop_W_S_curves(
            Thrust_array,               #similar to other outer loop for S
            TOGW_guess_init,
            S_wing_guess_init,          #Honestly just take a swing at it
            S_ht, 
            S_vt, 
            S_wet_fuselage,
            num_engines, 
            W_crew, 
            W_payload,
            W_S_function):
    tol_T_rel=1e-3          
    max_iter_T=10 #change this so its higher
    T_grid = []         #Storing final Thrust values
    S_hist = [] # iteration history
    wing_array = []

    for i in range(0,len(Thrust_array)): #basically just a linspace of possible thrust values


        T_0 = Thrust_array[i] #Take thrust value from the array
        #S_hist_landing.append(S_wing_guess_landing)
        #S_hist_takeoff.append(S_wing_guess_takeoff)
        T_grid.append(T_0)
        
        S_hist.append(S_wing_guess_init)

        for k in range(max_iter_T):
            W0_constraint, wconv, it_w, W0_hist = inner_loop_weight(
            TOGW_guess_init, S_wing_guess_init, S_ht, S_vt, S_wet_fuselage,
            num_engines, W_crew, W_payload, T_0)

            W_S_constraint = W_S_function

            S_wing_guess = W0_constraint/W_S_constraint

            if abs(S_wing_guess - S_hist[i])/abs(S_hist[i]) < tol_T_rel:
                break

        wing_array.append(S_wing_guess)
    
    return(T_grid,wing_array)

# Set grid of wing areas to analyze
S_wing_grid = list(range(100, 3000, 2))    # Example range of wing areas to analyze
# Set grid of thrust values to analyze
T_engine_grid = list(range(0,250000,1000))     # used for the W/S driven constraint plots

TOGW_guess_init = 55000  # Initial guess for Takeoff Gross Weight in pounds
T_total_guess_init = 24000 * cv.num_engines  # Initial guess for total thrust in pounds-force

S_wing_guess=900

T_grid,S_W_S_array=outer_loop_W_S_curves(T_engine_grid,TOGW_guess_init,S_wing_guess,cv.S_ht,cv.S_vt,cv.S_wet_fuselage,cv.num_engines,cv.W_crew,cv.W_payload)

T_total_curve, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=cv.num_engines,
    S_ht=cv.S_ht, S_vt=cv.S_vt, S_wet_fuselage=cv.S_wet_fuselage,
    W_crew=cv.W_crew, W_payload=cv.W_payload,
    coef_1_cruise_constraint=cc.coef_1_cruise_constraint,
    coef_2_cruise_constraint=cc.coef_2_cruise_constraint,
    tol_T_rel=1e-6,
    max_iter_T=200,
    relax=1
)


print("\nStarting Inner Loop Weight Calcs for aircraft\n")


#cruise constraint
T_cruise, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=cv.num_engines,
    S_ht=cv.S_ht, S_vt=cv.S_vt, S_wet_fuselage=cv.S_wet_fuselage,
    W_crew=cv.W_crew, W_payload=cv.W_payload,
    TWfunc= ds.tw_cruise, 
    tol_T_rel=1e-6,
    max_iter_T=200,
    relax=1)

#SL dash constraint
T_SLdash, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=cv.num_engines,
    S_ht=cv.S_ht, S_vt=cv.S_vt, S_wet_fuselage=cv.S_wet_fuselage,
    W_crew=cv.W_crew, W_payload=cv.W_payload,
    TWfunc= ds.tw_SLdash, 
    tol_T_rel=1e-6,
    max_iter_T=200,
    relax=1)

#SL dash ideal
T_SLdashideal, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=cv.num_engines,
    S_ht=cv.S_ht, S_vt=cv.S_vt, S_wet_fuselage=cv.S_wet_fuselage,
    W_crew=cv.W_crew, W_payload=cv.W_payload,
    TWfunc= ds.tw_SLdashideal, 
    tol_T_rel=1e-6,
    max_iter_T=200,
    relax=1)

#30k ft dash
T_30dash, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=cv.num_engines,
    S_ht=cv.S_ht, S_vt=cv.S_vt, S_wet_fuselage=cv.S_wet_fuselage,
    W_crew=cv.W_crew, W_payload=cv.W_payload,
    TWfunc= ds.tw_30dash, 
    tol_T_rel=1e-6,
    max_iter_T=200,
    relax=1)

#30k ft dash Ideal
T_30dashideal, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=cv.num_engines,
    S_ht=cv.S_ht, S_vt=cv.S_vt, S_wet_fuselage=cv.S_wet_fuselage,
    W_crew=cv.W_crew, W_payload=cv.W_payload,
    TWfunc= ds.tw_30dashideal, 
    tol_T_rel=1e-6,
    max_iter_T=200,
    relax=1)

#maneuver
T_maneuver, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=cv.num_engines,
    S_ht=cv.S_ht, S_vt=cv.S_vt, S_wet_fuselage=cv.S_wet_fuselage,
    W_crew=cv.W_crew, W_payload=cv.W_payload,
    TWfunc= ds.tw_maneuver, 
    tol_T_rel=1e-6,
    max_iter_T=200,
    relax=1)

#maneuver
T_maneuverideal, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=cv.num_engines,
    S_ht=cv.S_ht, S_vt=cv.S_vt, S_wet_fuselage=cv.S_wet_fuselage,
    W_crew=cv.W_crew, W_payload=cv.W_payload,
    TWfunc= ds.tw_maneuverideal, 
    tol_T_rel=1e-6,
    max_iter_T=200,
    relax=1)

#ceiling
T_ceiling, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=cv.num_engines,
    S_ht=cv.S_ht, S_vt=cv.S_vt, S_wet_fuselage=cv.S_wet_fuselage,
    W_crew=cv.W_crew, W_payload=cv.W_payload,
    TWfunc= ds.tw_ceiling, 
    tol_T_rel=1e-6,
    max_iter_T=200,
    relax=1)

#SEROC climb
T_climb, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=cv.num_engines,
    S_ht=cv.S_ht, S_vt=cv.S_vt, S_wet_fuselage=cv.S_wet_fuselage,
    W_crew=cv.W_crew, W_payload=cv.W_payload,
    TWfunc= ds.tw_climb, 
    tol_T_rel=1e-6,
    max_iter_T=500,
    relax=0.2)

engine_array = T_engine_grid
S_wing_guess_init = S_wing_guess

# T_grid, wing_takeoff_array, wing_landing_array = outer_loop_W_S_curves(
    # engine_array,               #similar to other outer loop for S
    # TOGW_guess_init,
    # S_wing_guess_init,          #Honestly just take a swing at it
    # cv.S_ht, 
    # cv.S_vt, 
    # cv.S_wet_fuselage,
    # cv.num_engines, 
    # cv.W_crew, 
    # cv.W_payload)


# T_grid,S_W_S_array_takeoff,S_W_S_array_landing=outer_loop_W_S_curves(T_engine_grid,TOGW_guess_init,S_wing_guess,cv.S_ht,cv.S_vt,cv.S_wet_fuselage,cv.num_engines,cv.W_crew,cv.W_payload)

# T_grid,S_W_S_array_takeoff=outer_loop_W_S_curves(T_engine_grid,TOGW_guess_init,S_wing_guess,cv.S_ht,cv.S_vt,cv.S_wet_fuselage,cv.num_engines,cv.W_crew,cv.W_payload,ds.W_S_takeoff)

# T_grid,S_W_S_array_landing=outer_loop_W_S_curves(T_engine_grid,TOGW_guess_init,S_wing_guess,cv.S_ht,cv.S_vt,cv.S_wet_fuselage,cv.num_engines,cv.W_crew,cv.W_payload,ds.W_S_landing56lb)

# T_grid,S_W_S_array_stall=outer_loop_W_S_curves(T_engine_grid,TOGW_guess_init,S_wing_guess,cv.S_ht,cv.S_vt,cv.S_wet_fuselage,cv.num_engines,cv.W_crew,cv.W_payload,ds.W_S_stall)





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

# Create mesh
S_mesh, T_mesh = np.meshgrid(S_main, np.linspace(0, T_top, 400))

# Interpolate landing S requirement at each T (left boundary)
S_landing_required = np.interp(T_mesh, T_land_sorted, S_land_sorted)

# Interpolate 30k dash ideal S at each T (right boundary)
S_30_required = np.interp(T_mesh, T_30_sorted, S_30_sorted)

# Mask: above maneuver, right of landing, left of 30k dash ideal
mask = (
    (T_mesh >= np.interp(S_mesh, S_main, T_lower_curve)) &  # above maneuver
    (S_mesh >= S_landing_required) &                        # right of landing
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
#plt.plot(S_wing_grid, T_climb, label='SEROC')
plt.legend(loc='upper right')
plt.ylim(0,100000)
plt.grid()
plt.show()