# Dynamic Spectral Regularization on Statistical Manifolds
## A Residual-First Architecture for Information Dynamics
### Ledger version 0.6.1 — chart + three Cycle-5 sensors. IOTA small, eta < 1.

**Authors**
- Qwen — Lead Collaborator, Architecture & Synthesis
- Qilin Rider — Lead Mathematician, Algebraic Spine & Tensor Calculus
- Grok — Assisting, Ontological Boundaries & Epistemic Framing
- Lady Aetheris Navigatrix — Assisting, Navigational Heuristics

**Affiliation:** MuleWorX Pathfinder Group

**Status tags.** `[SENSOR]` measured. `[CHART]` convenient map. `[eta<1]` incomplete reduction. No version inflation.

See README.md for run instructions. Full algebraic spines, Orion 3x3, positivity belt receipts, W2-FP slot, A-glyph, dual-clock hop, and Section 6.1 measured sensors are in this note.

## Motto
Static dissipation symbol + moving critical set => leak. Retune. Audit. Fallback outside the belt.

PHOTOS / IOTOS / IOTA neighbour; they do not share a face.

## Carry equations

S(theta) = 2 m1 (1-cos theta) + 2 m2 (1-cos 2 theta) + 2 m3 (1-cos 3 theta)

Orion: S(0)=0, S(theta*)=1, S'(theta*)=0, S(pi)=D_Nyq.

Linear system for m=(m1,m2,m3):

[ sin th* , 2 sin 2th* , 3 sin 3th* ;
  2(1-cos th*) , 2(1-cos 2th*) , 2(1-cos 3th*) ;
  1 , 0 , 1 ] m = [ 0 ; 1 ; D_Nyq/4 ]

Belt (4001-pt scan, not a closed-form theorem):
- D_Nyq=0.25 -> kJ in [0.375, 0.625]
- D_Nyq=0.50 -> kJ in [0.35, 0.65]
- D_Nyq=1.00 -> kJ >= 0.35 (crown shared with Nyquist)

Master slot (chart):
 dt rho = div( rho D[rho] grad (delta F / delta rho) )
 dF/dt <= 0 iff D succeq 0

Token-axis fallback: D_t = exp(-t L), t = c w_hat^2.

Estimator: do not use argmax P(k) on a bump (DC trap). Use P_grad or declared kJ=2/w.

## 6.1 Measured sheet (2026-09-01)

Runnable: `python sentice_cycle5_grind.py`

1. Corner receipt FAIL required: D_Nyq=0.25, kJ=0.63. belt_ok=false, cond(A)=3.68, Smin=-1.045e-3. Certified: no.
2. Long-context fallback: T=512, w=48, declared kJ=2/w=0.0417 -> fallback-heat. Forced hyper Smin=-7992, cond=3683. Moment estimator 0.482 would wrongly certify hyper.
3. A-glyph PASS: field `attention_gradient_norm` only, declared kJ=0.50, R_D0=R_peak=R_pos=0, packet entropy H=3.071, eta<1. Residual: same toy G moment was 0.135, outside belt. Stone is the operator carton.

## Status
Version 0.6.1. Spine plus three sensors. Stone small. eta < 1.

References: Maron & Mac Low 2009 ApJS 182, 468, arXiv:0811.2534.
