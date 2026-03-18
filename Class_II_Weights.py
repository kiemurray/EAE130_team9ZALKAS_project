import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# All Equations used are from Raymer's section on Fighter/Attack Weights

# Parameters
K_dw = 1 # Non-Delta Wing
K_vs = 1.0 # non-variable sweep
W_dg = 56631 # Design Gross Weight (lbf)
n_z = 8.0 # limit load, desired by RFP
N_z = 1.5 * n_z # Ultimate Load Factor
n_zv = 3.0 # Vertical Tail Limit Load (estimated)
N_zv = 1.5 * n_zv # Vertical Tail Limit Load
S_w = 685 # Trapezoidal Wing Area ft^2
AR = 2.46 # Aspect Ratio
tc_root = 0.06 # t/c ratio at root chord
taper_ratio = 0.295 # Taper Ratio
wing_sweep = 45 # Wing Sweep at 25% MAC
S_csw = 103 # Wing Mounted Control Surface Area ft^2
K_rht = 1.047 # Rolling Tail (Stabilators)
H_t = 0 # Horizontal Tail Height Above Fuselage
H_v = 4.5 # Vertical Tail Height Above Fuselage (this gets cancelled out anyways)
S_vt = 145 # Vertical Tail Area ft^2
M = 2.0 # Mach Number
L_t = 10.78 # Tail Length
S_r = 120 # Rudder Area ft^2
AR_vt = 1.85 # Vertical Tail Aspect Ratio
taper_ratio_vt = 0.3 # Vertical Tail Taper Ratio
sweep_vt = 50 # Vertical Tail Sweep
K_dwf = 1 # For Non-Delta Wing Aircraft
L_f = 47.5 # Fuselage Length, ft
D_f = 6.4 # Fuselage Depth, ft
W_f = 14.6 # Fuselage Width, ft
K_cb = 1.0 # Non Cross Beam
K_tpg = 1.0 # Non-Tripod Landing Gear
W_l = 34000 # Landing Gross Weight, lbf
N_gear = 3.8 # Landing Limit Load (Raymer Assumption)
N_l = 1.5 * N_gear # Ultimate Landing Load Factor
L_m = 48 # Length of Landing Gear, in.
L_n = 48 # Length of Nose Gear, in.
N_nw = 2 # Number of Nose Wheels
N_en = 2 # Number of Engines
T = 44000 # Total Engine Thrust
S_fw = 45 # Firewall Surface Area, ft^2 (discuss estimation later)
W_en = 2445 # Engine Weight, each, lbf
K_vg = 1.62 # Variable Inlet Geometry
L_d = 11.23 # Duct Length, ft
K_d = 2.6 # Duct Constant
L_s = 11.23 # Single Duct Length, ft
D_e = 6.68 # Engine Diameter, ft
L_tp = 2.5 # Length of Tailpipe, ft
L_sh = 12.83 # Length of Engine Shroud, ft
L_ec = 21.6 # Length From Engine Front to Cockpit, ft
T_e = 22000 # Thrust per Engine, lbf
V_t = 3127 # Total Fuel Volume, gal
V_i = 0.75 * V_t # Integral Fuel Tank Volume, gal
V_p = 0.25 * V_t # Self-Sealing Wing Tank Volume, gal
N_t = 10 # Number of Tanks
SFC = 1.85 # SFC at max thrust
S_cs = 223 # Total Area of Flight Control Surfaces
N_s = 10 # Number of Flight Control Surfaces
N_c = 6 # Number of Functions Performed By Controls (4-7)
N_ci = 1.0 # Single Pilot
K_vsh = 1.0 # Non-Variable Sweep Wing
N_u = 10 # Number of Hydraulic Utility Functions (5-15)
K_mc = 1.45 # Mission Completion Required After Failure
R_kva = 160 # System Electrical Rating, kV * A
L_a = 35 # Electrical Routing Distance, ft
N_gen = N_en # Number of Generators
W_uav = 2500 # Uninstalled Avionics Weight, lbf
N_c = 1 # Number of Crew

# Wing Weight
W_wing = 0.0103 * K_dw * K_vs * (W_dg * N_z)**0.5 * S_w**0.622 * AR**0.785 * tc_root**(-0.4) * (1 + taper_ratio)**0.05 * np.cos(np.radians(wing_sweep))**(-1.0) * S_csw**0.04
W_Wing = 0.85 * W_wing # Advanced Composites
print("Wing Weight: ", W_wing, "lbf")

