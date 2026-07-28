# Next 100 post-terminology export iterations

Date: 2026-07-04.

Scope: goals `3901-4000` for turning the current Google Doc and
Template2000n proof into an editor-ready publisher manuscript after the fresh
post-terminology DOCX export.

| # | Goal | Done when |
|---:|---|---|
| 3901 | Freeze the current Google Doc revision for editor reference. | Revision ID is recorded in the handoff note. |
| 3902 | Preserve the fresh raw DOCX export. | Raw DOCX path, hash and page count are recorded. |
| 3903 | Preserve the Template2000n proof. | Styled DOCX path, hash and page count are recorded. |
| 3904 | Store render QA metadata. | JSON contains raw and styled render metrics. |
| 3905 | Recheck raw/styled text equality. | Template2000n derivative has no text loss. |
| 3906 | Recheck bad terminology markers. | Known broken markers remain at zero. |
| 3907 | Spot-check lowest-density raw pages. | Each low-density page has intentional content. |
| 3908 | Spot-check lowest-density styled pages. | Each low-density page has intentional content. |
| 3909 | Check opening matter visually. | Title, annotation, keywords and bio block render cleanly. |
| 3910 | Check final appendix visually. | Online-support appendix renders cleanly. |
| 3911 | Check all H1 pages. | Part/chapter starts are present and not clipped. |
| 3912 | Check all H2-heavy chapters. | Dense heading areas do not become accidental TOC noise. |
| 3913 | Check code-heavy pages. | Listings fit the page or are marked for companion. |
| 3914 | Check checklist-heavy pages. | Long lists remain readable in styled proof. |
| 3915 | Check table-like text. | Pseudo-tables are readable or moved to companion. |
| 3916 | Check page-count delta. | Raw/styled page delta is explained by styles. |
| 3917 | Check artifact hashes. | Hashes match committed files. |
| 3918 | Check DOCX archive integrity. | `unzip -t` passes for both DOCX files. |
| 3919 | Check report links. | Report paths and Google Doc URL resolve. |
| 3920 | Mark export blocker closed. | Workflow and checklist no longer list fresh export as open. |
| 3921 | Review accepted English technical terms. | Terms kept in English are justified by terminology note. |
| 3922 | Review `companion` leftovers outside paths. | Remaining uses are intentional or translated. |
| 3923 | Review `rollout` leftovers in prose. | Remaining uses are accepted terms or localized. |
| 3924 | Review `production` usage. | Prose usage is intentional and not decorative. |
| 3925 | Review `workflow` usage. | Ordinary prose uses Russian wording where better. |
| 3926 | Review `gate` usage. | Gate as concept is consistent with Russian explanation. |
| 3927 | Review `trace` usage. | Trace remains consistent as a term. |
| 3928 | Review `verifier` usage. | Verifier is explained and not used as empty jargon. |
| 3929 | Review `payload` usage. | Payload remains only where artifact-specific. |
| 3930 | Review `dataset` usage. | Dataset remains only where artifact-specific. |
| 3931 | Review `runtime` usage. | Runtime remains where it names the execution layer. |
| 3932 | Review `sandbox` usage. | Sandbox/MCP references stay technically precise. |
| 3933 | Review `approval` usage. | Approval terms align with confirmation/approval model. |
| 3934 | Review `ownership` usage. | Ownership is explained through owner/accountability wording. |
| 3935 | Review `readiness` usage. | Readiness is localized where it is plain prose. |
| 3936 | Review mixed-language headings. | Headings are either deliberate terms or localized. |
| 3937 | Review mixed-language lists. | Lists do not look like raw notes accidentally pasted in. |
| 3938 | Review glossary alignment. | Body terminology matches glossary and term note. |
| 3939 | Review companion-route labels. | Route labels are consistent across chapters. |
| 3940 | Record terminology exceptions. | Exceptions are documented for the editor. |
| 3941 | Re-read the introduction for promise/coverage match. | The introduction matches the actual book scope. |
| 3942 | Re-read Part I for conceptual ramp. | Reader can follow from agent basics to contracts. |
| 3943 | Re-read Part II for security/control flow. | Policy, tools and confirmation flow are coherent. |
| 3944 | Re-read Part III for runtime boundaries. | Runtime, sandbox and MCP sections have no gaps. |
| 3945 | Re-read Part IV for state/memory/retrieval. | Memory and retrieval claims are bounded. |
| 3946 | Re-read Part V for observability/evals. | Trace, SLO and eval chapters reinforce each other. |
| 3947 | Re-read Part VI for lifecycle governance. | ADLC, assurance and incidents form one lifecycle. |
| 3948 | Re-read Part VII for launch readiness. | Launch checklist is actionable and not repetitive. |
| 3949 | Re-read appendices for navigation. | Appendices guide readers without replacing companion. |
| 3950 | Check cross-part transitions. | Each part connects to the next without abrupt jumps. |
| 3951 | Check repeated canonical cases. | Support-ticket and knowledge-agent cases stay consistent. |
| 3952 | Check chapter endings. | Each chapter ends with usable next-step guidance. |
| 3953 | Check chapter openings. | Each chapter opens with the problem, not a slogan. |
| 3954 | Check practical exercises. | Exercises are feasible for a real team. |
| 3955 | Check editor-facing density. | No chapter is just compressed notes. |
| 3956 | Check duplicated paragraphs. | Repetition is intentional or removed. |
| 3957 | Check orphaned references. | References to removed sections are fixed. |
| 3958 | Check source-map agreement. | Source map matches current manuscript structure. |
| 3959 | Check manuscript-map agreement. | Manuscript map reflects current proof status. |
| 3960 | Record structural risks. | Remaining structural risks are listed for editor review. |
| 3961 | Recheck fast-moving platform claims. | Claims about providers are current or generalized. |
| 3962 | Recheck security standard references. | NIST/OWASP/CISA references remain accurate. |
| 3963 | Recheck AI incident examples. | Public incident examples use reliable sources. |
| 3964 | Recheck Air Canada case wording. | The case stays tied to the official source. |
| 3965 | Recheck Anthropic/OpenAI wording. | Vendor references are accurate and not overstated. |
| 3966 | Recheck LangGraph/LangChain wording. | Framework references are current and scoped. |
| 3967 | Recheck Microsoft/Google/GitHub references. | Platform examples are current enough for print. |
| 3968 | Recheck MLCommons references. | Benchmark references are not used beyond evidence. |
| 3969 | Recheck OpenReview demotions. | Non-primary research leads are not treated as primary evidence. |
| 3970 | Recheck source catalog dates. | Source catalog records the latest verification dates. |
| 3971 | Recheck URL stability. | Long or fragile URLs are moved to companion where possible. |
| 3972 | Recheck citation economy. | The print manuscript is not overloaded with links. |
| 3973 | Recheck legal/compliance wording. | Non-legal advice boundaries are clear. |
| 3974 | Recheck AI-use disclosure placeholder. | Disclosure field is present and author-owned. |
| 3975 | Record source risks. | Remaining source risks are ready for author/editor decision. |
| 3976 | Collect final public author name. | Byline is author-approved. |
| 3977 | Collect short author bio. | Short bio is factual and usable by publisher. |
| 3978 | Collect long author bio. | Long bio is factual and usable by publisher. |
| 3979 | Collect role/public positioning. | Public role line is approved. |
| 3980 | Collect verified experience claims. | Experience claims are evidence-backed or softened. |
| 3981 | Collect public project links. | Links are accurate and author-approved. |
| 3982 | Collect online-support public URL. | Public URL replaces the placeholder in Google Doc. |
| 3983 | Collect online-support version route. | Versioning/changelog/errata route is clear. |
| 3984 | Collect acknowledgements. | Block is filled or explicitly removed. |
| 3985 | Collect legal disclaimer wording. | Required publisher wording is inserted or marked N/A. |
| 3986 | Collect AI-use disclosure wording. | Required disclosure is inserted or marked N/A. |
| 3987 | Collect final title/subtitle. | Metadata matches publisher agreement. |
| 3988 | Collect cover copy. | Cover copy is author/publisher-approved. |
| 3989 | Collect imprint metadata. | Imprint fields are complete. |
| 3990 | Apply author-owned fields in Google Doc. | No author placeholders remain accidentally. |
| 3991 | Backport author-owned fields to repository. | Markdown source agrees with Google Doc where appropriate. |
| 3992 | Run post-author placeholder scan. | Only intentional placeholders remain. |
| 3993 | Run post-author raw export. | Fresh raw DOCX exists after author fields. |
| 3994 | Run post-author Template2000n build. | Styled DOCX exists after author fields. |
| 3995 | Run post-author render QA. | Page counts and blank checks are recorded. |
| 3996 | Send proofread package. | Editor/proofreader receives Google Doc and DOCX proof. |
| 3997 | Triage proofread comments. | Each comment has a decision. |
| 3998 | Apply accepted proofread comments. | Accepted edits are in Google Doc and source. |
| 3999 | Freeze final publisher checkpoint. | Commit/tag/report identify exact final artifacts. |
| 4000 | Prepare final author-facing report. | Report lists results, proof paths and author-owned decisions. |
