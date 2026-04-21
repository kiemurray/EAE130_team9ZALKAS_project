import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv
import design_space as ds

#constants
e = 0.7    # need to come back
v = cv.v_cruise      # v_cruise?
rho = cv.rho_cruise

#const line values
AR_list = [2, 3, 4, 5]
CD0_list = [0.01, 0.015, 0.02, 0.025]

def get_LD_max(AR, CD0):
    LD_max = 0.5 * np.sqrt(np.pi*AR*e/CD0)
    return LD_max

def get_WS(AR, CD0):
    CL = np.sqrt(CD0 * np.pi * AR * e)
    WS = 0.5 * rho * v**2 * CL
    return WS

plt.figure(figsize=(8,6))

#const AR, changing CD0
for AR in AR_list:
    WS_vals = []
    LD_vals = []
    
    for CD0 in CD0_list:
        LD_max = get_LD_max(AR, CD0)
        WS = get_WS(AR, CD0)

        WS_vals.append(WS)
        LD_vals.append(LD_max)
    
    plt.plot(WS_vals, LD_vals)


#const CD0, changing AR
for CD0 in CD0_list:
    WS_vals = []
    LD_vals = []

    for AR in AR_list:
        LD_max = get_LD_max(AR, CD0)
        WS = get_WS(AR, CD0)

        WS_vals.append(WS)
        LD_vals.append(LD_max)

    plt.plot(WS_vals, LD_vals)


#plot labels
plt.xlabel('W/S (lbf/ft^2)')
plt.ylabel('L/D max')
plt.title('Carpet Plot: W/S vs L/Dmax')

plt.legend()
plt.grid(True)
plt.show()