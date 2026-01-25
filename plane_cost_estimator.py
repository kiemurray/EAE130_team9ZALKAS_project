import numpy as np

#Inputs
We = 37018              #Empty weight (lb) 
Tmax = 41000             #Engine max thrust lbs
Neng = 1                 #Number of engines per aircraft

Tturbine_inlet = 4060    #Turbine inlet temperature Rankine 
Vmax = 1050              #Maximum velocity (knots)
Q = 500                  #Production quantity
FTA = 4                  #Number of flight test aircraft
Mmax = 1.8               #Max Mach number of aircraft

#Labor costs wrapped rate (includes benefits and overhead) in 2026$(raymer)
CPI_1986_to_2026 = 2.94
RE = 59.10*CPI_1986_to_2026    #Engineering rate
RT = 60.70*CPI_1986_to_2026    #Tooling rate
RM = 55.40*CPI_1986_to_2026    #Manufacturing rate
RQC = 50.10*CPI_1986_to_2026   #QC rate
print(f"\nRE: {RE:.2f} $/hr")
print(f"RT: {RT:.2f} $/hr")
print(f"RM: {RM:.2f} $/hr")
print(f"RQC:{RQC:.2f} $/hr")


#Estimated avionics cost 
Cavionics = 40e6   #current money
#Cavionics = 2000*2500*CPI_1986_to_2026 #$2000/lb FY86(raymer txtbook estimation but seems too low) should be up to 25% of flyway cost

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
material_fudge_factor = 1.5 #covers complexity of non aluminum parts (raymer)
C_eng_hours = HE * RE * material_fudge_factor
C_tool_hours = HT * RT * material_fudge_factor
C_mfg_hours  = HM * RM * material_fudge_factor
C_QC_hours   = HQC * RM * material_fudge_factor

#Engine production cost 
Ceng = 20.4*1e6 #actual F135 engine price
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
complexity_factor = 1.5 #covers software dev, program management, other factors not covered by dapca method
investment_cost_factor = 1.2 #from raymer, profit margin
RDTE = C_eng_hours+ CF + CD + C_tool_hours
RDTE *= complexity_factor
flyaway_unit = (C_mfg_hours/Q + C_QC_hours/Q + Ceng + Cavionics + CM/Q) * investment_cost_factor
#unit = (RDTE + 500*flyaway_unit)/500 *investment_cost_factor (doesnt apply for military)
print(f"\nRDT&E cost:   ${RDTE/1e9:.2f} billion")
print(f"Flyaway cost: ${flyaway_unit/1e6:.2f} million/unit")







