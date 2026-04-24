import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv

#Stall based on GTOW 
W_TO=cv.W_TO
CL_max_clean=cv.CLmax_climb
CL_max_takeoff=cv.CLmax_TO
CLmax_landing=cv.CLmax_L
S_ref=cv.S_w

h_min = 0 #feet
h_max = 70000 #feet
numPoints = 100

rho_vals=np.zeros(numPoints)
h_vals = np.linspace(h_min,h_max,numPoints)



#stall curve
def getStallCurve(Weight,altitude_range,CL_max,S_ref):
    for i in range(numPoints):
        rho_vals[i] = cv.atmo_vals(altitude_range[i])[0]

    v_stall = np.sqrt(2*Weight/(rho_vals*CL_max*S_ref))
    return v_stall

#Specific power calculation
def getSpecificPower(Velocity,T_W,W_S,altitude,CD0,n,e):
    rho=cv.atmo_vals(altitude)[0]
    q=(1/2)*(rho)*(Velocity**2)
    K=1/(np.pi*cv.AR_w*e)
    P_s = Velocity*(T_W-(q*CD0/W_S)-(n**2)*(K/q)*(W_S))
    return P_s

def zeroExcessPowerVelo(T_W,W_S,altitude,CD0,n,e):
    coefficients = []

#ceiling curve













stall_vals = cv.ft_s_to_knots(getStallCurve(W_TO,h_vals,CL_max_clean,S_ref))













# PLOTS
plt.figure(figsize=(12, 8))
#plt.axvline(W_S_landing_runway, color='magenta', linewidth=2, label='Landing')
plt.plot(stall_vals,h_vals, color='orange', linewidth=2, label='Stall Line')
#plt.axvline(v_a, color='red', linewidth=2, label='Maneuvering Speed')
#plt.axhline(n_design_positive, color='green', linewidth=2, label='Positive Limit Load')
#plt.axhline(n_design_negative, color='red', linewidth=2, label='Negative Limit Load')

#design_envelope = np.maximum.reduce([T_W_climb * np.ones_like(W_S), T_W_maneuver, T_W_dash30])

#plt.fill_between(W_S, design_envelope, 2.0,  # 2.0 is a safe upper Y-limit
                 #where=(W_S <= W_S_stall), 
                 #color='yellow', 
                 #alpha=0.3, 
                 #zorder=1,
                 #label='Design Window')
plt.xlabel('V (KEAS)', fontsize=18)
plt.ylabel('Altitude (feet)', fontsize=18)
plt.title('Performance Envelope', fontsize=20)
plt.grid(True, alpha=0.4)
plt.legend(fontsize=14, loc='upper right')

plt.xlim(0, 1400)
plt.ylim(h_min, h_max)  

plt.show()