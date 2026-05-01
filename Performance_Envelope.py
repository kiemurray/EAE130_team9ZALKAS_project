import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv

#Stall based on GTOW 
W_TO=cv.W_TO
#W_TO=cv.W_cruise_i
#W_TO=W_TO*cv.wf_midcruise
q_max = 2200 #psf (range 1800 - 2200)
CL_max_clean=cv.CLmax_climb
CL_max_takeoff=cv.CLmax_TO
CLmax_landing=cv.CLmax_L
S_ref=cv.S_w
e_cr=cv.e_cr
T_0_mil = cv.T_0_mil
T_0_ab = cv.T_0
CD0=cv.CD0

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

def get_q_lim_curve(altitude_range,q_lim):
    v_lim = []
    for i in range(len(altitude_range)):
        rho_vals[i] = cv.atmo_vals(altitude_range[i])[0]
    v_lim=np.sqrt(2*q_lim/rho_vals)
    return v_lim



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


#expects excess power in ft/min, convert to ft/s
def ExcessPowerVelo(Weight,S_ref,altitude,CD0,n,e,Thrust,excessPower): #outputs in knots
    excessPower = excessPower/60 #convert ft/min to ft/s
    rho=cv.atmo_vals(altitude)[0]
    Thrust_Ratio = cv.Tratio(altitude)
    T_W = Thrust*Thrust_Ratio/Weight
    W_S = Weight/S_ref
    K=1/(np.pi*cv.AR_w*e)
    coefficients = [-0.5*rho*CD0/W_S,0,T_W,-excessPower,-(n**2)*(2*K/rho)*(W_S)]
    roots = np.roots(coefficients)
    print(altitude,"ft roots:",roots)
    velocityBuffer = []
    velocities = []
    for i in range(len(roots)):
        if roots[i] > 0:
            velocityBuffer.append(cv.ft_s_to_knots(float(roots[i])))
            #make sure the order is largest - smallest
    if(velocityBuffer[0] < velocityBuffer[1]):
        temp = velocityBuffer[0]
        velocityBuffer[0] = velocityBuffer[1]
        velocityBuffer[1] = temp


    return velocityBuffer

def splitExcessPowerPlot(Weight,S_ref,h_min,h_max,CL_max,q_lim,CD0,n,e,Thrust,excessPower):
    atCeiling = False
    bigAltitudeRange = np.linspace(h_min,h_max,numPoints)
    index = 0
    lowVelocityRoots = []
    highVelocityRoots = []
    leftSideVelocity = []
    ceilingIndex = 0
    updatedAltitudeRange = []
    #this step goes up to the ceiling altitude
    while (atCeiling == False):
        altitude = bigAltitudeRange[index]
        rho=cv.atmo_vals(altitude)[0]
        zeroPowerRoots = ExcessPowerVelo(Weight,S_ref,altitude,CD0,n,e,Thrust,excessPower)
        lowVelocityRoots.append(zeroPowerRoots[1])
        highVelocityRoots.append(zeroPowerRoots[0])
        updatedAltitudeRange.append(altitude)

        #compare which is most constraining
        leftSideVelocity.append(zeroPowerRoots[1])

        if (abs(zeroPowerRoots[0]-zeroPowerRoots[1]) < 0.1):
            ceilingIndex = index
            print("We are at the ceiling")
            break

        index=index+1
        if index >= (numPoints-1):
            #atCeiling == True
            print("We can go higher >:)")
            break

    rightSideVelocity = np.zeros_like(leftSideVelocity)

    #we now go from the ceiling to the pressure limit
    for i in range(ceilingIndex,-1,-1):
        rightSideVelocity[i] =(highVelocityRoots[i])

    return leftSideVelocity,rightSideVelocity,updatedAltitudeRange


