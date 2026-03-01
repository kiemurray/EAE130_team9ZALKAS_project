import numpy as np
import matplotlib.pyplot as plt
import math
# We have to figure out what Sw, Chord, AR, lt, Xcg, Xac, CL alpha, and CM alpha f pwr. 
# Convert
# Sw = Wing area (ft^2)
#c = Mean aerodynamic Chord (ft)
# AR = Aspect Ratio
#lt = Tail Moment Arm (Distance from CG to tail AC)
#Xcg = Distance from Wing Leading Edge to CG (ft)
#Xac = Distance from Wing Leading Edge to AC (ft)\
#CL, alpha,w = Wing Lift Curve Slope
#CM,α,f= pitching moment caused by the fuselage
#CM,α,pwr is the pitching moment caused by the engine

def per_deg_to_per_rad(per_deg):
    return per_deg * (180.0 / np.pi)

# ---------- longitudinal_stability ----------
def downwash_derivative(CL_alpha_wing, AR_wing):
    """
    Inputs:
      CL_alpha_wing : wing lift-curve slope (per rad)
      AR_wing       : wing aspect ratio (dimensionless)
    Returns:
      d_eps_d_alpha : downwash derivative (unitless, per rad)
    """
    return 2.0 * CL_alpha_wing / (np.pi * AR_wing)


def lift_curve_3d(a_2d, AR, e=1.0):
    """
    Convert 2D section lift-curve slope (a_2d) to 3D finite-wing lift-curve slope (a_3d).
    a_3d = a_2d / (1 + a_2d / (pi * AR * e))
    Inputs:
      a_2d : 2D section lift-curve slope (per rad)
      AR   : aspect ratio (dimensionless)
      e    : span efficiency factor (0..1; default 1)
    Returns:
      a_3d : 3D lift-curve slope (per rad)
    """
    return a_2d / (1.0 + (a_2d / (np.pi * AR * e)))


def tail_volume_coefficient(S_t, l_t, S, c):
    """
    Horizontal tail volume coefficient:
      V_H = (S_t * l_t) / (S * c)
    Inputs:
      S_t : horizontal tail area
      l_t : tail moment arm (distance from wing AC to tail AC)
      S   : wing area
      c   : mean aerodynamic chord
    Returns:
      V_H : tail volume coefficient (dimensionless)
    """
    return (S_t * l_t) / (S * c)


# ---------- main stability functions ----------
def C_m_alpha(C_m_ac,
              x_cg, x_ac, c,
              CL_alpha_wing,
              eta, V_H, CL_alpha_tail,
              deps_dalpha):
    """
    Total pitching-moment coefficient derivative w.r.t. alpha (C_m_alpha).
    """
    arm_term = ((x_cg - x_ac) / c) * CL_alpha_wing
    tail_term = eta * V_H * CL_alpha_tail * (1.0 - deps_dalpha)
    return C_m_ac + arm_term - tail_term


def neutral_point_location(x_ac,
                           C_m_ac,
                           CL_alpha_wing,
                           eta, V_H, CL_alpha_tail,
                           deps_dalpha):
    """
    Neutral point location x_NP (same datum as x_ac and x_cg).
    """
    term1 = x_ac - C_m_ac / CL_alpha_wing
    term2 = eta * V_H * (CL_alpha_tail / CL_alpha_wing) * (1.0 - deps_dalpha)
    return term1 + term2


def static_margin(x_NP, x_cg, c):
    """
    Static margin (SM) in chord fractions:
      SM = (x_NP - x_cg) / c
    """
    return (x_NP - x_cg) / c


# ---------- directional / vertical tail ----------
def sideslip_downwash_factor(Sv, S, AR):
    """
    Eq. (8)
    (1 + dσ/dβ) = 0.724 + (3.06 * (Sv/S)) / (1 + 0.009*AR)
    """
    return 0.724 + (3.06 * (Sv / S)) / (1.0 + 0.009 * AR)


def vertical_tail_volume_coefficient(Sv, lt, Sw, b):
    """
    Eq. (9)
    Vv = (Sv * lt) / (Sw * b)
    """
    return (Sv * lt) / (Sw * b)


