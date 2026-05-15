import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv
import math

#Need diagram based on minimum and maximum weight
#you can tweak these values
Weight = cv.W_TO
#Weight = cv.W_TO*cv.wf_landing
n_design_positive = cv.n_z
n_design_negative = cv.n_z_negative
numPoints = 100
# V_max = 700 #KEAS
V_min = 0 #KEAS
altitude = 30000 # NOT Sea Level
CL_max = cv.CLmax_climb
CL_min = -cv.CLmax_climb
CL_maxL = cv.CLmax_L
S_ref = cv.S_w
k = 0.97 #empirical correction factor that accounts for section lift curve slopes different from 2𝜋
c = cv.c_w #the mean geometric chord, also known as the standard mean chord, defined as S/b
g = 32.17 # idk, idt the metabook defined this
# V_C = 1179.476 # Mach 2.0 at 30000 ft in knots/s
V_C = 846.102544351 # Mach 0.85 at 30000 ft in knot/s, expected intermediate dash from RFP
CL_alpha = cv.CL_alpha # 1/rad from VSPAero

#Calculations

#using english units (pounds, feet, seconds)
V_D = 1.06*1.07*V_C
print('V_D')
print(V_D)
V_max = V_D + 100
KEAS = np.linspace(0,V_max,numPoints)

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

def get_gustV_B(altitude):
    if altitude <= 20000:
        V_B = 66
    elif altitude >= 50000:
        V_B = 38
    else:
        V_B = 38 + (66 - 38)/(20000 - 50000)*(altitude - 50000)

    return V_B

def get_gustV_C(altitude):
    if altitude <= 20000:
        V_C = 50
    elif altitude >= 50000:
        V_C = 25
    else:
        V_C = 25 + (50 - 25)/(20000 - 50000)*(altitude - 50000)

    return V_C

def get_gustV_D(altitude):
    if altitude <= 20000:
        V_D = 25
    elif altitude >= 50000:
        V_D = 12.5
    else:
        V_D = 12.5 + (25 - 12.5)/(20000 - 50000)*(altitude - 50000)

    return V_D

# def get_n_gust(Weight, S_ref, altitude, V_EAS, U_e, C_L_alpha, c, g):
#     rho = cv.atmo_vals(altitude)[0]
#     mu = (2*(Weight/S_ref))/(rho*c*C_L_alpha*g)
#     K_g = (0.88*mu)/(5.3+mu)
#     v = V_EAS
#     n_pos = 1 + (K_g*C_L_alpha*U_e*V_EAS)/(498*(Weight/S_ref))
#     n_neg = 1 - (K_g*C_L_alpha*U_e*V_EAS)/(498*(Weight/S_ref))
    
#     return n_pos, n_neg, v

def get_gust_constants(Weight, S_ref, altitude, CL_alpha, c, g):
    rho = cv.atmo_vals(altitude)[0]
    mu = (2*(Weight/S_ref))/(rho*c*CL_alpha*g)
    K_g = (0.88*mu)/(5.3+mu)
    n = (K_g*CL_alpha)/(498*(Weight/S_ref))      # metabook multiplies denominator by 498, Adam uses 2

    return rho, mu, K_g, n

# Equivalent Gust Velocities. These are in ft/s
print('getting gust velocities...')
gust_V_B = get_gustV_B(altitude)
print(gust_V_B)
gust_V_C = get_gustV_C(altitude)
print(gust_V_C)
gust_V_D = get_gustV_D(altitude)
print(gust_V_D)

rho, mu, K_g, constant = get_gust_constants(Weight, S_ref, altitude, CL_alpha, c, g)
print('constants')
print(rho)
print(mu)
print(K_g)
print(constant)

V_range = np.linspace(0,V_D,numPoints)

gust_B_pos = 1 + constant * gust_V_B * V_range
gust_C_pos = 1 + constant * gust_V_C * V_range
gust_D_pos = 1 + constant * gust_V_D * V_range
gust_B_neg = 1 - constant * gust_V_B * V_range
gust_C_neg = 1 - constant * gust_V_C * V_range
gust_D_neg = 1 - constant * gust_V_D * V_range

diveGust = 1 - constant * gust_V_D * V_D

# Create lower limit VC to VD gust line
VC_VD_range = np.linspace(V_C,V_D,numPoints)
VC_VD = n_design_negative + (diveGust - n_design_negative)/(V_D - V_C)*(VC_VD_range - V_C)

# Stall lines
n_stall_pos,v_stall_pos = get_Max_Lift_Line(CL_max,Weight,S_ref,altitude,n_design_positive)
n_stall_neg,v_stall_neg = get_Max_Lift_Line(CL_min,Weight,S_ref,altitude,n_design_negative)



#cut the stall plot off at maneuver speed----------------------------------------------------------------------

# Adam's code
def compute_intersection_velocity(stall_coeff, n_limit):
    """
    Solve stall_coeff * V^2 = |n_limit|
    """
    int_V = np.sqrt(abs(n_limit) / stall_coeff)
#    print(f"Intersection velocity for n_limit={n_limit:.2f} is {int_V:.2f} m/s")
    return int_V

c_stall = 0.5*cv.atmo_vals(altitude)[0]*CL_max/((Weight/S_ref))

# Compute intersection velocities for positive and negative limit load factors within the stall boundary
V_stall_pos_end = compute_intersection_velocity(c_stall, n_design_positive)/1.688   # /1.688 ft to knot
V_stall_neg_end = compute_intersection_velocity(c_stall, n_design_negative)/1.688

V_start_pos = V_stall_pos_end
V_start_neg = V_stall_neg_end

