# Chapter 4. Tool Gateway, Approval, and Audit Trail

## 1. Where the Expensive Incidents Actually Happen

The most expensive failures in agent systems usually happen not when the model "thought incorrectly," but when the system moved to action:

- wrote something;
- sent something;
- changed something;
- exported data somewhere.

That is why the execution boundary matters much more than many people expect.

## 2. A Tool Gateway Should Be Boring and Strict

A good tool gateway has a very simple job: do not let the agent turn pretty reasoning into an uncontrolled side effect.

Minimal requirements:

- accept only allowed tools;
- validate arguments;
- know the risk class of the operation;
- stop the call before the side effect happens;
- route dangerous operations to human approval;
- log both the decision and the fact of execution.

Here is a very practical policy template for tool execution:

```yaml
tools:
  read_kb:
    risk: low
    approval: none
    allowed_roles: ["agent_runtime"]
  create_ticket:
    risk: medium
    approval: manager
    allowed_roles: ["agent_runtime"]
  prod_db_write:
    risk: critical
    approval: security_and_owner
    allowed_roles: []
    environments: ["staging"]
```

There is nothing "smart" in that YAML, and that is exactly why it is good. Security perimeters like visible rules.

## 3. Human Approval Should Be a Real Process

There are actions the agent should not complete on its own at all:

- changing production data;
- sending messages to external channels;
- financial operations;
- access to sensitive documents;
- any action with a high blast radius.

For those, you need more than a toggle called "approval required." You need a real confirmation flow.

<div class="diagram-card">
<p>What an approval flow for a risky action looks like</p>

``` mermaid
sequenceDiagram
    autonumber
    participant R as Agent runtime
    participant P as Policy engine
    participant H as Human approver
    participant T as Tool gateway
    participant A as Audit trail

    R->>P: Request risky action
    P-->>R: Approval required
    R->>H: Ask for approval with context
    H-->>R: Approve / reject
    R->>T: Execute only if approved
    T->>A: Persist action + approval record
```

</div>

A good approval flow always stores:

- who requested the action;
- what the risk class was;
- what exactly the system wanted to do;
- who confirmed it;
- at what time;
- whether a policy gate was overridden.

## 4. Egress Needs Protection Too

Many teams carefully filter incoming data, but barely think about the output side. That is a mistake.

Leaks most often happen on egress:

- the agent inserted an extra fragment of a document into the answer;
- it sent sensitive text into an external tool;
- it wrote private data into logs;
- it returned a result from another tenant.

Minimal egress checklist:

- redact PII where required;
- mask secrets and tokens;
- validate tenant ownership of retrieved content;
- restrict outbound destinations;
- log all sensitive outbound actions.

## 5. The Audit Trail Must Be Useful for Investigation

Simply "turning on tracing" is not enough. For security, you need a trail from which you can reconstruct the history of an event.

For one risky run, it is useful to keep:

- the incoming request id;
- the principal and tenant;
- the policy decision;
- prompt assembly metadata;
- tool call arguments in safely redacted form;
- approval records;
- the final egress event.

If after an incident the team sees only "the model called tool X," the investigation is already half lost.

## 6. The Security Perimeter as a Set of Habits

It is very tempting to look for one magic library that will "do safety." In practice, the perimeter is a set of habits:

- untrusted data is marked explicitly;
- the agent runtime does not get extra permissions;
- tools go only through the gateway;
- dangerous actions require approval;
- all key steps land in the audit trail;
- the system knows not only how to execute, but also how to refuse.

That is what mature safety looks like for an agent platform.

## 7. Practical Checklist

If you want to quickly assess your current perimeter, go through this list:

- Does the agent have a separate identity model?
- Are trusted instructions separated from untrusted content?
- Do all tools go through a gateway?
- Is there an allowlist and argument validation?
- Is there an approval flow for high-risk actions?
- Is there egress filtering?
- Is the audit trail sufficient for investigation?
- Can you see which policy gate fired in traces?

If the answer is "no" several times in a row, then you opened this chapter at exactly the right moment.

## 8. What to Read Next

- [Chapter 3. Security Perimeter and Trust Boundaries](chapter-3.en.md)
- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](../part-iii/chapter-5.en.md)
- [Part II. Security Perimeter](index.en.md)
- [Sources](../../appendix/sources.en.md)
