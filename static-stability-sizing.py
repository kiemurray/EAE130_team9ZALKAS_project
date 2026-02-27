import numpy as np
import matplotlib.pyplot as plt
import math
import code_variables as cv

def m_to_ft(m):
    return m * 3.28084
def sqm_to_sqft(sq_m):
    return sq_m * 10.7639

# empennage sizing
# given values for vertical tail
c_vt = cv.c_vt # vertical tail volume coefficient
L_vt = cv.L_vt # vertical tail moment arm (ft)

# given values for wing
b_w = m_to_ft(60.9)         # wing span tip-to-tip (m) ---> (ft)
c_w = m_to_ft(8.75)         # wing chord (ft)
S_w = sqm_to_sqft(427.8)    # wing area (m^2) -----> (ft^2)

# given values for horizontal tail
c_ht = 0.891        # horizontal tail volume coefficient
L_ht = m_to_ft(32.95)   # horizontal tail moment arm (m) ----> (ft)

S_vt = cv.S_vt      # estimated vertical tail area (ft^2)
S_ht = cv.S_ht       # estimated horizontal tail area (ft^2)

# S_vt_actual = sqm_to_sqft(53.23)    # actual vertical tail area (m^2) ----> (ft^2)
# S_ht_actual = sqm_to_sqft(101.26)   # actual horizontal tail area ""

print("Estimated Vertical Tail Area = {} ft^2".format(S_vt))
# print("Actual Vertical Tail Area = {} ft^2".format(S_vt_actual))
print("Estimated Horizontal Tail Area = {} ft^2".format(S_ht))
# print("Actual Horizontal Tail Area = {} ft^2".format(S_ht_actual))


AR_w = cv.AR_w # Aspect ratio of wing
lambda_w = math.radians(cv.lambda_w)   # Sweep angle of wing (radians)

AR_h = cv.AR_h # Aspect ratio of horizontal stabilizer 
lambda_h = math.radians(cv.lambda_h)     # Sweep angle of horizontal tail (radians)

eta_w = cv.eta_w    # Difference factor between the theoretical section lift curve slope for the wing
eta_h = cv.eta_h     # Difference factor between th theoretical section lift curve slope for the horizontal tail

M = cv.M_cruise    # Mach number

def lift_curve_slope(AR,eta,lambda_,Ma):
    CL = (2 * np.pi * AR)/(((2) + (np.sqrt((((AR / eta)**2) * (1 + (np.tan(lambda_))**2 - Ma**2)) + (4)))))
    return CL

CL_a_w = lift_curve_slope(AR_w,eta_w,lambda_w,M)
CL_a_h0 = lift_curve_slope(AR_h,eta_h,lambda_h,M)

print("Lift curve slope of wing = {} / radian".format(CL_a_w))
print("Lift curve slope of horizontal tail = {} / radian".format(CL_a_h0))

de_dalpha = 2 * CL_a_w / (np.pi * AR_w)
print('Downwash: %.3f / radian' %de_dalpha)

CL_a_h = CL_a_h0 / (1 - de_dalpha)
print("Lift curve slope of horizontal tail corrected for downwash = {} / radian".format(CL_a_h))

Kf = 0.344      # Empirical factor (assumed)
Lf = cv.Lf     # Fuselage Length (ft)
Wf = cv.Wid_fuse       # maximum width of fuselage (ft)

dCmf_dCL = (Kf * (Wf ** 2) * Lf) / (S_w * c_w * CL_a_w)
print("dCmf_dCL = {}".format(dCmf_dCL))


# x_cg = cv.x_cg          # Aircraft center of gravity (ft) assumed
# x_25MAC = cv.x_25MAC    # Distance from nose to 25% MAC (ft) assumed

# SM = (x_cg-x_25MAC) / (c_w) - (CL_a_h * S_ht * L_ht) / (CL_a_w * S_w * c_w) + dCmf_dCL
# print("SM = {}".format(-SM))

