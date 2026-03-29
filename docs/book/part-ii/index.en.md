# Part II. Security Perimeter

If in the first part we assembled the basic architectural picture, here we begin to examine the most nerve-wracking layer of the whole system: safety.

This part exists so that you do not develop the dangerous illusion that agent security can be "added later." In reality, things work the other way around:

- if trust boundaries are not defined in advance, the agent quickly starts pulling in extra context;
- if tools are not isolated, one bad call turns into a real incident;
- if policy, approval, and audit are not built into the runtime, the team loses control at the worst possible moment.

## What You Get in This Part

- a map of the key threats in agent systems;
- a practical model of the security perimeter;
- a set of control points: ingress, prompt assembly, model gateway, retrieval, tools, egress;
- examples of policy-as-code and gated execution;
- a solid base for discussing the system with a security team without abstract hand-waving.

## Navigation

- [Chapter 3. Security Perimeter and Trust Boundaries](chapter-3.en.md)
- [Chapter 4. Tool Gateway, Approval, and Audit Trail](chapter-4.en.md)
- [Part I. Foundations](../part-i/index.en.md)
- [Sources](../../appendix/sources.en.md)
