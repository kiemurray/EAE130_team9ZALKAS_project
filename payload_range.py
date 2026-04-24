import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv

#CHECK UNITS

# parameters
V = cv.v_cruise        
ct = cv.ct_cruise         
rho = cv.rho_cruise
S = cv.S_w
CL = 
CD = 

W_MTOW = 
W_OEW = 

W_max_payload = 
W_payload_max_fuel = 

W_max_fuel = 
W_reserve_fuel = 
W_fuel_max_payload = 




def jet_range(W0, W1):
    return 2*np.sqrt(2/(rho*S)) * 1/ct * np.sqrt(CL)/CD * (np.sqrt(W0) - np.sqrt(W1))

# Point A
R_A = 0

# Point B
W0_B = W_OEW + W_reserve_fuel + W_max_payload + W_fuel_max_payload
W1_B = W_OEW + W_reserve_fuel + W_max_payload
R_B = jet_range(W0_B, W1_B)

# Point C
W0_C = W_OEW + W_reserve_fuel + W_payload_max_fuel + W_max_fuel
W1_C = W_OEW + W_reserve_fuel + W_payload_max_fuel
R_C = jet_range(W0_C, W1_C)

# Point D
W0_D = W_OEW + W_reserve_fuel + W_max_fuel
W1_D = W_OEW + W_reserve_fuel
R_D = jet_range(W0_D, W1_D)



ranges = [R_A, R_B, R_C, R_D] #possibly convert to nm
payloads = [W_max_payload, W_max_payload, W_payload_max_fuel, 0]

plt.figure(figsize=(8,6))
plt.plot(ranges, payloads, 'k-o')

# Labels
plt.xlabel('Range (ft)') 
plt.ylabel('Payload Weight (lbf)')
plt.title('Payload-Range Diagram')

plt.grid(True)

# annotate points
plt.text(R_A, W_max_payload, ' A')
plt.text(R_B, W_max_payload, ' B')
plt.text(R_C, W_payload_max_fuel, ' C')
plt.text(R_D, 0, ' D')

plt.show()