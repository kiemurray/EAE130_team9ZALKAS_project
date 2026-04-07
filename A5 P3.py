import numpy as np
import matplotlib.pyplot as plt
import math

# Unit conversions

def per_deg_to_per_rad(x_per_deg: float) -> float:
    return x_per_deg * (180.0 / np.pi)

def per_rad_to_per_deg(x_per_rad: float) -> float:
    return x_per_rad * (np.pi / 180.0)


# Longitudinal stability

def CL_alpha_low_AR(AR: float) -> float:
    """
    Finite-wing lift curve slope approximation for low AR wings (per rad).
    CL_a = (2*pi*AR) / (2 + sqrt(4 + AR^2))
    """
    return (2.0 * np.pi * AR) / (2.0 + np.sqrt(4.0 + AR**2))


def Cm_alpha_tailless(Cm_ac: float, x_cg: float, x_ac: float, c: float, CL_alpha: float) -> float:
    """
    Approximate longitudinal pitching moment slope.
    Stable if Cm_alpha < 0.
    """
    return Cm_ac + ((x_cg - x_ac) / c) * CL_alpha


def neutral_point_tailless(x_ac: float, Cm_ac: float, CL_alpha: float) -> float:
    """
    Tailless neutral point:
      x_NP = x_ac - Cm_ac / CL_alpha
    """
    return x_ac - (Cm_ac / CL_alpha)


def static_margin(x_NP: float, x_cg: float, c: float) -> float:
    return (x_NP - x_cg) / c


# Tail + downwash + full neutral point

def downwash_gradient(CL_alpha_w: float, AR: float) -> float:
    """
    dε/dα = (2 * CLα_w) / (π * AR)
    """
    return (2.0 * CL_alpha_w) / (np.pi * AR)


def horizontal_tail_volume(St: float, lt: float, S: float, c: float) -> float:
    """
    V_H = (S_t * l_t) / (S * c)
    """
    return (St * lt) / (S * c)


def neutral_point_full(
    x_ac: float,
    c: float,
    Cm_alpha_f: float,
    CL_alpha_w: float,
    eta: float,
    V_H: float,
    CL_alpha_t: float,
    d_eps_d_alpha: float,
) -> float:
    """
    Full neutral point equation:

    x_NP/c = x_ac/c
             - Cm_alpha_f / CL_alpha_w
             + eta * V_H * (CL_alpha_t / CL_alpha_w) * (1 - dε/dα)
    """
    x_np_over_c = (
        (x_ac / c)
        - (Cm_alpha_f / CL_alpha_w)
        + eta * V_H * (CL_alpha_t / CL_alpha_w) * (1.0 - d_eps_d_alpha)
    )
    return x_np_over_c * c


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
    alpha_deg = np.linspace(-5, 15, 201)
    alpha_rad = np.deg2rad(alpha_deg)
    alpha_trim_rad = np.deg2rad(alpha_trim_deg)

    Cm0 = -Cm_alpha_per_rad * alpha_trim_rad
    Cm = Cm0 + Cm_alpha_per_rad * alpha_rad

    plt.figure(figsize=(6, 3.6))
    color = 'g' if Cm_alpha_per_rad < 0 else 'r'
    label = r'Stable ($Cm_{\alpha}$ < 0)' if Cm_alpha_per_rad < 0 else r'Unstable ($Cm_{\alpha}$ > 0)'
    plt.plot(np.rad2deg(alpha_rad), Cm, color=color, linewidth=2, label=label)
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(alpha_trim_deg, color='gray', linestyle='--', label=f'Trim α={alpha_trim_deg}°')
    plt.xlabel(r'$\alpha$ (deg)')
    plt.ylabel(r'$C_m$')
    plt.title(rf'Cm vs $\alpha$  |  $Cm_{{\alpha}}$ = {per_rad_to_per_deg(Cm_alpha_per_rad):.4f} /deg')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_Cn_vs_beta(Cn_beta_per_rad: float):
    beta_deg = np.linspace(-30, 30, 300)
    beta_rad = np.deg2rad(beta_deg)

    Cn = Cn_beta_per_rad * beta_rad

    plt.figure(figsize=(6, 4.5))
    color = 'g' if Cn_beta_per_rad > 0 else 'r'
    label = r'Stable ($Cn_{\beta}$ > 0)' if Cn_beta_per_rad > 0 else r'Unstable ($Cn_{\beta}$ < 0)'
    plt.plot(beta_deg, Cn, color=color, linewidth=2, label=label)
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.xlabel(r'$\beta$ (deg)')
    plt.ylabel(r'$C_n$')
    plt.title(rf'$C_n$ vs $\beta$  |  $Cn_{{\beta}}$ = {per_rad_to_per_deg(Cn_beta_per_rad):.4f} /deg')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# MAIN

