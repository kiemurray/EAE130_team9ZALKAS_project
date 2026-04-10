import numpy as np
import code_variables as cv
atmo_vals=cv.atmo_vals
T_0=cv.T_0
ct_cruise = cv.ct_cruise
T_0_mil=cv.T_0_mil
W_TO=cv.W_TO
Tratio=cv.Tratio
e_cr=cv.e_cr
AR_w=cv.AR_w
CD0=cv.CD0
S_w=cv.S_w



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


wf_takeoff = fuelFraction(5/60,ct_cruise,2*T_0_mil,W_TO)
#W_cruise_i = W_TO*wf_warmup*wf_taxi*wf_climb

def getGamma(T_W,L_D):
    return np.arcsin(T_W - 1/(L_D))
def getClimbVelocity(rho,W_S,CD_0,k_cr,T_W):
    return np.sqrt((W_S/(3*rho*CD_0))*(T_W + np.sqrt((T_W)**2)+12*CD_0*k_cr))

def climbFuelFraction(numSegments,h_cruise,TotalThrust,W_takeoff,S_w,k_cr,C_D_0,c_climb):
    weight = np.zeros(numSegments+1)
    weight[0] = W_takeoff
    altitudeArray=np.zeros(numSegments+1)

    #guess L/D
    L_D_guess = 8
    gamma = getGamma(TotalThrust/weight,L_D_guess)
    W_S = weight / S_w
    T_alt = Tratio(0)*TotalThrust
    v_climb = getClimbVelocity(rho,W_S,CD0,k_cr,T_alt/weight)

    


    # v_climb=np.zeros(numSegments)
    # for step in range(numSegments):
    #     rho, a = atmo_vals(altitudeArray[step])[:2]
    #     T_W = Tratio(altitudeArray[step])*TotalThrust/weight[step]
    #     v_climb[step] = np.sqrt(((weight[step]/S_w)/(3*rho*C_D_0))*(T_W)+np.sqrt((T_W)**2+12*C_D_0*k_cr))
    #     D=0
    #     #D= (1/2*rho*v_climb[step]**2)*S_w*(C_D_0+k_cr*)
    #     delta_He = (h_cruise/numSegments + v_climb[step]**2/(2*32.17))
    #     weight[step+1]=weight[step]*np.exp(-c_climb*delta_He/(v_climb[step](1-D/Tratio(altitudeArray[step])*TotalThrust))) #D is drag



def get_cruisefuelFraction(numSegments,range_nm,W_topOfClimb,altitude,S_w,k_cr,C_D_0,C_cruise):
    #range in nm
    stepDistance=range_nm/numSegments
    print("step distance: ",stepDistance,"nm")
    weightArray=[W_topOfClimb]
    velocityArray=[]
    fuelBurned=0
    for step in range(numSegments):
        V_cruise_step = get_V_bestRange(weightArray[step],altitude,S_w,k_cr,C_D_0)
        time = 6076.12 * stepDistance / V_cruise_step #convert distance in nm to feet
        print("time for step",step,": ",time,"sec")
        T_req = get_D_bestRange(C_D_0,V_cruise_step,S_w,altitude)
        print("Thrust Required",T_req,"lbf")
        W_fuel_burned = T_req*(time/3600)*C_cruise #need to convert to hours since specific fuel consumption in hours
        weightArray.append(weightArray[step]-W_fuel_burned)
        velocityArray.append(V_cruise_step)
    #print("length of weightarray: ",len(weightArray))
    print("Weight Array:        Velocity Array")
    for i in range(len(velocityArray)):
        print(weightArray[i],"lbf       ",velocityArray[i],"ft/s")
        fuelBurned = fuelBurned + weightArray[i]-weightArray[i+1]
    print("fuel burned:",fuelBurned,"lbs\n")


#I think this assumes that you're flying at best cruise speed
def getFuelBurn(Altitude,V_cruise,S_wing,CD_0,k_cruise,W_start,c_t_cruise,Range):
    rho, a = atmo_vals(Altitude)[:2] #grabbing density and speed of sound

    W_end = (1/2)*(rho*V_cruise**2)*S_wing*np.sqrt(CD_0/k_cruise)*np.tan(np.arctan((2*W_start/(rho*V_cruise**2*S_wing))*np.sqrt(k_cruise/CD_0))-(c_t_cruise*(1/3600)*Range*6076.12*np.sqrt(CD_0*k_cruise)/V_cruise))
    
    print("W_end: ",W_end,"lbs")
    fuelBurned=W_start-W_end    
    print("Fuel Burn: ",fuelBurned,"lbs")
    fuelFraction = (W_start-fuelBurned)/W_start
    return fuelBurned,fuelFraction

