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

W_OEW = 29445                 #from A1 table 3

#functions
def dCD0_dirty(n_tanks):
    Doverq = 1.0
    dCD0 = Doverq / S * n_tanks
    return dCD0

def get_CL(W0, W1):
    W = (W0 + W1) / 2
    CL = 2 * W / (S * rho * v**2)
    return CL

def get_CD(CL, CD0, n_tanks):
    CD = CD0 + dCD0_dirty(n_tanks) + CL**2 / (np.pi*AR*e)
    return CD

def jet_range(W0, W1, CD0, n_tanks):
    CL = get_CL(W0, W1)
    CD = get_CD(CL, CD0, n_tanks)
    return 2*np.sqrt(2/(rho*S)) * 1/ct * np.sqrt(CL)/CD * (np.sqrt(W0) - np.sqrt(W1))


# Point A
R_A = 0

# Point B
W0_B = W_OEW + W_reserve_fuel + W_max_payload + W_fuel_max_payload
W1_B = W_OEW + W_reserve_fuel + W_max_payload

R_B = jet_range(W0_B, W1_B, CD0, 4)

# Point C
W0_C = W_OEW + W_reserve_fuel + W_payload_max_fuel + W_max_fuel + 2*W_480gal_tank + 2*W_330gal_tank
W1_C = W_OEW + W_reserve_fuel + W_payload_max_fuel
R_C = jet_range(W0_C, W1_C, CD0, 4)

# Point D
W0_D = W_OEW + W_reserve_fuel + W_max_fuel + 2*W_480gal_tank + 2*W_330gal_tank
W1_D = W_OEW + W_reserve_fuel
R_D = jet_range(W0_D, W1_D, CD0, 4)

# Point S (strike)
W0_strike = W_OEW + W_reserve_fuel + cv.strike_payload + W_fuel_max_payload
W1_strike = W_OEW + W_reserve_fuel + cv.strike_payload 
R_strike = jet_range(W0_strike, W1_strike, CD0, 0)
W_payload_strike = cv.strike_payload

# Point A2A (air-to-air)
W0_a2a = W_OEW + W_reserve_fuel + cv.a2a_payload + W_fuel_max_payload
W1_a2a = W_OEW + W_reserve_fuel + cv.a2a_payload
R_a2a = jet_range(W0_a2a, W1_a2a, CD0, 0)
W_payload_a2a = cv.a2a_payload

# plotting
ranges = 0.000164579 * np.array([R_A, R_B, R_C, R_D]) #nautical miles
payloads = [W_max_payload, W_max_payload, W_payload_max_fuel, 0]

plt.figure(figsize=(8,6))
plt.plot(ranges, payloads, 'k-o')
plt.plot(R_strike*0.000164579, W_payload_strike, 'k-o')
plt.plot(R_a2a*0.000164579, W_payload_a2a, 'k-o')


# Labels
plt.xlabel('Range (nm)') 
plt.ylabel('Payload Weight (lbf)')
plt.title('Payload-Range Diagram')

plt.grid(True)

# annotate points
plt.text(ranges[0], payloads[0], ' A')
plt.text(ranges[1], payloads[1], ' B')
plt.text(ranges[2], payloads[2], ' C')
plt.text(ranges[3], payloads[3], ' D')
plt.text(R_strike*0.000164579, W_payload_strike, ' Strike')
plt.text(R_a2a*0.000164579, W_payload_a2a, ' Air-to-Air')

plt.show()