if __name__ == "__main__":

    # OpenVSP geometry (MAIN WING)
    S = 684.1245
    b = 41.0
    c = 19.90529
    AR = b**2 / S

    # Absolute coordinates from OpenVSP
    x_wing_le_abs = -17.190
    x_cg_abs = -9.229

    # Convert CG to wing-LE datum
    x_cg = x_cg_abs - x_wing_le_abs

    # Wing-body aerodynamic center assumption
    x_ac = 0.25 * c

    # Wing-body pitching moment about AC
    Cm_ac = -0.03

    # Lift curve slope
    CL_alpha = CL_alpha_low_AR(AR)

    # Tail / longitudinal stability parameters
    eta = 0.9
    CL_alpha_t = 2.0 * np.pi
    Cm_alpha_f = 0.02
    St = 150.0

    # Longitudinal derivative
    Cm_alpha_val = Cm_alpha_tailless(Cm_ac, x_cg, x_ac, c, CL_alpha)

    print("---- Longitudinal Stability ----")
    print(f"S = {S:.4f}, b = {b:.4f}, c(MAC) = {c:.5f}, AR = {AR:.4f}")
    print(f"Wing LE abs = {x_wing_le_abs:.3f}, CG abs = {x_cg_abs:.3f}")
    print(f"CG from wing LE = {x_cg:.3f}  => {100*x_cg/c:.2f}% MAC")
    print(f"Assumed x_ac = {x_ac:.3f}  => {100*x_ac/c:.2f}% MAC")
    print(f"CL_alpha = {CL_alpha:.4f} per rad")
    print(f"Cm_ac = {Cm_ac:.4f}")
    print(f"Cm_alpha = {Cm_alpha_val:.6f} per rad  (stable if negative)")

    # Plot longitudinal stability
    plot_Cm_vs_alpha(Cm_alpha_val, alpha_trim_deg=5.0)

    # Tail geometry
    XLoc_v_abs = 5.598
    MAC_v = 5.01667

    # Tail AC approx at quarter-chord
    x_ac_v_abs = XLoc_v_abs + 0.25 * MAC_v

    # Tail arm relative to CG
    lt = x_ac_v_abs - x_cg_abs

    # Derived longitudinal stability terms
    V_H = horizontal_tail_volume(St, lt, S, c)
    d_eps_d_alpha = downwash_gradient(CL_alpha, AR)

    # Full neutral point and static margin
    x_NP = neutral_point_full(
        x_ac=x_ac,
        c=c,
        Cm_alpha_f=Cm_alpha_f,
        CL_alpha_w=CL_alpha,
        eta=eta,
        V_H=V_H,
        CL_alpha_t=CL_alpha_t,
        d_eps_d_alpha=d_eps_d_alpha,
    )

    SM = static_margin(x_NP, x_cg, c)

    print("\n---- Neutral Point (Full Model) ----")
    print(f"Tail XLoc abs = {XLoc_v_abs:.3f}, MAC_v = {MAC_v:.5f}")
    print(f"Tail AC abs ≈ {x_ac_v_abs:.3f}")
    print(f"lt = x_ac_v_abs - x_cg_abs = {lt:.3f}")
    print(f"dε/dα = {d_eps_d_alpha:.4f}")
    print(f"V_H = {V_H:.4f}")
    print(f"x_NP = {x_NP:.3f} => {100*x_NP/c:.2f}% MAC")
    print(f"Static Margin = {SM:.4f}  (~{100*SM:.2f}%)")

    # Directional stability inputs
    Cn_beta_target_deg = 0.10
    Cn_beta_target = per_deg_to_per_rad(Cn_beta_target_deg)

    Cn_beta_wf = 0.0
    CL_alpha_v = 2.0 * np.pi

    print("\n---- Directional Stability ----")

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

        # Plot directional stability
        plot_Cn_vs_beta(Cn_beta)

    except ValueError as e:
        print("Could not solve for Sv:", e)
        print("No Cn vs beta plot produced.")