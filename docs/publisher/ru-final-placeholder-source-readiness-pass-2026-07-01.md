# Final placeholder/source readiness pass

Date: 2026-07-01.

Status: mechanical readiness pass complete for the pre-author package. Final
semantic verification of fast-moving platform/API/security claims still belongs
after author/source metadata sync and before final publisher submission.

## Placeholder scan

Command:

```bash
rg -n "\\[заполнить\\]" docs/publisher/ru-manuscript-full.md docs/book docs/appendix/sources.md
```

Result:

- one hit in `docs/publisher/ru-manuscript-full.md:19`;
- the hit is in the author/front-matter placeholder area:
  `Публичные проекты и ссылки: [заполнить].`;
- no `[заполнить]` hits in `docs/book` or `docs/appendix/sources.md`.

Command:

```bash
rg -n "TODO|FIXME|TBD" docs/publisher/ru-manuscript-full.md docs/book docs/appendix/sources.md
```

Result: no matches.

## Source wording scan

OpenReview:

- Chapter 13 no longer carries the OpenReview HCI footnote as primary support.
- `The Illusion of Consensus in Human-Centered Interactive AI` remains only in
  the source appendix/full manuscript as a demoted research lead.
- OpenReview records remain out of primary evidence unless metadata is
  separately verified and deliberately promoted later.

Air Canada:

- Russian Chapter 18 and the Russian full manuscript use the official Civil
  Resolution Tribunal source for `Moffatt v. Air Canada`.
- No `American Bar Association` or `americanbar` references remain in the
  Russian packet paths checked in this pass.

## Remaining final source gate

This pass does not replace the final semantic source pass. Before final
publisher submission, re-check fast-moving platform/API/security claims and
record the date and scope in the source catalog.