V_cutoff = V_D
V_end_pos = V_cutoff
V_end_neg = V_cutoff

# max speed
n_design_line = np.linspace(n_design_negative, n_design_positive, 100)
n_exceed_line = np.linspace(diveGust, n_design_positive, 100)
V_exceed_line = V_D * np.ones_like(n_exceed_line)
V_NO_line = V_C* np.ones_like(n_exceed_line)

# stall speed
v_stall = (Weight/(0.5*rho*CL_max*S_ref))**0.5/1.688
v_stall_line = v_stall * np.ones_like(n_exceed_line)
# Compute intersection velocities for positive and negative limit load factors within the stall boundary
F_stall = (1/2)*rho*(cv.knots_to_ft_per_s(v_stall)**2)*CL_max*S_ref
stall_pos = F_stall/Weight
stall_neg = -F_stall/Weight

n_stall_line = np.linspace(stall_neg, stall_pos, 100)

# limiting gust load lines
V_rangeB = np.linspace(0,V_stall_pos_end,numPoints)
V_rangeC = np.linspace(0,V_C,numPoints)

# # side quest to double check stall speed fits RFP (YAY we still got it)
# rhoSL = cv.atmo_vals(0)[0]
# v_stallSL = (Weight/(0.5*rhoSL*CL_maxL*S_ref))**0.5/1.688
# print('SIDE QUEST: RFP stall check')
# print(v_stallSL)

# relevant values
print(v_stall)
print(V_stall_pos_end)
print(V_C)
print(V_D)


#Plot based on Equivalent airspeed
# PLOTS
plt.figure(figsize=(12, 8))
# plt.ylabel("n (-)")
# plt.plot(v_stall_pos,n_stall_pos, color='#d55e00', linewidth=2, label='Max lift line')
# plt.plot(v_stall_neg,n_stall_neg, color='#0072b2', linewidth=2, label='Min lift line')
plt.plot(v_stall_pos,n_stall_pos, color='black', linewidth=3)
plt.plot(v_stall_neg,n_stall_neg, color='black', linewidth=3)

# plot those vertical lines
# plt.plot(V_exceed_line, n_exceed_line,label='Never exceed speed', linewidth=2, color='red')
plt.plot(V_exceed_line, n_exceed_line, linewidth=3, color='black')
plt.plot(V_NO_line, n_design_line,label='Design air speed', linestyle='--',linewidth=2, color='#009e73')
plt.plot(v_stall_line, n_stall_line, label='Stall speed',linewidth=3, color='#cc79a7')

# plot pos and neg loads
# plt.hlines(n_design_positive, V_start_pos, V_end_pos, colors='#000000', linewidth=2, label='Positive limit load')
# plt.hlines(n_design_negative, V_start_neg, V_C, colors='#cc79a7', linewidth=2, label='Negative limit load')
plt.hlines(n_design_positive, V_start_pos, V_end_pos, colors='black', linewidth=3)
plt.hlines(n_design_negative, V_start_neg, V_C, colors='black', linewidth=3)

# plot that awkward negative load line between VC and VD
# plt.plot(VC_VD_range, VC_VD, color='#cc79a7', linewidth=2, label='Negative limit load')
plt.plot(VC_VD_range, VC_VD, color='black', linewidth=3)

# plot gust load lines
plt.plot(V_rangeB, gust_B_pos,label='Rough air gust (56.67 ft/s)', linestyle='--',linewidth=2, color='#000000')
plt.plot(V_rangeC, gust_C_pos,label='Gust at max design speed (41.67 ft/s)', linestyle='--',linewidth=2, color='#56b4e9')
plt.plot(V_range, gust_D_pos,label='Gust at max dive speed (20.83 ft/s)', linestyle='--',linewidth=2, color='#e69f00')
plt.plot(V_rangeB, gust_B_neg, linestyle='--',linewidth=2, color='#000000')
plt.plot(V_rangeC, gust_C_neg, linestyle='--',linewidth=2, color='#56b4e9')
plt.plot(V_range, gust_D_neg, linestyle='--',linewidth=2, color='#e69f00')

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
plt.title('Maximum Weight V-n Diagram', fontsize=20)

plt.annotate('${V_A}$', (V_stall_pos_end, 8.1), xytext=(-5,5), textcoords='offset points',fontsize=15)
plt.annotate('${V_C}$', (V_C, 8.1), xytext=(-5,5), textcoords='offset points',fontsize=15)
plt.annotate(f'$V_D$ = {math.floor(V_D)} kts', (V_D-50, 8.1), xytext=(-5,5), textcoords='offset points',fontsize=15)
plt.annotate('${V_{Stall}}$', (v_stall+20, -0.5), xytext=(-5,5), textcoords='offset points',fontsize=15)
plt.annotate('Positive Stall Line', (425, 5), xytext=(-5,5), textcoords='offset points',fontsize=15)
plt.annotate('Negative Stall Line', (150,-2), xytext=(-5,5), textcoords='offset points',fontsize=15)
plt.annotate('Positive Load Limit', (770,6.7), xytext=(-5,5), textcoords='offset points',fontsize=15)
plt.annotate('Negative Load Limit', (600,-1.75), xytext=(-5,5), textcoords='offset points',fontsize=15)
plt.annotate('${V_{NE}}$', (V_D+25,3.5), xytext=(-5,5), textcoords='offset points',fontsize=15)

plt.grid(True, alpha=0.4)
plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=2, fontsize=14)
plt.tight_layout()
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlim(0, V_max)
plt.ylim(n_design_negative - 1, n_design_positive + 1)  

plt.show()