def BreguetExponential(numSegments,Altitude,S_wing,CD_0,k_cruise,W_topOfClimb,C_t_cruise,Range):
    stepDistance=6076.12*Range/numSegments #step distance in feet
    #print("step distance: ",stepDistance,"nm")
    rho, a = atmo_vals(Altitude)[:2] #grabbing density and speed of sound
    weightArray=np.zeros(numSegments+1)
    weightArray[0]=W_topOfClimb
    #velocityArray=np.zeros(numSegments)
    C_L_array = np.zeros(numSegments)
    L_D_array = np.zeros(numSegments)
    velocity_array = []
    fuelBurned=0
    for step in range(numSegments):
        velocity_array.append(0.85 * a)
        #velocity_array.append(get_V_bestRange(weightArray[step],Altitude,S_wing,k_cruise,CD_0))
        C_L_array[step] = 2*weightArray[step]/(rho*(velocity_array[step]**2)*S_wing)
        L_D_array[step] = C_L_array[step]/(CD_0+k_cruise*C_L_array[step]**2)
        weightArray[step+1] = weightArray[step]*np.exp(-stepDistance*C_t_cruise*(1/3600)/(velocity_array[step]*L_D_array[step]))
    print("\n\nDiscretized Breguet Equations\nWeight Array:")
    for i in range(numSegments):
        fuelBurned = fuelBurned+(weightArray[i]-weightArray[i+1])
        print(round(weightArray[i],2),"lbf       Fuel burned (segment)",round(weightArray[i]-weightArray[i+1],2),"lbs     Fuel burned (total)",round(fuelBurned,2),"lbs    C_L",round(C_L_array[i],2),"  L_D",round(L_D_array[i],2),"    speed: ",round(velocity_array[step],2),"ft/s")
    return fuelBurned,((W_topOfClimb-fuelBurned)/W_topOfClimb)
    
    
    
#range in nm, c_t in lb/lbf*hr, v_cruise in ft/s
def breguetFraction(Range,c_t_cruise,v_cruise,L_D_max):
    return np.exp(-(6076.12*Range*c_t_cruise*(1/3600)/(v_cruise*0.94*L_D_max))) #range to ft, c_t to lb/lbf*sec

h_cruise = 30000 #ft
Range = 2000 #nm
L_D_max = 10
W_cruise_i = 52970

rho_range, a_range = atmo_vals(h_cruise)[:2]
#Test for Lecture example
#AR_w = 8
#e_cr = 0.885
#S_w = 960
#W_cruise_i = 50000
#CD0 = 0.0165
#L_D_max = 18.35
#Range = 5000 #nm
#W_cruise_i = 48800

#L_D = 0.94 * L_D_max
v_cruise = 0.85 * a_range
#cruise = np.exp((-combat_range*ct_cruise) / (v_cruise*L_D))
k_cr=1/(np.pi*e_cr*AR_w)

CL_bestRange = get_C_L_bestRange(CD0,k_cr)
V_bestRange = get_V_bestRange(W_cruise_i,h_cruise,S_w,k_cr,CD0) #ft/s
#get_cruisefuelFraction(20,Range,W_cruise_i,h_cruise,S_w,k_cr,CD0,ct_cruise)

#testFuelBurn = getFuelBurn(h_cruise,v_cruise,S_w,CD0,k_cr,52970,ct_cruise,Range)
print("\n\nFuel burn for test aircraft")
closedFuelBurn,closedFuelFrac  = getFuelBurn(h_cruise,v_cruise,S_w,CD0,k_cr,W_cruise_i,ct_cruise,Range)
print("Test Fuel Burn: ",closedFuelBurn,"lbs")
breguetFuelFrac = breguetFraction(Range,ct_cruise,v_cruise,L_D_max)
exponentialFuelBurn,exponentialFuelFrac = BreguetExponential(200,h_cruise,S_w,CD0,k_cr,W_cruise_i,ct_cruise,Range)
print("Fuel fraction (breguet): ",breguetFuelFrac)
print("Fuel fraction (closed equation): ",closedFuelFrac)
print("Fuel fraction (exponential): ",exponentialFuelFrac)
print("Fuel burned (breguet): ",(1-breguetFuelFrac)*W_cruise_i,"lbs")
print("Fuel burned (closed equation): ",closedFuelBurn,"lbs")
print("Fuel burned (exponential): ",exponentialFuelBurn,"lbs")


