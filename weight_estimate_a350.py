# Preliminary weight estimate example (A350-900)
# Template to adapt for A2

import numpy as np
import math

#constants
#set up
c_t = 0.52       #come back to put value from chosen engine
L_over_Dmax = 18.0 
L_over_D = L_over_Dmax*.94
endurance = 1/2 #hrs
speed = 251*1.94    #knots (251 m/s)
range = 9150    #nm 
tolerance = 1e-6            
max_iterations = 500

#payload
person = 181 #lb
luggage = 60 #lb
payload_weight = (2+12+314)*person + 314*luggage #lb
print(f"Payload weight: {payload_weight} lbs") 

# mission segment fuel fractions Wi+1/Wi (from ppt slides)
takeoff = 0.97
climb = 0.985 
landing = 0.995
cruise = math.exp(-(range)*c_t/(speed*L_over_D)) 
loiter = math.exp(-endurance*c_t/L_over_D)
print(f"cruise fuel fraction: {cruise}")
print(f"loiter fuel fraction: {loiter}")

# Initial guess for TOGW
TOGW_guess = 400000.0   #lb

# mission fuel uses: air to air or strike
final_weight_fraction = takeoff*climb*cruise*loiter*landing
fuel_fraction = 1 - final_weight_fraction
fuel_fraction *= 1.06 #reserve fuel
print(f"final fuel fraction: {fuel_fraction}")

if fuel_fraction >= 1.0:
    print("Fuel fraction exceeds 1.0. Your mission is not feasible")

# Iteration counter
iteration = 0
error = 1.0

while error > tolerance and iteration < max_iterations:
    iteration += 1

    # estimate empty weight fraction We/W0 using Raymer's method
    A = 0.97
    C = -0.06 
    empty_weight_fraction = A * (TOGW_guess ** C)
    empty_weight = empty_weight_fraction*TOGW_guess

    # compute weights
    #empty_weight = empty_weight_fraction * TOGW_guess #raymer only
    fuel_weight = fuel_fraction * TOGW_guess

    # solve for new TOGW
    TOGW_new = empty_weight + fuel_weight + payload_weight

    # error
    error = abs(TOGW_new - TOGW_guess) / TOGW_guess

    # update
    TOGW_guess = TOGW_new

# Final result
if error > tolerance:
    print("TOGW not converged")
    print(f"Unconvered TOGW: {round(TOGW_guess)}lb")
else:
    print(f"Converged TOGW: {round(TOGW_guess)}lb")
    print(f"Converged Empty Weight: {round(empty_weight)}lb")
    print("Iterations:", iteration)

