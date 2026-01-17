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

#Labor and CPI
RE = 59.10  #Engineering rate
RT = 60.7   #Tooling rate
RM = 50.1   #Manufacturing rate
RQC = 55.4  #QC rate
CPI_1986_to_2026 = 3.0 #Come back w real CPI or change to current labor rates (pick whatever is cheaper)

#Estimated avionics cost 
Cavionics = 40e6   #current money, same as superhornet

#Engineering hours 
HE = 4.86 * We**0.777 * Vmax**0.894 * Q**0.163
print(f"Engineering hours (HE): {HE:.1f} hrs")

#Tooling hours
HT = 5.99 * We**0.777 * Vmax**0.696 * Q**0.263
print(f"Tooling hours (HT): {HT:.1f} hrs")

#Manufacturing hours
HM = 7.37 * We**0.82 * Vmax**0.484 * Q**0.641
print(f"Manufacturing hours (HM): {HM:.1f} hrs")

#QC hours
HQC = 0.133 * HM
print(f"QC hours (HO): {HQC:.1f} hrs")

#Development support cost 
CD = (45.42 * We**0.63 * Vmax**1.3) * CPI_1986_to_2026
print(f"Development support cost: ${CD/1e6:.2f} million")

#Flight test cost 
CF = (1243.03 * We**0.325 * Vmax**0.822 * FTA**1.21) * CPI_1986_to_2026
print(f"Flight test cost: ${CF/1e6:.2f} million")

#Manufacturing materials cost
CM = (11.0 * We**0.921 * Vmax**0.621 * Q**0.799) * CPI_1986_to_2026
print(f"Manufacturing materials cost: ${CM/1e6:.2f} million")

#Engine production cost 
Ceng = 1548 * (0.043*Tmax + 243.25*Mmax + 0.969*Tturbine_inlet - 2228) * CPI_1986_to_2026 #should be around 20 million
print(f"Engine production cost per engine: ${Ceng/1e6:.2f} million")
Ceng_total = Ceng * Neng
print(f"Total engine cost per aircraft: ${Ceng_total/1e6:.2f} million")

#Labor costs
C_eng_hours = HE * RE * CPI_1986_to_2026
C_tool_hours = HT * RT * CPI_1986_to_2026
C_mfg_hours  = HM * RM * CPI_1986_to_2026
C_QC_hours   = HQC * RM * CPI_1986_to_2026
C_labor_tot = C_eng_hours + C_tool_hours + C_mfg_hours + C_QC_hours
print(f"Total labor cost: ${C_labor_tot/1e9:.2f} billion")

#need to find RDTE and unit costs still:
RDTE = C_eng_hours+ CF + CD + C_tool_hours
print(f"RDT&E cost: ${RDTE/1e6:.2f} million")
flyaway = C_mfg_hours + C_QC_hours + Ceng + Cavionics + CM
unit = (RDTE + 500*flyaway)/500 
print(f"unit cost: $ {unit/1e6:.2f} million")






