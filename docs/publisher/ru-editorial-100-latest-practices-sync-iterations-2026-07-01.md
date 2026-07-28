# 100 editorial goals for latest-practices manuscript sync

Date: 2026-07-01.

Context:

- The late-practices sync pass added 13 source practice sections to
  `docs/publisher/ru-manuscript-full.md`.
- The full Google Doc manuscript received eight missing print-oriented
  practice blocks and readback confirms each new heading exactly once.
- Final publisher-ready DOCX is still blocked by author-owned fields,
  publisher style application, export QA and external proofread.

| # | Goal | Done when |
| --- | --- | --- |
| 2701 | Re-read all inserted practice blocks in local manuscript. | Each block fits its chapter and has no duplicate heading. |
| 2702 | Compare local full practice blocks with Google Doc print blocks. | Intent and artifacts match despite different length. |
| 2703 | Normalize trace-practice terminology. | trace, span, event, evidence and eval terms are consistent. |
| 2704 | Normalize SLO-practice terminology. | SLI, SLO, error budget and action wording is consistent. |
| 2705 | Normalize eval-practice terminology. | regression gate, verdict, override and hard blocker wording is consistent. |
| 2706 | Normalize ownership-practice terminology. | owner, decision owner, role owner and escalation contact are distinct. |
| 2707 | Normalize golden-path terminology. | golden path, common gateway and exception wording is stable. |
| 2708 | Normalize runtime-practice terminology. | runtime skeleton, run context and rollout controls are distinct. |
| 2709 | Normalize policy/catalog practice terminology. | capability contract, policy decision and catalog lifecycle are aligned. |
| 2710 | Normalize launch-practice terminology. | containment, rollout wave, freeze and rollback are used consistently. |
| 2711 | Check chapter 13 practice placement. | Trace practice appears before readiness/checklist material. |
| 2712 | Check chapter 14 practice placement. | SLO practice appears before SLO readiness material. |
| 2713 | Check chapter 15 practice placement. | Eval practice appears before eval readiness material. |
| 2714 | Check chapter 17 practice placement. | Ownership practice appears before artifact ownership detail. |
| 2715 | Check chapter 18 practice placement. | Golden-path practice appears before gateway discussion. |
| 2716 | Check chapter 21 practice placement. | Runtime skeleton practice appears before chapter conclusion. |
| 2717 | Check chapter 22 practice placement. | Policy/catalog practice appears before launch-transition material. |
| 2718 | Check chapter 23 practice placement. | Launch-chain practice appears before trace evidence discussion. |
| 2719 | Review local heading demotion. | Inserted headings match publisher hierarchy. |
| 2720 | Review Google Doc paragraph rhythm. | Practice blocks read as book prose, not pasted notes. |
| 2721 | Verify no raw companion payload bloat in Google Doc. | Long schemas stay in companion routes. |
| 2722 | Verify local manuscript keeps full source detail. | `ru-manuscript-full.md` remains the complete source assembly. |
| 2723 | Add cross-reference from trace practice to eval practice. | Reader sees how trace review becomes regression evidence. |
| 2724 | Add cross-reference from SLO practice to rollout decisions. | SLO breach action is visible. |
| 2725 | Add cross-reference from ownership practice to ADLC. | Owner map is connected to lifecycle change. |
| 2726 | Add cross-reference from golden path to runtime skeleton. | Standard path leads into reference runtime. |
| 2727 | Add cross-reference from policy/catalog to launch checklist. | Capability control leads to release control. |
| 2728 | Check first-person/second-person balance in practices. | Instructional voice remains consistent. |
| 2729 | Check Russian/English term mix in practices. | English terms are stable names, not random jargon. |
| 2730 | Check examples for support-ticket continuity. | Duplicate-ticket/write-path case remains coherent. |
| 2731 | Check examples for knowledge-assistant continuity. | Read-only/retrieval case remains coherent. |
| 2732 | Check examples for incident-coordination continuity. | Incident case remains coherent. |
| 2733 | Review lists for print readability. | Long lists are split or converted to prose where needed. |
| 2734 | Review code-font density. | Inline code is used only for identifiers and fields. |
| 2735 | Review arrow notation. | `->` chains are readable and do not overload headings. |
| 2736 | Review table candidates. | Only true comparison material remains table-shaped. |
| 2737 | Review companion boundaries. | Full YAML, CLI and payload details are routed out of print flow. |
| 2738 | Verify author-owned gaps after practice sync. | No new placeholder is introduced beyond known author fields. |
| 2739 | Re-run placeholder scan. | `[заполнить]` hits are known and intentional. |
| 2740 | Re-run TODO/FIXME/TBD scan. | No accidental editorial marker remains. |
| 2741 | Re-run control heading matrix. | `docs/book`, local full and Google Doc status are recorded. |
| 2742 | Update source-map notes if chapter placement changes. | Source map remains enough for future sync. |
| 2743 | Update manuscript evolution ledger. | This pass is discoverable by date. |
| 2744 | Update Google Doc workflow. | This pass is visible in workflow history. |
| 2745 | Update sendable packet state. | Editor packet points to current Google Doc and sync report. |
| 2746 | Update roadmap workstream status. | Practical-content sync is not confused with final export. |
| 2747 | Re-check Google Doc readback after any follow-up edit. | Eight late practice headings still appear once. |
| 2748 | Re-check local full manuscript after any follow-up edit. | Thirteen practice headings still appear once. |
| 2749 | Prepare DOCX export after author fields. | Export is delayed until author data is resolved. |
| 2750 | Prepare Template2000n rerun after author fields. | Template proof route is ready but not run prematurely. |
| 2751 | Review trace practice against source chapter. | No essential investigation step was lost in print block. |
| 2752 | Review SLO practice against source chapter. | SLO map preserves owner/action/evidence logic. |
| 2753 | Review eval practice against source chapter. | Regression gate preserves verdict and blocker logic. |
| 2754 | Review ownership practice against source chapter. | Owner map preserves platform/product/security split. |
| 2755 | Review golden path practice against source chapter. | Write-agent path preserves gateway and approval logic. |
| 2756 | Review runtime practice against source chapter. | Runtime skeleton preserves launch-readiness logic. |
| 2757 | Review policy/catalog practice against source chapter. | Capability-to-SLO/eval/golden-path links are preserved. |
| 2758 | Review launch practice against source chapter. | Trace/eval/rollout/containment chain is preserved. |
| 2759 | Verify no contradictory page-count claims. | Reports distinguish word/export metrics from DOCX pages. |
| 2760 | Verify Google Doc URL consistency. | All current packet files use the same full manuscript link. |
| 2761 | Verify final revision recording. | Latest Google Doc revision is recorded in sync report. |
| 2762 | Verify old compressed doc is not referenced as current. | Stale staging docs remain excluded. |
| 2763 | Check practice headings in document outline manually. | Real headings are usable for editor navigation. |
| 2764 | Check inserted Google Doc blocks for style pollution. | No long body paragraph is styled as an inappropriate heading. |
| 2765 | Check local line length in new report. | Markdown stays readable in diffs. |
| 2766 | Check source-control cleanliness. | Only intended publisher manuscript files are staged. |
| 2767 | Run `git diff --check`. | No whitespace errors. |
| 2768 | Run focused docs tests. | Publisher/document surface tests pass or blockers are recorded. |
| 2769 | Run full docs build if feasible. | MkDocs strict build passes or known non-content blocker is recorded. |
| 2770 | Record verification commands. | Final report lists what was run. |
| 2771 | Prepare author-fill checklist. | Author-owned fields are listed plainly. |
| 2772 | Prepare editor note about practice sync. | Editor can see what changed since last proof. |
| 2773 | Prepare companion note about full YAML. | Editor understands why Google Doc has compact practice blocks. |
| 2774 | Review final cover-note implications. | Cover note does not claim final publisher DOCX is ready. |
| 2775 | Review final packet include list. | Sync report is included; iteration logs stay excluded. |
| 2776 | Confirm no new source claims require live web check. | New practice blocks rely on internal architecture, not new external facts. |
| 2777 | Confirm no invented author facts. | Bio/byline placeholders remain author-owned. |
| 2778 | Confirm no fake companion URL. | Companion metadata stays placeholder until author confirms. |
| 2779 | Confirm legal disclaimer remains unresolved. | Legal/compliance wording is not invented. |
| 2780 | Confirm acknowledgements remain unresolved. | Personal acknowledgements are not invented. |
| 2781 | Check glossary pressure from new practices. | New terms are already defined or need glossary follow-up. |
| 2782 | Check appendix alignment. | Companion/source appendix routes still match the body. |
| 2783 | Check internal references to chapter numbers. | Late practice insertion did not make references stale. |
| 2784 | Check numbering around practice sections. | Adjacent section numbers remain understandable in Google Doc. |
| 2785 | Check repeated practice titles. | No duplicate practice block exists after sync. |
| 2786 | Check for accidental English-only headings. | Mixed-language headings are intentional and understandable. |
| 2787 | Check publisher-facing status wording. | Status remains "working manuscript", not final submission. |
| 2788 | Check editor-facing risk register. | Open risks are author fields, proofread, style and export QA. |
| 2789 | Check diff size explanation. | Large local insertion is explained by 13 source sections. |
| 2790 | Check Google Doc export volume trend. | Word count increase is recorded without claiming final pages. |
| 2791 | Check old proof artifact relevance. | 2026-06-28 DOCX proofs are marked stale after content sync. |
| 2792 | Plan fresh proof after author data. | New proof is scheduled only after author fields. |
| 2793 | Plan external proofread scope. | Proofread should include newly inserted practices. |
| 2794 | Plan publisher style pass scope. | Style pass should include practice blocks and list rhythm. |
| 2795 | Plan source-to-Google sync audit. | Future audit compares all practice headings again. |
| 2796 | Plan final export gate. | Final gate requires author data, style pass, DOCX export and render QA. |
| 2797 | Plan editor handoff note. | Handoff note explains full local vs compact Google Doc practice treatment. |
| 2798 | Plan errata/companion update. | Companion should receive full YAML/examples for practice blocks. |
| 2799 | Plan final repository push. | Branch contains sync report, manuscript update and workflow records. |
| 2800 | Decide readiness after practice sync. | Manuscript is stronger for editor review but still not final publisher DOCX. |

