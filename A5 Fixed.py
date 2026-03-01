import numpy as np
import matplotlib.pyplot as plt
import math

# Convert "per degree" -> "per radian"
def per_deg_to_per_rad(per_deg: float) -> float:
    return per_deg * (180.0 / np.pi)

# ---------- longitudinal_stability ----------
def downwash_derivative(CL_alpha_wing, AR_wing):
    """
    d_eps/d_alpha ≈ 2 * CL_alpha_wing / (pi * AR_wing)
    """
    return 2.0 * CL_alpha_wing / (np.pi * AR_wing)

def lift_curve_3d(a_2d, AR, e=1.0):
    """
    a_3d = a_2d / (1 + a_2d / (pi * AR * e))
    """
    return a_2d / (1.0 + (a_2d / (np.pi * AR * e)))

def tail_volume_coefficient(S_t, l_t, S, c):
    """
    V_H = (S_t * l_t) / (S * c)
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
    SM = (x_NP - x_cg) / c
    """
    return (x_NP - x_cg) / c

# ---------- directional / vertical tail ----------
def sideslip_downwash_factor(Sv, S, AR):
    """
    (1 + dσ/dβ) = 0.724 + (3.06 * (Sv/S)) / (1 + 0.009*AR)
    """
    return 0.724 + (3.06 * (Sv / S)) / (1.0 + 0.009 * AR)

def vertical_tail_volume_coefficient(Sv, lt, Sw, b):
    """
    Vv = (Sv * lt) / (Sw * b)
    """
    return (Sv * lt) / (Sw * b)

def Cn_beta_total(Cn_beta_wf, CL_alpha_v, Vv, sideslip_factor):
    """
    Cnβ = Cnβ,wf + CLα,v * Vv * (1 + dσ/dβ)
    """
    return Cn_beta_wf + CL_alpha_v * Vv * sideslip_factor

def solve_Sv_for_target_Cn_beta(Cn_beta_target, Cn_beta_wf, CL_alpha_v, lt, Sw, b, S, AR):
    """
    Solve for Sv given a target Cn_beta using bisection on a bracket.
    """
    def f(Sv):
        factor = sideslip_downwash_factor(Sv, S, AR)
        Vv = vertical_tail_volume_coefficient(Sv, lt, Sw, b)
        return Cn_beta_total(Cn_beta_wf, CL_alpha_v, Vv, factor) - Cn_beta_target

    lo, hi = 1e-6, 1e4  # broad bracket (area units consistent with your S, Sv)
    flo, fhi = f(lo), f(hi)

    if flo * fhi > 0:
        raise ValueError("Bracket does not contain root; try different lo/hi or check inputs/units.")

    for _ in range(120):
        mid = 0.5 * (lo + hi)
        fmid = f(mid)
        if abs(fmid) < 1e-12:
            return mid
        if flo * fmid < 0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid

    return 0.5 * (lo + hi)

# ------------------------------- main -------------------------------
if __name__ == "__main__":
    # Example numbers (replace with our actual values)
    C_m_ac = -0.02
    x_ac = 1.2        # datum units (must match x_cg and c)
    x_cg = 1.0
    c = 1.5           # mean aerodynamic chord
    CL_alpha_wing = 5.7    # per rad

    a2d_tail = 2.0 * np.pi # per rad (section)
    AR_tail = 4.0
    e_tail = 0.9

    eta = 0.95
    S_t = 2.0
    l_t = 4.5
    S = 25.0
    Sw = S

    # Wing AR used for downwash derivative
    AR_wing = 8.0

    CL_alpha_tail = lift_curve_3d(a2d_tail, AR_tail, e_tail)
    V_H = tail_volume_coefficient(S_t, l_t, S, c)
    deps_dalpha = downwash_derivative(CL_alpha_wing, AR_wing=AR_wing)

    Cm_alpha_val = C_m_alpha(C_m_ac, x_cg, x_ac, c,
                             CL_alpha_wing, eta, V_H, CL_alpha_tail, deps_dalpha)
    x_NP = neutral_point_location(x_ac, C_m_ac, CL_alpha_wing,
                                  eta, V_H, CL_alpha_tail, deps_dalpha)
    SM = static_margin(x_NP, x_cg, c)

    print(f"Cm_alpha = {Cm_alpha_val:.6f} per rad")
    print(f"Neutral point x_NP = {x_NP:.4f}")
    print(f"Static margin (fraction of c) = {SM:.4f}")

    # ---------------- Cm vs alpha curves ----------------
    # ---------------- Cm vs alpha curves ----------------

    alpha_deg = np.linspace(0, 10, 201)