def envelopePlot(Weight,S_ref,h_min,h_max,CL_max,q_lim,CD0,n,e,Thrust,excessPower):
    atCeiling = False
    bigAltitudeRange = np.linspace(h_min,h_max,numPoints)
    index = 0
    lowVelocityRoots = []
    highVelocityRoots = []
    leftSideVelocity = []
    ceilingIndex = 0
    updatedAltitudeRange = []
    #this step goes up to the ceiling altitude
    while (atCeiling == False):
        altitude = bigAltitudeRange[index]
        rho=cv.atmo_vals(altitude)[0]
        v_stall = cv.ft_s_to_knots(np.sqrt(2*Weight/(rho*CL_max*S_ref))) #calculate stall speed (kts)

        zeroPowerRoots = ExcessPowerVelo(Weight,S_ref,altitude,CD0,n,e,Thrust,excessPower)
        lowVelocityRoots.append(zeroPowerRoots[1])
        highVelocityRoots.append(zeroPowerRoots[0])
        updatedAltitudeRange.append(altitude)

        #print("Index:",index,"Altitude:",altitude,"ft  v_stall:",v_stall,"kts  V_P:",zeroPowerRoots[1],"kts    V_p_max",zeroPowerRoots[0],"kts")

        # print("V_stall:",v_stall,"kts")
        # print("Zero Excess Power Speed (Small):",zeroPowerRoots[1],"kts")
        # print("Zero Excess Power Speed (Large):",zeroPowerRoots[0],"kts")

        #compare which is most constraining
        leftSideVelocity.append(max(zeroPowerRoots[1],v_stall))

        if (abs(zeroPowerRoots[0]-zeroPowerRoots[1]) < 0.1):
            ceilingIndex = index
            print("We are at the ceiling")
            break

        index=index+1
        if index >= (numPoints-1):
            #atCeiling == True
            print("We are at the limit")
            break

    rightSideVelocity = np.zeros_like(leftSideVelocity)

    #we now go from the ceiling to the pressure limit
    for i in range(ceilingIndex,-1,-1):
        altitude = bigAltitudeRange[i]
        rho_r= cv.atmo_vals(altitude)[0]
        dyn_pressure_velo = cv.ft_s_to_knots(np.sqrt(2*q_lim/rho_r))
        rightSideVelocity[i] =(min(highVelocityRoots[i],dyn_pressure_velo))
        #rightSideVelocity[i] = (highVelocityRoots[i])
        #print("Index:",i,"Altitude:",altitude,"ft  v_dyn:",dyn_pressure_velo,"kts  V_P:",highVelocityRoots[i])
    
    print("right side velo is funky")
    for i in range(0,ceilingIndex+1):
        print("Altitude:",updatedAltitudeRange[i],"ft  left:",leftSideVelocity[i],"kts  v_right:",rightSideVelocity[i],"kts")

    return leftSideVelocity,rightSideVelocity,updatedAltitudeRange


        



v_to_ceiling, v_from_ceiling, altitudeArray = envelopePlot(W_TO,S_ref,h_min,h_max,CL_max_clean,q_max,CD0,1,e_cr,T_0_ab*2,0)
v_slow_ps0_ab, v_fast_ps0_ab, awesomeAltitudeArray_ab = splitExcessPowerPlot(W_TO,S_ref,h_min,h_max,CL_max_clean,q_max,CD0,1,e_cr,T_0_ab*2,0)
v_slow_ps0_mil, v_fast_ps0_mil, awesomeAltitudeArray_mil = splitExcessPowerPlot(W_TO,S_ref,h_min,h_max,CL_max_clean,q_max,CD0,1,e_cr,T_0_mil*2,0)

v_slow_ps150_mil, v_fast_ps150_mil, awesomeAltitudeArray_mil_excess = splitExcessPowerPlot(W_TO,S_ref,h_min,h_max,CL_max_clean,q_max,CD0,1,e_cr,T_0_mil*2,500)

dyn_pressure_vals = cv.ft_s_to_knots(get_q_lim_curve(h_vals,q_max))
stall_vals = cv.ft_s_to_knots(getStallCurve(W_TO,h_vals,CL_max_clean,S_ref))


print("T_0_mil: ",T_0_mil,"lb")
print("T_0_ab: ",T_0_ab,"lb")









# PLOTS
plt.figure(figsize=(12, 8))
#plt.axvline(W_S_landing_runway, color='magenta', linewidth=2, label='Landing')

#plt.plot(v_slow_ps150_mil,awesomeAltitudeArray_mil_excess, color='cyan', linewidth=1, linestyle='--',label='500 ft/min Excess Power (military power)')
#plt.plot(v_fast_ps150_mil,awesomeAltitudeArray_mil_excess, color='cyan', linewidth=1,linestyle='--')
plt.plot(stall_vals,h_vals, color='orange', linewidth=2, linestyle='--',label='Stall Line')
plt.plot(v_slow_ps0_ab,awesomeAltitudeArray_ab, color='blue', linewidth=2, linestyle='--',label='Zero Excess Power (AB)')
plt.plot(v_fast_ps0_ab,awesomeAltitudeArray_ab, color='blue', linewidth=2,linestyle='--')
plt.plot(v_slow_ps0_mil,awesomeAltitudeArray_mil, color='green', linewidth=2, linestyle='--',label='Zero Excess Power (military power)')
plt.plot(v_fast_ps0_mil,awesomeAltitudeArray_mil, color='green', linewidth=2,linestyle='--')
plt.plot(dyn_pressure_vals,h_vals, color='purple', linewidth=2,linestyle='--', label='Dynamic Pressure Limit (2200 psf)')

plt.plot(v_to_ceiling,altitudeArray, color='magenta', linewidth=3, label='Flight Envelope')
plt.plot(v_from_ceiling,altitudeArray, color='magenta', linewidth=3,)



plt.xlabel('V (KEAS)', fontsize=18)
plt.ylabel('Altitude (feet)', fontsize=18)
plt.title('Performance Envelope (Takeoff Weight)', fontsize=20)
plt.grid(True, alpha=0.4)
plt.legend(fontsize=14, loc='upper left')

plt.xlim(0, 1800)
plt.ylim(h_min, 80000)  

plt.show()