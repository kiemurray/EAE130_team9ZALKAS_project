import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv

#Inputs
W0 = 54307#cv.W_TO
We = W0*(2.34*W0**-0.13)*1.04 #Empty weight for fighter using Raymer table 3.1
print(f"Empty Weight: {We} lbs")
Neng = 2                      #Number of engines per aircraft

#F414 info
Tmax = 28500/2#22000                  #Engine max thrust lbs F414
Tturbine_inlet = 3060         #Turbine inlet temperature Rankine 
Vmax = 1178.6                 #Maximum velocity (knots) Ma 2.0 at 30k ft
Q = 500                       #Production quantity [RFP]
FTA = 10                      #Number of flight test aircraft
Mmax = 2.0                    #Max Mach number of aircraft [RFP]

#Labor costs wrapped rate (includes benefits and overhead) in 2026$ [Raymer]
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
W_avionics = 2500   #lbs [RFP]
Cavionics = W_avionics*2000*CPI_1986_to_2026 #$2000/lb FY86 [Raymer] should be up to 25% of flyway cost

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
material_fudge_factor = 2.0 #covers complexity of non aluminum parts (raymer)
C_eng_hours = HE * RE * material_fudge_factor
C_tool_hours = HT * RT * material_fudge_factor
C_mfg_hours  = HM * RM * material_fudge_factor
C_QC_hours   = HQC * RQC * material_fudge_factor

#Engine production cost 
#Ceng = 10*1e6 #approximate F414 engine price
Ceng= 1548*(0.0437*Tmax + 243.25*Mmax +0.969*Tturbine_inlet-2228)    #[raymer]
Ceng_total = Ceng * Neng
print(f"\nEngine production cost per engine: ${Ceng/1e6:.2f} million")
print(f"Total engine cost per aircraft:    ${Ceng_total/1e6:.2f} million")

# Non-labor Costs
C_Dev = (45.42 * We**0.63 * Vmax**1.3) * CPI_1986_to_2026                             #Development support cost 
C_Flight_test = (1243.03 * We**0.325 * Vmax**0.822 * FTA**1.21) * CPI_1986_to_2026    #Flight test cost 
C_Material = (11.0 * We**0.921 * Vmax**0.621 * Q**0.799) * CPI_1986_to_2026           #Manufacturing materials cost
print(f"\nDevelopment support cost: ${C_Dev/1e6:.2f} million")
print(f"Flight test cost:         ${C_Flight_test/1e6:.2f} million")
print(f"Materials cost:           ${C_Material/1e6:.2f} million")

#need to find RDTE and unit costs still:
investment_cost_factor = 1.15 #from raymer, profit margin
RDTE = C_eng_hours+ C_Flight_test + C_Dev + C_tool_hours
flyaway_unit = C_mfg_hours/Q + C_QC_hours/Q + Ceng_total + Cavionics + C_Material/Q 
unit_procurement =  (C_mfg_hours/Q + C_QC_hours/Q + Ceng_total + Cavionics + C_Material/Q) * investment_cost_factor
print(f"\nRDT&E cost:   ${RDTE/1e9:.2f} billion")
print(f"Flyaway cost: ${flyaway_unit/1e6:.2f} million/unit")
print(f"Unit procurement cost: ${unit_procurement/1e6:.2f} million/unit")


# Per-unit cost components (including investment factor)
material_unit = investment_cost_factor * C_Material / Q
qc_unit = investment_cost_factor * C_QC_hours / Q
manufacturing_unit = investment_cost_factor * C_mfg_hours / Q
engine_unit = investment_cost_factor * Ceng_total
avionics_unit = investment_cost_factor * Cavionics

print(f"Material cost: ${material_unit/1e6:.2f} million/unit")
print(f"QC cost: ${qc_unit/1e6:.2f} million/unit")
print(f"Manufacturing cost: ${manufacturing_unit/1e6:.2f} million/unit")
print(f"Engine cost: ${engine_unit/1e6:.2f} million/unit")
print(f"Avionics cost: ${avionics_unit/1e6:.2f} million/unit")

labels = [
    "Materials",
    "QC Labor",
    "Manufacturing Labor",
    "Engines",
    "Avionics"
]

sizes = [
    material_unit,
    qc_unit,
    manufacturing_unit,
    engine_unit,
    avionics_unit
]

colors = [
    "#7BA8C9",  
    "#7CC79D", 
    "#C89ED9",  
    "#FF8F85", 
    "#FFD27A"   
]


# Function to show percent + cost
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = pct * total / 100
        return f"{pct:.1f}%\n(${val/1e6:.1f}M)"
    return my_format

plt.figure(figsize=(8,8))

plt.pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct=autopct_format(sizes),
    startangle=90,
    pctdistance=0.75,
    textprops={'fontsize':15}
)

plt.title("Unit Procurement Cost Breakdown", fontsize=18, weight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()




# DOC/O&M cost
flight_hours = 400 #FH/YR/AC
maintainance_hours = 12.5 #MMH/FH
