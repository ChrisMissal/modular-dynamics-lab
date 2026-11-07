# Study 002 — Prime feature vectors and modular zero intersections

**Status:** predeclared exploratory visualization and replication. **Not a new theorem.**

## Research question

Do base-2 Wieferich primes 1093 and 3511 show nontrivial structure in *independent* measurements, beyond the defining flat cycle lift and harmonic returns forced by known congruences?

## Protocol

- Population: every odd prime `3 <= p < 10000` (1,228 primes), selected by a deterministic sieve. No sampling or search for new Wieferich primes.
- Bases `2, 3, 5`; omit pairs with `gcd(base,p) != 1` (3 and 5 when p equals the base).
- At each valid `(p,base)`: exact orders modulo `p`, `p²`, and `p³`, Fermat quotient modulo `p`, lift defect, distinct factors of `p-1`, whether the base is primitive modulo `p`.
- At every odd prime: compute `H_k = sum_{j=1}^k j^-1 (mod p)` for `1 <= k <= (p-1)/2`. Save every zero return and classify theorem-forced returns when the base-2 Fermat quotient vanishes.
- Plot 2D feature coordinates **exactly** as `(ord_p(2)/(p-1), ord_p(3)/(p-1))`; points are not PCA, inferred geometry, or independent physical dimensions. Draw origin-to-point vectors for the focus primes.
- Plot discrete harmonic zero returns near each focus prime, 14 neighboring primes per side, normalized by the half-length. These are *intersection points with zero*, not interpolated continuous crossings.

## Falsifiability, controls and null explanations

The known equivalences predict exact flat lifts, fixed points, and returns at `floor(p/4)` and `(p-1)/2` for base-2 Wieferich primes. Such agreements do **not** count as an independent finding. Additional zero returns, if any, are observational features that require statistical testing, broad control populations and correction for selection effects. Cross-base order fractions depend on `p-1` divisors; clusters may be arithmetic artifacts.

**Null hypothesis for exploratory plots:** apparent alignments and clusters arise from known modular identities, factorization constraints, and discrete possible ratios. This first study does not attempt to reject it.

## Output and limitations

- `feature_vectors.jsonl`: one record per valid pair, sorted by `(p,base)`.
- `harmonic_stats.jsonl`: one record per prime, with exact zero intersections.
- `intersection_summary.json`: population counts and descriptive histograms.
- `feature_map.svg`: cross-base feature plane and lift-growth signatures.
- `harmonic_intersections.svg`: neighborhood strips of observed zero returns.
- `manifest.json`: input configuration and SHA-256 checksums.

**Limitations:** order fractions are redundant with components of the lift data; 2D projections can obscure structure. Nearby-prime strips are not matched statistical controls. Graphical zero-return patterns are not evidence of cryptographic security or of new spatial dimensions. Numerical scans below 10,000 cannot resolve distribution questions.

## Reproduction

```bash
python -m modular_dynamics_lab feature-space --config experiments/feature_space_v1.json --output out/feature_space
python -m modular_dynamics_lab verify --output out/feature_space
```

The CI workflow publishes the exact generated plots and records as `modular-dynamics-feature-space-v1`.

## Follow-up (not part of this implementation)

Perform a preregistered test of **additional** zero returns (excluding known forced positions), controlling for prime magnitude and order/factorization patterns; compare several bases and lifting coefficients with corrections for multiple testing.
