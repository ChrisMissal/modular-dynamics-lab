# Independent code and research review

This is the **required pre-PR review protocol** for experiments, visualizations, algorithms, and systems changes in Modular Dynamics Lab. Follow it in addition to [AGENTS.md](AGENTS.md).

## When to review

1. **Author creates a working branch and drafts the implementation.** "Draft" means the code, experiment description, tests, outputs, and docs are ready for inspection **on the branch**; do **not** open a GitHub PR (even a draft PR) yet.
2. **Author runs relevant tests and reproducibility checks** and records the intended scope and draft commit SHA. Passing CI or unit tests is not an independent review.
3. **Launch two independent reviewer subagents** after the draft is ready. Each reviews the *same frozen draft commit* in a **separate context**, and receives this protocol and the code/experiment files, not the other reviewer's verdict. The implementation author must not serve as either reviewer.
4. **Collect both written reviews**, then resolve blocking findings on the branch. Repeat any affected checks and request independent follow-up review of material revisions, quoting the updated commit SHA.
5. **Open a PR only after both independent reviews have completed** and all high/critical findings are resolved or explicitly documented as unverified/blocking. If review capability is unavailable, **do not invent a reviewer, mark a review complete, or open a PR as reviewed**. Escalate to the human maintainer.

Reviewers are *advisors*, not automated merge approvers. The human maintainer makes the merge decision. Repo automation does not currently create subagents or enforce the pre-PR gate; agents executing a task must orchestrate this explicitly when their environment supports subagents.

### Independent reviewer roles

**Reviewer A — implementation and systems**
- Check correctness, edge cases, validation, overflow/integer exactness, algorithmic complexity, performance, safety, and output schemas.
- Run relevant tests; challenge whether tests would detect regressions. Inspect determinism, input provenance, manifest and SHA-256 checks, CI workflow permissions, and untrusted inputs.
- Cross-check at least one small case with a separate implementation or direct arithmetic, not only the submitted functions.
- Flag generated-data bloat, accidental environment assumptions, or misleading visual encodings.

**Reviewer B — mathematics and methodology**
- Independently derive or locate supporting theorems, congruences, domains, and limitations; verify representative numeric examples without assuming the author's claimed outputs.
- Separate equivalent characterizations (e.g., Fermat quotient, unchanged first order lift, Teichmüller fixed point, forced harmonic zeros) from genuinely independent observables.
- Challenge sampling, matched controls, feature leakage, normalization, multiple comparisons, and visual interpretations.
- Identify plausible counterexamples and ways to falsify each novel hypothesis; distinguish replication, exploration, and proof.
- For proposed cryptographic uses, explicitly review threat models and do not claim security from unusual arithmetic alone.

The two roles may be supported by different models or by separately instantiated agents with isolated contexts. **Two passes by the author, or the same context repeating itself, do not count as two independent reviews.** External model agreement is not proof.

### Evidence to produce before the PR

Each reviewer should return a Markdown report, saved after both reviews complete as:
- `docs/reviews/<change-id>-implementation.md`
- `docs/reviews/<change-id>-mathematics.md`

Use the same template for each report:

```markdown
# Independent review: <change-id> — <role>
Reviewed draft commit: <full SHA>
Reviewer: <agent/model/session identifier, or human>
Review context: <what inputs were supplied and which checks were independent>
Verdict: PASS | CHANGES_REQUESTED | INCONCLUSIVE

## Checks performed
- <commands or calculations actually executed, plus results>
## Findings
- [BLOCKER | MAJOR | MINOR | NOTE] <file/line or formula, explanation, reproduction>
## Unverified claims and limitations
- <explicitly list gaps; never claim checks ran if they did not>
## Recommendations
- <concrete actions>
```

Reports must be **specific and evidence-based**, not a generic "looks good." A PASS means no known blocking concerns *within the reviewed scope*, not mathematical proof or independent scientific peer review. The author records resolutions separately without silently rewriting independent reviewers' conclusions. Cite both reports in the eventual PR body and include its final diff/test evidence.

### Change control

- Freeze and identify the draft commit each reviewer saw.
- Any **material** follow-up change requires a re-review of the changed portions by the affected independent reviewer(s). A report must name the updated commit SHA or explicitly describe the delta reviewed.
- Open the PR only after the report paths are committed to the source branch and the final source revision is covered by the reviews.
- If findings conflict, preserve the disagreement, investigate and document a resolution rather than averaging model opinions.
- Already-open PRs that predate this policy (including Study 002 PR #1) require the same independent evidence **before merge**; do not represent them as having passed the pre-PR gate retroactively.

### PR description checklist

```markdown
- [ ] Implementation review completed; link to report
- [ ] Mathematical/methodological review completed; link to report
- [ ] Blocking findings resolved; material changes re-reviewed
- [ ] Tests and independent reproduction completed (or limitations disclosed)
- [ ] Hypothesis, controls, negative results, and known equivalences documented
```
