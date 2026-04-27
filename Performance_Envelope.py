import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv

#Stall based on GTOW 
W_TO=cv.W_TO
#W_TO=20000
CL_max_clean=cv.CLmax_climb
CL_max_takeoff=cv.CLmax_TO
CLmax_landing=cv.CLmax_L
S_ref=cv.S_w
e_cr=cv.e_cr
T_0_mil = cv.T_0_mil
T_0_ab = cv.T_0
CD0=cv.CD0

h_min = 0 #feet
h_max = 60000 #feet
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
def getSpecificPower(Velocity,Weight,S_ref,altitude,CD0,n,e,Thrust):
    rho=cv.atmo_vals(altitude)[0]
    Thrust_Ratio = cv.Tratio(altitude)
    T_W = Thrust*Thrust_Ratio/Weight
    W_S = Weight/S_ref
    q=(1/2)*(rho)*(Velocity**2)
    K=1/(np.pi*cv.AR_w*e)
    P_s = Velocity*(T_W-(q*CD0/W_S)-(n**2)*(K/q)*(W_S))
    return P_s


def zeroExcessPowerVelo(Weight,S_ref,altitude,CD0,n,e,Thrust): #outputs in knots
    rho=cv.atmo_vals(altitude)[0]
    Thrust_Ratio = cv.Tratio(altitude)
    T_W = Thrust*Thrust_Ratio/Weight
    W_S = Weight/S_ref
    K=1/(np.pi*cv.AR_w*e)
    coefficients = [-0.5*rho*CD0/W_S,0,T_W,0,-(n**2)*(2*K/rho)*(W_S)]
    roots = np.roots(coefficients)
    print(roots)
    velocityBuffer = []
    velocities = []
    for i in range(len(roots)):
        if roots[i] > 0:
            velocityBuffer.append(cv.ft_s_to_knots(float(roots[i])))
    if (velocityBuffer[0] == velocityBuffer[1]):
        return np.zeros(2)

    return velocityBuffer


def zeroExcessPowerVeloPlot(Weight,S_ref,h_min,h_max,CD0,n,e,Thrust): #outputs in knots
    
    altitudeArray=np.linspace(h_min,h_max,numPoints)
    velocityBuffer = []
    heights = []
    velocities = []
    roots = np.zeros((numPoints,5))
    velo_roots = np.zeros(4)


    #get the array
    for i in range(len(altitudeArray)):
        #print(altitude)
        rho=cv.atmo_vals(altitudeArray[i])[0]
        Thrust_Ratio = cv.Tratio(altitudeArray[i])
        T_W = Thrust*Thrust_Ratio/Weight
        W_S = Weight/S_ref
        K=1/(np.pi*cv.AR_w*e)
        coefficients = [-0.5*rho*CD0/W_S,0,T_W,0,-(n**2)*(2*K/rho)*(W_S)]
        # print("AltitudeArray[",i,"]: ",altitudeArray[i])
        # coefficients.append(altitudeArray[i])
        # print("Coefficients: ",coefficients)
        # roots[i] = np.roots(coefficients)


        coefficients = [-0.5*rho*CD0/W_S,0,T_W,0,-(n**2)*(2*K/rho)*(W_S)]
        velo_roots = np.roots(coefficients)
        velo_roots = np.append(velo_roots,altitudeArray[i])
        roots[i] = velo_roots
    

    #take only the positive values
    doubleUp = 0
    for i in range(numPoints):

        #isolate the row
        rootBuffer = []
        for j in range(len(roots[i])):
            if roots[i,j] > 0:
                rootBuffer.append(float(roots[i,j]))
        #print("Root Buffer: ",rootBuffer)
        #created row of positive values
        if abs(rootBuffer[0] - rootBuffer[1]) > 0.001:
            if i == 0:
                rootBuffer.append(0)
                velocityBuffer = rootBuffer
                #print("velocityBuffer: ",velocityBuffer,"rootBuffer: ",rootBuffer)
            else:
                #print("velocityBuffer: ",velocityBuffer,"rootBuffer: ",rootBuffer)
                velocityBuffer = np.vstack([velocityBuffer,rootBuffer])
        else:
            if doubleUp == 0:
                velocityBuffer = np.vstack([velocityBuffer,rootBuffer])
                doubleUp = 1


    velocities = velocityBuffer[:,[0,1]]
    heights = velocityBuffer[:,2]


    return cv.ft_s_to_knots(velocities),cv.ft_s_to_knots(heights)
#ceiling curve













stall_vals = cv.ft_s_to_knots(getStallCurve(W_TO,h_vals,CL_max_clean,S_ref))
zeroExcessPowerVelocity=np.zeros((len(h_vals),2))
for i in range(len(h_vals)):
    zeroExcessPowerVelocity[i] = zeroExcessPowerVelo(W_TO,S_ref,h_vals[i],CD0,1,e_cr,2*T_0_mil)
#print("P_s = 0 at sea level",zeroExcessPowerVelocity)


print("T_0_mil: ",T_0_mil,"lb")
print("T_0_ab: ",T_0_ab,"lb")

P_s_velo_mil,altitudes_mil =zeroExcessPowerVeloPlot(W_TO,S_ref,h_min,h_max,CD0,1,e_cr,2*T_0_mil)
P_s_velo_ab,altitudes_ab =zeroExcessPowerVeloPlot(W_TO,S_ref,h_min,h_max,CD0,1,e_cr,2*T_0_ab)







# PLOTS
plt.figure(figsize=(12, 8))
#plt.axvline(W_S_landing_runway, color='magenta', linewidth=2, label='Landing')

plt.plot(stall_vals,h_vals, color='orange', linewidth=2, label='Stall Line')
plt.plot(P_s_velo_mil,altitudes_mil, color='green', linewidth=2, label='Zero Excess Power (Military Power)')
plt.plot(P_s_velo_ab,altitudes_ab, color='blue', linewidth=2, label='Zero Excess Power (Afterburner)')

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