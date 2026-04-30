import numpy as np
import code_variables as cv
import matplotlib.pyplot as plt

y = [ 6.2006, 7.0408, 7.8728, 8.6970, 9.5138, 10.3233, 11.1260, 11.9220, 12.7116, 13.4951, 14.2727, 15.0446, 15.8112, 16.5726, 17.3268, 18.0245, 18.6333, 19.1792, 19.6807, 20.1518, 20.6036, 21.0456, 21.4866, 21.9352, 22.4006, 22.8937, 23.4274]

c = [ 25.7143, 24.4868, 23.2711, 22.0668, 20.8734, 19.6906, 18.5178, 17.3548, 16.2010, 15.0563, 13.9201, 12.7922, 11.6722, 10.5597, 9.8590, 9.5868, 9.3492, 9.1362, 8.9405, 8.7566, 8.5803, 8.4079, 8.2358, 8.0607, 7.8791, 7.6867, 7.4784]

q = 0.5*cv.rho_sl*cv.V_TO**2
# Section lift coefficient, averaged across all 14 alpha cases (1° to 12°)
cl_avg = [ 0.20526,  0.32908,  0.33192,  0.38061,  0.41146,
          0.44058,  0.45177,  0.46774,  0.49529,  0.50752,  0.55687,
          0.58246,  0.61875,  0.70245,  0.76539,  0.54394,  0.83429,
          0.66246,  0.62588,  0.61378,  0.52100,  0.83315,  0.56414,
          0.91631,  0.66672,  0.39907,  0.51742]
# Section drag coefficient, averaged across all 14 alpha cases (1° to 12°)
cd_avg = [ -0.03856,  0.01720,  0.01924,  0.01498,  0.01535,
           0.00226,  0.00186, -0.00277, -0.01048, -0.02152, -0.04528,
          -0.05834, -0.10134, -0.24597, -0.33822,  0.03088,  0.09665,
           0.10569,  0.06547,  0.04564,  0.06692,  0.07451,  0.21767,
           0.25654,  0.28150,  0.18610,  0.14376]
# Section pitching moment coefficient (cm∞), averaged across all 14 alpha cases (1° to 12°)
cm_inf = [  0.16284,  0.10681,  0.11098,  0.09778,  0.08923,
           0.08526,  0.07867,  0.07424,  0.07182,  0.06146,  0.05542,
           0.04644,  0.03142,  0.01966, -0.03135, -0.08441, -0.09164,
          -0.13683, -0.16124, -0.17088, -0.17209, -0.25250, -0.23373,
          -0.40591, -0.32889, -0.21214, -0.35191]
# Side force coefficient (cs = cy, wind/body axes identical for beta=0)
cs_avg = [ -0.06810, -0.00763, -0.00051,  0.00553,  0.00466,
          0.01080,  0.01152,  0.01518,  0.02187,  0.02370,  0.03477,
          0.03915,  0.04679,  0.03903,  0.04778,  0.00633, -0.05212,
         -0.06413, -0.03071, -0.02670, -0.05656, -0.06553, -0.21652,
         -0.24418, -0.26092, -0.15452, -1.62481]

# Body-axis X force coefficient (axial/drag direction)
cx_avg = [ -0.08255, -0.03222, -0.03265, -0.04092, -0.04361,
          -0.06037, -0.06250, -0.06938, -0.08046, -0.09371, -0.12397,
          -0.14104, -0.18873, -0.33906, -0.44506, -0.06341, -0.00038,
           0.01106, -0.02805, -0.04483, -0.02045, -0.01448,  0.13678,
           0.17363,  0.20939,  0.12768,  0.07551]

# Body-axis Y force coefficient (= cs for beta=0)
cy_avg = [ -0.06810, -0.00763, -0.00051,  0.00553,  0.00466,
          0.01080,  0.01152,  0.01518,  0.02187,  0.02370,  0.03477,
          0.03915,  0.04679,  0.03903,  0.04778,  0.00633, -0.05212,
         -0.06413, -0.03071, -0.02670, -0.05656, -0.06553, -0.21652,
         -0.24418, -0.26092, -0.15452, -1.62481]

# Body-axis Z force coefficient (normal/lift direction)
cz_avg = [  0.19741,  0.32764,  0.33068,  0.37833,  0.40901,
          0.43597,  0.44712,  0.46226,  0.48864,  0.49939,  0.54508,
          0.56837,  0.59851,  0.66080,  0.70507,  0.53789,  0.82941,
          0.65782,  0.62016,  0.60570,  0.51318,  0.82484,  0.55796,
          0.91158,  0.66309,  0.39047,  0.52020]

dLw_dy_array = []
dDw_dy_array = []
dMac_dy_array = []
dNw_dy_array = []

for i in range(len(y)):
    dLw_dy = q*c[i]*cl_avg[i]
    dDw_dy = q*c[i]*cd_avg[i]
    dMac_dy = -q*(c[i]**2)*cm_inf[i]
    dNw_dy = q*c[i]*cz_avg[i]

    dLw_dy_array.append(dLw_dy)
    dDw_dy_array.append(dDw_dy)
    dMac_dy_array.append(dMac_dy)
    dNw_dy_array.append(dNw_dy)


plt.figure(figsize=(10, 6))
plt.subplot(2, 2, 1)
plt.title('Spanwise Distribution of Load Derivatives')
plt.plot(y, dLw_dy_array, label='dLw/dy', marker='o')
plt.ylabel('Load Derivative')
plt.grid()
plt.legend()
plt.subplot(2, 2, 2)
plt.plot(y, dDw_dy_array, label='dDw/dy', marker='o')
plt.legend()
plt.grid()
plt.subplot(2, 2, 3)
plt.plot(y, dMac_dy_array, label='dMac/dy', marker='o')
plt.xlabel('Spanwise Location (y)')
plt.ylabel('Load Derivative')
plt.grid()
plt.legend()
plt.subplot(2, 2, 4)
plt.plot(y, dNw_dy_array, label='dNw/dy', marker='o')
plt.xlabel('Spanwise Location (y)')
plt.legend()
plt.grid()
plt.show()