# Match reference-style slope
    Cm0 = 0.2
    Cm_alpha_per_deg = -0.04   # stable slope

    Cm_stable = Cm0 + Cm_alpha_per_deg * alpha_deg
    Cm_unstable = -Cm_stable

    plt.figure(figsize=(6, 3.6))

    plt.plot(alpha_deg, Cm_stable, 'g-', linewidth=2, label='Stable Aircraft')
    plt.plot(alpha_deg, Cm_unstable, 'r-', linewidth=2, label='Unstable Aircraft')

# Trim line
    plt.axhline(0, color='black', linestyle='-', linewidth=1)

# A, B, C positions
    alpha_A = 3
    alpha_B = 5
    alpha_C = 7

# Plot markers
    plt.plot([alpha_A, alpha_B, alpha_C],
         [0, 0, 0],
         'o',
         markeredgecolor='blue',
         markerfacecolor='white')

# Label them
    plt.text(alpha_A - 0.15, 0.02, 'A')
    plt.text(alpha_B - 0.15, 0.02, 'B')
    plt.text(alpha_C - 0.15, 0.02, 'C')

plt.xlim(0, 10)
plt.ylim(-0.4, 0.4)

plt.xlabel(r'$\alpha$')
plt.ylabel(r'$C_m$')
plt.legend(loc='upper right')
plt.grid(False)

plt.tight_layout()
plt.show()
    # ---------------- Directional stability (Cn vs beta) ----------------
    # Inputs
Cn_beta_target_deg = 0.001   # per degree (as your comment said)
Cn_beta_target = per_deg_to_per_rad(Cn_beta_target_deg)  # convert to per rad

Cn_beta_wf = 0.0002          # per rad (make sure this matches your convention!)
CL_alpha_v = 2.0 * np.pi     # per rad (approx)
b = 10.0
AR = AR_wing                 # reuse if you want

Sv_needed = None
try:
        Sv_needed = solve_Sv_for_target_Cn_beta(
            Cn_beta_target, Cn_beta_wf, CL_alpha_v,
            l_t, Sw, b, S, AR
        )
        print(f"Estimated vertical tail area Sv = {Sv_needed:.4f}")
except ValueError as e:
        print("Could not find Sv:", e)

    # Only proceed if we actually solved for Sv
if Sv_needed is not None:
        Vv = vertical_tail_volume_coefficient(Sv_needed, l_t, Sw, b)
        sideslip_factor = sideslip_downwash_factor(Sv_needed, S, AR)
        Cn_beta_deriv = Cn_beta_total(Cn_beta_wf, CL_alpha_v, Vv, sideslip_factor)

        print(f"Directional stability derivative Cn_beta = {Cn_beta_deriv:.6f} per rad")

        beta = np.linspace(-1.0, 1.0, 300)
        Cn_stable = Cn_beta_deriv * beta
        Cn_unstable = -Cn_beta_deriv * beta

        plt.figure(figsize=(6, 4.5))
        plt.plot(beta, Cn_stable, 'g-', linewidth=2, label='Stable Aircraft')
        plt.plot(beta, Cn_unstable, 'r-', linewidth=2, label='Unstable Aircraft')

        plt.axhline(0, color='k', linestyle='--')
        plt.axvline(0, color='k')

        plt.xlabel(r'$\beta$')
        plt.ylabel(r'$C_N$')
        plt.title('C_N vs Sideslip β')
        plt.legend(loc='upper left')
        plt.xlim(-1, 1)
        plt.tight_layout()
        plt.show()