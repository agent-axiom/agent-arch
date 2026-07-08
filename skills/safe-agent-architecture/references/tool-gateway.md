# Tool Gateway, MCP/A2A, and Approval Boundaries

Tools are authority. Treat every tool as a capability with policy, identity, and evidence.

## Capability Contract

For each tool/capability, define:

- `capability_name`
- read/write/destructive classification
- actor identity and tool principal
- input schema and validation
- allowed data classes and tenant scope
- required approval state
- idempotency key rules
- retry and rollback behavior
- audit payload
- redaction policy
- owner

## Tool Gateway Rules

- Put tools behind a gateway instead of exposing raw functions directly to the model.
- Validate arguments before execution.
- Separate policy decision from tool execution.
- Emit trace events for policy decision, approval request, execution, failure, and result.
- Do not let retrieved content, tool output, or web content become higher-priority instructions.
- Treat tool descriptions as policy surface: review diffs, new endpoints, expanded parameters, and changed scopes.

## Approval Rules

Human approval must specify:

- exact payload being approved;
- approver role;
- scope: single action, session, time-boxed class, or denied;
- expiry;
- linked `trace_id`, `session_id`, `approval_id`;
- tool principal used for the side effect;
- idempotency key;
- audit record after execution.

A vague "human in the loop" is not enough.

## Sandbox and Execution

For code, browser, shell, file, or network access, define:

- filesystem scope;
- network posture;
- secrets posture;
- package/install policy;
- process timeout and resource limits;
- artifact retention;
- snapshot/resume policy;
- egress rules;
- whether outputs can be trusted as data only.

Default for prototypes: fake data, restricted filesystem, no network, no secrets, no live writes.

## MCP/A2A Threats to Check

- Tool poisoning: tool descriptions or schemas steer behavior.
- Rug pull: remote server changes behavior after approval.
- Tool shadowing: a malicious tool imitates a trusted capability.
- Confused deputy: agent uses its authority for another actor's goal.
- Over-scoped tokens: credential scope exceeds job need.
- Data exfiltration through legitimate channels.
- Replay/tampering: old or altered calls reused.
- Local control-plane crossing: browser/web content reaches localhost or debug/MCP sockets.
- Delegated authority drift across A2A handoffs.

## Design Output

For action-capable agents, include a table:

| Capability | Risk | Approval | Identity | Idempotency | Trace events | Rollback/disable |
| --- | --- | --- | --- | --- | --- | --- |

If the table cannot be filled, the tool surface is not ready.
