# QA Strategy — JobFitGPT QA Assistant

**Author:** Lauren Byrd
**Status:** Planning-stage strategy for a scaffolded system

---

## 0. Honest Status Summary — Read This First

**This repository is currently a project scaffold.** The package modules (`parser`, `scoring`, `analyzer`, `cli`, `prompts`, `models`) contain no implemented business logic. The test suite consists of three import-smoke tests that verify the modules exist — nothing more. No LLM integration is present yet; `prompts.py` is a placeholder.

This document is therefore a **QA strategy written *ahead of* implementation** — it defines how the system should be evaluated as it is built, and it will be updated as real components land. No coverage described below exists yet.

## 1. What the System Is Intended to Do

Compare a candidate resume against a QA job description, then produce:
- an interpretable **fit score** for the role,
- a **skill-gap analysis** (missing / underrepresented skills),
- **recommendations** for resume tailoring, cover letters, and interview prep.

## 2. Where AI Plays a Role — and Where It Doesn't

| Component | Intended nature | Why |
|-----------|----------------|-----|
| Resume / JD text parsing | **Deterministic** | Extracting skills, tools, experience signals must be reproducible and unit-testable |
| Fit scoring & gap analysis | **Deterministic (transparent)** | A score a candidate acts on must be explainable — same inputs, same outputs, inspectable logic |
| Recommendation generation | **Probabilistic (LLM-assisted)** | Natural-language advice is where a model adds value — and where QA must change its model |

The core principle: **deterministic where the output is a decision, probabilistic only where the output is guidance.** A fit score that fluctuates between runs for identical inputs is a defect; a recommendation paragraph that varies in wording is acceptable, as long as its substance is correct.

## 3. Quality Risks (Planned System)

**Input risks**
- Malformed or adversarial input files (a resume is untrusted text; prompt injection via resume content is a real scenario — the planned LLM prompt must treat file contents as data, never as instructions).
- Encoding/format edge cases: PDFs, empty files, extremely long files, non-English text.

**Scoring risks**
- Non-transparent scoring (black-box score the candidate can't act on).
- Overweighting keyword matches vs. real experience (e.g., "knows Selenium" listed once vs. years of use).
- Score instability across near-identical inputs.

**AI-output risks (recommendation layer)**
- **Hallucinated skills**: recommending improvement in skills the JD doesn't require.
- **False confidence**: advice implying certainty about recruiter behavior.
- **Harmful advice**: recommendations that encourage misrepresentation.
- **Drift**: same resume/JD producing materially different recommendations across runs or model updates.

## 4. How QA Differs for the AI Component

Conventional assertions (`assert score == 42`) don't apply to the LLM recommendation layer, where correct output is a *class* of acceptable answers. The evaluation model must distinguish:

1. **Deterministic assertions** — parsing and scoring: exact, unit-tested.
2. **Threshold evaluations** — recommendation layer: e.g., "≥90% of required JD skills referenced; 0 prohibited suggestions (misrepresentation advice); required sections present in output structure."
3. **Human-review-required cases** — nuanced judgment calls (is this advice actually *good*?) that no automated check should gate.

This mirrors how the field handles AI system QA: automated checks where possible, human judgment where necessary, and no pretending AI behavior is perfectly deterministic.

## 5. Current Test Coverage (as of this writing)

- 3 pytest import-smoke tests (one per module). They verify the package imports and nothing else.
- No CI pipeline — deliberately. A green badge representing three import tests would be decorative, not evidence of quality. CI will be added when there is real logic to run.

## 6. What Is Not Tested Today

Everything functional: parsing, scoring, gap analysis, recommendations, CLI behavior, error handling, encoding edge cases, adversarial inputs, LLM behavior. All of it.

## 7. How QA Expands When Implementation Begins

1. **Parser**: unit tests against a corpus of resumes/JDs (including malformed and adversarial samples); exact expected skill extractions on golden examples.
2. **Scoring**: determinism tests (same input → same score, repeatedly); monotonicity tests (adding a required skill should never *lower* the fit score); boundary tests (empty resume, JD with no skills section).
3. **Analyzer**: workflow tests verifying parsing → scoring → gap analysis → recommendations integrate correctly.
4. **LLM layer (once integrated)**: golden-dataset evaluation of recommendations against expected-behavior definitions; repeat-run consistency analysis; injection-attempt suite; regression fixtures capturing known-good outputs.
5. **CLI**: exit codes, error messages, output formatting.
6. **CI**: pytest (with coverage) on every push once logic exists.

## 8. Failures That Would Matter to an End User

- A materially wrong fit score → candidate skips a role they should pursue (or wastes effort on a poor match).
- A hallucinated skill gap → candidate "fixes" a non-problem.
- Misrepresentation-adjacent advice → candidate's credibility harmed.
- Crash on an unusual resume format → the tool silently loses its user at the first hurdle.

## 9. AI Regression Approach (Planned)

Regression for the deterministic layers is conventional: golden inputs → exact expected outputs, run on every change. For the LLM layer, regression means **material change detection**: same golden inputs, evaluated against expected-behavior definitions and consistency thresholds across N repeated runs — flagging drift, not wording differences. Failures route to human review, not auto-block, until thresholds prove reliable.

## 10. Explicit Non-Goals

- No claims that this system is a validated career-advice product.
- No production claims for any component in this portfolio artifact.
- QA evidence will only ever describe what is implemented — see §0.