# Vertical Tail Weight
W_tail = (0.452 * K_rht * (1 + H_t/H_v)**0.5 * (W_dg * N_zv)**0.488 * S_vt**0.718 * M**0.341 * L_t**(-1.0) * (1 + S_r/S_vt)**0.348 * AR_vt**0.223 * (1 + taper_ratio_vt)**0.25 * np.cos(np.radians(sweep_vt))**(-0.323))
W_tail = 0.83 * W_tail # Advanced Composites
print("Tail Weight:", W_tail, "lbf")

# Fuselage Weight
W_fuselage = (0.499 * K_dwf * W_dg**0.35 * N_z**0.25 * L_f**0.5 * D_f**0.849 * W_f**0.685)
W_fuselage = 0.90 * W_fuselage # Advanced Composites
print("Fuselage Weight:", W_fuselage, "lbf")

# Rear Landing Gear
W_rear_landing_gear = K_cb * K_tpg * (W_l * N_l)**0.25 * L_m**0.973
W_rear_landing_gear = 0.95 * W_rear_landing_gear # Advanced Composites
print("Rear Landing Gear:", W_rear_landing_gear, "lbf")

# Nose Landing Gear Weight
W_nose_landing_gear = (W_l * N_l)**0.290 * L_n**0.5 * N_nw**0.525
W_nose_landing_gear = 0.95 * W_nose_landing_gear # Advanced Composites
print("Nose Gear Weight:", W_nose_landing_gear, "lbf")

# Engine Mounts Weight
W_engine_mounts = 0.013 * N_en**0.795 * T**0.579 * N_z
print(f"Engine Mounts Weight: {W_engine_mounts} lbf")

# Firewall Weight
W_firewall = 1.13 * S_fw
print(f"Firewall Weight: {W_firewall} lbf")

# Engine Section Weight
W_engine_section = 0.01 * W_en**0.717 * N_en * N_z
print(f"Engine Section Weight: {W_engine_section} lbf")

# Engine Weight
W_engine = N_en * W_en
print("Total Engine Weight:", W_engine, "lbf")

# Air Induction System Weight
W_inlet = 13.29 * K_vg * L_d**0.643 * K_d**0.182 * N_en**1.498 * (L_s/L_d)**(-0.373) * D_e
W_inlet = 0.85 * W_inlet # Advanced Composites
print(f"Air Induction System Weight: {W_inlet} lbf")

# Tailpipe Weight
W_tailpipe = 3.5 * D_e * L_tp * N_en
print(f"Tailpipe Weight: {W_tailpipe} lbf")

# Engine Cooling Weight
W_engine_cooling = 4.55 * D_e * L_sh * N_en
print(f"Engine Cooling Weight: {W_engine_cooling} lbf")

# Oil Cooling Weight
W_oil_cooling = 37.82 * N_en**1.023
print(f"Oil Cooling Weight: {W_oil_cooling} lbf")

# Engine Controls Weight
W_engine_controls = 10.5 * N_en**1.008 * L_ec**0.222
print(f"Engine Controls Weight: {W_engine_controls} lbf")

# Starter (Pneumatic) Weight
W_starter = 0.025 * T_e**0.760 * N_en**0.72
print(f"Starter (Pneumatic) Weight: {W_starter} lbf")

# Fuel System and Tanks Weight
W_fuel_system = (7.45 * V_t**0.47 * (1 + V_i/V_t)**(-0.095) * (1 + V_p/V_t) * N_t**0.066 * N_en**0.052 * (T * SFC/1000)**0.249)
print(f"Fuel System and Tanks Weight: {W_fuel_system} lbf")

# Flight Controls Weight
W_flight_controls = 36.28 * M**0.003 * S_cs**0.489 * N_s**0.484 * N_c**0.127
print(f"Flight Controls Weight: {W_flight_controls} lbf")

# Instruments Weight
W_instruments = 8.0 + 36.37 * N_en**0.676 * N_t**0.237 + 26.4 * (1 + N_ci)**1.356
print(f"Instruments Weight: {W_instruments} lbf")

# Hydraulics Weight
W_hydraulics = 37.23 * K_vsh * N_u**0.664
print(f"Hydraulics Weight: {W_hydraulics} lbf")

# Electrical System Weight
W_electrical = 172.2 * K_mc * R_kva**0.152 * N_c**0.10 * L_a**0.10 * N_gen**0.091
print(f"Electrical System Weight: {W_electrical} lbf")

# Avionics Weight
W_avionics = 2.117 * W_uav**0.933
print(f"Avionics Weight: {W_avionics} lbf")

# Furnishings Weight
W_furnishings = 217.6 * N_c
print(f"Furnishings Weight: {W_furnishings} lbf")

# Air Conditioning and Anti-Ice Weight
W_air_conditioning = 201.6 * ((W_uav + 200 * N_c) / 1000)**0.735
print(f"Air Conditioning and Anti-Ice Weight: {W_air_conditioning} lbf")