def Cn_beta_total(Cn_beta_wf, CL_alpha_v, Vv, sideslip_factor):
    """
    Eq. (7)
    Cnβ = Cnβ,wf + CLα,v * Vv * (1 + dσ/dβ)
    """
    return Cn_beta_wf + CL_alpha_v * Vv * sideslip_factor


def solve_Sv_for_target_Cn_beta(Cn_beta_target, Cn_beta_wf, CL_alpha_v, lt, Sw, b, S, AR):
    """
    Solve for Sv given a target Cn_beta. Uses bisection on reasonable bracket.
    """
    def f(Sv):
        factor = sideslip_downwash_factor(Sv, S, AR)
        Vv = vertical_tail_volume_coefficient(Sv, lt, Sw, b)
        return Cn_beta_total(Cn_beta_wf, CL_alpha_v, Vv, factor) - Cn_beta_target

    lo, hi = 1e-6, 1e4  # broad bracket (m^2). Adjust if needed.
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        raise ValueError("Bracket does not contain root; try different lo/hi or check inputs.")
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        fmid = f(mid)
        if fmid == 0:
            return mid
        if flo * fmid < 0:
            hi = mid
            fhi = fmid
        else:
            lo = mid
            flo = fmid
    return 0.5 * (lo + hi)



if __name__ == "__main__":
    # Example numbers have to replace with our actual #s
    C_m_ac = -0.02
    x_ac = 1.2        # m from leading edge
    x_cg = 1.0        # m from leading edge
    c = 1.5           # mean aerodynamic chord (m)
    CL_alpha_wing = 5.7    # per rad
    a2d_tail = 2.0 * np.pi # per rad (section)
    AR_tail = 4.0
    e_tail = 0.9
    eta = 0.95
    S_t = 2.0
    l_t = 4.5
    S = 25.0
    Sw = S

    CL_alpha_tail = lift_curve_3d(a2d_tail, AR_tail, e_tail)
    V_H = tail_volume_coefficient(S_t, l_t, S, c)
    deps_dalpha = downwash_derivative(CL_alpha_wing, AR_wing=8.0)

    Cm_alpha_val = C_m_alpha(C_m_ac, x_cg, x_ac, c,
                             CL_alpha_wing, eta, V_H, CL_alpha_tail, deps_dalpha)
    x_NP = neutral_point_location(x_ac, C_m_ac, CL_alpha_wing,
                                  eta, V_H, CL_alpha_tail, deps_dalpha)
    SM = static_margin(x_NP, x_cg, c)

    print(f"Cm_alpha = {Cm_alpha_val:.6f} per rad")
    print(f"Neutral point x_NP = {x_NP:.4f} m")
    print(f"Static margin (fraction of c) = {SM:.4f}")

    # Vertical tail example
    Cn_beta_target = 0.001   # per deg, or convert to per rad as needed
    # NOTE: units consistency. If Cn_beta_target is per deg, convert to per rad: per_rad = per_deg * (180/pi)
    # Use consistent units across all our inputs 
    Cn_beta_wf = 0.0002
    CL_alpha_v = 2 * np.pi  # per rad (approx)
    Sw = S
    b = 10.0
    AR = 8.0

    try:
        Sv_needed = solve_Sv_for_target_Cn_beta(Cn_beta_target, Cn_beta_wf, CL_alpha_v, l_t, Sw, b, S, AR)
        print(f"Estimated vertical tail area Sv = {Sv_needed:.4f} m^2")
    except ValueError as e:
        print("Could not find Sv:", e)

           # ---------------- Cm vs alpha curves 
alpha_deg = np.linspace(0, 10, 201)         # 0..10 deg like the example
alpha_rad = np.deg2rad(alpha_deg)

# pick trim point B at 5 deg (so both curves cross Cm=0 at alpha_trim)
alpha_trim_deg = 5.0
alpha_trim_rad = math.radians(alpha_trim_deg)

