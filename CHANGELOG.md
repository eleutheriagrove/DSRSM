# Changelog

## 0.7.0 — 2026-09-01

- Fisher-ridge estimator: const-Q windowed integrated power of the gradient spectrum.
- Width-triggered gate keys on `kappa = 2/w` (or ridge `k_J`), not on length `L`.
- Radius-5 equality system implemented with a **non-vacuous** 5th constraint `S''(pi)=0`.
  `S'(pi)=0` is identically zero for every even cosine symbol — not a DOF.
- Sensor: on a bimodal `P(k)` (fat sheet at 0.12 + tall spike at 0.82), `argmax` locks the spike; ridge locks the sheet.
- Sensor: fat `kappa=0.08` makes radius-3 `Smin ~ -572`. Radius-5 restores `Smin>=0` but the **global peak walks** (`peak_kJ~0.57`, `Smax~8203`). Route falls through to heat. Do not stamp r5 as Orion-complete.
- New entrypoint: `sentice_v2_grind.py`.
