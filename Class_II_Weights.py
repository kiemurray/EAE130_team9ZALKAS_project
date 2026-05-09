import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import code_variables as cv

# All Equations used are from Raymer's section on Fighter/Attack Weights

# Parameters
K_dw = cv.K_dw # Non-Delta Wing
K_vs = cv.K_vs # non-variable sweep
W_dg = cv.W_dg # Design Gross Weight (lbf)
n_z = cv.n_z # limit load, desired by RFP
N_z = cv.N_z # Ultimate Load Factor
n_zv = cv.n_zv # Vertical Tail Limit Load (estimated)
N_zv = cv.N_zv * n_zv # Vertical Tail Limit Load
S_w = cv.S_w # Trapezoidal Wing Area ft^2
AR = cv.AR_w # Aspect Ratio
tc_root = cv.tc_root# t/c ratio at root chord
taper_ratio = cv.taper_ratio # Taper Ratio
wing_sweep = cv.lambda_w # Wing Sweep at 25% MAC
S_csw = cv.S_csw # Wing Mounted Control Surface Area ft^2
K_rht = cv.K_rht # Rolling Tail (Stabilators)
H_t = cv.H_t# Horizontal Tail Height Above Fuselage
H_v = cv.H_v # Vertical Tail Height Above Fuselage (this gets cancelled out anyways)
S_vt = cv.S_vt # Vertical Tail Area ft^2
M = cv.M # Mach Number
L_t = cv.L_t # Tail Length
S_r = cv.S_r # Rudder Area ft^2
AR_vt = cv.AR_vt # Vertical Tail Aspect Ratio
taper_ratio_vt = cv.taper_ratio_vt # Vertical Tail Taper Ratio
sweep_vt = cv.sweep_vt # Vertical Tail Sweep
K_dwf = cv.K_dwf # For Non-Delta Wing Aircraft
L_f = cv.L_f # Fuselage Length, ft
D_f = cv.D_f # Fuselage Depth, ft
W_f = cv.W_f # Fuselage Width, ft
K_cb = cv.K_cb # Non Cross Beam
K_tpg = cv.K_tpg # Non-Tripod Landing Gear
W_l = cv.W_l # Landing Gross Weight, lbf
N_gear = cv.N_gear # Landing Limit Load (Raymer Assumption)
N_l = cv.N_l # Ultimate Landing Load Factor
L_m = cv.L_m # Length of Landing Gear, in.
L_n = cv.L_n # Length of Nose Gear, in.
N_nw = cv.N_nw # Number of Nose Wheels
N_en = cv.num_engines # Number of Engines
T = cv.T_0 * N_en # Total Engine Thrust
S_fw = cv.S_fw # Firewall Surface Area, ft^2 (discuss estimation later)
W_en = cv.W_en # Engine Weight, each, lbf
K_vg = cv.K_vg # Variable Inlet Geometry
L_d = cv.L_d # Duct Length, ft
K_d = cv.K_d # Duct Constant
L_s = cv.L_s # Single Duct Length, ft
D_e = cv.D_e # Engine Diameter, ft
L_tp = cv.L_tp # Length of Tailpipe, ft
L_sh = cv.L_sh # Length of Engine Shroud, ft
L_ec = cv.L_ec # Length From Engine Front to Cockpit, ft
T_e = cv.T_e # Thrust per Engine, lbf
V_t = cv.V_t # Total Fuel Volume, gal
V_i = cv.V_i # Integral Fuel Tank Volume, gal
V_p = cv.V_p # Self-Sealing Wing Tank Volume, gal
N_t = cv.N_t # Number of Tanks
SFC = cv.SFC # SFC at max thrust
S_cs = cv.S_cs # Total Area of Flight Control Surfaces
N_s = cv.N_s # Number of Flight Control Surfaces
N_c = cv.N_c # Number of Functions Performed By Controls (4-7)
N_ci = cv.num_pilot # Single Pilot
K_vsh = cv.K_vsh # Non-Variable Sweep Wing
N_u = cv.N_u # Number of Hydraulic Utility Functions (5-15)
K_mc = cv.K_mc # Mission Completion Required After Failure
R_kva = cv.R_kva # System Electrical Rating, kV * A
L_a = cv.L_a # Electrical Routing Distance, ft
N_gen = N_en # Number of Generators
W_uav = cv.W_uav # Uninstalled Avionics Weight, lbf
W_urdr = cv.W_urdr # Uninstalled Radar Weight, lbf
N_c = N_ci # Number of Crew

