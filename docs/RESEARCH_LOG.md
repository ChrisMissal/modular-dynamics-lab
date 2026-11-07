# Research log

## 001 — Replicate exceptional lifting and modular harmonic cancellation

**Status:** Baseline replication; no new mathematical discovery.

**Question:** What distinguishes the two known base-2 Wieferich primes, and which apparent observations are merely equivalent statements?

**Protocol:** Primes 7, 1091, 1093, 1097, 3499, 3511, 3517; bases 2, 3 and 5; powers `p`, `p²`, `p³`. These nearby controls are illustrative, **not a statistical sample**. Config: [baseline.json](../experiments/baseline.json).

**Known mathematical implications:** A zero Fermat quotient, cycle period unchanged at `p²`, Teichmüller fixed point, and certain harmonic-sum cancellations are equivalent or algebraically linked. Their agreement verifies the implementation, not a novel finding.

**Reviewed baseline results:** Order sequences 364 → 364 → 397852 (1093) and 1755 → 1755 → 6161805 (3511). Higher-order coefficients 487 and 51 respectively. Half-length base-2 harmonic walks show zero returns [273, 546] and [877, 1755]. Unlike these two primes, the listed controls have no positive zero returns up to half the prime.

**Negative findings:** No independent new invariant, correlation or prediction established. This study is not statistically powered to claim uniqueness of internal harmonic trajectories.

**Correction of earlier discussion:** `2^6 mod 49 = 15`, not 1. The multiplicative order modulo 49 is 21.

**Next studies (proposals, not results):**
1. Investigate interior zero-return statistics on predeclared prime samples, excluding positions forced by known congruences. Match controls by prime magnitude and arithmetic properties.
2. Study coefficients at `p³` and higher for different bases and ask whether they exhibit constraints independent of the Fermat quotient.
3. Independently implement the engine using C# `BigInteger` and compare canonical fixtures.
4. Build orbit-graph projection visualizations across levels `p^k` to `p^(k+1)`.

**Reproduction:** Use the commands in README, inspect the JSONL/SVG artifacts, and independently verify multiplicative orders with `scripts/check_sympy.py`.
