import numpy as np
import code_variables as cv

g = cv.g 
H = 10 
l = 32 
rho = cv.rho_to 
S = cv.S_w 
CL = 0.7 * cv.CLmax_TO 
m = cv.W_TO / g 
V_min = np.sqrt(g / ((2*H / l**2) + (rho * S * CL / (2*m))))
print(V_min)