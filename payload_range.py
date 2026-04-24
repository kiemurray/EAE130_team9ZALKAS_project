import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv
import Class_II_Weights as c2w

#CHECK UNITS

# parameters
v = cv.knots_to_ft_per_s(cv.v_cruise)      
ct = cv.ct_cruise / 3600        #converts to sec     
print(ct)    
rho = cv.rho_cruise
S = cv.S_w
AR = cv.AR_w
e = cv.e_cr
CD0_clean = cv.CD0
print(CD0_clean)
CD0_dirty = CD0_clean + 0.02

W_MTOW = cv.W_TO + 10000      # typical TO weight + 10,000 extra store weight
W_OEW = 29445                 #from A1 table 3

W_max_payload = cv.W_payload + 10000
W_payload_max_fuel = cv.W_payload 


fuel_tanks = [c2w.tank_1_w,
              c2w.tank_2_w,
              c2w.tank_34_w,
              c2w.tank_5_w,
              c2w.tank_6_w,
              c2w.tank_78_w,
              c2w.wing_tank_w]
W_max_fuel = np.sum(fuel_tanks) + 10000
W_reserve_fuel = 5000 #REVISIT sufficient fuel for 20 minutes loiter at 10,000 ft and two landing attempts, 25% maximum fuel weight, and 50% store weight
W_fuel_max_payload = W_max_fuel - 10000

#real max fuel
W_max_fuel -= W_reserve_fuel

#functions
def CD0_dirty(n_tanks):
    Doverq = 0.7
    q = 
    D = Doverq * q
    dCD = 
    return

def get_CL(W0, W1):
    W = (W0 + W1) / 2
    CL = 2 * W / (S * rho * v**2)
    return CL

def get_CD(CL, CD0):
    CD = CD0 + CL**2 / (np.pi*AR*e)
    return CD

def jet_range(W0, W1, CD0):
    CL = get_CL(W0, W1)
    print(CL)
    CD = get_CD(CL, CD0)
    return 2*np.sqrt(2/(rho*S)) * 1/ct * np.sqrt(CL)/CD * (np.sqrt(W0) - np.sqrt(W1))


# Point A
R_A = 0

# Point B
W0_B = W_OEW + W_reserve_fuel + W_max_payload + W_fuel_max_payload
W1_B = W_OEW + W_reserve_fuel + W_max_payload

R_B = jet_range(W0_B, W1_B, CD0_dirty)

# Point C
W0_C = W_OEW + W_reserve_fuel + W_payload_max_fuel + W_max_fuel
W1_C = W_OEW + W_reserve_fuel + W_payload_max_fuel
R_C = jet_range(W0_C, W1_C, CD0_dirty)

# Point D
W0_D = W_OEW + W_reserve_fuel + W_max_fuel
W1_D = W_OEW + W_reserve_fuel
R_D = jet_range(W0_D, W1_D, CD0_dirty)


# plotting
ranges = 0.000164579 * np.array([R_A, R_B, R_C, R_D]) #nautical miles
payloads = [W_max_payload, W_max_payload, W_payload_max_fuel, 0]

plt.figure(figsize=(8,6))
plt.plot(ranges, payloads, 'k-o')

# Labels
plt.xlabel('Range (nm)') 
plt.ylabel('Payload Weight (lbf)')
plt.title('Payload-Range Diagram')

plt.grid(True)

# annotate points
plt.text(R_A, W_max_payload, ' A')
plt.text(R_B, W_max_payload, ' B')
plt.text(R_C, W_payload_max_fuel, ' C')
plt.text(R_D, 0, ' D')

plt.show()