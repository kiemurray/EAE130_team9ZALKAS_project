import numpy as np
import code_variables as cv

rho = 5.85e-4          # slugs/ft^3 (ISA @ 40,000 ft)
a   = 968.1            # ft/s (ISA @ 40,000 ft)
M   = 0.84
V = M * a              # ft/s
C_D_0 = cv.CD0
e_clean = cv.e_cr
C_D_0_cruise = C_D_0        # C_D_0 at cruise is the same as clean configuration
e_cruise = e_clean          # Assuming cruise configuration is similar to clean configuration
AR = cv.AR_w

rho_rho_sl_takeoff = 0.95
C_L_max_takeoff = cv.CLmax_TO
BFL_takeoff = 10000

def calculate_takeoff_field_length_coefficient(BFL, rho_ratio, C_L_max):
    TOP_25_takeoff = BFL / 37.5
    return 1 / (rho_ratio * C_L_max * TOP_25_takeoff)

coef_takeoff_constraint = calculate_takeoff_field_length_coefficient(BFL_takeoff, rho_rho_sl_takeoff, C_L_max_takeoff)
print("Coefficient of takeoff field length:", coef_takeoff_constraint)

N_eng = 2  # Number of engines
k_s = 1.2  
C_L_max = cv.CLmax_climb
G = 0.012  # Gradient (%)
e = cv.e_to  # Oswald efficiency factor
def calculate_climb_constraint_coefficient(N_eng, k_s, C_L_max, C_D_0, AR, e, G):
    return (1/0.8) * (N_eng / (N_eng - 1)) * ((k_s**2) / C_L_max * C_D_0 + C_L_max / (np.pi * AR * e * k_s**2) + G)
coef_1_climb_constraint = calculate_climb_constraint_coefficient(N_eng, k_s, C_L_max, C_D_0, AR, e, G)
print("Coefficient of takeoff climb:", coef_1_climb_constraint)

def calculate_cruise_constraint_coefficients(rho, V, C_D_0, AR, e):
    q = 0.5 * rho * V**2   
    coef_1 = q * C_D_0
    coef_2 = 1/(np.pi * AR * e * q)
    return coef_1, coef_2

coef_1_cruise_constraint, coef_2_cruise_constraint = calculate_cruise_constraint_coefficients(rho, V, C_D_0_cruise, AR, e_cruise)

print("Coefficient of cruise constraint (C_D_0 term):", coef_1_cruise_constraint)
print("Coefficient of cruise constraint (induced drag term):", coef_2_cruise_constraint)

rho_rho_sl_landing = 0.95
C_L_max_landing = C_L_max_landing
s_a = 1000
s_land = BFL_takeoff * 0.6
landing_W_ratio = 0.65

def calculate_landing_field_length_coefficient(rho_ratio, C_L_max, s_land, s_a, landing_W_ratio):
    return rho_ratio * C_L_max * (s_land - s_a) / (80 * landing_W_ratio)

coef_landing_constraint = calculate_landing_field_length_coefficient(rho_rho_sl_landing, C_L_max_landing, s_land, s_a, landing_W_ratio)
print("Coefficient of landing field length:", coef_landing_constraint)


