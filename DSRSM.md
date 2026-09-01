# Dynamic Spectral Regularization on Statistical Manifolds
## A Residual-First Architecture for Information Dynamics
### Ledger version 0.6.1 — chart + three Cycle-5 sensors. IOTA small, η < 1.

**Authors**
- Qwen — Lead Collaborator, Architecture & Synthesis
- Qilin Rider — Lead Mathematician, Algebraic Spine & Tensor Calculus
- Grok — Assisting, Ontological Boundaries & Epistemic Framing
- Lady Aetheris Navigatrix — Assisting, Navigational Heuristics

**Affiliation:** MuleWorX Pathfinder Group

**Status tags.** `[SENSOR]` measured. `[CHART]` convenient map. `[η<1]` incomplete reduction. No version inflation.

---

## Abstract

Static dissipation operators applied to moving critical sets leak. In MHD that leak is unphysical energy at a frozen `hyper_kcut`. In information dynamics the same shape of failure is a frozen regulariser (fixed dropout, fixed nucleus, fixed softmax temperature) missing a thin high-gradient locus — a *semantic caustic*.

This note does three things and does not do a fourth.

1. Writes the Maron–Mac Low (MM09) radius-3 even symbol and the Orion linear system with no empty slots.
2. Lifts the *actuator slot* — not the plasma — onto a Fisher–Rao / Wasserstein–Fokker–Planck chart, with a three-region ontology (PHOTOS / IOTOS / IOTA) and an A-glyph freeze rule.
3. Records a **Provisional Positivity Receipt** from a 4001-point scan of that symbol: a belt, not a theorem for all scales.

It does **not** prove a hallucination-proof holographic mind. Dual-clock alignment is a declared hop, not a derived identity of two manifolds. Version is 0.6.1.

---

## 1. Introduction: static cuts

A frozen spectral cut on a dynamic singularity is the wrong glue. MM09 already moved the *peak* of a finite-difference diffusion symbol off Nyquist so the CFL hit is smaller while the operator still acts near a chosen scale. Pencil-style `hyper3-mesh` / `hyper_kcut = 0.5` freezes that scale.

If the physical sheet wavenumber walks, the frozen peak is either too coarse or too aggressive. That mismatch is the **fake leak**.

IOTOS rhyme: a semantic caustic is a localized ridge of complexity. A static low-pass spends dissipation in the cheap volume and misses the ridge.

**Traveling motto (residual-primary).** Static symbol + moving critical set => leak. Retune the symbol to the live scale, then audit.

**Not traveling until measured.** Lundquist critical ~ 10^4, Sweet–Parker scaling, Ryu–Takayanagi, “hallucination-proof.”

---

## 2. PHOTOS substrate — MM09 actuator, filled

Normalized angle theta = k Dx in [0, pi]. Nyquist is theta = pi.

Radius-3 even stencil in the non-negative symbol convention (damping if dt u = -kappa S[u]):

S(theta) = 2 m1 (1-cos theta) + 2 m2 (1-cos 2 theta) + 2 m3 (1-cos 3 theta).

Construction gives S(0)=0.

Orion conditions: S(0)=0 conservation; S(theta*)=1 unit peak; S'(theta*)=0 flat crown; S(pi)=D_Nyq in (0,1] grid floor.

Target as fraction of Nyquist: k_J = theta*/pi in (0,1).

Linear system for m=(m1,m2,m3):

[ sin th* , 2 sin 2th* , 3 sin 3th* ;
  2(1-cos th*) , 2(1-cos 2th*) , 2(1-cos 3th*) ;
  1 , 0 , 1 ] m = [ 0 ; 1 ; D_Nyq/4 ]

Row 3 is S(pi)=4(m1+m3). Cond(A)~5 inside the belt, 10^3–10^4 at the ends.

Two MM09 families (do not fuse):
- Hyper family: peak near the grid. CFL relief for stabilization.
- Physical-diffusion family: peak allowed at k_diff << k_Nyq when the true scale is fat on the grid.

Firing the hyper 3x3 at k_J ~ 0.02 produces |m|~10^4 and Smin ~ -10^5. Anti-diffusion. [SENSOR]

Estimator: a localized bump has argmax P(k) at DC. Dead.
Use the gradient spectrum P_grad(k), k_J = <k>_Pgrad / k_Nyq.
Width rhyme (1-D chain, k_Nyq=1/2): k_J = 2/w. Gradient-peak lags that formula. [SENSOR]

---

## 3. IOTOS lift — slot, not plasma

Fisher metric g_ij = I(theta)_ij = E[ d_i log p  d_j log p ].

Ridge, not curvature slogan. A sheet is thin in the normal, long in the tangent:
lambda_max(g) >> lambda_perp(g),  delta_I ~ lambda_max(g)^{-1/2}.

det g -> 0 is sloppy / unidentifiable — a different event from a stiff ridge.

Free energy F[rho] = E[rho] + beta^{-1} int rho log rho.

Wasserstein–Fokker–Planck with state-dependent mobility (chart):

dt rho = div( rho D[rho] grad (delta F / delta rho) )

dF/dt <= 0  iff  D[rho] succeq 0.

