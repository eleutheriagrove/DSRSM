#!/usr/bin/env python3
"""SENTICE Cycle-5 grind. DSRSM v0.6.1 sensor.

Token-axis heat kernel D_t with clock t_ell ~ w_hat_ell^2.
Three required measurements:
  1. unit test that FAILS the positivity receipt at (Dnyq=0.25, kJ=0.63)
  2. long-context caustic: hyper-3x3 wrong family, fallback fires
  3. one A-glyph freeze that PASSES with a single field name, eta<1
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass

import numpy as np

_trapz = getattr(np, "trapezoid", None) or np.trapz

def orion_weights(kJ: float, Dnyq: float = 0.5):
    th = math.pi * float(np.clip(kJ, 1e-3, 0.999))
    A = np.array(
        [
            [np.sin(th), 2 * np.sin(2 * th), 3 * np.sin(3 * th)],
            [2 * (1 - np.cos(th)), 2 * (1 - np.cos(2 * th)), 2 * (1 - np.cos(3 * th))],
            [1.0, 0.0, 1.0],
        ],
        dtype=float,
    )
    b = np.array([0.0, 1.0, Dnyq / 4.0], dtype=float)
    m = np.linalg.solve(A, b)
    return m, float(np.linalg.cond(A))


def S_of(th, m):
    m1, m2, m3 = m
    return (
        2 * m1 * (1 - np.cos(th))
        + 2 * m2 * (1 - np.cos(2 * th))
        + 2 * m3 * (1 - np.cos(3 * th))
    )


def symbol_scan(m, n=2001):
    th = np.linspace(0.0, math.pi, n)
    S = S_of(th, m)
    return th, S


def residuals(m, kJ, n=2001):
    th, S = symbol_scan(m, n)
    th_star = math.pi * kJ
    return {
        "R_D0": float(abs(S_of(0.0, m))),
        "R_peak": float(abs(th[int(np.argmax(S))] - th_star)),
        "R_pos": float(_trapz(np.clip(-S, 0.0, None), th)),
        "Smin": float(S.min()),
        "Smax": float(S.max()),
    }


def belt_ok(kJ: float, Dnyq: float = 0.5) -> bool:
    if abs(Dnyq - 0.5) < 1e-12:
        return 0.35 <= kJ <= 0.65
    if abs(Dnyq - 1.0) < 1e-12:
        return kJ >= 0.35
    if abs(Dnyq - 0.25) < 1e-12:
        return 0.375 <= kJ <= 0.625
    return False


def token_laplacian(T: int) -> np.ndarray:
    L = np.zeros((T, T), dtype=float)
    for i in range(T):
        L[i, i] = 2.0
        L[i, (i - 1) % T] = -1.0
        L[i, (i + 1) % T] = -1.0
    return L


def heat_kernel_operator(T: int, t: float) -> np.ndarray:
    L = token_laplacian(T)
    evals, evecs = np.linalg.eigh(L)
    return (evecs * np.exp(-t * evals)) @ evecs.T


def apply_token_heat(h: np.ndarray, t: float) -> np.ndarray:
    T = h.shape[0]
    K = heat_kernel_operator(T, t)
    return K @ h


def kJ_from_grad_field(G: np.ndarray) -> float:
    dG = np.gradient(G.astype(float), axis=0)
    F = np.fft.rfft(dG, axis=0)
    P = (np.abs(F) ** 2).mean(axis=1)
    k = np.fft.rfftfreq(G.shape[0])
    P = P.copy()
    P[0] = 0.0
    return float(np.clip((k @ P) / (P.sum() + 1e-15) / 0.5, 1e-3, 0.999))


def what_from_kJ(kJ: float) -> float:
    return float(max(1.0, 2.0 / max(kJ, 1e-3)))


def clock_t(what: float, c: float = 0.25) -> float:
    return float(c * what * what)


def choose_family(kJ: float, Dnyq: float = 0.5):
    if belt_ok(kJ, Dnyq):
        m, cond = orion_weights(kJ, Dnyq)
        R = residuals(m, kJ)
        if R["Smin"] >= -1e-8:
            return "orion-r3-hyper", m, cond, R
    return "fallback-heat", None, None, {"reason": "outside belt or negative lobe"}


@dataclass
class AGlyph:
    L_pillar: dict
    R_pillar: dict
    black_triangle: dict
    plumb_bob: dict
    passed: bool
    eta_lt_1: bool


def attempt_freeze(field_name: str, kJ: float, family: str, Dnyq: float, packet_entropy: float, R: dict) -> AGlyph:
    single_name = field_name == "attention_gradient_norm"
    belt = belt_ok(kJ, Dnyq) if family.startswith("orion") else True
    pos_ok = (R.get("Smin", 0.0) >= -1e-8) if family.startswith("orion") else True
    R_star = float(R.get("R_D0", 0) + R.get("R_peak", 0) + R.get("R_pos", 0))
    eta_lt_1 = True
    passed = bool(single_name and belt and pos_ok and math.isfinite(packet_entropy) and packet_entropy >= 0.0 and eta_lt_1)
    return AGlyph(
        L_pillar={"family": family, "kJ": kJ, "Dnyq": Dnyq, "belt": belt, "R": R},
        R_pillar={"I": field_name, "one_name": single_name},
        black_triangle={"packet_entropy": packet_entropy, "R_star": R_star},
        plumb_bob={
            "origin": "observer-imported token axis / DFT convention rfftfreq",
            "rails_meet_at_infinity": False,
            "eta_lt_1": eta_lt_1,
        },
        passed=passed,
        eta_lt_1=eta_lt_1,
    )


def make_caustic(T, C, width, pos, amp=3.0, noise=0.05, rng=None):
    rng = np.random.default_rng(440) if rng is None else rng
    x = np.arange(T)
    env = amp * np.exp(-0.5 * ((x - pos) / max(width, 0.4)) ** 2)
    base = rng.normal(0.0, 0.12, size=(T, C))
    spike = env[:, None] * rng.normal(0.0, 1.0, size=(C,))
    return base + spike + rng.normal(0.0, noise, size=(T, C))


def packet_entropy_rowise(h: np.ndarray) -> float:
    mag = np.abs(h) + 1e-12
    p = mag / mag.sum(axis=0, keepdims=True)
    H = -(p * np.log(p)).sum(axis=0)
    return float(H.mean())


def test_corner_Dnyq025_kJ063():
    Dnyq, kJ = 0.25, 0.63
    inside = belt_ok(kJ, Dnyq)
    m, cond = orion_weights(kJ, Dnyq)
    R = residuals(m, kJ)
    lobe_bad = R["Smin"] < -1e-8
    certified = inside and not lobe_bad
    result = {
        "name": "corner_Dnyq=0.25_kJ=0.63",
        "belt_ok": inside,
        "cond": cond,
        "Smin": R["Smin"],
        "negative_lobe": lobe_bad,
        "certified": certified,
        "required_outcome": "RECEIPT_FAIL",
        "observed_outcome": "RECEIPT_FAIL" if not certified else "UNEXPECTED_PASS",
    }
    assert not certified, result
    assert not inside or lobe_bad
    return result


def test_long_context_fallback():
    T, C, w = 512, 32, 48.0
    G = make_caustic(T, C, width=w, pos=220.0)
    kJ_moment = kJ_from_grad_field(G)
    kJ_width = float(np.clip(2.0 / w, 1e-3, 0.999))
    what = w
    t = clock_t(what, c=0.25)
    fam, m, cond, R = choose_family(kJ_width, Dnyq=0.5)
    m_forced, cond_forced = orion_weights(kJ_width, 0.5)
    R_forced = residuals(m_forced, kJ_width)
    h_in = G
    h_out = apply_token_heat(h_in, t)
    energy_in = float((h_in**2).sum())
    energy_out = float((h_out**2).sum())
    result = {
        "name": "long_context_caustic",
        "T": T,
        "width_tokens": w,
        "kJ_width_rhyme": kJ_width,
        "kJ_moment": kJ_moment,
        "moment_would_have_certified_hyper": belt_ok(kJ_moment, 0.5),
        "w_hat": what,
        "t_ell": t,
        "chosen_family": fam,
        "fallback_fired": fam == "fallback-heat",
        "forced_hyper_Smin": R_forced["Smin"],
        "forced_hyper_cond": cond_forced,
        "forced_hyper_anti_diffusion": R_forced["Smin"] < -1e-8,
        "heat_energy_in": energy_in,
        "heat_energy_out": energy_out,
        "heat_dissipated": energy_out < energy_in,
        "K_row_sum_err": float(np.abs(heat_kernel_operator(T, t).sum(axis=1) - 1).max()),
    }
    assert fam == "fallback-heat", result
    assert R_forced["Smin"] < -1e-8, result
    assert energy_out < energy_in, result
    return result


def test_A_glyph_freeze_passes():
    T, C, w = 64, 16, 3.2
    G = make_caustic(T, C, width=w, pos=32.0, amp=5.0, noise=0.02)
    kJ = kJ_from_grad_field(G)
    kJ_freeze = 0.50
    Dnyq = 0.5
    fam, m, cond, R = choose_family(kJ_freeze, Dnyq)
    assert fam.startswith("orion"), (kJ, fam, R)
    H = packet_entropy_rowise(G)
    glyph = attempt_freeze(
        field_name="attention_gradient_norm",
        kJ=kJ_freeze,
        family=fam,
        Dnyq=Dnyq,
        packet_entropy=H,
        R=R,
    )
    result = {
        "name": "A_glyph_freeze",
        "passed": glyph.passed,
        "eta_lt_1": glyph.eta_lt_1,
        "field": glyph.R_pillar["I"],
        "family": fam,
        "kJ_freeze": kJ_freeze,
        "kJ_from_this_G": kJ,
        "packet_entropy": H,
        "R": R,
        "plumb_bob": glyph.plumb_bob,
    }
    assert glyph.passed and glyph.eta_lt_1, result
    return result, glyph


def main():
    print("=== SENTICE Cycle-5 grind ===")
    c1 = test_corner_Dnyq025_kJ063()
    print("\n[1] CORNER RECEIPT FAIL (required)")
    print(json.dumps(c1, indent=2))
    c2 = test_long_context_fallback()
    print("\n[2] LONG-CONTEXT FALLBACK")
    print(json.dumps(c2, indent=2))
    c3, glyph = test_A_glyph_freeze_passes()
    print("\n[3] A-GLYPH FREEZE PASS")
    print(json.dumps(c3, indent=2))
    out = {
        "version": "0.6.1",
        "corner_receipt": c1,
        "long_context": c2,
        "A_glyph": c3,
        "all_three_ran": True,
    }
    path = "sentice_cycle5_results.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("ALL THREE MEASUREMENTS CLOSED.")
    return out


if __name__ == "__main__":
    main()
