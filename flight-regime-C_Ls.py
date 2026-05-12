import numpy as np
import code_variables as cv

def getSpeedGivenC_L(Weight,rho,C_L,S):
    v_necessary = np.sqrt(2*Weight/(rho*C_L*S))
    return v_necessary

def getC_L_GivenSpeed(Weight,rho,v,S):
    C_L_necessary = 2*Weight/(rho*S*v**2)
    return C_L_necessary

def getSpeeds(Weight,altitude,C_L_max,S):
    rho = cv.atmo_vals(altitude)[0]
    v_stall = getSpeedGivenC_L(Weight,rho,C_L_max,S)
    print("V_stall at ",Weight,"lbs is ",cv.ft_s_to_knots(v_stall),"kts")

    print("Takeoff speed at these conditions: ",1.2*cv.ft_s_to_knots(v_stall),"kts")
    print("Required C_L: ",getC_L_GivenSpeed(Weight,rho,1.2*v_stall,S))

    print("Approach speed at these conditions: ",1.3*cv.ft_s_to_knots(v_stall),"kts")
    print("Required C_L: ",getC_L_GivenSpeed(Weight,rho,1.3*v_stall,S))


#For strike / air to air mission
getSpeeds(cv.W_TO,0,cv.CLmax_TO,cv.S_w)
getSpeeds(cv.W_TO*cv.wf_climb,40000,cv.CLmax_climb,cv.S_w)
getSpeeds(cv.W_TO*cv.wf_descent,2000,cv.CLmax_climb,cv.S_w)
getSpeeds(cv.W_TO*cv.wf_landing,0,cv.CLmax_L,cv.S_w)
getSpeeds(cv.W_TO*cv.wf_man,40000,cv.CLmax_climb,cv.S_w)