# cruise_heights = np.linspace(0,40000)
# cruiseFuelFractions=np.zeros(len(cruise_heights))
# for i in range(len(cruise_heights)):
#     cruiseFuelFractions[i] = discretizedBreguet(20,cruise_heights[i],v_cruise,S_w,CD0,k_cr,52970,ct_cruise,Range)

# import matplotlib.pyplot as plt
# plt.figure(figsize=(12, 8))
# plt.plot(cruise_heights,cruiseFuelFractions, color='darkgreen', linewidth=2, label='1000 nm range')
# plt.xlabel('Cruise Altitude (ft)', fontsize=18)
# plt.ylabel('Cruise Fuel Fraction', fontsize=18)
# plt.title('1000 nm Cruise Altitude vs Fuel Fraction', fontsize=20)
# plt.grid(True, alpha=0.4)
# plt.legend(fontsize=14, loc='upper right')
# plt.show()

#k_test = 1/(np.pi*AR*e)
#print("k_cr = ",k_cr)
#print("C_L_cruise: ",CL_bestRange)
#print("density at",h_cruise,"ft: ",rho_range,"slugs / ft^3")
#print("speed of sound at cruise (40000 ft): ",a_range,"ft/s")
#print("Thrust ratio at",h_cruise,"ft: ",Tratio(h_cruise))
#print("Max dry thrust at",h_cruise,"ft",Tratio(h_cruise)*26000)
#V_bestRange = get_V_bestRange(W_cruise_i,30000,S_w,k_cr,CD0) #ft/s
#print("V_best_range (at",h_cruise,"ft):",V_bestRange,"ft/s")
#print("Ma_cruise (at",h_cruise,"ft):",V_bestRange/a_range)
#print("cruise weight fraction: ",cruise)

topSpeed = 2000 #ft/s
velo = np.linspace(0,topSpeed)
Drag = (1/2)*(rho_range)*(velo)**2*(S_w)*(CD0+k_cr*CL_bestRange**2)


# import matplotlib.pyplot as plt
# plt.figure(figsize=(12, 8))
# plt.plot(velo,Drag, color='darkgreen', linewidth=2, label='Thrust Required')
# plt.axhline(44000*Tratio(40000), color='blue', linewidth=2, label='Thrust Available (Wet)')
# plt.axhline(26000*Tratio(40000), color='red', linewidth=2, label='Thrust Available (Dry)')
# plt.xlabel('Velocity (ft/s)', fontsize=18)
# plt.ylabel('Thrust Required', fontsize=18)
# plt.title('Cruise Thrust Requirement', fontsize=20)
# plt.grid(True, alpha=0.4)
# plt.legend(fontsize=14, loc='upper right')
# plt.xlim(0, topSpeed)
# plt.ylim(0, 44000*Tratio(40000)+1000)  
# plt.show()

# plt.figure(figsize=(12, 8))
# plt.plot(ft_s_to_knots(velo)/573,Drag, color='darkgreen', linewidth=2, label='Thrust Required')
# plt.axhline(44000*Tratio(40000), color='blue', linewidth=2, label='Thrust Available (Wet)')
# plt.axhline(26000*Tratio(40000), color='red', linewidth=2, label='Thrust Available (Dry)')
# plt.xlabel('Mach Number', fontsize=18)
# plt.ylabel('Thrust Required', fontsize=18)
# plt.title('Cruise Thrust Requirement', fontsize=20)
# plt.grid(True, alpha=0.4)
# plt.legend(fontsize=14, loc='upper right')
# plt.xlim(0,ft_s_to_knots(topSpeed)/573)
# plt.ylim(0, 44000*Tratio(40000)+1000)  
# plt.show()


