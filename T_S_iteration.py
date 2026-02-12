import numpy as np
import matplotlib.pyplot as plt

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
def calculate_induced_drag_coefficient(AR, e):
    return 1/(np.pi*AR*e)
e_clean = 0.820
coef_clean = calculate_induced_drag_coefficient(AR, e_clean)
print("Induced drag coefficient for clean configuration:", coef_clean)
clean = C_D_0 + coef_clean*cL_clean*cL_clean

# Takeoff configuration
e_takeoff = 0.75
delta_CD0_takeoff = 0.01 # additional drag due to takeoff flaps
coef_takeoff = calculate_induced_drag_coefficient(AR, e_takeoff)
print("Induced drag coefficient for takeoff configuration:", coef_takeoff)
takeoff = C_D_0 + delta_CD0_takeoff + coef_takeoff*cL_takeoff*cL_takeoff 

# Landing configuration
e_landing = 0.7
delta_CD0_landing = 0.055 # additional drag due to landing flaps and gear
coef_landing = calculate_induced_drag_coefficient(AR, e_landing)
print("Induced drag coefficient for landing configuration:", coef_landing)
landing_flaps = C_D_0 + delta_CD0_landing + coef_landing*cL_landing*cL_landing

# Additional drag due to landing gear only
e_gear = e_clean # Assuming landing gear does not affect the efficiency factor
delta_CD0_gear = 0.015 # additional drag due to landing gear
coef_gear = calculate_induced_drag_coefficient(AR, e_gear)
landing_gear = C_D_0 + delta_CD0_gear + coef_gear*cL_landing*cL_landing


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
W_payload = 2500     #lb

W_crew = num_pilot * (avg_wt_person)
print("W_crew: " + str(W_crew) + " lb")

W_payload = W_crew + W_payload
print("W_payload: " + str(W_payload) + " lb")



##----Inner loop-----
def calculate_engine_weight(T_0):
    """Calculate the single engine weight based on the given thrust using empirical relationships.
    Args:
        T_0 (float): Thrust in pounds-force (lbf).
    Returns:
        float: Estimated engine weight in pounds (lb).
    """
    W_eng_dry = 0.521 * T_0**0.9
    W_eng_oil = 0.082 * T_0**0.65
    W_eng_rev = 0.034 * T_0
    W_eng_control = 0.26 * T_0**0.5
    W_eng_start = 9.33 * (W_eng_dry/1000) ** 1.078
    W_eng = W_eng_dry + W_eng_oil + W_eng_rev + W_eng_control + W_eng_start
    return W_eng

def calculate_empty_weight(S_wing, S_ht, S_vt, S_wet_fuselage, TOGW, T_0 , num_engines):
    W_wing = S_wing * 10
    W_ht = S_ht * 5.5
    W_vt = S_vt * 5.5
    W_fuselage = S_wet_fuselage * 5
    W_landing_gear = 0.043 * TOGW
    Engine_weight = calculate_engine_weight(T_0)
    W_engines = Engine_weight * num_engines * 1.3
    W_all_else = 0.17 * TOGW
    W_empty = W_wing + W_ht + W_vt + W_fuselage + W_landing_gear + W_engines + W_all_else
    return W_empty

def calculate_weight_fraction(L_D_max, R, E, c, V):
    """This function calculates the weight fractions for cruise and loiter/descent phases based on the Breguet range and endurance equations, and also other terms.
    Args:
        L_D_max (float): Maximum lift-to-drag ratio of the aircraft.
        R (float): Range in nautical miles.
        E (float): Endurance in hours.
        c (float): Specific fuel consumption in lb/(lbf hr).
        V (float): Velocity in knots."""
    
    L_D = 0.94 * L_D_max

    W3_W2 = np.exp((-R*c) / (V*L_D))  # cruise
    # print("Cruise Fuel Fraction (W3/W2): " + str(round(W3_W2, 3)))

    W4_W3 = np.exp((-E*c) / (L_D))    # loiter/descent
    # print("Loiter Fuel Fraction (W4/W3): " + str(round(W4_W3, 3)))

    W1_W0 = 0.970   # engine start & takeoff
    W2_W1 = 0.985   # climb
    W5_W4 = 0.995   # landing

    W5_W0 = W5_W4 * W4_W3 * W3_W2 * W2_W1 * W1_W0
    # print("Final Fuel Fraction (W5/W0): " + str(round(W5_W0, 3)))

    Wf_W0 = (1 - W5_W0) * 1.06    # compute fuel fraction
    # print("Total Fuel Fraction Wf/W0: {:.3f}".format(Wf_W0))

    return Wf_W0


