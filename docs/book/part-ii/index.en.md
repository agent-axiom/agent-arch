# Part II. Security Perimeter

If in the first part we assembled the architectural picture, here the same support agent reaches the first real risks: access to data, tool calls, and actions with side effects.

!!! info "Short path through this part"
    If you want a fast pass, read it this way:

    - [Chapter 3](chapter-3.en.md): understand where the trust boundaries are;
    - [Chapter 4](chapter-4.en.md): see where the system must stop before a real action happens;
    - [Chapter 5](../part-iii/chapter-5.en.md): decide what the agent is allowed to remember after a run like that.

    Those three points already give you not just security vocabulary, but a working production contour.

!!! note "Part II canonical case routes"
    In the security perimeter, the three canonical cases require different control points. **Support triage** checks the tool gateway, approval stop, audit trail, and least-privilege access for ticket writes. **Internal knowledge assistant** checks retrieval boundary, access control, prompt assembly, and egress filtering for protected reads. **Incident coordination** checks escalation tools, notification approvals, incident-data boundary, and audit trail for side effects during response.

This part exists so that you do not develop the dangerous illusion that agent security can be "added later." In our running case, this is the moment when it becomes obvious that without a defined perimeter the agent stops helping and starts creating new risk.

<div class="book-cover" markdown="1">

![Cover for the security perimeter part](../../assets/images/part-ii-security.png)

</div>

- if trust boundaries are not defined in advance, the agent quickly starts pulling in extra context;
- if tools are not isolated, one bad call turns into a real incident;
- if policy, approval, and audit are not built into the runtime, the team loses control at the worst possible moment.

## What This Part Solves

- a map of the key threats in agent systems;
- a practical model of the security perimeter;
- a set of control points: ingress, prompt assembly, model gateway, retrieval, tools, egress;
- examples of policy-as-code and gated execution;
- a solid base for discussing the system with a security team without abstract hand-waving.

## In This Part

- [Chapter 3. Security Perimeter and Trust Boundaries](chapter-3.en.md)
- [Chapter 4. Tool Gateway, Approval, and Audit Trail](chapter-4.en.md)
  This chapter continues the same support case at the moment the system is about to turn a decision into an external action.
- [Part I. Foundations](../part-i/index.en.md)
- [Sources](../../appendix/sources.en.md)

## Where It Leads Next

The next natural step after this perimeter is [Part III](../part-iii/index.en.md): deciding what the agent is allowed to remember across runs, how retrieval returns context, and how memory avoids becoming a new source of risk.
