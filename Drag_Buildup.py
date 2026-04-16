import numpy as np
import code_variables as cv

CD0_old = cv.CD0
S_w = cv.S_w


#sum up all the component skin friction, form, interference factors

class components:
    def __init__(self):
    def __init__(self,C_f,F,F_c,Q_c,S_wet):
        self.C_f = C_f #skin friction coefficient
        self.F = F #no idea
        self.F_c = F_c #form factor
        self.Q_c = Q_c #interference factor
        self.S_wet = S_wet #wetted area

    def getDrag(self):
        self.drag = self.C_f*self.F*self.F_c*self.Q_c*self.S_wet
    
# component_1 = components(*insert whatever)
component_1 = components()
component_2 = components()
component_3 = components()

componentList = [component_1,component_2,component_3]

componentDrag = 0

#should return the total component drag
for component in componentList:
    componentDrag = componentDrag + component.getDrag()

C_D_missing = 0
C_D_leak = 0
C_D_wave = 0

C_D_0_new = (1/S_w)*(componentDrag) + C_D_missing + C_D_leak + C_D_wave
