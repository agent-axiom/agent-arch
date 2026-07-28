# 100 editorial goals after global heading normalization

Date: 2026-06-28

Context:

- Google Doc source was normalized with style-only updates.
- Raw proof: 504 pages, blank-like pages: 0.
- Template2000n proof: 315 pages, blank-like pages: 0.
- Long non-empty `Heading 2` debt: 0.
- Remaining style debt: 65 long `Heading 3` paragraphs over 220 chars.

Follow-up: goals 1901-1905 were implemented in
`docs/publisher/ru-google-doc-h3-normalization-pass-2026-06-28.md`. The next
100 goals continue in
`docs/publisher/ru-editorial-100-h3-normalization-iterations-2026-06-28.md`.

| # | Goal | Done when |
| --- | --- | --- |
| 1901 | Audit long `Heading 3` paragraphs globally. | Each long H3 is classified as real subhead or body-like text. |
| 1902 | Demote body-like H3 paragraphs in Google Doc. | No prose paragraph over 220 chars remains styled as H3 without structural reason. |
| 1903 | Re-export raw DOCX after H3 pass. | H3 metrics and page count are recorded. |
| 1904 | Rebuild Template2000n derivative after H3 pass. | Derived DOCX passes zip integrity and style metrics are recorded. |
| 1905 | Render raw and Template2000n after H3 pass. | Both proofs have 0 blank-like pages. |
| 1906 | Review front matter headings after H3 pass. | Author, preface, reading guide and map headings are intentional. |
| 1907 | Review chapter 1 outline. | Body paragraphs do not appear as headings. |
| 1908 | Review chapter 2 outline. | Decision-ladder sections are stable and not over-nested. |
| 1909 | Review chapter 3 outline. | Bridge into Part II has compact hierarchy. |
| 1910 | Review chapter 4 outline. | Platform vocabulary sections remain readable in TOC. |
| 1911 | Review chapter 5 outline. | Identity/session/policy/capability structure is not duplicated in H2/H3. |
| 1912 | Review chapter 6 outline. | Tool gateway and approval sections are structurally distinct. |
| 1913 | Review chapter 7 outline. | Security boundary sections are not body-style headings. |
| 1914 | Review chapter 8 outline. | Memory risk and provenance sections stay clear. |
| 1915 | Review chapter 9 outline. | Context/retrieval sections do not over-expand the TOC. |
| 1916 | Review chapter 10 outline. | Execution model sections match the tool architecture. |
| 1917 | Review chapter 11 outline. | Sandbox/MCP sections stay printable and not protocol-heavy. |
| 1918 | Review chapter 12 outline. | Retry/idempotency sections avoid checklist-as-heading drift. |
| 1919 | Review chapter 13 outline. | Trace/spans/event catalog hierarchy remains readable. |
| 1920 | Review chapter 14 outline. | SLO sections do not turn metric bullets into headings. |
| 1921 | Review chapter 15 outline. | Eval gate sections distinguish method from examples. |
| 1922 | Review chapter 16 outline. | Evidence-chain sections connect without repeated heading labels. |
| 1923 | Review chapter 17 outline. | Ownership/platform-team sections are stable. |
| 1924 | Review chapter 18 outline. | Golden path and anti-sprawl sections do not duplicate chapter 17. |
| 1925 | Review chapter 19 outline. | ADLC lifecycle sections remain compact. |
| 1926 | Review chapter 20 outline. | Assurance, incident, registry and retirement sections are balanced. |
| 1927 | Review chapter 21 outline. | Runtime sections explain architecture rather than CLI manual. |
| 1928 | Review chapter 22 outline. | Policy/catalog sections stay implementation-focused. |
| 1929 | Review chapter 23 outline. | Launch checklist sections remain the synthesis point. |
| 1930 | Review glossary outline. | Glossary letters and entries do not become false headings. |
| 1931 | Review practical cases outline. | Case headings are useful for navigation and not over-detailed. |
| 1932 | Review appendices outline. | Appendix sections route details to companion without clutter. |
| 1933 | Check front matter page density in raw proof. | No page is dominated by accidental oversized heading style. |
| 1934 | Check Part I page density in raw proof. | Low/high ink pages are intentional. |
| 1935 | Check Part II page density in raw proof. | Security/control pages are readable. |
| 1936 | Check Part III page density in raw proof. | Memory/context pages are readable. |
| 1937 | Check Part IV page density in raw proof. | Tool/execution pages are readable. |
| 1938 | Check Part V page density in raw proof. | Trace/eval pages are readable. |
| 1939 | Check Part VI page density in raw proof. | Lifecycle pages are readable. |
| 1940 | Check Part VII page density in raw proof. | Runtime/launch pages are readable. |
| 1941 | Check appendices page density in raw proof. | Reference material is not over-compressed. |
| 1942 | Check Template2000n low-ink pages. | Low-ink pages are meaningful tails, not broken pages. |
| 1943 | Check Template2000n high-ink pages 232-242. | Dense lifecycle/assurance pages are readable. |
| 1944 | Check Template2000n pages 265-274. | Chapter 23 and glossary transition remain stable. |
| 1945 | Check Template2000n pages 299-302. | Low-density appendix pages contain intended text. |
| 1946 | Check Template2000n final page. | No trailing blank or clipped footer remains. |
| 1947 | Reconcile raw page count after H3 pass. | Page count change is explained by style, not missing content. |
| 1948 | Reconcile Template2000n page count after H3 pass. | Page count change is explained by style, not missing content. |
| 1949 | Verify text equality after style-only passes. | Paragraph texts match before/after style update when no content edit is intended. |
| 1950 | Refresh render QA JSON schema. | QA JSON includes raw/template pages, blanks, markers and style metrics. |
| 1951 | Update author-owned fields list. | All `[заполнить]` areas are explicit for the author. |
| 1952 | Fill `Об авторе` short version. | Author supplies real name, role and public positioning. |
| 1953 | Fill `Об авторе` extended version. | Author supplies verified experience and projects. |
| 1954 | Fill companion URL. | Public companion route is stable and versioned. |
| 1955 | Fill legal/compliance disclaimer. | Publisher-appropriate wording is present. |
| 1956 | Fill AI tooling disclosure. | Disclosure is factual and not over-explained. |
| 1957 | Fill acknowledgements or remove placeholder. | No placeholder remains in front matter. |
| 1958 | Confirm title/subtitle. | Final title wording is agreed for cover and metadata. |
| 1959 | Confirm cover copy. | Back-cover text matches the actual manuscript promise. |
| 1960 | Confirm author public links. | Links are current and intended for publication. |
| 1961 | Run front matter proofread. | Typos and placeholders are cleared. |
| 1962 | Run Part I proofread. | Opening chapters read as a sample-quality path. |
| 1963 | Run Part II proofread. | Security/control terminology is consistent. |
| 1964 | Run Part III proofread. | Memory/context terminology is consistent. |
| 1965 | Run Part IV proofread. | Tool/runtime terminology is consistent. |
| 1966 | Run Part V proofread. | Trace/eval/SLO terminology is consistent. |
| 1967 | Run Part VI proofread. | ADLC/assurance/registry wording is consistent. |
| 1968 | Run Part VII proofread. | Reference runtime and launch wording are consistent. |
| 1969 | Run appendices proofread. | Templates and companion routes are consistent. |
| 1970 | Normalize repeated chapter endings. | Endings are intentionally templated and not mechanical. |
| 1971 | Strengthen running case continuity. | Cases recur across parts without forced repetition. |
| 1972 | Check English term policy. | English remains only for stable engineering artifacts. |
| 1973 | Check glossary coverage. | Key terms used in chapters have glossary support. |
| 1974 | Check cross-references. | Chapter references and companion routes are accurate. |
| 1975 | Check source/bibliography scope. | Sources are curated for book use, not raw web exhaust. |
| 1976 | Check diagrams and captions. | All figures have print-safe captions or fallback prose. |
| 1977 | Check tables. | Tables are readable in both raw and Template2000n proofs. |
| 1978 | Check code-like blocks. | Long configs and CLI outputs are routed to companion. |
| 1979 | Check list formatting. | Lists do not create oversized bullets or false headings. |
| 1980 | Check quote and dash consistency. | Typography is consistent with publisher expectations. |
| 1981 | Check front matter metadata. | ISBN/imprint/editorial fields are either filled or explicitly absent. |
| 1982 | Check page starts for all parts. | Part openings do not orphan after preceding text. |
| 1983 | Check page starts for all chapters. | Chapter openings are readable and not clipped. |
| 1984 | Check glossary transition. | Chapter 23 to glossary transition remains stable. |
| 1985 | Check practical cases transition. | Glossary to cases transition remains stable. |
| 1986 | Check appendix 4 final route. | Source/companion explanation remains clear. |
| 1987 | Prepare editor note about style-only passes. | Editor understands what changed and what did not. |
| 1988 | Prepare publisher artifact inventory. | Raw DOCX, Template2000n DOCX, reports and QA JSON are listed. |
| 1989 | Prepare clean external packet. | Internal iteration reports are excluded unless requested. |
| 1990 | Re-run `git diff --check`. | Whitespace is clean. |
| 1991 | Re-run DOCX zip checks. | Raw and Template2000n DOCX archives are valid. |
| 1992 | Re-run JSON validation. | Render QA JSON parses. |
| 1993 | Re-run docs build. | `mkdocs build --strict` passes. |
| 1994 | Re-run test suite. | Repository tests pass. |
| 1995 | Re-export Google Doc after final author fields. | Final author text is reflected in raw DOCX. |
| 1996 | Rebuild Template2000n after final author fields. | Derived proof matches final manuscript text. |
| 1997 | Render final raw proof. | Final raw pages and blanks are recorded. |
| 1998 | Render final Template2000n proof. | Final Template2000n pages and blanks are recorded. |
| 1999 | Produce final author handoff report. | Author sees what changed, what remains and what to fill. |
| 2000 | Produce final publisher-ready tag decision. | Repo state is ready for tag/PR/release decision. |
