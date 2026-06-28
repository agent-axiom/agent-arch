# Author query packet

Date: 2026-06-28.

Status: send to the author before final external proofread.

Purpose: collect the facts that cannot be inferred from the manuscript or the
repository. These answers should be copied into the Google Doc front matter and
then backported to the repository control files.

## How to answer

Use short factual answers. Avoid claims that the publisher, editor or reader
cannot verify. If a field is intentionally omitted, write `omit` rather than
leaving it ambiguous.

## 1. Author identity

- Public author name:
- Preferred Russian author line:
- Current role/title:
- Independent positioning if no company title should be used:
- City/country if publisher metadata requires it:

## 2. Short bio

Target: 40-70 words.

Draft to fill:

> [Author name] - [role/positioning]. [One factual sentence about practical
> experience]. [One sentence about public work/projects or why this book is
> relevant].

Author answer:

> [fill]

## 3. Long bio

Target: 120-180 words.

Must include only facts that can survive copyedit:

- professional focus;
- relevant engineering/security/platform experience;
- public projects or public writing;
- why the author is credible on agent architecture;
- no confidential client/employer details unless cleared.

Author answer:

> [fill]

## 4. Public links

- GitHub:
- Website:
- Blog:
- LinkedIn/other profile:
- Public project page:
- Preferred contact for publisher metadata:

## 5. Book metadata

- Final Russian title:
- Subtitle:
- One-sentence positioning:
- Short back-cover copy:
- Long catalog/website description:
- Target reader wording:
- Keywords:

## 6. Companion

- Public companion URL:
- Public repository URL, if different:
- First book release version:
- Errata route:
- Changelog route:
- License/usage terms for templates:
- Whether issues/discussions are enabled:

## 7. AI tooling disclosure

Answer in one of two forms:

- Approved wording:
- Or: publisher/editor should propose wording.

Minimum content to decide:

- whether AI tools were used for drafting, translation, editing or QA;
- whether final responsibility remains with the author;
- whether any generated material requires special disclosure by contract.

## 8. Legal and compliance disclaimer

Answer in one of two forms:

- Approved wording:
- Or: publisher/editor should propose wording.

Minimum content to decide:

- templates are architectural aids, not legal advice;
- security/compliance guidance must be adapted to the reader's jurisdiction and
  organization;
- examples do not guarantee production safety without local review.

## 9. Real and composite cases

For each case type, mark one:

- support triage: real / anonymized / composite / omit;
- internal knowledge assistant: real / anonymized / composite / omit;
- incident coordination: real / anonymized / composite / omit;
- coding or platform-agent examples: real / anonymized / composite / omit.

If any real case is used:

- required permission:
- details that must be anonymized:
- details that must never be published:

## 10. Acknowledgements

- Include acknowledgements: yes / no.
- Names or groups:
- Permission needed before naming anyone:
- Publisher-sensitive wording:

## 11. Final publisher metadata

- Author legal name for contract metadata, if different from public name:
- Preferred author name on cover:
- Final title page wording:
- Imprint/series data supplied by publisher:
- ISBN placeholder or final value:
- Required copyright wording:

## Transfer checklist

- [ ] Answers copied into the Google Doc.
- [ ] Repository author-open-fields note updated.
- [ ] Cover note updated.
- [ ] Clean editor handoff packet updated.
- [ ] Raw DOCX re-exported after author fields.
- [ ] Template2000n proof rebuilt after author fields.
- [ ] Render QA repeated after author fields.
