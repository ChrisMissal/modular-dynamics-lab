# Modular Dynamics Lab

A reproducible number-theory research playground for modular cycles, prime-power lifting, and base-2 Wieferich primes **1093** and **3511**.

**Goal:** Understand their arithmetic structure and search for useful mathematical or systems ideas, **not** hunt for a third Wieferich prime. This is an exploratory lab, not a cryptography library.

## Quick start

Requires Python 3.11+ and Git. The core engine needs no third-party packages.

```powershell
git clone https://github.com/ChrisMissal/modular-dynamics-lab.git
cd modular-dynamics-lab
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m unittest discover -s tests -v
python -m modular_dynamics_lab run --config experiments/baseline.json --output out/baseline
python -m modular_dynamics_lab verify --output out/baseline
```

For independent SymPy checks: `python -m pip install -e '.[verify]'` then `python scripts/check_sympy.py`.

On Linux/macOS use `python3 -m venv .venv`, `source .venv/bin/activate`, and equivalent Python commands.

## Generate SVGs in GitHub Actions

**Yes: GitHub Actions automatically regenerates the charts.** On pushes, pull requests, and manual runs, the [Experiment & CI](.github/workflows/ci.yml) workflow:

1. Tests the exact-arithmetic engine on Python 3.11 and 3.13; cross-checks multiplicative orders against SymPy.
2. Runs the versioned baseline experiment and generates `cycle_growth.svg` and `harmonic_walks.svg`.
3. Verifies output checksums and uploads **modular-dynamics-baseline** as a downloadable workflow artifact (30-day retention).

Go to [Actions](https://github.com/ChrisMissal/modular-dynamics-lab/actions) → **Experiment & CI** → open a successful run → **Artifacts** → `modular-dynamics-baseline`. To regenerate on demand, use **Run workflow**.

We deliberately **do not commit generated SVGs from CI**: data and plots are reproducible artifacts, not source files. This avoids noisy commits and CI loops. A reviewed figure can later be promoted intentionally.

## Outputs

Local runs write to ignored `out/baseline/`:

| File | Meaning |
|---|---|
| `cycles.jsonl` | Multiplicative orders, growth ratios, Fermat quotients, lift defects |
| `harmonic.jsonl` | Modular harmonic walk endpoints and positive zero returns |
| `summary.json` | Prime/base coverage and exceptional pairs |
| `cycle_growth.svg` | Prime-power cycle growth for selected primes |
| `harmonic_walks.svg` | Normalized modular harmonic trajectories |
| `manifest.json` | Input config, engine version and per-file SHA-256 |

The baseline [configuration](experiments/baseline.json) chooses seven primes (including nearby controls), bases 2/3/5, and three prime-power levels.

## Repo map

```text
src/modular_dynamics_lab/    Exact arithmetic, experiment runner, CLI and SVGs
experiments/                 Versioned experiment parameters
tests/                       Reference cases and deterministic pipeline checks
scripts/                     Reproduction and independent SymPy cross-check
src/modular_dynamics_lab/feature_*.py  Study 002 feature metrics and SVGs
data/baseline/               Reviewed small golden reference cases
docs/MATH.md                 Definitions and known equivalences
docs/RESEARCH_LOG.md         Hypotheses, limitations and findings
docs/EXPERIMENT_TEMPLATE.md  Template for future studies
docs/experiments/           Study-specific protocols
.github/workflows/           CI checks and generated SVG artifacts
AGENTS.md                    Coding agent guidance
CODE_REVIEW.md               Required independent pre-PR review protocol
```

## Independent review policy

Before opening a PR, author agents must follow **[CODE_REVIEW.md](CODE_REVIEW.md)**: finish the draft on a branch, request two isolated subagent reviews (implementation and mathematical methodology), resolve issues, then open the PR with written review evidence. This is a documented protocol, not yet an automated subagent service.

## Research conventions

- **Replicate before interpreting.** Mathematical equivalences are consistency checks, not independent evidence of new structure.
- **Predeclare hypotheses and controls.** Negative results belong in the research log.
- **Use exact integer arithmetic** for correctness and cross-check with a separate implementation.
- **Keep experiments deterministic.** Version configs; save hashes and schemas; avoid timestamps or machine paths in computational outputs.
- **Keep large generated results out of Git.** Save curated small reference data and document how to recreate full results.
- **Use small, reviewable PRs.** A change should explain the mathematical question and its falsifying result.

See [mathematical contract](docs/MATH.md) and [research log](docs/RESEARCH_LOG.md). No third-party license selected yet; choose one before outside contributions.

## Study 002 — prime feature space and harmonic intersections

Study 002 computes exact prime/base features for **all 1,228 odd primes below 10,000** and bases **2, 3, 5** (3,682 coprime prime/base records), alongside half-harmonic zero-return statistics.

Run and verify:

```powershell
python -m modular_dynamics_lab feature-space --config experiments/feature_space_v1.json --output out/feature_space
python -m modular_dynamics_lab verify --output out/feature_space
```

The experiment produces `feature_vectors.jsonl`, `harmonic_stats.jsonl`, `feature_intersections.jsonl`, and `intersection_summary.json`, plus `feature_map.svg` and `harmonic_intersections.svg`. Intersections group **exact reduced rational** coordinates and record the full set of contributing primes and each multiplicity, rather than hiding overlapping points. The SVGs are exploratory visualizations, **not proofs of new mathematical structure**.

GitHub Actions regenerates and checksums the figures and datasets in the **`modular-dynamics-feature-space-v1`** artifact. The workflow also runs an independent deterministic SymPy cross-check and saves a separate `ci_provenance.txt` containing source/checkout commit and run information. Generated data and figures remain uncommitted.

Read the [Study 002 research protocol](docs/experiments/002-feature-space.md) for axes, falsifiability, controls, and interpretation limits. The visual approach is influenced by 3Blue1Brown's emphasis on geometric intuition, without affiliation. For this and future work, follow [the independent review policy](CODE_REVIEW.md) before merging.
