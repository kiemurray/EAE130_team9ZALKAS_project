import numpy as np

CL_max_clean = 0.9
S_ref = 685

def get_dCL_max(dCl_max, S_flapped, lambda_HL_deg):
    dCL_max = 0.9*dCl_max*(S_flapped/S_ref)*np.cos(np.radians(lambda_HL_deg))
    return dCL_max

# FLAPS
dCl_max_plain_flap = 0.9
S_flapped_flap = 585
lambda_HL_flap = 10
dCL_max_flap = get_dCL_max(dCl_max_plain_flap, S_flapped_flap, lambda_HL_flap)
print(dCL_max_flap)

# SLATS
cprime_c = 1.1 #revisit, ratio of c'/c
dCl_max_slat = 0.4 * cprime_c
S_flapped_slat = 580
lambda_HL_slat = 45
dCL_max_slat = get_dCL_max(dCl_max_slat, S_flapped_slat, lambda_HL_slat)
print(dCL_max_slat)

# TOTAL CL_MAX
CL_max_landing = CL_max_clean + dCL_max_flap + dCL_max_slat 
print(CL_max_landing)