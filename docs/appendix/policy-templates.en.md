# Policy Templates and Checklists by Use Case

This page exists so the case studies in the book can be used, not just read.

The idea is not "here is one universal production policy." The point is the opposite: to show how the policy layer starts to differ depending on the scenario.

If you need the narrative context first, start with the [Practical Case Studies](case-studies.en.md). If you want the remaining project backlog, see the [Community Roadmap](community-roadmap.en.md).

## How to read these templates

Treat them not as finished production YAML, but as a skeleton:

- what the system considers risky;
- where the approval boundary lives;
- how read and write actions are separated;
- which stop conditions and escalation rules matter;
- which traces and audit signals should be mandatory.

## Template 1. Support Triage Agent

### What the policy should enforce

For support triage, you usually need to:

- safely read customer context;
- avoid write actions without enough confidence;
- avoid returning a model answer "as if everything is already resolved" when a human is needed;
- explicitly constrain ticket creation and sensitive updates.

### Example policy skeleton

```yaml
agent:
  name: support_triage
  allowed_models: ["gpt-5.4", "gpt-5-mini"]
  max_steps: 12
  stop_conditions:
    - enough_information_to_answer
    - requires_human_review
    - write_requires_approval

tools:
  read_customer_profile:
    mode: read
    tenant_scoped: true
    approval: none

  read_ticket_history:
    mode: read
    tenant_scoped: true
    approval: none

  create_ticket:
    mode: write
    approval: manager
    idempotency_key_required: true
    retry_on: ["retryable_failure"]

output:
  require_structured_decision: true
  require_escalation_reason: true
```

### Checklist

- Do read tools have tenant scope?
- Can the agent escalate honestly instead of always trying to answer?
- Is `create_ticket` protected by explicit approval policy?
- Does the trace show why the write path was selected?
- Is there a stop condition for low confidence?

## Template 2. Internal Knowledge Agent

### What the policy should enforce

In the knowledge scenario, the main risk is not side effects but access and grounding quality.

You usually need to:

- separate access by role;
- constrain retrieval to allowed sources;
- prevent the agent from mixing untrusted content with instructions;
- require source references in the answer.

### Example policy skeleton

```yaml
agent:
  name: internal_knowledge
  allowed_models: ["gpt-5.4", "gpt-5-mini"]
  max_steps: 8
  stop_conditions:
    - answer_ready
    - insufficient_grounding
    - access_denied

retrieval:
  role_scoped: true
  tenant_scoped: true
  max_documents: 8
  require_source_labels: true

output:
  require_sources: true
  deny_if_no_grounding: true
  deny_sensitive_snippets_without_access: true
```

### Checklist

- Does role-based filtering really work on the retrieval path?
- Does the agent return sources instead of only polished text?
- Is there a policy for weak grounding?
- Can retrieval leak a private knowledge zone?
- Do traces show which documents were actually used?

## Template 3. Incident Coordination Agent

### What the policy should enforce

In the incident scenario, policy must govern not only access but orchestration discipline.

You usually need to:

- keep one trace across the entire run;
- record ownership at handoffs;
- constrain risky remediation;
- prevent noisy input from turning into unnecessary side effects.

### Example policy skeleton

```yaml
agent:
  name: incident_coordinator
  allowed_models: ["gpt-5.4"]
  max_steps: 20
  orchestration:
    pattern: manager_with_controlled_handoffs
    require_handoff_reason: true
    require_current_owner: true

tools:
  create_incident_thread:
    mode: write
    approval: oncall_lead
    idempotency_key_required: true

  notify_team:
    mode: write
    approval: oncall_lead
    idempotency_key_required: true

  suggest_remediation:
    mode: advisory
    approval: none

  execute_remediation:
    mode: write
    approval: security_and_service_owner
    disabled_by_default: true

audit:
  require_trace_per_run: true
  require_handoff_log: true
  require_write_intent_log: true
```

### Checklist

- Does every handoff have an owner and a reason?
- Is risky remediation disabled by default?
- Are ticketing and notifications protected by idempotency?
- Does the incident trace show the full decision path?
- Can a noisy alert alone trigger a dangerous write path?

## Universal Checklist for the Policy Layer

Regardless of the use case, ask:

- Do you know where `read`, `write`, and `advisory` actions live in the system?
- Do risky actions have a separate approval boundary?
- Is it visible in policy where the agent must stop rather than continue reasoning?
- Are critical rules stored only inside prompts?
- Can the security team read policy artifacts without knowing every detail of prompt engineering?

If the answer is "no" several times in a row, the policy layer is still too implicit.

## Where to go next

- [Practical Case Studies](case-studies.en.md)
- [Chapter 3. Security Perimeter and Trust Boundaries](../book/part-ii/chapter-3.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../book/part-vii/chapter-17.en.md)
