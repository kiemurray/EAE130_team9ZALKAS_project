import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv


CL_clean = np.linspace(-cv.CLmax_TO, cv.CLmax_TO, 500)
CL_landing = np.linspace(-cv.CLmax_L, cv.CLmax_L, 500)
print('start')
#CLEAN
CDo_cl = 0.01124
e_cl = 0.71
CD_cl = CDo_cl + (1/((3.14)*(e_cl)*(cv.AR_w)))*np.square(CL_clean)
print((1/((3.14)*(e_cl)*(cv.AR_w))))

#TAKEOFF / GEAR UP
CDO_tkup = CDo_cl + 0.015
print(CDO_tkup)
e_tk = 0.63
CD_tkup = CDO_tkup + (1/((3.14)*(e_tk)*(cv.AR_w)))*np.square(CL_clean)
print((1/((3.14)*(e_tk)*(cv.AR_w))))

#TAKEOFF / GEAR DOWN
CDO_tkdwn = CDo_cl + 0.015 + 0.020
print(CDO_tkdwn)
e_tk = 0.63
CD_tkdwn = CDO_tkdwn + (1/((3.14)*(e_tk)*(cv.AR_w)))*np.square(CL_clean)
print((1/((3.14)*(e_tk)*(cv.AR_w))))

#LANDING / GEAR UP
CDO_lndup = CDo_cl + 0.065
print(CDO_lndup)
e_lnd = 0.50
CD_lndup = CDO_lndup + (1/((3.14)*(e_lnd)*(cv.AR_w)))*np.square(CL_landing)
print(1/((3.14)*(e_lnd)*(cv.AR_w)))

#LANDING / GEAR DOWN
CDO_lndwn = CDo_cl + 0.065 + 0.020
print(CDO_lndwn)
e_lnd = 0.50
CD_lndwn = CDO_lndwn + (1/((3.14)*(e_lnd)*(cv.AR_w)))*np.square(CL_landing)
print(1/((3.14)*(e_lnd)*(cv.AR_w)))

#PLOTTING
plt.figure(figsize=(8,7))
plt.plot(CD_cl, CL_clean, label = "Clean")
plt.plot(CD_tkup, CL_clean, label = "Takeoff / Gears Up")
plt.plot(CD_tkdwn, CL_clean, label = "Takeoff / Gears Down")
plt.plot(CD_lndup, CL_landing, label = "Landing / Gears Up")
plt.plot(CD_lndwn, CL_landing, label = "Landing / Gears Down")
plt.legend()
plt.legend(loc="best", fontsize=14)
plt.xlim(0, 1.2)
plt.ylim(-2.1, 2.1)
plt.title("Preliminary Drag Polar Plot", fontsize=26)
plt.xlabel("$C_D$", fontsize=20)
plt.ylabel("$C_L$", fontsize=20)
plt.show()