#!/usr/bin/env python3
"""DSRSM v0.7.0 Fisher-ridge, width gate, radius-5 attempt + heat fallthrough."""
from __future__ import annotations
import json, math
from dataclasses import dataclass
import numpy as np

_trapz = getattr(np, "trapezoid", None) or np.trapz

def S_of(th, m):
    acc = np.zeros_like(np.asarray(th), dtype=float)
    for j, mj in enumerate(np.asarray(m, dtype=float), start=1):
        acc = acc + 2.0 * mj * (1.0 - np.cos(j * th))
    return acc

def orion_r3(kJ, Dnyq=0.5):
    th = math.pi * float(np.clip(kJ, 1e-3, 0.999))
    A = np.array([
        [np.sin(th), 2*np.sin(2*th), 3*np.sin(3*th)],
        [2*(1-np.cos(th)), 2*(1-np.cos(2*th)), 2*(1-np.cos(3*th))],
        [1.0, 0.0, 1.0],
    ])
    return np.linalg.solve(A, np.array([0.0, 1.0, Dnyq/4.0])), float(np.linalg.cond(A))

def orion_r5(kJ, Dnyq=0.5, gamma=0.5):
    th = math.pi * float(np.clip(kJ, 1e-3, 0.999))
    js = np.arange(1, 6, dtype=float)
    A = np.vstack([
        2*js*np.sin(js*th),
        2*(1.0-np.cos(js*th)),
        2*(js**2)*np.cos(js*th),
        2*(1.0-np.cos(js*np.pi)),
        2*(js**2)*np.cos(js*np.pi),
    ])
    b = np.array([0.0, 1.0, -float(gamma), float(Dnyq), 0.0])
    m = np.linalg.solve(A, b)
    return m, float(np.linalg.cond(A))

def symbol_audit(m, kJ, n=2001):
    th = np.linspace(0.0, math.pi, n)
    S = S_of(th, m)
    peak_kJ = float(th[int(np.argmax(S))] / math.pi)
    return {
        "Smin": float(S.min()), "Smax": float(S.max()),
        "R_D0": float(abs(S_of(0.0, m))),
        "R_peak": float(abs(peak_kJ - kJ)),
        "R_pos": float(_trapz(np.clip(-S, 0.0, None), th)),
        "peak_kJ": peak_kJ,
        "peak_on_target": abs(peak_kJ - kJ) < 0.08,
    }

def belt_ok_r3(kJ, Dnyq=0.5) -> bool:
    if abs(Dnyq-0.5)<1e-12: return 0.35 <= kJ <= 0.65
    if abs(Dnyq-0.25)<1e-12: return 0.375 <= kJ <= 0.625
    if abs(Dnyq-1.0)<1e-12: return kJ >= 0.35
    return False

def kJ_width(w):
    return float(np.clip(2.0/max(w,1e-6), 1e-3, 0.999))

def kJ_argmax(k, P):
    return float(np.clip(k[int(np.argmax(P))]/0.5, 1e-3, 0.999))

def kJ_moment(k, P):
    return float(np.clip((k@P)/(P.sum()+1e-15)/0.5, 1e-3, 0.999))

def fisher_ridge_kJ(k, P, q=0.45, n_sweep=80):
    kJ_axis = k/0.5
    sweep = np.linspace(0.04, 0.96, n_sweep)
    var = np.empty_like(sweep)
    for i, kc in enumerate(sweep):
        sigma = max(0.04, q*kc)
        w = np.exp(-0.5*((kJ_axis-kc)/sigma)**2)
        var[i] = float((P*w).sum())
    return float(sweep[int(np.argmax(var))])

@dataclass
class Route:
    family: str
    m: object
    audit: dict
    kappa: float
    gate: str