# Wing Weight (Raymer Eq 15.1)
W_wing = 0.0103 * K_dw * K_vs * (W_dg * N_z)**0.5 * S_w**0.622 * AR**0.785 * tc_root**(-0.4) * (1 + taper_ratio)**0.05 * np.cos(np.radians(wing_sweep))**(-1.0) * S_csw**0.04
W_Wing = 0.85 * W_wing # Advanced Composites
print("Wing Weight: ", W_wing, "lbf")

# Vertical Tail Weight (Raymer Eq 15.3)
W_tail = (0.452 * K_rht * (1 + H_t/H_v)**0.5 * (W_dg * N_zv)**0.488 * S_vt**0.718 * M**0.341 * L_t**(-1.0) * (1 + S_r/S_vt)**0.348 * AR_vt**0.223 * (1 + taper_ratio_vt)**0.25 * np.cos(np.radians(sweep_vt))**(-0.323))
W_tail = 0.85 * W_tail # Advanced Composites
print("Tail Weight:", W_tail, "lbf")

# Fuselage Weight (Raymer Eq 15.4)
W_fuselage = (0.499 * K_dwf * W_dg**0.35 * N_z**0.25 * L_f**0.5 * D_f**0.849 * W_f**0.685)
W_fuselage = 0.90 * W_fuselage # Advanced Composites
print("Fuselage Weight:", W_fuselage, "lbf")

# Rear Landing Gear (Raymer Eq 15.5)
W_rear_landing_gear = K_cb * K_tpg * (W_l * N_l)**0.25 * L_m**0.973
W_rear_landing_gear = 0.95 * W_rear_landing_gear # Advanced Composites
print("Rear Landing Gear:", W_rear_landing_gear, "lbf")

# Nose Landing Gear Weight (Raymer Eq 15.6)
W_nose_landing_gear = (W_l * N_l)**0.290 * L_n**0.5 * N_nw**0.525
W_nose_landing_gear = 0.95 * W_nose_landing_gear # Advanced Composites
print("Nose Gear Weight:", W_nose_landing_gear, "lbf")

# Engine Mounts Weight (Raymer Eq 15.7)
W_engine_mounts = 0.013 * N_en**0.795 * T**0.579 * N_z
print(f"Engine Mounts Weight: {W_engine_mounts} lbf")

# Firewall Weight (Raymer Eq 15.8)
W_firewall = 1.13 * S_fw
print(f"Firewall Weight: {W_firewall} lbf")

# Engine Section Weight (Raymer Eq 15.9)
W_engine_section = 0.01 * W_en**0.717 * N_en * N_z
print(f"Engine Section Weight: {W_engine_section} lbf")

# Engine Weight
W_engine = N_en * W_en
print("Total Engine Weight:", W_engine, "lbf")

# Air Induction System Weight (Raymer Eq 15.10)
W_inlet = 13.29 * K_vg * L_d**0.643 * K_d**0.182 * N_en**1.498 * (L_s/L_d)**(-0.373) * D_e
W_inlet = 0.85 * W_inlet # Advanced Composites
print(f"Air Induction System Weight: {W_inlet} lbf")

# Tailpipe Weight (Raymer Eq 15.11)
W_tailpipe = 3.5 * D_e * L_tp * N_en
print(f"Tailpipe Weight: {W_tailpipe} lbf")

# Engine Cooling Weight (Raymer Eq 15.12)
W_engine_cooling = 4.55 * D_e * L_sh * N_en
print(f"Engine Cooling Weight: {W_engine_cooling} lbf")

# Oil Cooling Weight (Raymer Eq 15.13)
W_oil_cooling = 37.82 * N_en**1.023
print(f"Oil Cooling Weight: {W_oil_cooling} lbf")

# Engine Controls Weight (Raymer Eq 15.14)
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

# Hydraulics Weight (Raymer Eq. 15.19)
W_hydraulics = 37.23 * K_vsh * N_u**0.664
print(f"Hydraulics Weight: {W_hydraulics} lbf")

# Electrical System Weight
W_electrical = 172.2 * K_mc * R_kva**0.152 * N_c**0.10 * L_a**0.10 * N_gen**0.091
print(f"Electrical System Weight: {W_electrical} lbf")

# Sensor Weight
W_radar = 2.117 * W_urdr**0.933
print(f"Radar Weight: {W_radar} lbf")

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
         W_avionics + W_radar + W_furnishings + W_air_conditioning + W_handling_gear + W_engine)
print(f"Empty Weight: {W_empty} lbf")


# X-Axis Center of Gravity

