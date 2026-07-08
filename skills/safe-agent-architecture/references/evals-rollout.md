# Evals, Deployment Simulation, and Rollout Gates

Production safety comes from repeatable evidence, not demo confidence.

## Eval Layers

Use multiple layers:

1. **Unit and contract tests** for deterministic code, schemas, policies, and adapters.
2. **Offline evals** for known scenarios and regressions.
3. **Trace grading** for tool choice, policy compliance, retrieval grounding, approvals, recovery, and efficiency.
4. **Behavioral evals** for process quality, not only final answer.
5. **Control evals** for oversight avoidance, excessive agency, approval bypass, and tool misuse.
6. **Deployment simulation** for representative historical contexts before rollout.
7. **Online monitoring** for real traffic, drift, incidents, and calibration.

## Eval Artifact Minimum

Each scenario should have:

- `scenario_id`
- labels
- risk class
- input(s)
- expected outcomes
- blocked behaviors
- required trace events
- verifier or grading rule
- blocking/non-blocking decision
- owner

## Deployment Simulation

Use when model, prompt, policy, tool surface, or runtime changes could affect production behavior.

Define:

- source traffic/session window;
- privacy filtering;
- candidate model/runtime/policy;
- removed historical assistant completion;
- simulated or read-only tool environment;
- failure modes measured;
- behavior deltas;
- post-release calibration plan.

Caution: simulation does not replace adversarial evals. Representative replay finds common/emerging failures; targeted evals find rare tail risks.

## Tool Simulation Fidelity

For tool-heavy agents, document:

- which tools are simulated;
- state model;
- reset rules;
- error/latency/empty-result cases;
- schema enforcement;
- where the simulator is known to be unrealistic;
- when a sandbox or canary is required.

## Rollout Gate

A release gate should answer:

- Which evals passed or failed?
- Which failures block rollout?
- Which risk tier is being expanded?
- What telemetry must be present before expansion?
- What disables or rolls back the agent?
- Who owns the decision?

## Post-Release Telemetry

Track:

- tool policy denials;
- approval requests/decisions;
- side-effect failures;
- idempotency/retry events;
- retrieval freshness/source attribution;
- memory write decisions;
- user correction/escalation;
- cost/latency budget;
- incident signals;
- rollout wave.

## Readiness Rule

Do not call an agent production-ready unless it has:

- passing blocking evals;
- observable traces;
- rollout gate;
- owner;
- incident path;
- rollback/disable path.
