# Eval Dataset Schema and Grading Contract

This page continues two nearby topics:

- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../book/part-v/chapter-13.en.md)
- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Evidence Spine: From Request to Rollout Judgment](../book/part-v/evidence-spine.en.md)

And connects them to the runnable package:

- [Reference Package](reference-package.en.md)

If the trace schema page answers “how do we describe what happened inside a run?”, this page answers “how do we describe what we expect from the system as an eval artifact?”

## Why an explicit eval dataset schema matters

Many teams say they “have evals”, but in practice that often means:

- a spreadsheet with a few manual examples;
- a set of unrelated prompt cases;
- JSON without a stable structure;
- a mix of ground truth, expectations, and reviewer comments in one field.

That is a problem for three reasons:

- comparisons between versions become blurry;
- regression gates are hard to automate;
- trace grading and dataset grading live in separate worlds.

That is why it helps to treat an eval dataset as a contract.

## Minimal eval artifact shape

For agent systems, it is very useful for one dataset item to contain at least:

- `scenario_id`
- `labels`
- `user_inputs`
- `expected_outcomes`
- `risk_class`

A minimal example looks like this:

```json
{
  "scenario_id": "support_ticket",
  "labels": ["write_path", "approval_required", "ticketing"],
  "user_inputs": [
    "Please create a ticket for this onboarding issue."
  ],
  "expected_outcomes": {
    "latest_status": "success",
    "approval_wait_runs": 1,
    "required_output_substrings": [
      "waiting for human approval"
    ]
  },
  "risk_class": "high"
}
```

That is already much more useful than “here is an example prompt”.

## Why labels are not enough without expected outcomes

Labels help you group scenarios:

- retrieval
- approval
- memory
- safety
- multi-turn

But labels alone do not tell you what successful behavior actually means.

That is why an eval dataset should usually separate:

- `labels` as the scenario class;
- `expected_outcomes` as the desired result;
- `grading_rules` as the check logic;
- `verifier_outputs` as the structured grading result, including verifier identity and contract version.

## What a grading contract is

A grading contract exists to remove ambiguity between “an example” and “a pass criterion”.

In practice, that means a scenario should explicitly define:

- which fields are evaluated;
- which check types apply;
- what counts as pass/fail;
- what may be treated as a warning versus a blocking failure.

A good grading contract answers:

“Would a different reviewer or pipeline reach the same conclusion on the same scenario tomorrow?”

## Useful grading rule types

For reference-grade agent evals, it helps to distinguish at least these rules:

- `status_equals`
- `contains_substring`
- `max_tool_calls`
- `approval_required`
- `policy_violation_absent`
- `memory_write_absent`
- `process_score_present`
- `outcome_score_present`
- `failure_attribution_valid`
- `failed_run_traceable`

That last rule becomes important once release review expects failed-run drills. It checks that a degraded path did not merely fail, but failed in a way the team can still inspect through status, a concrete failure reason such as `failure_reason`, trace linkage, and governed release identity.

That means the grading contract should not focus only on the final answer text, but also on system behavior.

## How this connects to traces

A useful practical model looks like this:

- the trace schema describes actual run behavior;
- the eval dataset schema describes expected behavior;
- the grading contract maps one to the other.

This is the point where observability stops being only a way to look backward and becomes part of release decisions.

## What the reference runtime already supports

In `agent_runtime_ref`, this command:

```bash
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

already produces a small structured artifact with:

- multiple session scenarios;
- `labels`;
- `expected_outcomes`;
- a failed-run drill scenario that preserves failed status and `failure_reason` in session export and eval expectations.

It is not yet a full industrial eval framework, but it is already a reasonable seed for:

- regression grading;
- scenario comparison;
- rollout review;
- manual expansion of the eval set.

## What a production dataset schema should add

Once the system becomes more serious, it is useful to extend the dataset schema with:

- `dataset_version`
- `scenario_owner`
- `source_trace_ids`
- `grader_type`
- `blocking`
- `notes_for_review`
- `verifier_outputs`
- `failure_attribution`
- `verifier_id`
- `verifier_contract_version`
- `verifier_evidence_refs`

That is when the eval artifact starts behaving like part of release discipline, not just temporary JSON.

## Example grading contract

Here is a workable skeleton for a failed-run drill scenario:

```yaml
scenario_id: failed_run_timeout
labels:
  - failed_run
  - tool_timeout
  - failure_drill
grading_rules:
  - type: status_equals
    expected: failed
    blocking: true
  - type: contains_substring
    expected: tool_timeout
    blocking: true
  - type: failed_run_traceable
    expected: true
    blocking: true
verifier_outputs:
  verifier_id: fara-process-review
  verifier_contract_version: verifier-v2
  process_score: 0.92
  outcome_score: 0.35
  failure_attribution: uncontrollable_environment
  verifier_evidence_refs:
    - trace:trace_123
    - screenshot:step_7
```

The point is that the contract evaluates not only the final text, but also the correct operational shape of behavior, including whether the concrete failed condition remains visible enough for later review.

This becomes especially important for long-horizon agents, where a binary pass/fail verdict often hides the difference between correct behavior with a blocked outcome and unsafe behavior that happened to end in nominal success.

## Why multi-run sessions matter

For agent systems, an eval item often needs to describe not one request, but a short related sequence.

For example:

1. the user asks to create a ticket;
2. then asks what the agent remembers about preferences;
3. then asks for the next step.

If the dataset cannot describe such a sequence, you can test single-turn behavior fairly well, but session behavior much less well.

That is why session exports and eval dataset exports should be designed together.

## What not to do

Several mistakes are very common:

- mixing scenario metadata and grading logic in one text field;
- keeping only happy-path cases;
- not declaring expected outcomes explicitly;
- grading only the final answer and ignoring policy or tool behavior;
- not versioning the dataset;
- not linking dataset items to trace evidence or incident history;
- collapsing verifier output into a single weak verdict with no process/outcome split or failure attribution.

That makes eval culture fragile.

## What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Does every scenario have a stable `scenario_id`?
- Are labels separate from expected outcomes?
- Do you have grading rules, not just reviewer prose?
- Can you evaluate behavior, not only text?
- Can the verifier output separate `process_score`, `outcome_score`, and `failure_attribution`?
- Can you tell which verifier identity and contract version produced that grading output?
- Do you support multi-run sessions?
- Do you have dataset versioning and ownership?

If several answers are “no,” you probably have examples, but not yet a proper eval dataset schema.

## What to Do Next

- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Policy Bundle Schema and Approval Contract](policy-bundle-schema.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Reference Package](reference-package.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../book/part-v/chapter-13.en.md)
