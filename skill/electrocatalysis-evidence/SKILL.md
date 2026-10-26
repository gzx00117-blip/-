---
name: electrocatalysis-evidence
description: Use a traceable electrocatalysis literature library for critical reading, condition and assay checks, manuscript arguments, figure interpretation or experiment planning. Covers NO3RR, Cu/Ni, fullerene and molecular microenvironments; apply when literature evidence is needed.
---

# Electrocatalysis Evidence

Use the user's library of 183 DOI records to answer a scientific question with traceable evidence and bounded transfer. It is a selected collection, not comprehensive journal coverage or model-weight training. Previous151 preserve their actual scopes (5 main-section,146 focused). E152–E183 add32 systematic argument/all-main-figure analyses (184 figure groups:27 primary papers,4 reviews,1 commentary); eight SI sources have overviews and targeted methods/selected visual pages, not full numeric replication. Some papers are historical or neighboring applications. Each card records its actual scope.

## Locate and retrieve

The portable repository contains `cards/`, `analysis/` and `scripts/`. When installed, [library-location.md](references/library-location.md) identifies its local clone. If absent, resolve the repository two levels above this skill folder or locate the clone before claiming access.

1. Search authored cards with `python scripts/query_evidence.py "供氢"` or English scientific terms. This is lexical search with limited aliases, not vector retrieval. Use `--card E029` for claims and locators. Read relevant cards, including contrary results.
2. Use `analysis/151篇论文索引.md` for DOI/title and `analysis/跨论文分析与使用框架.md` for cross-paper synthesis. For critical reading and the latest methods/conflicts, read [critical-reading.md](references/critical-reading.md) and `analysis/新增30篇综合文献能力学习总结_2026-10-21.md`. Load relevant sections, not the whole library on every task.
For the current index use `analysis/183篇论文索引.md`. For figure reasoning, storytelling, experiment phenomena, palettes or titles, read [story-and-figures.md](references/story-and-figures.md), then retrieve only relevant cases with `python scripts/story_query.py --card E183` or `--query "峰面积"`. E152–E183 return physical PDF pages. E183's local document ID is SI06 because its source combines24 main/cover pages with44 SI pages. SI01 has no acquired parent main text and is not another full-paper review.
3. Before a new quantitative claim, peak assignment or method, read complete supporting source sections. `python scripts/query_evidence.py --card E001 --source-pages 7-8 --corpus <local-corpus>` retrieves full extracted pages. Without `--corpus`, a local ignored config or `ELECTROCATALYSIS_CORPUS` may supply it. The ignored local config may contain `source_corpora` for multiple dated corpora. Sources are not included in GitHub.
4. Inspect original page images when axes, molecular geometry, multipliers, peak shapes or equations matter. Text extraction does not verify a figure. Existing visual checks cover E001 p.7, E002 p.6, E003 p.8, E016 p.3, E029 p.5 E030 pp.5–6, E054 p.4, E055 p.7, E071 p.5, E076 p.3, E088 p.6 and E090 p.6; do not extend that status to other figures.
For E092–E121, use `--source-units` for indexed JATS paragraphs/captions; these are not PDF pages. Their selected-figure checks are recorded in `analysis/visual_reading_receipts.json`; this does not verify every figure.
E122–E151 also use JATS units; their figure checks are in `analysis/methods_visual_receipts.json`. SI retrieval is separately `--si-pages`, only for explicitly recorded sources; main-text units never stand for SI pages.
E152–E183 main figure groups and exact image receipts are in `analysis/story_visual_receipts.json`; do not extend this to every SI panel. Eight separate SI audits are in `analysis/story_si_audits.json`; retrieve with `python scripts/story_query.py --si SI04`. Old151 cards were preserved; these audits extend them without silently changing their claims. Use the SI document ID to find local `texts/SIxx.json` when full source detail is needed.
5. Use verified source identity and SHA256 over filenames; a local attachment named as another paper's SI actually contains E030. Old locators are1-indexed PDF pages; new JATS units are separately labeled. SI is read only when explicitly recorded. Final proof metadata may still need checking.

## Apply to the task

Read [task-workflows.md](references/task-workflows.md) for writing, figures, experiments or updates. For each substantive conclusion report claim ID, DOI/PDF page, author-reported observation, interpretation, and applicability to the actual sample. Do not turn a literature mechanism into a measured fact about the user's material.

Match substrate, NO3 vs NO3–N basis, electrolyte/pH, potential reference/iR, reactor, loading, denominator, time and product assay before numerical comparison. Prioritize product FE and partial current/yield over total current alone.

## High-value evidence routes

