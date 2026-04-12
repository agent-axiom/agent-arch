# Part VI. Operating Model

By this point, we already have most of the technical frame:

- architecture;
- safety;
- memory;
- execution layer;
- observability and eval loop.

But after that, the bottleneck is usually not technical anymore. It becomes organizational.

Even a good agent platform quickly runs into questions like:

- who owns the base layers;
- who is responsible for policy and guardrails;
- how product teams use the platform without breaking it;
- how not to end up with five incompatible agent runtimes inside one company.

In this part, we will look at the operating model: who owns what, how to build golden paths, and how to avoid turning the platform into a chaotic set of local decisions.

!!! info "Short path through this part"
    If you want a fast pass, read it this way:

    - [Chapter 14](chapter-14.en.md): understand where platform ownership ends and product ownership begins;
    - [Chapter 15](chapter-15.en.md): see how that boundary becomes golden paths and shared gateways;
    - [Part VII](../part-vii/index.en.md): see how the operating model becomes concrete in the reference implementation.

    Together, this shows that the operating model is not for org charts. It is for keeping the production system stable.

## In This Part

- [Chapter 14. Platform Team vs Product Teams](chapter-14.en.md)
  This chapter continues the same support case at the ownership layer: who should own the runtime, policies, gateways, and platform-grade incidents.
- [Chapter 15. Golden Paths, Shared Gateways, and Anti-Zoo Patterns](chapter-15.en.md)

The next natural step after this part is to complete the platform roadmap and move into the reference implementation.