fuselage_cg = 15.26 # 0.26 * L_f # ft
wing_cg = 27.330 # ft
empennage_cg = 42.3 # ft
engine_cg = 40.287 # ft
engine_cooling_cg = 40.3 # ft
inlet_cg = 38.2315 # 26.5 # ft
forward_gear_cg = 12.442 # 10.1 ft
rear_gear_cg = 29.063 # 33.8 # ft
radar_cg = 5.524 # 6.9 # ft
avionics_cg = 13.167 # 16.9 # ft (this also got thanos snapped, so i put in the cockpit x_cg)
AC_cg = 16.1 # ft
AIM_120_cg = 19.8 # ft
MK_83_cg = 19.8 # ft
AIM_9X_cg = 36.359 # ft
tank_78_cg = 13.78 # ft
tank_6_cg = 40.2 # ft # this got thanos snapped
wing_tank_cg = 27.064 # ft
tank_34_cg = 23.004 # ft
tank_1_cg = 19.299 # ft
tank_2_cg = 26.611 # ft
tank_5_cg = 36.563 # ft

# Z-Axis Center of Gravity

fuselage_z_cg = 0 # ft
wing_z_cg = 0 # ft
empennage_z_cg = 2.3 # ft
engine_z_cg = 0 # ft
engine_cooling_z_cg = 0 # ft
inlet_z_cg = -0.5 # ft
forward_gear_z_cg = -2.0 # ft
rear_gear_z_cg = 0.2 # ft
radar_z_cg = -0.4 # ft
avionics_z_cg = 2.1 # ft
AC_z_cg = 2.1 # ft
AIM_120_z_cg = -1.7 # ft
MK_83_z_cg = -1.7 # ft
AIM_9X_z_cg = -2.0 # ft
tank_78_z_cg = 0.2 # ft
tank_6_z_cg = 0 # ft
wing_tank_z_cg = 0 # ft
tank_34_z_cg = 0 # ft
tank_1_z_cg = 1.8 # ft
tank_2_z_cg = 0 # ft
tank_5_z_cg = 1.6 # ft

# Individual Tank Weights

tank_1_w = (cv.tank_1_v * cv.rho_jp5) * cv.packing_factor_deep_fuselage # lbf
tank_2_w = (cv.tank_2_v * cv.rho_jp5) * cv.packing_factor_deep_fuselage # lbf
tank_34_w = (cv.tank_34_v * cv.rho_jp5) * cv.packing_factor_shallow_fuselage # lbf
tank_5_w = (cv.tank_5_v * cv.rho_jp5) * cv.packing_factor_deep_fuselage # lbf
tank_6_w = (cv.tank_6_v * cv.rho_jp5) * cv.packing_factor_deep_fuselage # lbf
tank_78_w = (cv.tank_78_v * cv.rho_jp5) * cv.packing_factor_shallow_fuselage # lbf
wing_tank_w = (cv.wing_tank_v * cv.rho_jp5) * cv.packing_factor_wing # lbf

# Ordinance Weights

AIM_120_w = 2136 # 6x Aim-120C
MK_83_w = 4052 # 4x MK-83
AIM_9X_w = 372 # 2x Aim-9x

# X-Axis Center of Gravity

def calculate_cg(ordnance_cg, ordnance_w, label,
                 inc_AIM_9X=True, inc_tank_1=True, inc_tank_2=True,
                 inc_tank_34=True, inc_tank_5=True, inc_tank_6=False,
                 inc_tank_78=True, inc_wing_tank=True, inc_ordinance=True):

    numerator = (
        (wing_cg * W_wing)
        + (empennage_cg * W_tail)
        + (fuselage_cg * W_fuselage)
        + (rear_gear_cg * W_rear_landing_gear)
        + (forward_gear_cg * W_nose_landing_gear)
        + (engine_cg * W_engine)
        + (engine_cooling_cg * W_engine_cooling)
        + (inlet_cg * W_inlet)
        + (radar_cg * W_radar)
        + (avionics_cg * W_avionics)
        + (AC_cg * W_air_conditioning)
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
        + W_engine + W_engine_cooling + W_inlet + W_avionics + W_radar + W_air_conditioning
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

MAC_LE = 18.318175   # MAC x location
MAC_len = 17.68470 # MAC length

def ft_to_pct_MAC(cg_ft):
    return ((cg_ft - MAC_LE) / MAC_len) * 100

# Air to Air
air_points = [
    calculate_cg(AIM_120_cg, AIM_120_w, "Fully Loaded Air-To-Air"),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 7-8 Empty", inc_tank_78=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 6 Empty", inc_tank_78=False, inc_tank_6=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 5 Empty", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 3-4 Empty", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "AIM-120C Dropped", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False, inc_ordinance=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "AIM-9X Dropped", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False, inc_ordinance=False, inc_AIM_9X=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 1 Empty", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_1=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Tank 2 Empty", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_1=False, inc_tank_2=False),
    calculate_cg(AIM_120_cg, AIM_120_w, "Wing Tanks Empty", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_1=False, inc_tank_2=False, inc_wing_tank=False),
]
air_labels = ["Fully Loaded", "Tanks 7-8 Empty", "Tank 6 Empty", "Tank 5 Empty", "Tanks 3-4 Empty",
              "AIM-120 Drop", "AIM-9X Drop", "Tank 1 Empty", "Tank 2 Empty", "Wing Tanks Empty"]

