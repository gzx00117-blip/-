# Critical reading and reusable checks

Use for a new paper, a cross-paper comparison or a mechanistic claim. Retrieve only relevant evidence; paper count is not confidence.

## Read a paper into an argument

Identify the actual question and document type first. Extract: intervention/comparator; measured outcome and denominator; conditions; methods that produced that outcome; author interpretation; plausible alternatives; next discriminating test. Separate author report from our critique and from observations on the user's sample.

The 2026-10-21 batch E122–E151 adds `capabilities`, `critical_reading`, 30 figure receipts and six explicitly scoped SI reviews. `analysis/新增30篇综合文献能力学习总结_2026-10-21.md` links the new conflicts and application limits. Two review/perspective records and one computational record must not become independent experimental replications.

For important numbers read complete supporting sections and SI where necessary. Check reference calibration, iR, cell, mass basis, time/current integration, product standards, blanks, recovery/LOD/LOQ, replication unit and normalization. Missing reporting is unknown, not proof the authors omitted the experiment. Do not issue a universal paper-quality number from these partial reviews.

## Retrieval and source scope

```powershell
python scripts/query_evidence.py --capability counterexample --limit 10
python scripts/query_evidence.py --capability replication
python scripts/query_evidence.py --kind methods_research
python scripts/query_evidence.py --disclosed-software COMSOL
python scripts/query_evidence.py --card E129 --source-units 22-24
python scripts/query_evidence.py --card E134 --si-pages 3-4
```

Local source corpora are needed for full passages. Main-text JATS U numbers and SI physical PDF pages are separate selectors and sources. Retrieval beyond recorded reading scope is allowed for verification but does not automatically upgrade the stored review status. Original source text/images remain local.

## Comparability and numerical checks

```powershell
python scripts/compare_conditions.py --list
python scripts/compare_conditions.py --a E151-performance --b E151-raman
python scripts/quant_checks.py concentration --mg-l 14.0067 --basis N
python scripts/quant_checks.py charge --coulomb 1.9297066424 --molar 0.01 --litre 0.02
python scripts/quant_checks.py urea --after 0.000005 --before 0.000002 --enzyme-blank 0.000001
python scripts/check_faraday.py --substrate NO3 --rate-mmol 15.5 --current-ma 3330
python scripts/export_citations.py --card E144
```

`compare_conditions.py` compares explicitly entered fields exactly. It detects known differences and preserves missing values; it does not understand chemical synonyms, rank catalyst quality or prove equivalence. Add custom profiles with `--profiles` only after checking the supporting source and units. Supplied profiles are condition snapshots, not a complete machine extraction of each paper.

Concentration input is mg/L with an explicit basis, never unspecified ppm. Charge output is a stoichiometric ceiling under assumptions, not measured conversion; do not use it above depletion as a real conversion. Urea correction uses NH4 molar amounts and retains negative results; uncertainty assumes independence. With shared calibration or correlated blanks, use covariance rather than this simple propagation. Rate/current disagreement prompts context/raw-data checks, not accusation or silent data correction.

## High-value challenge routes

- Fair comparison: E123, E131, E133, E139. Same RHE or normalized current does not remove pH, transport, conversion or area-model differences.
- Quantification: E124/E125; check reagent contamination, background and probe stoichiometry. E131 repeats areas on one wafer; E129 explicitly usually n=1. Multiple scans, pixels or fitted points are not independent catalysts.
- Contrary evidence: E135 (fullerene/porosity effects depend on metal), E143 (HER inhibition can accompany better NH3), E145/E150 (failure and interface instability), E151 (modifier does not necessarily improve FE).
- Mechanism: E128/E130/E149 lattice isotope participation versus exchange/dissolution; E132 ensemble/sampling; E136 time resolution; E146 tandem intermediate identification. A computed structure or stronger spectrum alone cannot establish a productive pathway.
- System boundary: E135 sacrificial Fe anode, E147 hydrazine oxidation, E141 external thermal/solar/recovery modules. Distinguish half-cell, paired cell and whole-system energy/material inputs.
- Internal disagreements: E134 SI equation, E139 enrichment multiplier, E144 peak performance, E145 band-direction wording. Preserve unresolved entries; do not select the best number to make the argument stronger.

For a writing task, use the narrowest supported phrasing with DOI, claim and locator. For an experiment, select the test most likely to distinguish the leading explanation from a concrete alternative. For a figure, choose the required comparison and denominator first; follow the user's graphical-software/native-editability preference. Do not turn this workflow into a rigid checklist for a trivial question.

## Maintenance and validation

```powershell
python scripts/validate_library.py
python scripts/test_capabilities.py
```

These test retrieval, schema and numerical behavior, not scientific truth or general model gains. Citation export currently covers only the30 Crossref-checked new records. Before formal submission, verify current publisher metadata, corrections/retractions and complete quoted context; the snapshot is not a comprehensive update clearance. Preserve old cards and dated reading scope.
