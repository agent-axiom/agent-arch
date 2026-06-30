# Source follow-up pass

Date: 2026-06-30.

Status: targeted follow-up completed for the URLs that were blocked, timed out
or challenge-gated in the 2026-06-29 full URL availability pass. This closes
the actionable URL cleanup that can be completed in this environment, but it
does not close OpenReview metadata verification.

Evidence:

- `docs/publisher/ru-source-follow-up-live-check-2026-06-30.tsv`

## Decisions

1. **Microsoft Research Human-AI Interaction Guidelines** remains in the source
   catalog. The page title was confirmed by body/title read, while HEAD still
   returns 403 through Akamai.
2. **Anthropic Claude Code Security** moved from the old
   `docs.anthropic.com` route to the current canonical route:
   `https://code.claude.com/docs/en/security`.
3. **MLCommons AILuminate v1.0 Release** remains in the source catalog. The
   follow-up request returned HTTP 200 and the expected page title.
4. **Air Canada chatbot case** now uses the official Civil Resolution Tribunal
   primary source instead of the challenge-gated ABA article:
   `https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do`.
5. **OpenReview records** remain browser/API-gated. Public page and API access
   returned challenge verification instead of paper metadata. The source
   appendix now demotes these links to non-primary research leads; they must
   not be used as primary evidence in the final publisher packet unless
   metadata is verified later through browser/API access.

## Manuscript/source updates

Updated:

- `docs/appendix/sources.md`
- `docs/book/part-ii/chapter-3.md`
- `docs/book/part-vii/chapter-18.md`
- `docs/publisher/ru-manuscript-full.md`

## Remaining source boundary

The source catalog is cleaner than after the 2026-06-29 URL pass, but final
publisher submission still requires:

- no OpenReview primary-evidence dependency remains; if these records are
  promoted again later, metadata must be manually verified first;
- a final semantic pass over fast-moving platform claims after author fields are
  filled and before the final DOCX export;
- confirmation that source-status wording in the Google Doc matches the
  repository source-of-truth.
