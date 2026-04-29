import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv
import Class_II_Weights as c2w

# parameters
v = cv.knots_to_ft_per_s(cv.v_cruise)      
ct = cv.ct_cruise / 3600        #converts to sec     
print(ct)    
rho = cv.rho_cruise
S = cv.S_w
AR = cv.AR_w
e = cv.e_cr
CD0 = cv.CD0

W_TO = cv.W_TO        # typical TO weight 


def get_deadload_endspeed(W_TO):
    W1 = 72000
    W2 = 90000
    v1 = cv.knots_to_ft_per_s(146)
    v2 = cv.knots_to_ft_per_s(132)
    m = (v2-v1)/(W2-W1)
    v_endspeed = m*(W_TO - W1) + v1
    return v_endspeed

#Payload weights
W_max_payload = cv.strike_payload + 10000
W_payload_max_fuel = cv.strike_payload 

#Fuel weights
W_480gal_tank = 310
W_480gal_fuel = 3264

W_330gal_tank = 290
W_330gal_fuel = 2244


fuel_tanks = [c2w.tank_1_w,
              c2w.tank_2_w,
              c2w.tank_34_w,
              c2w.tank_5_w,
              c2w.tank_6_w,
              c2w.tank_78_w,
              c2w.wing_tank_w]


W_fuel_internal = np.sum(fuel_tanks)  
W_reserve_fuel = 0.1 * W_fuel_internal
W_max_fuel = W_fuel_internal - W_reserve_fuel + 2*W_480gal_fuel + 2*W_330gal_fuel
W_fuel_max_payload = W_fuel_internal - W_reserve_fuel
W_max_fuel -= W_reserve_fuel

print(f"usable int fuel: {W_fuel_max_payload} lbs")
print(f"usable ext fuel: {2*W_480gal_fuel + 2*W_330gal_fuel} lbs")
print(f"reserve fuel: {W_reserve_fuel} lbs")

print(f"int payload: {W_payload_max_fuel} lbs")
print(f"a2a payload: {cv.a2a_payload} lbs")

W_OEW = 29445                 #from A1 table 3

def get_CL(W0, W1):
    W = (W0 + W1) / 2
    CL = 2 * W / (S * rho * v**2)
    return CL

def get_CD(CL, dirty):
    CD = CD0  + CL**2 / (np.pi*AR*e)
    CD = CD + CD*0.5*dirty
    return CD

def jet_range(W0, W1, dirty):
    CL = get_CL(W0, W1)
    CD = get_CD(CL, dirty)
    print(CD)
    R =2*np.sqrt(2/(rho*S)) * 1/ct * np.sqrt(CL)/CD * (np.sqrt(W0) - np.sqrt(W1))
    return 0.000164579*R


# Point A
R_A = 0

# Point B
W0_B = W_OEW + W_reserve_fuel + W_max_payload + W_fuel_max_payload
W1_B = W_OEW + W_reserve_fuel + W_max_payload
vb = get_deadload_endspeed(W0_B)
print(f"W0_B takeoff speed: {vb:.1f} ft/s")
R_B = jet_range(W0_B, W1_B, dirty = True)
print(f"RB = {R_B:.1f} nm")


# Point C
W0_C = W_OEW + W_reserve_fuel + W_payload_max_fuel + W_max_fuel + 2*W_480gal_tank + 2*W_330gal_tank
W1_C = W_OEW + W_reserve_fuel + W_payload_max_fuel
vc = get_deadload_endspeed(W0_C)
print(f"W0_C takeoff speed: {vc:.1f} ft/s")
R_C = jet_range(W0_C, W1_C, dirty = True)
print(f"RC = {R_C:.1f} nm")

# Point D
W0_D = W_OEW + W_reserve_fuel + W_max_fuel + 2*W_480gal_tank + 2*W_330gal_tank
W1_D = W_OEW + W_reserve_fuel
vd = get_deadload_endspeed(W0_D)
print(f"W0_D takeoff speed: {vd:.1f} ft/s")
R_D = jet_range(W0_D, W1_D, dirty = True)
print(f"RD = {R_D:.1f} nm")

# Point S (strike)
W0_strike = W_OEW + W_reserve_fuel + cv.strike_payload + W_fuel_max_payload
W1_strike = W_OEW + W_reserve_fuel + cv.strike_payload 
R_strike = jet_range(W0_strike, W1_strike, dirty = False)
R_strike = 2000
W_payload_strike = cv.strike_payload

# # Point A2A (air-to-air)
# W0_a2a = W_OEW + W_reserve_fuel + cv.a2a_payload + W_fuel_max_payload
# W1_a2a = W_OEW + W_reserve_fuel + cv.a2a_payload
# R_a2a = jet_range(W0_a2a, W1_a2a, CD0, 0)
# W_payload_a2a = cv.a2a_payload


# data for plotting
ranges =  np.array([R_A, R_B, R_C, R_D])  # nautical miles
payloads = [W_max_payload, W_max_payload, W_payload_max_fuel, 0]


plt.figure(figsize=(10, 7))

plt.plot(ranges, payloads, color='black', marker='o', linewidth=2, markersize=8, clip_on=False)
plt.plot(R_strike, W_payload_strike, color='red', marker='*', linewidth=2, markersize=8)

# labels
plt.xlabel('Range (nm)', fontsize=14)
plt.ylabel('Payload Weight (lbf)', fontsize=14)
plt.title('Payload-Range Diagram', fontsize=16, fontweight='bold')

# origin at 0,0
plt.xlim(left=0)
plt.ylim(bottom=0)

# Grid styling
plt.grid(True, linestyle='--', linewidth=0.6, alpha=0.7)

# Tick size
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Annotate points with slight offset for readability
offset_x = max(ranges) * 0.01
offset_y = max(payloads) * 0.02

#lables w offset so it doesnt get covered up
plt.text(ranges[0]+10, payloads[0]+200, ' A', fontsize=12, fontweight='bold')
plt.text(ranges[1]+10, payloads[1]+200, ' B', fontsize=12, fontweight='bold')
plt.text(ranges[2]+10, payloads[2]+200, ' C', fontsize=12, fontweight='bold')
plt.text(ranges[3]+10, payloads[3]+200, ' D', fontsize=12, fontweight='bold')
plt.text(R_strike+10, W_payload_strike+200, ' Strike', fontsize=12, fontweight='bold')

plt.show()
