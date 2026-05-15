# Google Integration Roadmap

This page fixes a separate integration plan for what is worth borrowing from recent Google Cloud materials and folding into the book. The goal is not to duplicate what is already written, but to strengthen the parts where Google is especially strong: platform operations, runtime isolation, identity, and governance.

## Why a separate roadmap helps

Google's strongest recent material is not generic "AI agents" commentary. It is practical, production-grade guidance in four areas:

- platform view of agent systems;
- sandboxed execution as infrastructure;
- agent identity, registry, and governance;
- a clean distinction between `MCP` and `A2A`.

That complements the OpenAI, Anthropic, and LangGraph material already embedded in the book.

!!! note "Canonical Google integration cases"
    The Google integration roadmap is more useful when platform-grade ideas are checked against the three canonical cases. **Support triage** tests agent identity, least privilege, approval/audit linkage, sandbox profile, high-risk tools, and duplicate-ticket controls. **Internal knowledge assistant** tests context layers, memory governance, retrieval policy, source provenance, and tenant-aware access. **Incident coordination** tests registry governance, A2A boundaries, continuous controls, rollout gates, escalation traces, and response ownership.

## Step-by-step plan

### Step 1. Five pillars of the platform and context layers

Where it goes:

- [Chapter 2. Reference Architecture for a Safe Agent](../book/part-i/chapter-2.en.md)

What to add:

- the `framework -> model -> tools -> runtime -> trust` frame;
- context layers: static, session, turn, cached context;
- a practical section on prompt budget and context discipline.

### Step 2. Agent identity and access boundaries

Where it goes:

- [Chapter 3. Security Perimeter and Trust Boundaries](../book/part-ii/chapter-3.en.md)
- [Chapter 4. Tool Gateway, Approval, and Audit Trail](../book/part-ii/chapter-4.en.md)

What to add:

- machine identity and agent identity as a separate layer;
- least privilege for tools, memory, and external systems;
- the connection between identity and auditability.

### Step 3. Memory governance and memory revisions

Where it goes:

- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](../book/part-iii/chapter-5.en.md)
- [Chapter 6. Short-Term, Long-Term, and Profile Memory](../book/part-iii/chapter-6.en.md)

What to add:

- a clean split between memory read policy and memory write policy;
- revisions and provenance for memory updates;
- the idea that memory is itself a governable subsystem.

### Step 4. Sandbox execution as infrastructure

Where it goes:

- [Chapter 9. Sandbox Execution and MCP as an Integration Contract](../book/part-iv/chapter-9.en.md)

What to add:

- the distinction between logical isolation, process isolation, and runtime isolation;
- ephemeral sandboxes;
- network egress controls and artifact discipline;
- a practical checklist for high-risk tools.

### Step 5. MCP for tools, A2A for agents

Where it goes:

- [Chapter 9. Sandbox Execution and MCP as an Integration Contract](../book/part-iv/chapter-9.en.md)
- a new practical block in Part IV

What to add:

- a clean distinction between `MCP` and `A2A`;
- when you need a capability contract and when you actually need agent-to-agent collaboration;
- criteria for not moving into multi-agent coordination too early.

### Step 6. User simulator and continuous eval loop

Where it goes:

- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../book/part-v/chapter-13.en.md)

What to add:

- user simulator as a separate eval pattern;
- continuous grading on top of traces;
- stronger linkage between eval loops and rollout gates.

### Step 7. Registry, approved inventory, and organizational controls

Where it goes:

- [Chapter 14. Platform Team vs Product Teams](../book/part-vi/chapter-14.en.md)
- [Chapter 15. Golden Paths, Shared Gateways, and Anti-Zoo Patterns](../book/part-vi/chapter-15.en.md)

What to add:

- an approved registry of agents, tools, and connectors;
- platform inventory as part of governance;
- continuous controls rather than one-time manual review.

### Step 8. Reference implementation uplift

Where it goes:

- [Chapter 16. Baseline Runtime Blueprint](../book/part-vii/chapter-16.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../book/part-vii/chapter-17.en.md)
- `agent_runtime_ref`

What to add:

- context layers in the runtime;
- agent identity;
- memory provenance;
- sandbox profile;
- registry-like inventory of capabilities.

## Priority

If we rank by practical reader value, the order is:

1. context layers;
2. identity;
3. sandbox infrastructure;
4. MCP vs A2A;
5. memory governance;
6. user simulator;
7. registry and continuous controls;
8. runtime uplift.

## Sources

- Google Cloud, [Achieve agentic productivity with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/get-started-with-vertex-ai-agent-builder)
- Google Cloud, [More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
- Google Cloud, [Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
- Google Cloud Architecture Center, [Multi-agent AI system in Google Cloud](https://docs.cloud.google.com/architecture/multiagent-ai-system)
- Google Cloud, [How Google secures AI Agents](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-how-google-secures-ai-agents)
- Google Cloud, [Introducing Agent Sandbox](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke/)
- Google Cloud, [Building Connected Agents with MCP and A2A](https://cloud.google.com/blog/topics/developers-practitioners/building-connected-agents-with-mcp-and-a2a)
- Google Cloud, [Recommended AI Controls framework](https://cloud.google.com/blog/products/identity-security/audit-smarter-introducing-our-recommended-ai-controls-framework)
