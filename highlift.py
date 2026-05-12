import numpy as np
import code_variables as cv

CL_max_clean = 0.9
S_ref = cv.S_w



def get_dCL_max(dCl_max, S_flapped, lambda_HL_deg):
    dCL_max = 0.9*dCl_max*(S_flapped/S_ref)*np.cos(np.radians(lambda_HL_deg))
    return dCL_max

# OUTBOARD FLAPS
dCl_max_plain_flap = 0.9
S_flapped_out = cv.A_outboard_flapped *cv.S_w
lambda_HL_flap_out = 45
dCL_max_flap_outboard = get_dCL_max(dCl_max_plain_flap, S_flapped_out, lambda_HL_flap_out)
print("dCL_max_flap_outboard:",dCL_max_flap_outboard)

#INBOARD FLAPS
dCl_max_plain_flap = 0.9
S_flapped_in = cv.A_inboard_flapped *cv.S_w
lambda_HL_flap_in = 0
dCL_max_flap_inboard = get_dCL_max(dCl_max_plain_flap, S_flapped_in, lambda_HL_flap_in)
print("dCL_max_flap_inboard:",dCL_max_flap_inboard)


# SLATS
cprime_c = 1.1 #revisit, ratio of c'/c
dCl_max_slat = 0.4 * cprime_c
S_flapped_slat = 580
lambda_HL_slat = 45
dCL_max_slat = get_dCL_max(dCl_max_slat, S_flapped_slat, lambda_HL_slat)
print("dCL_max_slat:",dCL_max_slat)

# TOTAL CL_MAX
CL_max_landing = CL_max_clean + dCL_max_flap_inboard + dCL_max_flap_outboard+ dCL_max_slat 
CL_max_takeoff = CL_max_clean + 0.7*(dCL_max_flap_inboard + dCL_max_flap_outboard+ dCL_max_slat)
print("C_L_max_landing:",CL_max_landing)
print("C_L_max_takeoff:",CL_max_takeoff)