# Handling Gear Weight
W_handling_gear = 3.2e-4 * W_dg
print(f"Handling Gear Weight: {W_handling_gear} lbf")

# Empty Weight
W_empty = (W_wing + W_tail + W_fuselage + W_rear_landing_gear + W_nose_landing_gear +
         W_engine_mounts + W_firewall + W_engine_section + W_inlet +
         W_tailpipe + W_engine_cooling + W_oil_cooling + W_engine_controls + W_starter +
         W_fuel_system + W_flight_controls + W_instruments + W_hydraulics + W_electrical +
         W_avionics + W_furnishings + W_air_conditioning + W_handling_gear + W_engine)
print(f"Empty Weight: {W_empty} lbf")


# Center of Gravity

fuselage_cg = 0.26 * L_f # ft
wing_cg = 29.9 # ft
empennage_cg = 42.3 # ft
engine_cg = 40.3 # ft
inlet_cg = 26.5 # ft
forward_gear_cg = 10.1 # ft
rear_gear_cg = 33.8 # ft
avionics_cg = 6.9 # ft
AIM_120_cg = 19.8 # ft
MK_83_cg = 19.8 # ft
AIM_9X_cg = 30.9 # ft
tank_78_cg = 12.5 # ft
tank_6_cg = 39.9 # ft
wing_tank_cg = 29.8 # ft
tank_34_cg = 20.0 # ft
tank_1_cg = 22.1 # ft
tank_2_cg = 27.9 # ft
tank_5_cg = 33.0 # ft

# Individual Tank Weights

tank_1_w = 5411 * 0.85 # lbf
tank_2_w = 3194 * 0.85 # lbf
tank_34_w = 1114 * 0.85 # lbf
tank_5_w = 3286 * 0.85 # lbf
tank_6_w = 4073 * 0.85 # lbf
tank_78_w = 2310 * 0.85 # lbf
wing_tank_w = 5580 * 0.85 # lbf

# Ordinance Weights

AIM_120_w = 2136 # 6x Aim-120C
MK_83_w = 4052 # 4x MK-83
AIM_9X_w = 372 # 2x Aim-9x

def calculate_cg(ordnance_cg, ordnance_w, label,
                 inc_AIM_9X=True, inc_tank_1=True, inc_tank_2=True,
                 inc_tank_34=True, inc_tank_5=True, inc_tank_6=True,
                 inc_tank_78=True, inc_wing_tank=True, inc_ordinance=True):

    numerator = (
        (wing_cg * W_wing)
        + (empennage_cg * W_tail)
        + (fuselage_cg * W_fuselage)
        + (rear_gear_cg * W_rear_landing_gear)
        + (forward_gear_cg * W_nose_landing_gear)
        + (engine_cg * W_engine)
        + (inlet_cg * W_inlet)
        + (avionics_cg * W_avionics)
        + (ordnance_cg * ordnance_w if inc_ordinance else 0)
        + (AIM_9X_cg * AIM_9X_w if inc_AIM_9X else 0)
        + (tank_1_cg * tank_1_w if inc_tank_1 else 0)
        + (tank_2_cg * tank_2_w if inc_tank_2 else 0)
        + (tank_34_cg * tank_34_w if inc_tank_34 else 0)
        + (tank_5_cg * tank_5_w if inc_tank_5 else 0)
        + (tank_6_cg * tank_6_w if inc_tank_6 else 0)
        + (tank_78_cg * tank_78_w if inc_tank_78 else 0)
        + (wing_tank_cg * wing_tank_w if inc_wing_tank else 0)
    )
    denominator = (
        W_wing + W_tail + W_fuselage + W_rear_landing_gear + W_nose_landing_gear
        + W_engine + W_inlet + W_avionics
        + (ordnance_w if inc_ordinance else 0)
        + (AIM_9X_w if inc_AIM_9X else 0)
        + (tank_1_w if inc_tank_1 else 0)
        + (tank_2_w if inc_tank_2 else 0)
        + (tank_34_w if inc_tank_34 else 0)
        + (tank_5_w if inc_tank_5 else 0)
        + (tank_6_w if inc_tank_6 else 0)
        + (tank_78_w if inc_tank_78 else 0)
        + (wing_tank_w if inc_wing_tank else 0)
    )
    cg = numerator / denominator
    print(f"{label} CG: {cg:.2f} ft  |  Weight: {denominator:.0f} lbf")
    return cg, denominator

MAC_LE = 17.9
MAC_len = 19.91

def ft_to_pct_MAC(cg_ft):
    return ((cg_ft - MAC_LE) / MAC_len) * 100