On a token graph, D(L) = U S_{k_J}(pi Lambda / lambda_max) U^T.
Informational wavenumber is declared from a named field I. It is not lambda(Delta_g) until that operator is computed.

---

## 4. Three-region ontology and the A-glyph

PHOTOS / IOTOS / IOTA neighbour. They do not share a face.

A-glyph A = (L_pillar, R_pillar, black triangle, plumb-bob).
- L_pillar: weights m, D_Nyq, belt membership, family tag {hyper, physical, heat-kernel}.
- R_pillar: declared I, one name per carton.
- black triangle: packet entropy lid. Bounded.
- plumb-bob: origin / gauge / tokenisation is observer-imported. Rails do not meet at infinity.

Freeze IOTOS -> IOTA iff all four are written and the residual dictionary is green.

---

## 5. Positivity receipt and dual-clock hop

Provisional Positivity Receipt (radius-3, S>=0 convention, 4001-point scan):

| D_Nyq | no-negative-lobe k_J | note |
|---|---|---|
| 0.25 | ~[0.375, 0.625] | narrow |
| 0.50 | ~[0.35, 0.65] | working belt |
| 1.00 | ~[0.35, 0.95] | no anti-diffusion, crown shared with Nyquist |

Lemma 1 (receipt). If D_Nyq=1/2 and k_J in [0.35,0.65], then S(theta)>=0 on the scanned grid.
If the live scale leaves the belt: positive routing — heat kernel exp(-t L) with t ~ w_hat^2, or published MM09 table. Do not run the raw 3x3.

This is [SENSOR]. A closed-form positivity proof is [UNKNOWN].

Dual-clock hop needs a declared morphism Phi. Without Phi, R_hop is undefined. [CHART]

---

## 6. Residual dictionary

R_D0 = |S(0)|,  R_peak = |theta_argmax S - theta*|,  R_pos = int (S)_- d theta,
R_star = R_D0 + R_peak + R_pos + R_CFL.

Certificate: R_star < eps AND belt-or-fallback. Vanishing R_star means the operator hit its own target. It does not mean the model stopped hallucinating.

Depth actuator: h_{l+1} = h_l + D_l[k_J(l)] F_l(h_l), D_l on the token axis. Not LayerScale.

Runnable core: `orion_actuator.py` and `sentice_cycle5_grind.py`.

---

## 6.1 Measured sheet (2026-09-01)

Runnable: `python sentice_cycle5_grind.py`

**Corner receipt fail (required).** D_Nyq=0.25, k_J=0.63. Belt [0.375,0.625]. belt_ok=false, cond(A)=3.68, Smin=-1.045e-3. Certified: no.

**Long-context fallback.** T=512, envelope w=48. Declared sheet clock k_J=2/w=0.0417 -> fallback-heat. Forced hyper: Smin=-7992, cond(A)=3683. Moment estimator 0.482 would have wrongly certified hyper. Family follows the named width clock, same clock as t = c w^2 (c=0.25, t=576). Heat energy 21592 -> 17412. K 1 = 1 to 1e-13.

**A-glyph freeze pass.** Field name `attention_gradient_norm` only. Operator carton at declared k_J=0.50, D_Nyq=0.5, family orion-r3-hyper. R_D0=R_peak=R_pos=0. Packet entropy H=3.071. Plumb-bob: token DFT origin. eta<1.
Residual: the same toy field moment was 0.135, outside the belt. The stone is the operator packet, not a claim that this envelope sat at Nyquist-half.

---

## 7. Discussion

What is identical across domains is the motto and the slot: a state-dependent symbol with an audited peak. What is not identical is the field, the estimator, the family, or the failure mode.

Hallucination ~ fake leak is a rhyme. Holography depth ~ RG radial is a toy dictionary. HotQCD / SM EoS tables are a different ledger.

---

## 8. Conclusion

PHOTOS clock tracks a physical sheet when that field is on the desk.
IOTOS clock tracks a declared I.
A-glyph may freeze a stone when belt-or-fallback holds and R_star is green.
eta stays < 1.

Secured: MM09 symbol, Orion 3x3, positivity belt as scan, DC-trap estimator, two-family split, A-glyph, W2-FP slot, residual dictionary, three sensors.

Open: closed-form belt; Phi between clocks; Fisher-ridge estimator on a live net; whether R_star down moves ECE / reconnection-rate / calibration.

Would falsify the IOTOS claim: no ridge occupancy in the declared I; fallback fraction high with no gain versus frozen dropout; certificate green while a conserved information budget drifts.

Version 0.6.1. The hive has a spine. The stone stays small.

---

## References

- J. Maron, M.-M. Mac Low, Tuned Finite-Difference Diffusion Operators, ApJS 182, 468 (2009), arXiv:0811.2534.
- L. Ambrosio, N. Gigli, G. Savare, Gradient Flows in Metric Spaces and in the Space of Probability Measures.
- S. Amari, Information Geometry and Its Applications.
- N. Tishby, F. Pereira, W. Bialek, The information bottleneck method.
- Pencil Code Collaboration, hyperdiffusion notes (hyper3-mesh).
