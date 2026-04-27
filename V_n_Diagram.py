import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv

#Need diagram based on minimum and maximum weight
#you can tweak these values
W_max = cv.W_TO
# n_design_positive = cv.n_z
# n_design_negative = cv.n_z_negative
numPoints = 100
V_max = 700 #KEAS
V_min = 0 #KEAS
altitude = 0 #Sea Level
CL_max = cv.CLmax_climb
CL_min = -cv.CLmax_climb
S_ref = cv.S_w
k = 0.97 #empirical correction factor that accounts for section lift curve slopes different from 2𝜋
c = cv.c_w #the mean geometric chord, also known as the standard mean chord, defined as S/b
g = 32.17 # idk, idt the metabook defined this

#Calculations

#using english units (pounds, feet, seconds)
KEAS = np.linspace(0,700,numPoints)

def get_Max_Lift_Line(CL_max,Weight,S_ref,altitude,n):
    rho_lift = cv.atmo_vals(altitude)[0]
    v_a = cv.ft_s_to_knots(np.sqrt(2*Weight*np.abs(n)/(rho_lift*np.abs(CL_max)*S_ref)))
    print("v_a:",v_a,"KEAS")
    v_stall = np.linspace(0,v_a,numPoints)
    F_stall = (1/2)*rho_lift*(cv.knots_to_ft_per_s(v_stall)**2)*CL_max*S_ref
    n_stall = F_stall/Weight
    
    return n_stall,v_stall

def compute_positive_limit_loads(weight_lb):
    n_pos_formula = 2.1 + 24000 / (weight_lb + 10000)  # FAR 25.337 formula


    if n_pos_formula < 2.5:
        print(f"Computed positive limit load factor is {n_pos_formula:.2f}, "
              f"so use 2.50 based on FAR 25 minimum.")
        selected_n_pos_limit = 2.5
    elif n_pos_formula > 3.8:
        print(f"Computed positive limit load factor is {n_pos_formula:.2f}, "
              f"so cap at 3.80 based on FAR 25 maximum.")
        selected_n_pos_limit = 3.8
    else:
        print(f"Computed positive limit load factor is {n_pos_formula:.2f}, "
              f"so use the computed value.")
        selected_n_pos_limit = n_pos_formula


    return selected_n_pos_limit

def get_V_B(altitude):
    if altitude <= 20000:
        V_B = 66
    elif altitude >= 500000:
        V_B = 38
    else:
        V_B = 66 + (20000 - 50000)/(66 - 38)*(altitude - 20000)

    return V_B

def get_V_C(altitude):
    if altitude <= 20000:
        V_C = 50
    elif altitude >= 500000:
        V_C = 25
    else:
        V_C = 50 + (20000 - 50000)/(50 - 25)*(altitude - 20000)

    return V_C

def get_V_D(altitude):
    if altitude <= 20000:
        V_D = 25
    elif altitude >= 500000:
        V_D = 12.5
    else:
        V_D = 25 + (20000 - 50000)/(25 - 12.5)*(altitude - 20000)

    return V_D

def get_n_gust(Weight, S_ref, altitude, V_EAS, U_e, C_L_alpha, c, g):
    rho = cv.atmo_vals(altitude)[0]
    mu = (2*(Weight/S_ref))/(rho*c*C_L_alpha*g)
    K_g = (0.88*mu)/(5.3+mu)
    n_pos = 1 + (K_g*C_L_alpha*U_e*V_EAS)/(498*(Weight/S_ref))
    n_neg = 1 - (K_g*C_L_alpha*U_e*V_EAS)/(498*(Weight/S_ref))
    
    return n_pos, n_neg


n_design_positive = compute_positive_limit_loads(W_max)
n_design_negative = -1

n_stall_pos,v_stall_pos = get_Max_Lift_Line(CL_max,W_max,S_ref,altitude,n_design_positive)
n_stall_neg,v_stall_neg = get_Max_Lift_Line(CL_min,W_max,S_ref,altitude,n_design_negative)

#cut the stall plot off at maneuver speed----------------------------------------------------------------------

# Adam's code
def compute_intersection_velocity(stall_coeff, n_limit):
    """
    Solve stall_coeff * V^2 = |n_limit|
    """
    int_V = np.sqrt(abs(n_limit) / stall_coeff)
#    print(f"Intersection velocity for n_limit={n_limit:.2f} is {int_V:.2f} m/s")
    return int_V

c_stall = 0.5*cv.atmo_vals(altitude)[0]*CL_max/((W_max/S_ref))
print(c_stall)

# Compute intersection velocities for positive and negative limit load factors within the stall boundary
V_stall_pos_end = compute_intersection_velocity(c_stall, n_design_positive)/1.688
# V_stall_pos = np.linspace(0, V_stall_pos_end, 100)
print('TEST')
print(V_stall_pos_end)

V_stall_neg_end = compute_intersection_velocity(c_stall, n_design_negative)/1.688
# V_stall_neg = np.linspace(0, V_stall_neg_end, 100)


# Compute the corresponding n values at the intersection points
# n_stall_pos_intersection = n_stall_pos * V_stall_pos**2
# n_stall_neg_intersection = n_stall_neg * V_stall_neg**2

# V_pos_limit_extended = np.linspace(V_stall_pos_end, V_max, 100)
# V_neg_limit_extended = np.linspace(V_stall_neg_end, V_max, 100)

# n_pos_extended = n_design_positive * np.ones_like(V_pos_limit_extended)
# n_neg_extended = n_design_negative * np.ones_like(V_neg_limit_extended)
V_start_pos = V_stall_pos_end
V_start_neg = V_stall_neg_end

V_cutoff = V_max
V_end_pos = V_cutoff
V_end_neg = V_cutoff

# max speed


#Plot based on Equivalent airspeed
# PLOTS
plt.figure(figsize=(12, 8))
plt.xlabel("V (m/s)")
plt.ylabel("n (-)")
#plt.axvline(W_S_landing_runway, color='magenta', linewidth=2, label='Landing')
plt.plot(v_stall_pos,n_stall_pos, color='orange', linewidth=2, label='Max Lift Line')
plt.plot(v_stall_neg,n_stall_neg, color='blue', linewidth=2, label='Min Lift Line')
#plt.axvline(v_a, color='red', linewidth=2, label='Maneuvering Speed')

plt.hlines(n_design_positive, V_start_pos, V_end_pos, colors='green', linewidth=2, label='Positive Limit Load')
plt.hlines(n_design_negative, V_start_neg, V_end_neg, colors='red', linewidth=2, label='Negative Limit Load')

# plt.axhline(n_design_positive, color='green', linewidth=2, label='Positive Limit Load')
# plt.axhline(n_design_negative, color='red', linewidth=2, label='Negative Limit Load')

#design_envelope = np.maximum.reduce([T_W_climb * np.ones_like(W_S), T_W_maneuver, T_W_dash30])

#plt.fill_between(W_S, design_envelope, 2.0,  # 2.0 is a safe upper Y-limit
                 #where=(W_S <= W_S_stall), 
                 #color='yellow', 
                 #alpha=0.3, 
                 #zorder=1,
                 #label='Design Window')
plt.xlabel('V (KEAS)', fontsize=18)
plt.ylabel('Load Factor, n', fontsize=18)
plt.title('Flight Envelope', fontsize=20)
plt.grid(True, alpha=0.4)
plt.legend(fontsize=14, loc='upper right')

plt.xlim(0, 700)
plt.ylim(-8, 12)  

plt.show()