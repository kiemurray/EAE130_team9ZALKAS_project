import numpy as np
import matplotlib.pyplot as plt

CL = np.linspace(-2, 3, 500)

#Aspect Ratio
AR = 2.066

#CLEAN
CDO_cl = 0.01111
e_cl = 0.820
CD_cl = CDO_cl + (1/(3.14)*(e_cl)*(AR))*np.square(CL)

#TAKEOFF / GEAR UP
CDO_tkup = 0.02611
e_tk = 0.775
CD_tkup = CDO_tkup + (1/(3.14)*(e_tk)*(AR))*np.square(CL)

#TAKEOFF / GEAR DOWN
CDO_tkdwn = 0.04611
e_tk = 0.775
CD_tkdwn = CDO_tkdwn + (1/(3.14)*(e_tk)*(AR))*np.square(CL)

#LANDING / GEAR UP
CDO_lndup = 0.07611
e_lnd = 0.725
CD_lndup = CDO_lndup + (1/(3.14)*(e_lnd)*(AR))*np.square(CL)

#LANDING / GEAR DOWN
CDO_lndwn = 0.09611
e_lnd = 0.725
CD_lndwn = CDO_lndwn + (1/(3.14)*(e_lnd)*(AR))*np.square(CL)

#PLOTTING
plt.plot(CD_cl, CL, label = "Clean")
plt.plot(CD_tkup, CL, label = "Takeoff / Gears Up")
plt.plot(CD_tkdwn, CL, label = "Takeoff / Gears Down")
plt.plot(CD_lndup, CL, label = "Landing / Gears Up")
plt.plot(CD_lndwn, CL, label = "Landing / Gears Down")
plt.legend()
plt.legend(loc="best")
plt.xlim(0, 0.45)
plt.ylim(-1, 1)
plt.title("Drag Polar Plot")
plt.xlabel("$C_D$")
plt.ylabel("$C_L$")
plt.show()