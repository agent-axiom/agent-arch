# Errata

Status: public practice draft, unreleased (2026-10-03).

The affected previous practice baseline is
`6fa79caa76d53b82953f285f8452b9b0ccd6c50d`. No `v1.0-book` tag exists as of
this draft. Reproducing the correction requires a commit that contains it.

## How to report

Report reproducible public practice issues in the
[repository issue tracker](https://github.com/agent-axiom/agent-arch/issues).
Include the exact revision, command, expected result and actual result.

Keep private manuscript and publisher material in the private editorial workflow.
Do not attach or copy those files into public issues or this repository.

## Errata policy

- Typos and formatting mistakes can be fixed in patch releases.
- Technical corrections should name the affected chapter, section and companion
  file.
- Fast-changing platform facts should include the date and source checked.
- Material guidance changes must be reflected in the changelog, not silently
  rewritten.

## Known correction: stale completion evidence

- Affected practice: chapter 26, lease/version negative scenario in
  `examples/run_lab_negative_scenario.py`, at the pinned baseline above.
- Baseline behavior: `_run_stale_completion` constructs two claims but returns
  `accepted=false`, `expected_version_mismatch` and `not_executed` as constants.
  That output illustrates a result shape; it does not exercise a completion
  guard or establish that a side effect was prevented.
- Draft correction: a local completion function checks version and nonempty
  lease-owner identity before invoking a callback. The scenario exercises a
  rejected stale claim and an accepted current claim, recording their effects
  separately. Tests also isolate version mismatch from owner mismatch so that
  removing either guard is detectable.
- Command in the corrected draft checkout:

  ```bash
  python docs/companion/examples/run_lab_negative_scenario.py lab26-negative-lease
  ```

  `stale-run-completion` remains supported. The top-level rejection fields keep
  their meanings; `positive_control` reports the valid attempt. The new alias
  and evidence fields are not available at the unchanged baseline revision.
- Limits: this is a sequential in-memory check against a caller-supplied current
  snapshot, not a distributed lease implementation. It does not provide atomic
  compare-and-set storage, lease expiry, durable completion, replay prevention,
  or exactly-once external effects. `idempotency_scope` is context only, not an
  implemented deduplication guarantee. A callback exception propagates and does
  not establish that no effect occurred.

## Practice clarification: paired policy traces

The default `export-events` request asks the demo planner to create a ticket;
changing a `search_docs` rule alone does not exercise that rule. The demo planner
does not select arbitrary tools from a natural-language prompt.

For a reproducible read-only pair, run from a corrected checkout:

```bash
uv run python docs/companion/examples/export_policy_trace_pair.py \
  --output-dir artifacts/ch27-policy-pair
```

The output directory must be absent or empty. `allow.jsonl`, `deny.jsonl` and
`summary.json` record separate runs of the same request. Only the copied
`search_docs` policy decision changes; the source config remains untouched.
The helper replaces the model's choice, not the catalog, policy or executor.
No LLM or external search service is contacted.

With the default configs, allow yields a successful synthetic read; deny yields
`permission_denied` and a failed run. Both report
`side_effect_status=not_executed`: a successful read is not an external write.
`tool_execution` is also recorded for a rejected request and does not by itself
prove that an external adapter ran. Tests check the executor's post-policy
stage separately. Other source-config guards remain active and can deny either
case; the summary reports observed outcomes rather than forcing success.

## Publication status

- The [online companion](index.md) contains working public practice materials.
- A first-edition release remains unassigned. Record the exact tested commit
  containing this correction when using it as a practice reference; a feature
  branch name alone is not an immutable version.