def route_operator(kappa, Dnyq=0.5, gamma=0.5, smax_cap=4.0):
    if belt_ok_r3(kappa, Dnyq):
        m, cond = orion_r3(kappa, Dnyq)
        A = symbol_audit(m, kappa); A["cond"]=cond
        if A["Smin"]>=-1e-8 and A["peak_on_target"] and A["Smax"]<=smax_cap:
            return Route("orion-r3", m, A, kappa, "inside_r3_belt")
    try:
        m5, cond5 = orion_r5(kappa, Dnyq, gamma)
        A5 = symbol_audit(m5, kappa); A5["cond"]=cond5
        if A5["Smin"]>=-1e-8 and A5["peak_on_target"] and A5["Smax"]<=smax_cap:
            return Route("orion-r5", m5, A5, kappa, "width_gate_r5")
        A5["reason"]="r5_peak_walk_or_gain"
        heat_meta = A5
    except np.linalg.LinAlgError as e:
        heat_meta = {"reason": f"r5_singular:{e}"}
    return Route("fallback-heat", None, heat_meta, kappa, "width_gate_heat")

def test_toy_dies_on_bimodal():
    k = np.fft.rfftfreq(512); kJ = k/0.5
    k_fat, k_spike = 0.12, 0.82
    P = 1.6*np.exp(-0.5*((kJ-k_fat)/0.14)**2) + 3.2*np.exp(-0.5*((kJ-k_spike)/0.02)**2)
    P[0]=0.0
    a, mom, ridge = kJ_argmax(k,P), kJ_moment(k,P), fisher_ridge_kJ(k,P)
    result = {"name":"toy_dies_on_bimodal","kJ_argmax":a,"kJ_moment":mom,"kJ_fisher_ridge":ridge,
              "k_fat":k_fat,"k_spike":k_spike,
              "argmax_locks_spike": abs(a-k_spike)<abs(a-k_fat),
              "ridge_locks_fat": abs(ridge-k_fat)<abs(ridge-k_spike)}
    assert result["argmax_locks_spike"] and result["ridge_locks_fat"], result
    return result

def test_width_gate_not_length():
    L,w = 512.0, 48.0
    kappa = kJ_width(w)
    r = route_operator(kappa, 0.5)
    result = {"name":"width_gate_not_length","L":L,"w":w,"kappa":kappa,"family":r.family,"gate":r.gate,"r3_belt":belt_ok_r3(kappa,0.5)}
    assert not belt_ok_r3(kappa,0.5) and r.family!="orion-r3", result
    return result

def test_r3_negative_r5_or_heat_on_fat():
    kappa=0.08
    m3,_=orion_r3(kappa,0.5); A3=symbol_audit(m3,kappa)
    r=route_operator(kappa,0.5)
    result={"name":"fat_caustic_families","kappa":kappa,"r3_Smin":A3["Smin"],"r3_negative":A3["Smin"]<-1e-8,
            "routed_family":r.family,"routed_gate":r.gate,"r5_attempt_Smin":r.audit.get("Smin"),
            "r5_attempt_Smax":r.audit.get("Smax"),"r5_attempt_peak_kJ":r.audit.get("peak_kJ"),
            "r5_peak_on_target":r.audit.get("peak_on_target")}
    assert A3["Smin"]<-1.0 and r.family in ("orion-r5","fallback-heat"), result
    return result

def test_r5_Sprime_pi_vacuous():
    m=np.array([0.1,-0.02,0.03,0.01,-0.004]); Sp=0.0
    for j,mj in enumerate(m, start=1):
        Sp += 2*mj*j*math.sin(j*math.pi)
    result={"name":"Sprime_pi_identically_zero","Sprime_pi":Sp}
    assert abs(Sp)<1e-12, result
    return result

def main():
    print("=== DSRSM v0.7.0 grind ===")
    tests=[test_r5_Sprime_pi_vacuous(), test_toy_dies_on_bimodal(), test_width_gate_not_length(), test_r3_negative_r5_or_heat_on_fat()]
    for t in tests:
        print(json.dumps(t, indent=2, default=str))
    with open("sentice_v2_results.json","w") as f:
        json.dump({"version":"0.7.0","tests":tests}, f, indent=2, default=str)
    print("v0.7.0 SENSORS CLOSED")

if __name__=="__main__":
    main()
