import numpy as np
import matplotlib.pyplot as plt


# Unit conversions

def per_deg_to_per_rad(x_per_deg: float) -> float:
    return x_per_deg * (180.0 / np.pi)

def per_rad_to_per_deg(x_per_rad: float) -> float:
    return x_per_rad * (np.pi / 180.0)

# Longitudinal (tailless cranked-arrow / delta-like)

def CL_alpha_low_AR(AR: float) -> float:
    """
    Finite-wing lift curve slope approximation for low AR wings (per rad).
    CL_a = (2*pi*AR) / (2 + sqrt(4 + AR^2))
    """
    return (2.0 * np.pi * AR) / (2.0 + np.sqrt(4.0 + AR**2))

def Cm_alpha_tailless(Cm_ac: float, x_cg: float, x_ac: float, c: float, CL_alpha: float) -> float:
    """
    Tailless: Cm_alpha = Cm_ac + ((x_cg - x_ac)/c)*CL_alpha
    Stable if Cm_alpha < 0
    """
    return Cm_ac + ((x_cg - x_ac) / c) * CL_alpha

def neutral_point_tailless(x_ac: float, Cm_ac: float, CL_alpha: float) -> float:
    """
    Tailless neutral point:
      x_NP = x_ac - Cm_ac/CL_alpha
    """
    return x_ac - (Cm_ac / CL_alpha)

def static_margin(x_NP: float, x_cg: float, c: float) -> float:
    return (x_NP - x_cg) / c


# Directional stability (vertical tail)

def sideslip_downwash_factor(Sv: float, S_ref: float, AR_wing: float) -> float:
    """
    (1 + dσ/dβ) = 0.724 + (3.06*(Sv/S)) / (1 + 0.009*AR)
    """
    return 0.724 + (3.06 * (Sv / S_ref)) / (1.0 + 0.009 * AR_wing)

def vertical_tail_volume_coefficient(Sv: float, lt: float, S_ref: float, b: float) -> float:
    """
    Vv = (Sv * lt) / (S * b)
    """
    return (Sv * lt) / (S_ref * b)

def Cn_beta_total(Cn_beta_wf: float, CL_alpha_v: float, Vv: float, sideslip_factor: float) -> float:
    """
    Cnβ = Cnβ,wf + CLα,v * Vv * (1 + dσ/dβ)
    """
    return Cn_beta_wf + CL_alpha_v * Vv * sideslip_factor

def solve_Sv_for_target_Cn_beta(
    Cn_beta_target: float,
    Cn_beta_wf: float,
    CL_alpha_v: float,
    lt: float,
    S_ref: float,
    b: float,
    AR_wing: float,
    max_iter: int = 120
) -> float:
    """
    Bisection solve for Sv such that Cn_beta_total == Cn_beta_target (all per rad).
    """
    def f(Sv: float) -> float:
        factor = sideslip_downwash_factor(Sv, S_ref, AR_wing)
        Vv = vertical_tail_volume_coefficient(Sv, lt, S_ref, b)
        return Cn_beta_total(Cn_beta_wf, CL_alpha_v, Vv, factor) - Cn_beta_target

    lo, hi = 1e-6, 1e5
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        raise ValueError("Bisection bracket failed. Check target/units or adjust bracket limits.")

    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        fmid = f(mid)
        if abs(fmid) < 1e-12:
            return mid
        if flo * fmid < 0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid

    return 0.5 * (lo + hi)

# Plotting 
def plot_Cm_vs_alpha(Cm_alpha_per_rad: float, alpha_trim_deg: float = 5.0):
    alpha_rad = np.linspace(np.deg2rad(-0.4), np.deg2rad(10), 201)
    alpha_trim_rad = np.deg2rad(alpha_trim_deg)

    m = abs(Cm_alpha_per_rad)
    Cm_alpha_stable = -m
    Cm_alpha_unstable = +m

    Cm0 = -Cm_alpha_stable * alpha_trim_rad  # stable passes through trim

    Cm_stable = Cm0 + Cm_alpha_stable * alpha_rad
    Cm_unstable = Cm0 + Cm_alpha_unstable * alpha_rad

    plt.figure(figsize=(6, 3.6))
    plt.plot(alpha_rad, Cm_stable, 'g-', linewidth=2, label='Stable Aircraft')
    plt.plot(alpha_rad, Cm_unstable, 'r-', linewidth=2, label='Unstable Aircraft')
    plt.axhline(0, color='black', linewidth=1)

    # markers at A,B,C (still in degrees, converted to rad)
    alpha_A, alpha_B, alpha_C = map(np.deg2rad, [3, 5, 7])
    plt.plot([alpha_A, alpha_B, alpha_C], [0, 0, 0],
             'o', markeredgecolor='blue', markerfacecolor='white')
    plt.text(alpha_A, 0.02, 'A')
    plt.text(alpha_B, 0.02, 'B')
    plt.text(alpha_C, 0.02, 'C')

    plt.xlim(np.deg2rad(-0.4), np.deg2rad(10))
    plt.ylim(-0.4, 0.4)
    plt.xlabel(r'$\alpha$ (rad)')
    plt.ylabel(r'$C_m$')
    plt.legend(loc='upper right')
    plt.grid(False)
    plt.tight_layout()
    plt.show()

