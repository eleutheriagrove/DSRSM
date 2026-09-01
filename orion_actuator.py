"""Orion radius-3 symbol + belt gate. DSRSM v0.6.1 companion."""
import numpy as np

def orion_weights(kJ, Dnyq=0.5):
    th = np.pi * float(np.clip(kJ, 1e-3, 0.999))
    A = np.array([
        [np.sin(th), 2 * np.sin(2 * th), 3 * np.sin(3 * th)],
        [2 * (1 - np.cos(th)), 2 * (1 - np.cos(2 * th)), 2 * (1 - np.cos(3 * th))],
        [1.0, 0.0, 1.0],
    ])
    b = np.array([0.0, 1.0, Dnyq / 4.0])
    return np.linalg.solve(A, b), float(np.linalg.cond(A))

def S_of(th, m):
    m1, m2, m3 = m
    return (
        2 * m1 * (1 - np.cos(th))
        + 2 * m2 * (1 - np.cos(2 * th))
        + 2 * m3 * (1 - np.cos(3 * th))
    )

def belt_ok(kJ, Dnyq=0.5):
    if abs(Dnyq - 0.5) < 1e-12:
        return 0.35 <= kJ <= 0.65
    if abs(Dnyq - 1.0) < 1e-12:
        return kJ >= 0.35
    if abs(Dnyq - 0.25) < 1e-12:
        return 0.375 <= kJ <= 0.625
    return False

def residuals(m, kJ, n=2001):
    th = np.linspace(0.0, np.pi, n)
    S = S_of(th, m)
    th_star = np.pi * kJ
    pos_int = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
    return dict(
        R_D0=float(abs(S_of(0.0, m))),
        R_peak=float(abs(th[int(np.argmax(S))] - th_star)),
        R_pos=float(pos_int(np.clip(-S, 0.0, None), th)),
        Smin=float(S.min()),
        Smax=float(S.max()),
    )

def kJ_from_grad_field(G):
    dG = np.gradient(G, axis=0)
    F = np.fft.rfft(dG, axis=0)
    P = (np.abs(F) ** 2).mean(axis=1)
    k = np.fft.rfftfreq(G.shape[0])
    P[0] = 0.0
    return float(np.clip((k @ P) / (P.sum() + 1e-15) / 0.5, 1e-3, 0.999))

def choose_family(kJ, Dnyq=0.5):
    if belt_ok(kJ, Dnyq):
        m, cond = orion_weights(kJ, Dnyq)
        return "orion-r3", m, cond, residuals(m, kJ)
    return "fallback-physical-or-heat", None, None, {"reason": "outside belt"}

if __name__ == "__main__":
    for kJ in (0.20, 0.40, 0.50, 0.60, 0.80):
        fam, m, cond, R = choose_family(kJ)
        print(f"kJ={kJ:.2f} family={fam} cond={cond} R={R}")
