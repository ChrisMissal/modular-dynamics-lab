# Modular Dynamics Lab

**A reproducible research playground** for modular cycles, prime-power lifting, and the base-2 Wieferich primes **1093** and **3511**. We are **not** searching for a third prime. We are asking which of their unusual properties are equivalent statements of known mathematics, which reveal useful structure, and what new, falsifiable questions they suggest.

> Status: **baseline / replication**, not a mathematical discovery. No security claims or production cryptography.

## Start here (Windows / PowerShell)

Requires **Python 3.11+** and Git. No external Python dependencies for core experiments.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m unittest discover -s tests -v
python -m modular_dynamics_lab run --config experiments/baseline.json --output out/baseline
python -m modular_dynamics_lab verify --output out/baseline
```

Optional independent mathematical verification:

```powershell
python -m pip install -e '.[verify]'
python scripts/check_sympy.py
```

Mac/Linux: `python3 -m venv .venv && source .venv/bin/activate && python -m pip install -e .`; then use the same commands. Or run `bash scripts/reproduce.sh` after installation. The CLI entry point `mdl` is also available.

## Outputs

Running the baseline creates `out/baseline/` (ignored by Git):

| File | Why it exists |
|---|---|
| `cycles.jsonl` | Exact integer properties per `(prime, base)` |
| `harmonic.jsonl` | Modular reciprocal sums and zero-return indices per prime |
| `summary.json` | A compact experiment summary |
| `cycle_growth.svg` | Diagram of order growth, with flat vs. expanding lifts |
| `harmonic_walks.svg` | Visualization of modular harmonic sums and returns to zero |
| `manifest.json` | SHA-256 of the input config and every output |

The reviewed, small baseline snapshot lives in [`data/baseline`](data/baseline). CI **recomputes and diffs every byte** against this snapshot. Large sweeps, provisional results, and scratch plots belong under `out/`, not in Git. To promote a new reference result, review the mathematics and commit a deliberately named snapshot.

## Repository map

```text
experiments/           Explicit, versioned experiment inputs
src/modular_dynamics_lab/
  core.py              Exact arithmetic, no floating point
  experiments.py       Runner, JSONL/manifest output, validation
  plots.py             Dependency-free SVG plots
  cli.py               run and verify commands
tests/                 Known-answer and invariant tests
scripts/               Reproduction scripts; independent SymPy check
data/baseline/          Small reviewed golden artifacts
docs/MATH.md            Known mathematics and hypotheses
docs/RESEARCH_LOG.md    Experiment log: observations, limitations, next steps
.github/workflows/      CI on multiple Python versions
```

## How research work differs from application work

1. **State the hypothesis before the experiment.** Write down the outcome that would disprove it; record when a hypothesis was revised after observing data.
2. **Separate discovery from validation.** Exploring a plot is allowed, but exploratory patterns are *not* independent confirmations. Design matched controls or holdout samples before reporting significance.
3. **Prefer invariants to screenshots.** Use exact modular arithmetic, unit tests, known results, and an unrelated implementation (SymPy) to cross-check the interesting cases.
4. **Record provenance.** Check in configs and small reviewed outputs; use SHA-256 manifests for artifacts; track software version, code commit and environment in experiment notes when publishing a result.
5. **Make negative findings visible.** A pattern that disappears under suitable controls is a result, not a failed experiment.
6. **Keep computation and interpretation separate.** Raw records are JSONL. Visualizations are derived outputs, not evidence by themselves.

See [the mathematics](docs/MATH.md) and [the research log](docs/RESEARCH_LOG.md).

## Git workflow

The initial branch is `main`, with the first baseline committed. A normal research change is one branch and one coherent experiment/claim; commit its config, code, tests, and short research-log entry together. Use descriptive conventional commits such as `experiment: compare harmonic zero returns` or `fix: correct lifting-order check`.

When your GitHub remote exists:

```bash
git remote add origin https://github.com/YOUR-ACCOUNT/modular-dynamics-lab.git
git push -u origin main
```

No remote is configured in this starter repo. A license has deliberately not been granted; choose one before making the repository public or accepting contributions.

## Scope and computational limits

This starter intentionally uses deterministic trial-division primality checks and exact Python modular arithmetic. It is adequate for small baseline experiments, **not** a high-performance or cryptographically trustworthy large-prime search. Add faster vetted primality/factorization implementations and stronger statistical controls before scaling to millions of primes. The next logical systems step is a C# `BigInteger` worker that produces the same documented JSONL schema, independently compared with Python—not replacing the verified reference calculations prematurely.

## Study 002 — expanded feature space and modular intersections

This follow-up study enumerates **all 1,228 odd primes below 10,000** with bases 2, 3 and 5 (3,682 coprime prime/base pairs) and analyzes the modular harmonic half-walk at each prime. It uses exact arithmetic and emits deterministic JSONL datasets, two 3Blue1Brown-inspired *static* SVG visualizations, an exact-rational intersection dataset, and a checksum manifest.

```powershell
python -m modular_dynamics_lab feature-space --config experiments/feature_space_v1.json --output out/feature_space
python -m modular_dynamics_lab verify --output out/feature_space
```

The [GitHub Actions workflow](.github/workflows/ci.yml) independently checks a deterministic prime sample using SymPy, and publishes the results as `modular-dynamics-feature-space-v1` with `feature_map.svg` and `harmonic_intersections.svg`. Plots are stored as workflow artifacts rather than automatically committed. See the [experiment protocol](docs/experiments/002-feature-space.md) for exact axes, caveats, and next research questions. The visual treatment is influenced by 3Blue1Brown's emphasis on geometric intuition, not associated with or an imitation of its branding.

Study 002 also writes `feature_intersections.jsonl` with reduced rational coordinate pairs, the complete list of primes at each coordinate, and multiplicities. Circle size in `feature_map.svg` encodes that multiplicity; repeated points are no longer hidden. The workflow artifact includes `ci_provenance.txt` for commit/run identity, separate from checksummed deterministic results.
