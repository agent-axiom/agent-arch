# Next 100 quality-sync and export iterations

Date: 2026-07-04.

Status: next-goal ledger after Google Doc terminology cleanup, Template2000n
quality-sync rebuild and render QA. Goals 3801-3900 continue after the
3701-3800 editorial quality ledger.

| # | Goal | Done when |
| --- | --- | --- |
| 3801 | Re-export raw DOCX from the updated Google Doc. | Fresh post-terminology raw DOCX exists locally. |
| 3802 | Verify fresh raw DOCX archive integrity. | `unzip -t` passes for the fresh raw export. |
| 3803 | Rebuild Template2000n from the fresh raw DOCX. | New styled DOCX exists and is dated. |
| 3804 | Compare fresh raw/styled paragraph text. | Text equality passes or intentional deltas are documented. |
| 3805 | Render the fresh raw DOCX. | Page count and blank-like page list are recorded. |
| 3806 | Render the fresh Template2000n DOCX. | Page count and blank-like page list are recorded. |
| 3807 | Visually inspect raw first/final pages. | No clipping, overlap or accidental blank page is visible. |
| 3808 | Visually inspect Template2000n first/final pages. | Styled opening and ending are readable. |
| 3809 | Inspect lowest-density raw pages. | Sparse pages are intentional and not broken layout. |
| 3810 | Inspect lowest-density styled pages. | Sparse styled pages are intentional and not broken layout. |
| 3811 | Re-run exact old-anglicism scan in Google Doc. | `online companion`, `policy gateway`, `tool gateway`, `incident response` stay absent except deliberate code/quote contexts. |
| 3812 | Scan local Markdown for excessive prose anglicisms. | Remaining English terms are code, protocol names or accepted terms. |
| 3813 | Review `workflow` usage in prose. | Prose uses `рабочий процесс` unless contrasting with a named artifact. |
| 3814 | Review `rollout` usage in prose. | Prose uses `поэтапный выпуск` unless code/CLI requires English. |
| 3815 | Review `runtime` usage in prose. | Prose uses `среда исполнения` unless discussing package names. |
| 3816 | Review `tool` usage in prose. | Prose uses `инструмент` unless code/field names require English. |
| 3817 | Review `policy` usage in prose. | Prose uses `политика` or `слой политик` unless code fields require English. |
| 3818 | Review `prompt` usage in prose. | Prose uses `промпт` or `подсказка` consistently. |
| 3819 | Review `companion` usage in prose. | Prose uses `сопроводительные материалы` or `онлайн-сопровождение`. |
| 3820 | Update terminology report after scan. | `ru-terminology.md` reflects the accepted Russian forms. |
| 3821 | Reconcile Google Doc after terminology update with `ru-manuscript-full.md`. | Deltas are copied back or explicitly documented. |
| 3822 | Reconcile front matter terminology. | Opening pages use the same Russian terms in Doc and source. |
| 3823 | Reconcile chapter 20 terminology. | Lifecycle chapter terms match the terminology table. |
| 3824 | Reconcile chapter 21 terminology. | Runtime chapter terms match the terminology table. |
| 3825 | Reconcile appendix terminology. | Appendices do not reintroduce stale English editorial labels. |
| 3826 | Update manuscript map current proof section. | Map points only to current artifacts. |
| 3827 | Update submission checklist current status. | Checklist shows current blocker state. |
| 3828 | Update Google Doc workflow notes. | Workflow notes reflect post-terminology export requirement. |
| 3829 | Update evolution ledger. | Ledger records the quality-sync pass. |
| 3830 | Update source map notes. | Source map records terminology cleanup and sync rule. |
| 3831 | Review title page after styled export. | Title page is readable and not over-styled. |
| 3832 | Review annotation page after styled export. | Annotation remains compact and readable. |
| 3833 | Review `Что получит читатель` block. | Bullets fit and do not create awkward spacing. |
| 3834 | Review keywords block. | Keywords balance Russian and accepted English terms. |
| 3835 | Review terminology agreement block. | It does not look like a raw glossary dump. |
| 3836 | Review author placeholder block. | All author-owned placeholders are visible and isolated. |
| 3837 | Review companion metadata block. | Placeholder route is explicit and not misleading. |
| 3838 | Review legal/disclosure placeholders. | The publisher can see what must be supplied. |
| 3839 | Review cover-copy placeholders. | Marketing metadata is not confused with body text. |
| 3840 | Review table of contents exposure. | Body paragraphs do not leak into the outline. |
| 3841 | Inspect Chapter 1 styled pages. | Opening chapter rhythm remains strong. |
| 3842 | Inspect Chapter 2 styled pages. | Decision ladder reads clearly. |
| 3843 | Inspect Chapter 3 styled pages. | Reference architecture diagram/context is readable. |
| 3844 | Inspect Chapter 4 styled pages. | Security boundary explanation is not fragmented. |
| 3845 | Inspect Chapter 5 styled pages. | Identity/policy terms are consistent. |
| 3846 | Inspect Chapter 6 styled pages. | Tool gateway examples render cleanly. |
| 3847 | Inspect Chapter 7 styled pages. | Memory risk framing is readable. |
| 3848 | Inspect Chapter 8 styled pages. | Memory taxonomy does not turn into a field dump. |
| 3849 | Inspect Chapter 9 styled pages. | Retrieval/context material remains book-like. |
| 3850 | Inspect Chapter 10 styled pages. | Evaluation gates and traces render without oversized lists. |
| 3851 | Inspect Chapter 11 styled pages. | Sandbox/MCP material stays readable. |
| 3852 | Inspect Chapter 12 styled pages. | Checklists fit the page. |
| 3853 | Inspect Chapter 13 styled pages. | Trace/evidence chapter is coherent. |
| 3854 | Inspect Chapter 14 styled pages. | SLO material has stable page rhythm. |
| 3855 | Inspect Chapter 15 styled pages. | Eval gates do not become a schema catalog. |
| 3856 | Inspect Chapter 16 styled pages. | Evidence chain tables/examples are readable. |
| 3857 | Inspect Chapter 17 styled pages. | Ownership chapter has clear role language. |
| 3858 | Inspect Chapter 18 styled pages. | Organizational model is not too abstract. |
| 3859 | Inspect Chapter 19 styled pages. | ADLC chapter keeps lifecycle sequence clear. |
| 3860 | Inspect Chapter 20 styled pages. | Assurance/retirement transition is readable. |
| 3861 | Inspect Chapter 21 styled pages. | Reference runtime material is book-readable. |
| 3862 | Inspect Chapter 22 styled pages. | Policy catalog chapter is not overloaded. |
| 3863 | Inspect Chapter 23 styled pages. | Launch checklist closes the book cleanly. |
| 3864 | Inspect glossary styled pages. | Terms and definitions fit without awkward breaks. |
| 3865 | Inspect practical cases styled pages. | Cases read as examples, not raw logs. |
| 3866 | Inspect appendices styled pages. | Appendix boundaries are visible. |
| 3867 | Inspect code-heavy pages. | Code/listing pages do not overflow. |
| 3868 | Inspect table-heavy pages. | Tables fit or are marked for redesign. |
| 3869 | Inspect sparse pages. | Sparse pages are intentional or fixed. |
| 3870 | Inspect final 20 styled pages. | Ending has no accidental blank or orphan content. |
| 3871 | Collect author public byline. | Final byline is provided by author. |
| 3872 | Collect short author bio. | Short bio is provided or intentionally omitted. |
| 3873 | Collect long author bio. | Long bio is provided or intentionally omitted. |
| 3874 | Collect public role/positioning. | Role wording is approved by author. |
| 3875 | Collect verified experience claims. | Claims are factual and author-approved. |
| 3876 | Collect public project links. | Links are approved and reachable. |
| 3877 | Collect acknowledgements. | Acknowledgements are supplied or omitted. |
| 3878 | Collect companion URL. | Public support/companion route is known. |
| 3879 | Collect errata/changelog route. | Publisher-facing update route is defined. |
| 3880 | Collect legal/disclosure wording. | Required wording is supplied by author/publisher. |
| 3881 | Run final placeholder scan. | Only intentionally unresolved placeholders remain. |
| 3882 | Run final URL scan. | Links are reachable or marked for publisher handling. |
| 3883 | Run final source-claim scan. | Fast-moving claims have current evidence. |
| 3884 | Run final cross-reference scan. | Chapter and appendix references resolve. |
| 3885 | Run final glossary consistency scan. | Glossary terms match body usage. |
| 3886 | Run final code/listing label scan. | Listing numbers and captions are consistent. |
| 3887 | Run final figure/table label scan. | Figure/table references are consistent. |
| 3888 | Run final duplicate heading scan. | Duplicate headings are intentional or fixed. |
| 3889 | Run final TOC sanity check. | TOC contains only real structural headings. |
| 3890 | Run final whitespace check. | `git diff --check` passes. |
| 3891 | Prepare external proofread package. | Editor receives current Google Doc and proof DOCX paths. |
| 3892 | Record external proofread instructions. | Editor sees what kind of review is requested. |
| 3893 | Triage proofreader comments. | Every comment is accepted, rejected or deferred. |
| 3894 | Apply accepted proofread edits to Google Doc. | Accepted edits are present in the manuscript. |
| 3895 | Backport accepted proofread edits to Markdown. | Source and Google Doc agree. |
| 3896 | Re-export raw DOCX after proofread edits. | Fresh raw proof exists. |
| 3897 | Rebuild Template2000n after proofread edits. | Fresh styled proof exists. |
| 3898 | Re-run render QA after proofread edits. | Page counts and blank checks are recorded. |
| 3899 | Freeze final editor-review checkpoint. | Commit/tag/report identify exact artifacts. |
| 3900 | Prepare author-facing final report. | Report lists results, blockers and author-owned fields. |
