import numpy as np

#Inputs
We = 30000               #Empty weight (lb) 
Vmax = 1050              #Maximum velocity (knots)
Q = 500                  #Production quantity
FTA = 4                  #Number of flight test aircraft
Mmax = 1.8               #Max Mach number of aircraft
Tmax = 41000             #Engine max thrust lbs
Tturbine_inlet = 4060    #Turbine inlet temperature Rankine 
Neng = 2                 #Number of engines per aircraft

#Labor costs in 2026$ and CPI value (labor cost using graph from slides)
year = 2026
RE = 2.576*year - 5058    #Engineering rate
RT = 2.883*year - 5666    #Tooling rate
RM = 2.316*year - 4552    #Manufacturing rate
RQC = 2.6*year - 5112     #QC rate
print(f"\nRE: {RE:.2f} $/hr")
print(f"RT: {RT:.2f} $/hr")
print(f"RM: {RM:.2f} $/hr")
print(f"RQC:{RQC:.2f} $/hr")
CPI_1986_to_2026 = 2.94

#Estimated avionics cost 
Cavionics = 40e6   #current money

#Man Hours
HE = 4.86 * We**0.777 * Vmax**0.894 * Q**0.163 #Engineering hours 
HT = 5.99 * We**0.777 * Vmax**0.696 * Q**0.263 #Tooling hours
HM = 7.37 * We**0.82 * Vmax**0.484 * Q**0.641  #Manufacturing hours
HQC = 0.133 * HM                               #QC hours
print(f"\nEngineering hours:   {HE:.1f} hrs")
print(f"Tooling hours:       {HT:.1f} hrs")
print(f"Manufacturing hours: {HM:.1f} hrs")
print(f"QC hours:            {HQC:.1f} hrs")

#Labor costs
C_eng_hours = HE * RE 
C_tool_hours = HT * RT 
C_mfg_hours  = HM * RM 
C_QC_hours   = HQC * RM 
C_labor_tot = C_eng_hours + C_tool_hours + C_mfg_hours + C_QC_hours
print(f"\nTotal labor cost: ${C_labor_tot/1e9:.2f} billion")

#Engine production cost 
Ceng = 1548 * (0.043*Tmax + 243.25*Mmax + 0.969*Tturbine_inlet - 2228) * CPI_1986_to_2026 #should be around 20 million
Ceng_total = Ceng * Neng
print(f"\nEngine production cost per engine: ${Ceng/1e6:.2f} million")
print(f"Total engine cost per aircraft:    ${Ceng_total/1e6:.2f} million")

# Non-labor Costs
CD = (45.42 * We**0.63 * Vmax**1.3) * CPI_1986_to_2026                  #Development support cost 
CF = (1243.03 * We**0.325 * Vmax**0.822 * FTA**1.21) * CPI_1986_to_2026 #Flight test cost 
CM = (11.0 * We**0.921 * Vmax**0.621 * Q**0.799) * CPI_1986_to_2026     #Manufacturing materials cost
print(f"\nDevelopment support cost: ${CD/1e6:.2f} million")
print(f"Flight test cost:         ${CF/1e6:.2f} million")
print(f"Materials cost:           ${CM/1e6:.2f} million")

#need to find RDTE and unit costs still:
RDTE = C_eng_hours+ CF + CD + C_tool_hours
modernization_factor = 1.5 #covers software dev, program management, other factors not covered by dapca method
RDTE *= modernization_factor
flyaway_unit = C_mfg_hours/Q + C_QC_hours/Q + Ceng + Cavionics + CM/Q
unit = (RDTE + 500*flyaway_unit)/500 
print(f"\nRDT&E cost:   ${RDTE/1e9:.2f} billion")
print(f"Flyaway cost: ${flyaway_unit/1e6:.2f} million/unit")
print(f"Unit cost:    ${unit/1e6:.2f} million")