# Strike
strike_points = [
    calculate_cg(MK_83_cg, MK_83_w, "Fully Loaded Strike"),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 7-8 Empty", inc_tank_78=False),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 6 Empty", inc_tank_78=False, inc_tank_6=False),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 5 Empty", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 3-4 Empty", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False),
    calculate_cg(MK_83_cg, MK_83_w, "MK-83 Dropped", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False, inc_ordinance=False),
    calculate_cg(MK_83_cg, MK_83_w, "AIM-9X Dropped", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False, inc_ordinance=False, inc_AIM_9X=False),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 1 Empty", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_1=False),
    calculate_cg(MK_83_cg, MK_83_w, "Tank 2 Empty", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_1=False, inc_tank_2=False),
    calculate_cg(MK_83_cg, MK_83_w, "Wing Tanks Empty", inc_tank_78=False, inc_tank_6=False, inc_tank_5=False, inc_tank_34=False, inc_ordinance=False, inc_AIM_9X=False, inc_tank_1=False, inc_tank_2=False, inc_wing_tank=False),
]
strike_labels = ["Fully Loaded", "Tanks 7-8 Empty", "Tank 6 Empty", "Tank 5 Empty", "Tanks 3-4 Empty",
                 "MK-83 Drop", "AIM-9X Drop", "Tank 1 Empty", "Tank 2 Empty", "Wing Tanks Empty"]

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

# Z-Axis Center of Gravity

def calculate_z_cg(ordnance_z_cg, ordnance_w, label,
                 inc_AIM_9X=True, inc_tank_1=True, inc_tank_2=True,
                 inc_tank_34=True, inc_tank_5=True, inc_tank_6=False,
                 inc_tank_78=True, inc_wing_tank=True, inc_ordinance=True):

    numerator = (
        (wing_z_cg * W_wing)
        + (empennage_z_cg * W_tail)
        + (fuselage_z_cg * W_fuselage)
        + (rear_gear_z_cg * W_rear_landing_gear)
        + (forward_gear_z_cg * W_nose_landing_gear)
        + (engine_z_cg * W_engine)
        + (engine_cooling_z_cg * W_engine_cooling)
        + (inlet_z_cg * W_inlet)
        + (radar_z_cg * W_radar)
        + (avionics_z_cg * W_avionics)
        + (AC_z_cg * W_air_conditioning)
        + (ordnance_z_cg * ordnance_w if inc_ordinance else 0)
        + (AIM_9X_z_cg * AIM_9X_w if inc_AIM_9X else 0)
        + (tank_1_z_cg * tank_1_w if inc_tank_1 else 0)
        + (tank_2_z_cg * tank_2_w if inc_tank_2 else 0)
        + (tank_34_z_cg * tank_34_w if inc_tank_34 else 0)
        + (tank_5_z_cg * tank_5_w if inc_tank_5 else 0)
        + (tank_6_z_cg * tank_6_w if inc_tank_6 else 0)
        + (tank_78_z_cg * tank_78_w if inc_tank_78 else 0)
        + (wing_tank_z_cg * wing_tank_w if inc_wing_tank else 0)
    )
    denominator = (
        W_wing + W_tail + W_fuselage + W_rear_landing_gear + W_nose_landing_gear
        + W_engine + W_engine_cooling + W_inlet + W_avionics + W_radar + W_air_conditioning
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
    z_cg = numerator / denominator
    print(f"{label} z_CG: {z_cg:.2f} ft  |  Weight: {denominator:.0f} lbf")
    return z_cg, denominator


z_cg_air = calculate_z_cg(AIM_120_z_cg, AIM_120_w, "Air-To-Air Configuration")
z_cg_strike = calculate_z_cg(MK_83_z_cg, MK_83_w, "Strike Configuration")