def inner_loop_weight(
    TOGW_guess,
    S_wing, S_ht, S_vt, S_wet_fuselage,
    num_engines, w_crew, w_payload, T_0,
    err=1e-6,
    max_iter=200
):
    W0_history = []
    delta = np.inf
    it = 0

    while delta > err and it < max_iter:
        # 1) fuel fraction (could be constant or updated)
        Wf_W0 = calculate_weight_fraction(L_D_max, R, E, c, V)
        W_fuel = Wf_W0 * TOGW_guess

        # 2) empty weight based on current TOGW guess + geometry + thrust
        W_empty = calculate_empty_weight(
            S_wing, S_ht, S_vt, S_wet_fuselage,
            TOGW_guess, T_0, num_engines
        )

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
L_D_max = 9
R = 2000            # nmi
E = 20 / 60         # min --> hr
c = 0.7            # lb/(lbf hr)
V = 490             # knots
S_ht = 0
S_vt = 74
S_wet_fuselage = 700
num_engines = 2  # Example number of engines

# The value we can adjust by the constraint curve. For example, if we want to be on the takeoff constraint curve, we can find the corresponding W/S and then calculate the TOGW based on that W/S and the wing area.
S_wing = 2400
T_0 = 23000  # Example value for thrust per engine

TOGW_guess = 55000  # Initial guess for Takeoff Gross Weight in pounds
final_TOGW, converged, iterations, W0_history = inner_loop_weight(
    TOGW_guess,
    S_wing, S_ht, S_vt, S_wet_fuselage,
    num_engines, W_crew, W_payload, T_0
)

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
            rho = 5.85e-4          # slugs/ft^3 (ISA @ 40,000 ft)
            a   = 968.1            # ft/s (ISA @ 40,000 ft)
            M   = 0.84
            V = M * a              # ft/s
            C_D_0_cruise = C_D_0        # C_D_0 at cruise is the same as clean configuration
            e_cruise = e_clean          # Assuming cruise configuration is similar to clean configuration

            def calculate_cruise_constraint_coefficients(rho, V, C_D_0, AR, e):
                q = 0.5 * rho * V**2   
                coef_1 = q * C_D_0
                coef_2 = 1/(np.pi * AR * e * q)
                return coef_1, coef_2

            coef_1_cruise_constraint, coef_2_cruise_constraint = calculate_cruise_constraint_coefficients(rho, V, C_D_0_cruise, AR, e_cruise)

            print("Coefficient of cruise constraint (C_D_0 term):", coef_1_cruise_constraint)
            print("Coefficient of cruise constraint (induced drag term):", coef_2_cruise_constraint)
            
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
S_wing_grid = list(range(3000, 6000, 2))  # Example range of wing areas to analyze

TOGW_guess_init = 55000  # Initial guess for Takeoff Gross Weight in pounds
T_total_guess_init = 24000 * num_engines  # Initial guess for total thrust in pounds-force

T_total_curve, W0_curve, n_iter_T, T_hist_allS, W0_final, wconv_final, it_w_final, W0_hist_final = outer_loop_thrust_for_one_constraint(
    S_wing_grid=S_wing_grid,
    TOGW_guess_init=TOGW_guess_init,
    T_total_guess_init=T_total_guess_init,
    num_engines=num_engines,
    S_ht=S_ht, S_vt=S_vt, S_wet_fuselage=S_wet_fuselage,
    W_crew=W_crew, W_payload=W_payload,
    coef_1_cruise_constraint=coef_1_cruise_constraint,
    coef_2_cruise_constraint=coef_2_cruise_constraint,
    tol_T_rel=1e-6,
    max_iter_T=200,
    relax=1
)

##---plot---
# Plot the resulting T vs S curve from the outer loop convergence
T_actual_777 = 220000
S_actual_777 = 4605
print(f'Actual T for 777: {T_actual_777} lbf, Actual S for 777: {S_actual_777} ft^2')

plt.figure(figsize=(16,9))
plt.title('Converged T vs S for Cruise Constraint')
plt.xlabel("Wing Area S (ft^2)")
plt.ylabel("Total Thrust T (lbf)")
plt.plot(S_actual_777, T_actual_777, label='Actual 777', marker='x', markersize=10, color='red')
plt.plot(S_wing_grid, T_total_curve, label='Converged T for Cruise Constraint', marker='o')
plt.legend(loc='best')
plt.grid()
plt.show()