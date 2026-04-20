import numpy as np
import code_variables as cv

CD0 = cv.CD0
S_w = cv.S_w
c = cv.c_w


#Flap Drag
delta_CD_flaps = 1.7*(c_f/c)**(1.38)*(S_f/S_w)*(np.sin(delta_flap))**2 #plain and split flap


delta_CD_flaps = 0 #MSES or experimental data
C_D_trim = 0 #known trim state
C_D_wave = 0 #VSP Aero
C_D_induced = 0 #VSPAero / AVL

C_D_wave_mach2 = 0.0246
C_D_wave_mach1_6 = 0.0276


C_D = CD0 + delta_CD_flaps + C_D_trim + C_D_wave + C_D_induced