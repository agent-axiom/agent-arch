# Templates

Use these templates directly in responses or design docs.

## Safe Agent Architecture Brief

```markdown
## Safe Agent Architecture Brief

### Job and Non-Goals
- Intended outcome:
- Non-agent alternative:
- Explicit non-goals:

### Risk Tier
- Tier:
- Escalators:
- Lowest sufficient agency:

### Actors and Authority
- Human actor:
- Agent identity:
- Delegated authority:
- Tenant/data boundary:

### Tools and Capabilities
| Capability | Read/write | Risk | Approval | Identity | Idempotency | Rollback/disable |
| --- | --- | --- | --- | --- | --- | --- |

### Memory and Retrieval
- Sources:
- Filters:
- Memory write policy:
- Poisoning protections:

### Runtime
- Runtime shape:
- Checkpoints:
- Retry/idempotency:
- Sandbox/network/secrets:

### Evidence
- Required trace events:
- Approval/audit records:
- Redaction policy:

### Evals and Rollout
- Offline evals:
- Behavioral/control evals:
- Simulation:
- Rollout gate:
- Post-release telemetry:

### Lifecycle
- Owner:
- Incident path:
- Disable/rollback:
- Registry entry:
```

## Capability Review

```markdown
| Capability | Authority | Data touched | Failure mode | Required control |
| --- | --- | --- | --- | --- |
| | | | | |
```

## Eval Plan

```markdown
| Scenario | Risk | Expected outcome | Required trace evidence | Blocking? |
| --- | --- | --- | --- | --- |
| | | | | |
```

## Launch Checklist

```markdown
- [ ] Risk tier agreed
- [ ] Tool gateway in place
- [ ] Approval payload/audit record defined
- [ ] Idempotency and retry behavior tested
- [ ] Sandbox/network/secrets posture reviewed
- [ ] Retrieval filters and source grounding tested
- [ ] Memory write policy defined
- [ ] Required trace events emitted
- [ ] Offline evals pass
- [ ] Behavioral/control evals pass for high-risk paths
- [ ] Deployment/tool simulation done if relevant
- [ ] Rollout gate can block expansion
- [ ] Owner and incident path assigned
- [ ] Disable/rollback path tested
```
