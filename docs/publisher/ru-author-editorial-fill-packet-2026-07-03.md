# Author editorial fill packet

Date: 2026-07-03.

Status: ready for author completion against the current Template2000n proof.
These fields must be filled, explicitly omitted or delegated to the publisher
before final publisher submission.

Current proof context:

- Google Doc manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Template2000n pre-author proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-final-preauthor-2026-07-03.docx`
- final pre-author export report:
  `docs/publisher/ru-final-preauthor-export-pass-2026-07-03.md`
- style acceptance gate:
  `docs/publisher/ru-template2000n-acceptance-gate-2026-07-03.md`

## Fill rules

- Use factual, checkable wording.
- Do not add client, employer or case details unless they are cleared for
  publication.
- If a field should not appear in the book, write `omit`.
- If the publisher should decide the wording, write `publisher to propose`.
- Do not leave fields blank in the final answer packet.

## Required author answers

```text
Public byline:
Preferred Russian author line:
Short bio, 40-70 words:
Long bio, 120-180 words:
Current role/title:
Independent positioning if no company title should be used:
Verified experience claims that may be printed:
Public projects safe to mention:
GitHub/site/blog/profile links:
Preferred contact or public page for metadata:

Final Russian title:
Subtitle:
One-sentence positioning:
Short cover copy:
Long catalog/website description:
Target reader wording:
Keywords:

Companion URL:
Companion repository URL if different:
First public version:
Changelog route:
Errata route:
License/usage terms for templates:
Issues/discussions enabled or disabled:

AI-use disclosure wording:
Legal/compliance disclaimer wording:
Acknowledgements:
People or organizations requiring permission:

Real/composite/anonymized case policy:
Support triage case status:
Internal knowledge assistant case status:
Incident coordination case status:
Coding/platform-agent examples status:
Details that must never be published:

Legal author name for publisher metadata if different:
Preferred cover author name:
Imprint/series data:
ISBN or publisher placeholder:
Required copyright wording:

Fields intentionally omitted:
Fields delegated to publisher/editor:
```

## Where answers go

After the author answers:

1. Update the Google Doc front matter and `Об авторе` block.
2. Backport accepted text to repository control files.
3. Update cover note and editor handoff packet.
4. Re-export raw DOCX from Google Docs.
5. Rebuild the Template2000n derivative.
6. Repeat render QA and archive integrity checks.

## Current blocker

Codex must not invent the author bio, credentials, public links, case policy,
acknowledgements, legal disclaimer or AI-use disclosure. These are author-owned
facts and publication decisions.
