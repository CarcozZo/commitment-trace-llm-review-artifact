# Dataset Audit

- Raw responses were frozen in the source Phase 1B run before labels were computed.
- Source manual audit: frozen source-run audit retained internally; released records are validated by `scripts/validate_commitmenttrace.py`.
- Hidden truth labels are present only in claim and verifier outcome records for evaluation.
- Policy online features are generated separately and exclude hidden labels.
