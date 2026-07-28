# Next 100 visual/edit manuscript iterations

Date: 2026-07-05.

Scope: goals `4001-4100` for turning the current Google Doc visual/edit proof
and Template2000n derivative into a stronger editor-ready publisher manuscript.

| # | Goal | Done when |
|---:|---|---|
| 4001 | Freeze the current visual/edit Google Doc revision. | Revision ID is recorded in the handoff note and QA JSON. |
| 4002 | Preserve the fresh visual/edit raw DOCX export. | Raw DOCX path, hash, size and page count are recorded. |
| 4003 | Preserve the visual/edit Template2000n proof. | Styled DOCX path, hash, size and page count are recorded. |
| 4004 | Record the 12 embedded diagrams. | Raw and styled DOCX media counts both show 12 PNG files. |
| 4005 | Verify text equality after Template2000n build. | Styled derivative reports `text_equality=true`. |
| 4006 | Verify long reference excerpts are compressed. | No paragraph in raw or styled DOCX is 250+ words. |
| 4007 | Verify broken cross-reference markers remain absent. | Old Chapter 18/Chapter 2 markers are zero in source. |
| 4008 | Verify broken inflection markers remain absent. | `набор оценкиs`, `проверочный списокs` and similar forms are zero. |
| 4009 | Verify render output for raw DOCX. | Raw render has 501 pages and no blank-like pages. |
| 4010 | Verify render output for Template2000n DOCX. | Styled render has 366 pages and no blank-like pages. |
| 4011 | Spot-check the first raw page. | Title, annotation and opening matter are readable. |
| 4012 | Spot-check the first styled page. | Template typography keeps opening matter readable. |
| 4013 | Spot-check the final raw visualization page. | Final figure, caption and alt text render correctly. |
| 4014 | Spot-check the final styled visualization page. | Final figure, caption and alt text render correctly. |
| 4015 | Check all visualization captions. | Captions use one numbering style and Russian labels. |
| 4016 | Check all visualization alt text. | Alt descriptions are useful and not duplicates of captions. |
| 4017 | Decide figure placement strategy for layout. | Editor note says which figures move from appendix block into chapters. |
| 4018 | Check figure-page density. | No figure page is overloaded after relocation. |
| 4019 | Check figure references in nearby prose. | Every figure has a reason to exist in the chapter. |
| 4020 | Check visual terminology. | Diagram labels match body terminology and glossary. |
| 4021 | Review the opening promise after visual additions. | Annotation and preface reflect the visual/editorial proof state. |
| 4022 | Review the terminology agreement. | Accepted English terms are justified and not decorative. |
| 4023 | Review `production` usage. | Plain prose uses `промышленная эксплуатация` unless English is deliberate. |
| 4024 | Review `review` usage. | Ordinary review/proofread wording is localized where clearer. |
| 4025 | Review `owner` usage. | Owner/accountability wording is clear in Russian context. |
| 4026 | Review `runtime` usage. | Runtime remains only where it names the execution layer. |
| 4027 | Review `prompt` usage. | Prompt remains only where it is the technical object. |
| 4028 | Review `payload` usage. | Payload remains only where artifact-specific. |
| 4029 | Review `dataset` usage. | Dataset remains only where artifact-specific. |
| 4030 | Review `rollout` usage. | Rollout remains a declared term or becomes `поэтапный выпуск`. |
| 4031 | Review `gate` usage. | Gate is either a term with explanation or localized. |
| 4032 | Review `trace` usage. | Trace is consistent with evidence-chain chapters. |
| 4033 | Review `verifier` usage. | Verifier is explained before repeated use. |
| 4034 | Review `capability` usage. | Capability remains a declared contract term. |
| 4035 | Record terminology exceptions for the editor. | Exceptions list is concise and tied to the terminology agreement. |
| 4036 | Re-read Part I with the book-map figure in mind. | Conceptual ramp matches the figure route. |
| 4037 | Re-read Part II with trust-boundary figures in mind. | Policy/tool/approval chapters align with diagrams. |
| 4038 | Re-read Part III with sandbox/MCP figure in mind. | Runtime boundary text has no missing prerequisites. |
| 4039 | Re-read Part IV with memory/retrieval figure in mind. | Memory claims are bounded and operational. |
| 4040 | Re-read Part V with evidence-chain figure in mind. | Trace/eval/SLO sections reinforce one another. |
| 4041 | Re-read Part VI with ADLC figure in mind. | Lifecycle, assurance and incident text form one process. |
| 4042 | Re-read Part VII with launch-readiness figure in mind. | Launch checklist matches the readiness signals. |
| 4043 | Re-read appendices after companion compression. | Appendices guide readers without becoming a full reference dump. |
| 4044 | Check transitions between parts. | Each part explains why the next part follows. |
| 4045 | Check repeated chapter openings. | Openings are problem-driven, not generic. |
| 4046 | Check repeated chapter endings. | Endings give next action without formulaic repetition. |
| 4047 | Check running support case continuity. | The canonical support-ticket case remains consistent. |
| 4048 | Check knowledge-agent case continuity. | Knowledge-agent examples do not contradict support case logic. |
| 4049 | Check high-risk capability examples. | Examples consistently include owner, policy and evidence. |
| 4050 | Check low-risk capability examples. | Examples do not overstate required ceremony. |
| 4051 | Check human-confirmation examples. | Approval/human-in-the-loop wording is precise. |
| 4052 | Check incident examples. | Incidents show detection, containment, recovery and learning. |
| 4053 | Check retirement examples. | Decommissioning text includes owner and replacement route. |
| 4054 | Check SLO examples. | Error budgets and segmentation are explained with consequences. |
| 4055 | Check eval examples. | Evaluation gates are tied to release decisions. |
| 4056 | Check trace examples. | Evidence chain remains auditable and not merely illustrative. |
| 4057 | Check memory examples. | Memory entries include trust, source, provenance and revision. |
| 4058 | Check retrieval examples. | Retrieval boundaries avoid accidental tenant/source mixing. |
| 4059 | Check sandbox examples. | Sandbox claims match actual enforcement points. |
| 4060 | Check MCP examples. | MCP is described as a boundary, not as automatic safety. |
| 4061 | Recheck source-map agreement. | Source map reflects the current visual/edit proof. |
| 4062 | Recheck manuscript-map agreement. | Manuscript map includes current DOCX/page-count state. |
| 4063 | Recheck workflow agreement. | Google Doc/DOCX policy describes the latest proof pair. |
| 4064 | Recheck submission checklist. | Checklist no longer says fresh export is missing. |
| 4065 | Recheck companion file references. | Companion route points to the new CLI/API reference file. |
| 4066 | Recheck artifact paths. | All report paths resolve in the repository. |
| 4067 | Recheck generated image paths. | All 12 PNG files are committed and referenced. |
| 4068 | Recheck DOCX artifact paths. | Raw and Template2000n DOCX files are committed. |
| 4069 | Recheck metrics paths. | Metrics JSON files are committed. |
| 4070 | Recheck untracked noise. | Unrelated old artifacts are not staged accidentally. |
| 4071 | Re-run fast-moving platform claim review. | Provider/API/security claims are current or generalized. |
| 4072 | Re-run security standard source review. | NIST/OWASP/CISA references are still accurate. |
| 4073 | Re-run Air Canada case wording review. | Case remains tied to the official source. |
| 4074 | Re-run Anthropic/OpenAI wording review. | Vendor examples are scoped and not overstated. |
| 4075 | Re-run LangGraph/LangChain wording review. | Framework examples are current enough for print. |
| 4076 | Re-run Microsoft/Google/GitHub wording review. | Platform examples are accurate and not promotional. |
| 4077 | Re-run MLCommons reference review. | Benchmark references are not used beyond evidence. |
| 4078 | Re-run OpenReview demotion review. | Non-primary leads remain out of primary evidence. |
| 4079 | Re-run URL stability review. | Fragile URLs are moved to companion where possible. |
| 4080 | Record source risks for editor. | Remaining source risks are explicit and actionable. |
| 4081 | Collect public author name. | Byline is filled and author-approved. |
| 4082 | Collect short author bio. | Short bio is factual and publisher-ready. |
| 4083 | Collect long author bio. | Long bio is factual and not inflated. |
| 4084 | Collect author role line. | Role/public positioning is approved. |
| 4085 | Collect verified experience claims. | Claims are backed by public facts or softened. |
| 4086 | Collect public project links. | GitHub/site/blog/profile links are correct. |
| 4087 | Collect online-support public URL. | Placeholder in the manuscript is replaced. |
| 4088 | Collect online-support version route. | `v1.0-book`, changelog and errata route are defined. |
| 4089 | Collect acknowledgements decision. | Block is filled or explicitly removed. |
| 4090 | Collect legal disclaimer wording. | Publisher-required disclaimer is inserted or marked N/A. |
| 4091 | Collect AI-use disclosure wording. | Disclosure is inserted or marked N/A. |
| 4092 | Collect final title and subtitle. | Metadata matches publisher agreement. |
| 4093 | Collect cover copy. | Cover copy is author/publisher-approved. |
| 4094 | Collect imprint metadata. | Imprint fields are complete. |
| 4095 | Apply author-owned fields to Google Doc. | No accidental author placeholders remain. |
| 4096 | Backport author-owned fields to repository. | Markdown source agrees with Google Doc where appropriate. |
| 4097 | Run post-author raw DOCX export. | Fresh raw DOCX exists after author fields. |
| 4098 | Run post-author Template2000n build and render QA. | Styled DOCX and render metrics exist after author fields. |
| 4099 | Send external proofread/editor package. | Editor receives Google Doc, raw DOCX, Template2000n DOCX and report. |
| 4100 | Freeze final pre-submission checkpoint. | Commit/tag/report identify exact final artifacts and remaining decisions. |
