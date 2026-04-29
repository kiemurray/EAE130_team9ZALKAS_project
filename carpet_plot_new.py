import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv
import design_space as ds

#maybe change cost and TW?


#set ranges
dash_mach_start = 1
dash_mach_end = 2.5

cost_start = 50     #million FY26
cost_end = 150      #million. FY26

#const line values
dash_list = np.arange(dash_mach_start, dash_mach_end+0.25, 0.25)
cost_list =np.arange(cost_start, cost_end+10, 10)

#plotting values
dash_plotting = np.linspace(dash_mach_start, dash_mach_end, 100)
cost_plotting = np.linspace(cost_start, cost_end, 100)

#functions

def get_WS(cost, dashspeed):
    
    return

def get_TW(cost, dashspeed, WS):
    return

plt.figure(figsize=(8,6))


#const cost, changing dash speed
for cost in cost_list:
    WS_vals = []
    TW_vals = []
    
    for dashspeed in dash_plotting:
        TW = get_TW(cost, dashspeed)
        WS = get_WS(cost, dashspeed)

        WS_vals.append(WS)
        TW_vals.append(TW)
    
    plt.plot(WS_vals, TW_vals, 'b-')

    # label at end of line
    plt.text(WS_vals[-1], TW_vals[-1], f'Cost=${cost}million', fontsize=9, color='blue')


for dashspeed in dash_list:
    WS_vals = []
    TW_vals = []

    for cost in cost_plotting:
        TW = get_TW(cost, dashspeed)
        WS = get_WS(cost, dashspeed)

        WS_vals.append(WS)
        TW_vals.append(TW)

    plt.plot(WS_vals, TW_vals)

    # label at end of line
    plt.text(WS_vals[-1], TW_vals[-1], f'Dash Speed={dashspeed:.2f}', fontsize=9, color='red')

