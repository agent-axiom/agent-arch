# Next 100 editorial goals after editor handoff pass

Date: 2026-06-28.

Status: backlog for preparing an excellent editorial manuscript.

Baseline:

- Google Doc: <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Raw proof: 552 pages, blank-like pages: 0.
- H1 outline is normalized after the 2026-06-28 handoff pass.
- Remaining major formatting risk: 629 long H2 paragraphs that likely should be body text.

## Goals 1801-1900

| # | Goal | Acceptance |
| ---: | --- | --- |
| 1801 | Build a complete heading inventory from the latest DOCX export. | Real H1/H2/H3 headings and body-like headings are separated. |
| 1802 | Define the target heading hierarchy for the book. | Front matter, parts, chapters, sections and subsections have explicit style rules. |
| 1803 | Create a Google Doc-safe H2 normalization plan. | No mass rewrite is attempted without index/range safeguards. |
| 1804 | Identify H2 body-like paragraphs in front matter. | Front matter prose is not polluted by heading styles. |
| 1805 | Identify H2 body-like paragraphs in Part I. | Chapters 1-3 keep only real structural H2/H3. |
| 1806 | Identify H2 body-like paragraphs in Part II. | Chapters 4-6 have a clean outline. |
| 1807 | Identify H2 body-like paragraphs in Part III. | Memory/retrieval chapters have readable hierarchy. |
| 1808 | Identify H2 body-like paragraphs in Part IV. | Execution/tooling chapters avoid accidental heading inflation. |
| 1809 | Identify H2 body-like paragraphs in Part V. | Trace/SLO/eval chapters keep evidence hierarchy clear. |
| 1810 | Identify H2 body-like paragraphs in Part VI. | Organization/ADLC/assurance chapters preserve section rhythm. |
| 1811 | Identify H2 body-like paragraphs in Part VII. | Runtime/launch chapters are clean enough for final style mapping. |
| 1812 | Run first targeted H2 cleanup batch in Google Doc. | A small, auditable range is fixed and verified by DOCX export. |
| 1813 | Run second targeted H2 cleanup batch in Google Doc. | Batch does not damage real section headings. |
| 1814 | Run third targeted H2 cleanup batch in Google Doc. | Page count and outline changes are recorded. |
| 1815 | Re-export raw DOCX after H2 cleanup. | New proof artifact is saved. |
| 1816 | Re-render raw DOCX after H2 cleanup. | Page count and blank-like pages are recorded. |
| 1817 | Rebuild Template2000n derivative after H2 cleanup. | Derived DOCX opens and preserves publisher styles. |
| 1818 | Render Template2000n derivative after H2 cleanup. | Page count, blank-like pages and key pages are recorded. |
| 1819 | Compare raw and Template2000n outlines. | No body paragraphs appear in automatic outline. |
| 1820 | Update render QA JSON for heading normalization. | Metrics include H1/H2/H3 counts and remaining debt. |
| 1821 | Review front matter as a sample opening. | Promise, reader profile and reading route are concise. |
| 1822 | Review `Об авторе` placeholder with the author. | Placeholder is either filled or clearly blocked. |
| 1823 | Prepare final author bio variants. | Short and long versions are ready for publisher editing. |
| 1824 | Prepare title/subtitle options. | Options are concise and aligned with book positioning. |
| 1825 | Prepare cover-copy draft. | Back-cover wording explains the book without hype. |
| 1826 | Review chapter 1 as primary sample chapter. | It has strong story, thesis and practical payoff. |
| 1827 | Review chapter 2 decision ladder. | Workflow/agent/coordinator/handoff distinctions are crisp. |
| 1828 | Review chapter 3 architecture bridge. | It prepares Part II without repeating the entire architecture. |
| 1829 | Review Part I transition. | Reader sees why platform/control matters before security chapters. |
| 1830 | Review chapter 4 trust-boundary framing. | Security is agent-specific, not generic. |
| 1831 | Review chapter 5 conceptual control model. | Identity, session, policy and capability do not duplicate chapter 22. |
| 1832 | Review chapter 6 tool gateway/audit structure. | Confirmation and audit stay operational, not schema-heavy. |
| 1833 | Review Part II transition. | Security/control naturally leads into memory and retrieval. |
| 1834 | Review chapter 7 memory risk story. | Failure modes are concrete enough for production readers. |
| 1835 | Review chapter 8 memory layers. | Schema-like details are moved or summarized. |
| 1836 | Review chapter 9 retrieval/compaction. | Retrieval policy and provenance are practical without overloading. |
| 1837 | Review Part III transition. | Memory/retrieval leads into execution and tools. |
| 1838 | Review chapter 10 execution model. | Tool catalog is framed as contract, not function list. |
| 1839 | Review chapter 11 sandbox and MCP. | MCP is treated as integration boundary, not connector catalog. |
| 1840 | Review chapter 12 idempotency and rollback. | Side-effect unknown and reconciliation are easy to apply. |
| 1841 | Review Part IV transition. | Runtime/tooling leads into evidence and evaluation. |
| 1842 | Review chapter 13 trace/event model. | It reads as evidence-chain chapter, not logging reference. |
| 1843 | Review chapter 14 SLO framing. | SLOs are tied to user harm, tool actions and regression gates. |
| 1844 | Review chapter 15 eval gates. | Evaluation material is deep but not a long evaluator manual. |
| 1845 | Review chapter 16 evidence chain. | Trace, eval, rollout and decision artifacts connect clearly. |
| 1846 | Review Part V transition. | Evidence naturally leads into organization and lifecycle. |
| 1847 | Review chapter 17 ownership model. | Platform/product/security responsibilities are explicit. |
| 1848 | Review chapter 18 golden paths. | Golden paths reduce unsafe agent sprawl with concrete examples. |
| 1849 | Review chapter 19 ADLC. | Lifecycle stages and artifacts are coherent without schema sprawl. |
| 1850 | Review chapter 20 after previous compression. | Assurance, incident, registry and retirement are balanced. |
| 1851 | Review chapter 20 incident terminology. | Finding, incident, near miss and postmortem remain distinct. |
| 1852 | Review chapter 20 retirement route. | Retirement is operational and not buried in registry detail. |
| 1853 | Review Part VI transition. | Organization/lifecycle leads into reference implementation and launch. |
| 1854 | Review chapter 21 runtime narrative. | It explains implementation shape without becoming CLI manual. |
| 1855 | Review chapter 22 policy/catalog runtime. | It stays implementation-focused and does not re-teach chapter 5. |
| 1856 | Review chapter 23 launch decision. | Final chapter feels like climax, not appendix preview. |
| 1857 | Review glossary. | Terms match usage across the manuscript. |
| 1858 | Review practical cases. | Cases are concrete, balanced and aligned with the architecture. |
| 1859 | Review appendices. | Appendices are working aids, not duplicated chapters. |
| 1860 | Normalize repeated chapter endings. | Mechanical `Что делать дальше` blocks are merged or renamed. |
| 1861 | Strengthen running support-triage case. | Each part references a consistent production system. |
| 1862 | Add case reminders to part openings where useful. | Reminders are short and do not feel repetitive. |
| 1863 | Audit all companion references. | Each route points to a real or planned companion file. |
| 1864 | Fill capability contract companion template. | Template can be used by a reader after minor adaptation. |
| 1865 | Fill release decision record companion template. | Template captures eval, trace, rollout and risk acceptance. |
| 1866 | Fill incident record companion template. | Template links trace, change, rollout and containment. |
| 1867 | Expand production readiness checklist. | Checklist matches chapter 23 and avoids false compliance claims. |
| 1868 | Add assurance review packet template. | Chapter 20 companion route becomes actionable. |
| 1869 | Add finding record template. | Finding taxonomy is reusable outside the book. |
| 1870 | Add retirement plan template. | Retirement is visible as an engineering process. |
| 1871 | Add registry entry template. | Registry fields align with lifecycle and policy enforcement. |
| 1872 | Add eval dataset skeleton. | Dataset structure supports prompt injection and tool misuse tests. |
| 1873 | Add trace example skeleton. | Good run, denied action and incident run are represented. |
| 1874 | Add source/date policy to companion. | Fast-changing references carry date/version discipline. |
| 1875 | Add errata process details. | Readers know where and how to report corrections. |
| 1876 | Add companion changelog release placeholder. | `v1.0-book` can be cut when the book ships. |
| 1877 | Audit OpenAI/provider-specific claims. | Current product facts are either verified or generalized. |
| 1878 | Audit security-standard references. | Standards are cited as context, not as certification guarantees. |
| 1879 | Audit MCP statements. | Protocol/boundary claims are accurate and not over-specific. |
| 1880 | Audit legal/compliance language. | Book avoids giving legal advice through templates. |
| 1881 | Prepare AI-use disclosure draft. | Disclosure is factual and publisher-editable. |
| 1882 | Prepare author case-study decision list. | Author knows which real/composite cases to approve. |
| 1883 | Prepare acknowledgements placeholder. | No accidental omissions or unauthorized names. |
| 1884 | Check all `[заполнить]` markers. | Remaining placeholders are intentional and listed. |
| 1885 | Check all English-heavy headings. | English remains only where it names stable engineering artifacts. |
| 1886 | Check terminology consistency for capability/tool/action. | Terms do not collapse into each other. |
| 1887 | Check terminology consistency for policy/verifier/guardrail. | Runtime boundaries stay explicit. |
| 1888 | Check terminology consistency for trace/span/event. | Observability language is stable. |
| 1889 | Check terminology consistency for rollout/canary/gate. | Release language is stable. |
| 1890 | Check terminology consistency for assurance/finding/incident. | Operational review language is stable. |
| 1891 | Run full raw DOCX export after all edits. | Artifact path and revision are recorded. |
| 1892 | Run full raw render QA after all edits. | Pages and blank-like pages are recorded. |
| 1893 | Run full Template2000n derivative after all edits. | Derived proof passes zip integrity. |
| 1894 | Run full Template2000n render QA after all edits. | Pages and blank-like pages are recorded. |
| 1895 | Review title page and final page. | No orphan title artifact or trailing blank page remains. |
| 1896 | Update submission checklist. | All remaining blockers are current and specific. |
| 1897 | Update editor handoff packet. | Packet reflects latest proof and author fields. |
| 1898 | Run repository tests. | Test result is recorded. |
| 1899 | Run strict docs build. | Build result and known warnings are recorded. |
| 1900 | Decide final editor/publisher readiness. | Manuscript is marked ready, almost ready or blocked with named reasons. |

## Author-owned inputs to collect

- Final author bio and public links.
- Final title/subtitle/cover copy.
- Public companion URL and release version.
- AI-use disclosure wording.
- Legal/compliance limitations.
- Real/composite case-study approvals.
- Acknowledgements.
