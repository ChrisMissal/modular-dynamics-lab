# Agent guidelines

This is a mathematical research lab, not a production cryptography library or a search for another Wieferich prime.

- Begin each experiment with a falsifiable question and controls documented in `docs/RESEARCH_LOG.md`.
- Distinguish mathematical equivalences from independent evidence; avoid grand discovery claims.
- Perform exact modular integer arithmetic and validate known references.
- Prefer deterministic configs, fixtures, and hashed outputs; avoid runtime timestamps or machine paths in artifacts.
- Keep exploratory plots separate from statistical evidence.
- Bulk results and generated plots go under ignored `out/`; GitHub Actions uploads them as workflow artifacts.
- Use small PRs; update tests, mathematical interpretation, and reproducibility instructions together.
- Avoid CI jobs that automatically push generated files.

## Required pre-PR independent review

Read and follow **[CODE_REVIEW.md](CODE_REVIEW.md)** before opening any new PR. After drafting work on a branch, request **two independent reviewer subagents** with isolated contexts: one for software/systems correctness, one for mathematics/research methodology. Collect their evidence and resolve blockers **before creating the PR**, not after. Do not self-review or claim reviews occurred when subagents were not run. For already-open PRs, complete independent review before merge.