# Air to Air
air_points = [
    calculate_cg(AIM_120_cg, AIM_120_w, "Fully Loaded Air-To-Air"),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 7-8 Empty", inc_tank_78=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 3-4 Empty", inc_tank_78=False, inc_tank_34=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 1 Empty", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 2 Empty", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "AIM-120C Dropped", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False, inc_ordinance=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "AIM-9X Dropped", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False, inc_ordinance=False, inc_AIM_9X=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 5 Empty", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_5=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Wing Tanks Empty", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_5=False, inc_wing_tank=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 6 Empty", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_5=False, inc_wing_tank=False, inc_tank_6=False),
]
air_labels = ["Fully Loaded", "Tanks 7-8 Empty", "Tanks 3-4 Empty", "Tank 1 Empty", "Tank 2 Empty",
              "AIM-120 Drop", "AIM-9X Drop", "Tank 5 Empty", "Wing Tanks Empty", "Tank 6 Empty"]

# Strike
strike_points = [
    calculate_cg(MK_83_cg, MK_83_w, "Fully Loaded Strike"),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 7-8 Empty", inc_tank_78=False),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 3-4 Empty", inc_tank_78=False, inc_tank_34=False),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 1 Empty", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 2 Empty", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False),
    calculate_cg(MK_83_cg, MK_83_w, "MK-83 Dropped", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False, inc_ordinance=False),
    calculate_cg(MK_83_cg, MK_83_w, "AIM-9X Dropped", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False, inc_ordinance=False, inc_AIM_9X=False),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 5 Empty", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_5=False),
    calculate_cg(MK_83_cg, MK_83_w, "Wing Tanks Empty", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_5=False, inc_wing_tank=False),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 6 Empty", inc_tank_78=False, inc_tank_34=False, inc_tank_1=False, inc_tank_2=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_5=False, inc_wing_tank=False, inc_tank_6=False),
]
strike_labels = ["Fully Loaded", "Tanks 7-8 Empty", "Tanks 3-4 Empty", "Tank 1 Empty", "Tank 2 Empty",
                 "MK-83 Drop", "AIM-9X Drop", "Tank 5 Empty", "Wing Tanks Empty", "Tank 6 Empty"]

air_cg   = [p[0] for p in air_points]
air_wt   = [p[1] for p in air_points]
str_cg   = [p[0] for p in strike_points]
str_wt   = [p[1] for p in strike_points]

air_cg_mac = [ft_to_pct_MAC(cg) for cg in air_cg]
str_cg_mac = [ft_to_pct_MAC(cg) for cg in str_cg]

markers = ['o', 's', '^', 'D', 'v', 'P', '*', 'X', 'h', 'p']

fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(air_cg_mac, air_wt, 'b-', linewidth=3)
ax.plot(str_cg_mac, str_wt, 'r--', linewidth=3)

air_handles = []
str_handles = []

for i, (label, marker) in enumerate(zip(air_labels, markers)):
    h, = ax.plot(air_cg_mac[i], air_wt[i], color='blue', marker=marker, markersize=10, linestyle='None')
    air_handles.append((h, f"A2A: {label}"))

for i, (label, marker) in enumerate(zip(strike_labels, markers)):
    h, = ax.plot(str_cg_mac[i], str_wt[i], color='red', marker=marker, markersize=10, linestyle='None')
    str_handles.append((h, f"Strike: {label}"))

all_handles = [h for h, _ in air_handles] + [h for h, _ in str_handles]
all_labels  = [l for _, l in air_handles] + [l for _, l in str_handles]
ax.legend(all_handles, all_labels, loc='upper left', fontsize=9, ncol=2)

takeoff_cg_mac = air_cg_mac[0]
fwd_limit_mac = takeoff_cg_mac - (0.1 * 100)
aft_limit_mac = takeoff_cg_mac + (0.1 * 100)

ax.axvline(x=fwd_limit_mac, color='black', linewidth=2, linestyle='-')
ax.axvline(x=aft_limit_mac, color='black', linewidth=2, linestyle='-')
y_mid = (ax.get_ylim()[0] + ax.get_ylim()[1]) / 2

ax.text(fwd_limit_mac - 0.1, y_mid, 'Fwd Limit', rotation=90, va='center', ha='right',
        fontsize=11, fontweight='bold')
ax.text(aft_limit_mac + 0.2, y_mid, 'Aft Limit', rotation=90, va='center', ha='left',
        fontsize=11, fontweight='bold')

ax.set_xlabel("CG Location (% MAC from Datum)", fontsize=13, fontweight='bold')
ax.set_ylabel("Gross Weight (lbf)", fontsize=13, fontweight='bold')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("CG Excursion Diagram", fontsize=15, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()