- **Working state and spectroscopy:** E001/E015/E016/E030. Raman intensity depends on coverage, consumption, enhancement and scaling; E001 Fig.5b is scaled 5×. Raman and IR labels are not interchangeable.
- **Hydrogen generation, transfer and use:** E002–E004/E007/E013/E014/E018. Ni4N/Cu is not ordinary CuNi; more H coverage or more Ni does not guarantee more NH3.
- **Molecular environment:** E006/E011/E012/E022/E028/E031. Separate proton, charge, area, wetting and ion-composition changes. E022's control still has K+ from KNO3; E031 is PDMS-Cu2O/C, not COF.
- **C60 roles:** E005/E026–E029. Separate synthesis reductant, electron acceptor/donor, direct active site and regenerable mediator. E029's charge-then-open-circuit perturbation tests regeneration; its CV uses Fc/Fc+, performance uses RHE.
- **Computational and assay limits:** E003/E004/E020/E030. ΔG is not a transition-state barrier; E030 Figures 4/5 use fixed/unfixed frameworks. KSCN interferes with E020's ammonia assay, so poisoned total current cannot establish NH3 inhibition.
- **Figure/phenomenon counterexamples:** E160 peak decline can accompany faster proposed consumption; E183 Fig.5C reports correlation, not a universal Raman rate calibration. SI04 flags CO feed versus CO2 electron-count conventions: confirm actual carbon source before using urea FE. SI05 reports overlapping CN uncertainties and a ratio-table discrepancy. E180 requires retention/reset before claiming memory. E179 separates surface potential, derived field and nested replicates. E182 establishes PyCEE's PSC context, not the user's CuNi mechanism.
- **Device/other reactions:** E017–E019/E021/E023–E025/E029–E031. E019 is mainly NO2RR; E030 uses CO, E029 CO2. Include maintenance and external H2/light/plasma energy when relevant. Cathode stability does not certify the paired anode.

## New evidence that changes decisions

- **H and impedance are conditional:** E036's H comes mainly from ethylene glycol under light; E046 separates H detected from H used in the target reaction. E055 uses dissolved O2 as an indirect DMPO–OH probe and can show larger impedance while NH3 selectivity improves. E074 separates surface H from subsurface hydride; E075/E083 distinguish stock from productive consumption.
- **Avoid universal structure rules:** E054 supports Cu(100) over Cu(111) for its controlled alkaline single crystals; do not transfer MOF facets (E048) or initial morphologies (E041) to metallic working surfaces. E056 tests lattice-N regeneration by isotope switching; finite lattice inventory alone is not a catalytic cycle. E076 explicitly limits N/O/C EXAFS assignments and scales its Cu reference ×0.4.
- **Modifiers depend on substrate and state:** E051 improves CO2RR but suppresses CORR; E077 favors coupling over NH3 yet low-loading single atoms initially have lower area productivity. E065 changes molecular stability as well as electronics. E091 proposes hydrated-K+ repulsion, unlike systems that benefit from enrichment; inspect conditions before averaging these claims.
- **Check definitions and numerical closure:** E057's relative purity is not neat-acid concentration; E059 ppm KNO3 is not ppm nitrate-N. E062/E063 have unresolved replication statements. E071/E088/E090 have reported rate/current pairs needing raw-data or condition checks. Run `scripts/check_faraday.py` with the actual substrate (NO3:8e, NO2:6e, NO:5e); a discrepancy prompts verification, not automatic correction or a misconduct claim.
- **Separate review and neighboring reactions:** E058/E064/E078 are reviews, not independently repeated data. E036/E047/E060/E067 involve light/heat/cascades. E032's 2027 issue date has no confirmed online-first date; do not claim every record is verified recent publication.

## Manuscript and visual workflow

Read [visual-workflow.md](references/visual-workflow.md) for argument design, software selection, journal requirements and editable figure generation. Consult `analysis/新增30篇学习总结.md` for recent conflicts and `analysis/软件绘图与期刊风格实操.md` for reproducible steps. Never infer authors' software or acceptance reasons from appearance. Keep official requirements, observed conventions and our presets separate.
Current practical guides: `analysis/图文论证与科研叙事手册_2026-10-26.md`, `analysis/原生软件与期刊图形规范_2026-10-26.md`, and `analysis/标题与证据强度工作坊_2026-10-26.md`. Explain observations before interpretations; each main figure needs a central claim, alternatives and a bridge. Use `templates/argument_plan_example.json` with `scripts/audit_argument.py` to flag explicit missing conditions/controls and unsupported signal-to-rate/ΔG-to-barrier jumps; this is a checklist, not scientific certification.

For this user, final scientific figures must be made in graphical software with editable native projects: Origin `.opju` for plots; PowerPoint/vector-native layers for schematics and assembly, with ChemDraw/VESTA/Fiji/Blender sources as appropriate. Historic Python-rendered training examples remain archival; do not make them the default for new figure deliveries.

## Persistence and updates

Preserve raw PDFs/Zotero and dated snapshots. Add new reviews with distinct DOI, actual read scope, page-level claims, condition mismatches and unresolved contradictions. Run `scripts/validate_library.py`; extraction counts never become review counts. Do not rerun ingestion over the original snapshot during routine queries.

Publish only authored cards, bibliography and skill/scripts. Keep PDFs, full extracted text, source excerpts/images, Zotero DB, local configs and unpublished sample records local. No scheduled reading or native memory-folder writes are implied. Missing source access remains explicit.