def plot_Cn_vs_beta(Cn_beta_per_rad: float):
    beta = np.linspace(-1.0, 1.0, 300)
    Cn_stable = Cn_beta_per_rad * beta
    Cn_unstable = -Cn_beta_per_rad * beta

    plt.figure(figsize=(6, 4.5))
    plt.plot(beta, Cn_stable, 'g-', linewidth=2, label='Stable Aircraft')
    plt.plot(beta, Cn_unstable, 'r-', linewidth=2, label='Unstable Aircraft')
    plt.axhline(0, color='k', linestyle='--')
    plt.axvline(0, color='k')
    plt.xlabel(r'$\beta$ (rad)')
    plt.ylabel(r'$C_N$')
    plt.title('C_N vs Sideslip β')
    plt.legend(loc='upper left')
    plt.xlim(-1, 1)
    plt.tight_layout()
    plt.show()


# MAIN

if __name__ == "__main__":

   
    # OpenVSP geometry (MAINWING) 
    S = 684.1245
    b = 41.0
    c = 19.90706  # MAC length
    AR = b**2 / S

    # Absolute coordinates from OpenVSP:
    x_wing_le_abs = -13.107   # wing XLoc from your earlier XForm 
    x_cg_abs = -9.229         # your actual CG (absolute)

    # Convert CG to wing-LE datum (so x=0 at wing LE)
    x_cg = x_cg_abs - x_wing_le_abs  # = 3.878...

    # Wing-body AC assumption (subsonic): ~ 25% MAC from wing LE
    x_ac = 0.25 * c

    # Wing-body pitching moment about AC 
    Cm_ac = -0.03

    # Lift curve slope (per rad)
    CL_alpha = CL_alpha_low_AR(AR)

    # Longitudinal derivatives
    Cm_alpha_val = Cm_alpha_tailless(Cm_ac, x_cg, x_ac, c, CL_alpha)
    x_NP = neutral_point_tailless(x_ac, Cm_ac, CL_alpha)
    SM = static_margin(x_NP, x_cg, c)

    print("---- Longitudinal (Tailless Cranked-Arrow) ----")
    print(f"S={S:.4f}, b={b:.4f}, c(MAC)={c:.5f}, AR={AR:.4f}")
    print(f"Wing LE abs = {x_wing_le_abs:.3f}, CG abs = {x_cg_abs:.3f}")
    print(f"CG from wing LE = {x_cg:.3f}  => {100*x_cg/c:.2f}% MAC")
    print(f"Assumed x_ac = {x_ac:.3f}  => {100*x_ac/c:.2f}% MAC")
    print(f"CL_alpha = {CL_alpha:.4f} per rad")
    print(f"Cm_ac = {Cm_ac:.4f}")
    print(f"Cm_alpha = {Cm_alpha_val:.6f} per rad  (stable if negative)")
    print(f"x_NP = {x_NP:.3f} => {100*x_NP/c:.2f}% MAC")
    print(f"Static Margin = {SM:.4f}  (~{100*SM:.2f}%)")

    # ---------------- PLOT 1: Cm vs alpha ----------------
    plot_Cm_vs_alpha(Cm_alpha_val, alpha_trim_deg=5.0)

   
    # OpenVSP geometry (VERTICAL TAIL / Stabilators)
    # From tail XForm + Plan:
    XLoc_v_abs = 8.598
    MAC_v = 5.01667

    # Tail AC approx at quarter-chord
    x_ac_v_abs = XLoc_v_abs + 0.25 * MAC_v

    # Tail arm relative to CG
    lt = x_ac_v_abs - x_cg_abs

    print("\n---- Directional (Vertical Tail) ----")
    print(f"Tail XLoc abs = {XLoc_v_abs:.3f}, MAC_v = {MAC_v:.5f}")
    print(f"Tail AC abs ≈ {x_ac_v_abs:.3f}")
    print(f"lt = x_ac_v_abs - x_cg_abs = {lt:.3f}")

    Cn_beta_target_deg = 0.10   # <-- CHANGE if needed
    Cn_beta_target = per_deg_to_per_rad(Cn_beta_target_deg)  # convert to per rad

    # Baseline wing-fuselage yaw stability (placeholder; set if known)
    Cn_beta_wf = 0.0  # per rad

    # Vertical tail lift curve slope (placeholder; can be refined with its AR)
    CL_alpha_v = 2.0 * np.pi  # per rad

    # Solve for Sv and plot Cn vs beta
    #Beta is just wind coming from the right or left, Positive B = right, negative B = left
    #cnb > 0 slope postive means stable and other way around means unstable
    try:
        Sv_needed = solve_Sv_for_target_Cn_beta(
            Cn_beta_target=Cn_beta_target,
            Cn_beta_wf=Cn_beta_wf,
            CL_alpha_v=CL_alpha_v,
            lt=lt,
            S_ref=S,
            b=b,
            AR_wing=AR
        )

        factor = sideslip_downwash_factor(Sv_needed, S, AR)
        Vv = vertical_tail_volume_coefficient(Sv_needed, lt, S, b)
        Cn_beta = Cn_beta_total(Cn_beta_wf, CL_alpha_v, Vv, factor)

        print(f"Target Cn_beta = {Cn_beta_target_deg:.4f} per deg = {Cn_beta_target:.6f} per rad")
        print(f"Sv_needed = {Sv_needed:.4f} (same area units as S)")
        print(f"Achieved Cn_beta = {Cn_beta:.6f} per rad = {per_rad_to_per_deg(Cn_beta):.6f} per deg")

        # ---------------- PLOT 2: Cn vs beta ----------------
        plot_Cn_vs_beta(Cn_beta)

    except ValueError as e:
        print("Could not solve for Sv:", e)
        print("No Cn vs beta plot produced.")