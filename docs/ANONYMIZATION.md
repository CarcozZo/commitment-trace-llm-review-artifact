# Double-Blind Anonymization Notes

## Review-Version Rule

This artifact is prepared for double-blind review.  During review, it must be
shared only through an anonymous repository or an identity-stripped mirror.

Do not use:

- a personal GitHub account;
- a lab or institution GitHub organization;
- a repository URL containing author, institution, project-group, or grant
  identifiers;
- a DOI record listing real creators before review decisions;
- local paths from the authors' machines or servers.

## Removed or Regenerated Fields

The release package uses regenerated anonymous metadata instead of the original
run metadata where the original files contained local absolute paths.  In
particular:

- `validation_report.json` is regenerated without local `dataset_dir` and
  `schema_path` fields;
- `summary.json` is regenerated without local `dataset_dir`, `source_dir`, and
  absolute Windows paths;
- raw model-backend paths are replaced with anonymous model identifiers;
- top-level development configs are not included;
- only selected data, metrics, and scripts needed for anonymous review are
  included.

## Required Pre-Submission Check

Run:

```bash
python scripts/check_anonymity.py --root .
```

The script checks for author/institution markers, local Windows or Unix paths,
private server identifiers, email addresses, SSH keys, and unresolved
placeholders.

## Camera-Ready Conversion

After acceptance:

1. replace `Anonymous Authors` with the real creators;
2. deposit the final version in a repository with DOI support;
3. update the dataset citation and Data Availability statement;
4. add the public repository URL to the camera-ready manuscript;
5. archive the exact code and data version used by the paper.
