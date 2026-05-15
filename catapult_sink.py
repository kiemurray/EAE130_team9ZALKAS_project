import numpy as np
import matplotlib.pyplot as plt
import code_variables as cv

# =========================================================
# CATAPULT POST-LAUNCH SINK SIMULATION
# =========================================================
# This simulates aircraft sink after catapult end-of-stroke.
#
# USER INPUTS:
#   - Aircraft parameters
#   - Aerodynamic parameters
#   - Engine thrust
#   - Test launch speed
#
# OUTPUTS:
#   - Maximum sink distance
#   - Time history plots
#
# =========================================================

# ---------------------------------------------------------
# USER INPUT PARAMETERS
# ---------------------------------------------------------

# Physical constants
g = 32.174              # ft/s^2
rho = 0.0023769         # slug/ft^3 (sea level standard)

# Aircraft parameters
W = cv.W_TO               # aircraft weight (lb) = 52000
m = W / g               # mass (slugs)

S = cv.S_w                 # wing area (ft^2) (560ft2)

# Aerodynamics
CL0 = -0.186            # lift coefficient at alpha=0
CL_alpha = cv.CL_alpha  # per radian (~1.8449/rad)
alpha_deg = 12          # angle of attack (deg)

CD0 = cv.CD0               # zero-lift drag coefficient (0.01)
k = cv.k_to                # induced drag factor (k=0.1629)
print(k)

# Engine
T = 44000               # thrust (lb)

# Launch condition
V0 = 160                # end-of-stroke speed (ft/s)

# Simulation controls
dt = 0.01               # timestep (sec)
t_final = 8             # total simulation time (sec)

# ---------------------------------------------------------
# INITIAL CONDITIONS
# ---------------------------------------------------------

alpha = np.radians(alpha_deg)

# Initial state
u = V0                  # forward speed (ft/s)
w = 0.0                 # vertical velocity (ft/s)
h = 0.0                 # altitude relative to EOS position

# Data storage
time_hist = []
height_hist = []
sink_hist = []
vz_hist = []

# ---------------------------------------------------------
# SIMULATION LOOP
# ---------------------------------------------------------

time = 0.0

while time <= t_final:

    # Total airspeed
    V = np.sqrt(u**2 + w**2)

    # Aerodynamic coefficients
    CL = CL0 + CL_alpha * alpha
    CD = CD0 + k * CL**2

    # Aerodynamic forces
    q = 0.5 * rho * V**2

    L = q * S * CL
    D = q * S * CD

    # Vertical force balance
    Fz = L + T * np.sin(alpha) - W

    # Vertical acceleration
    az = Fz / m

    # Longitudinal force balance
    Fx = T * np.cos(alpha) - D

    # Longitudinal acceleration
    ax = Fx / m

    # Integrate velocities
    w = w + az * dt
    u = u + ax * dt

    # Integrate altitude
    h = h + w * dt

    # Store data
    time_hist.append(time)
    height_hist.append(h)
    sink_hist.append(-h)
    vz_hist.append(w)

    # Advance time
    time += dt

# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------

max_sink = np.max(sink_hist)

print("========================================")
print("CATAPULT FLY-AWAY SINK ANALYSIS")
print("========================================")
print(f"Test launch speed      : {V0:.2f} ft/s")
print(f"Maximum sink distance  : {max_sink:.2f} ft")

if max_sink <= 10:
    print("RESULT: PASS (sink <= 10 ft)")
else:
    print("RESULT: FAIL (sink > 10 ft)")

# ---------------------------------------------------------
# PLOTS
# ---------------------------------------------------------

plt.figure(figsize=(10,6))

plt.subplot(2,1,1)
plt.plot(time_hist, height_hist)
plt.axhline(-10, color='r', linestyle='--', label='10 ft limit')
plt.ylabel("Altitude Change (ft)")
plt.title("Aircraft Sink After Launch")
plt.grid(True)
plt.legend()

plt.subplot(2,1,2)
plt.plot(time_hist, vz_hist)
plt.ylabel("Vertical Velocity (ft/s)")
plt.xlabel("Time (s)")
plt.grid(True)

plt.tight_layout()
plt.show()