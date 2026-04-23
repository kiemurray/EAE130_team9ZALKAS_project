import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv
import design_space as ds

#constants
e = cv.e_cr   # need to come back
v = cv.v_cruise      # v_cruise?
rho = cv.rho_cruise

#set ranges
AR_start = 1
AR_end = 10

CD0_start = 0.02
CD0_end = 0.06

#const line values
AR_list = np.arange(AR_start, AR_end+1, 1)
CD0_list =np.arange(CD0_start, CD0_end+0.005, 0.005)

#plotting values
AR_plotting = np.linspace(AR_start, AR_end, 100)
CD0_plotting = np.linspace(CD0_start, CD0_end, 100)



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
    
    for CD0 in CD0_plotting:
        LD_max = get_LD_max(AR, CD0)
        WS = get_WS(AR, CD0)

        WS_vals.append(WS)
        LD_vals.append(LD_max)
    
    plt.plot(WS_vals, LD_vals, 'b-')

    # label at end of line
    plt.text(WS_vals[-1], LD_vals[-1], f'AR={AR}', fontsize=9, color='blue')


#const CD0, changing AR
for CD0 in CD0_list:
    WS_vals = []
    LD_vals = []

    for AR in AR_plotting:
        LD_max = get_LD_max(AR, CD0)
        WS = get_WS(AR, CD0)

        WS_vals.append(WS)
        LD_vals.append(LD_max)

    plt.plot(WS_vals, LD_vals)

    # label at end of line
    plt.text(WS_vals[-1], LD_vals[-1], f'CD0={CD0:.3f}', fontsize=9, color='red')


#plot labels
plt.xlabel('W/S (lbf/ft^2)')
plt.ylabel('L/D max')
plt.title('Carpet Plot: W/S vs L/Dmax')

plt.grid(True)
plt.show()