# choose Cm0 so Cm(alpha_trim) = 0 for the stable curve:
# Cm_stable = Cm0 + Cm_alpha_val*alpha  -> 0 = Cm0 + Cm_alpha_val*alpha_trim  => Cm0 = -Cm_alpha_val*alpha_trim
Cm0 = -Cm_alpha_val * alpha_trim_rad

# stable (negative slope)
Cm_stable = Cm0 + Cm_alpha_val * alpha_rad

# unstable (positive slope) - flip sign of slope
Cm_unstable = Cm0 - Cm_alpha_val * alpha_rad

# plot
plt.figure(figsize=(6,3.6))                 # compact, like your example
plt.plot(alpha_deg, Cm_stable, color='green', lw=2, label='Stable Aircraft')
plt.plot(alpha_deg, Cm_unstable, color='red', lw=2, label='Unstable Aircraft')

# trim (Cm=0) dotted line
plt.axhline(0.0, color='0.2', linestyle=':', linewidth=1)

# Points A, B, C (alpha positions chosen to mimic the example)
alpha_A = 2.0
alpha_B = alpha_trim_deg
alpha_C = 8.0

Cm_A = Cm0 + Cm_alpha_val * math.radians(alpha_A)    # stable curve value at A (but plot markers on Cm=0 line in example)
Cm_B = 0.0
Cm_C = Cm0 + Cm_alpha_val * math.radians(alpha_C)

# Draw circular markers like example (blue hollow circles on Cm=0)
plt.plot(alpha_A, 0.0, marker='o', markersize=7, markeredgecolor='blue', markerfacecolor='white')
plt.plot(alpha_B, 0.0, marker='o', markersize=7, markeredgecolor='blue', markerfacecolor='red')   # B colored to emphasise
plt.plot(alpha_C, 0.0, marker='o', markersize=7, markeredgecolor='blue', markerfacecolor='white')

# annotate A B C slightly above/below marker
plt.text(alpha_A - 0.6, -0.04, 'A', color='blue', fontsize=10)
plt.text(alpha_B - 0.1, -0.04, 'B', color='blue', fontsize=10)
plt.text(alpha_C - 0.1, -0.04, 'C', color='blue', fontsize=10)

# axes / limits / ticks to match the look
plt.xlim(0, 10)
plt.ylim(-0.4, 0.4)
plt.xticks(np.arange(0, 11, 1))
plt.yticks(np.linspace(-0.4, 0.4, 5))

plt.xlabel(r'$\alpha$ (deg)')
plt.ylabel(r'$C_m$')
plt.title('')
plt.legend(loc='upper right', frameon=True)
plt.grid(False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.tight_layout()
plt.show()

# ---------------- Directional stability output (Cn vs beta) ----------------

# compute current vertical tail volume coefficient using your Sv result
Vv = vertical_tail_volume_coefficient(Sv_needed, l_t, Sw, b)

# sideslip downwash factor
sideslip_factor = sideslip_downwash_factor(Sv_needed, Sw, AR)

# actual slope Cn_beta from YOUR airplane numbers
Cn_beta_deriv = Cn_beta_total(Cn_beta_wf, CL_alpha_v, Vv, sideslip_factor)

print(f"Directional stability derivative Cn_beta = {Cn_beta_deriv:.6f} per rad")

# beta range
beta = np.linspace(-1.0, 1.0, 300)

# stable (restoring yaw moment)
Cn_stable = Cn_beta_deriv * beta

# unstable (sign flipped)
Cn_unstable = -Cn_beta_deriv * beta

# plot
plt.figure(figsize=(6,4.5))
plt.plot(beta, Cn_stable, 'g-', linewidth=2, label='Stable Aircraft')
plt.plot(beta, Cn_unstable, 'r-', linewidth=2, label='Unstable Aircraft')

plt.axhline(0, color='k', linestyle='--')
plt.axvline(0, color='k')

plt.xlabel(r'$\beta$')
plt.ylabel(r'$C_N$')
plt.title('C_N vs Sideslip β')
plt.legend(loc='upper left')
plt.xlim(-1,1)

plt.tight_layout()
plt.show()    

