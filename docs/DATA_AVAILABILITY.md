# Data Availability

## Double-Blind Submission Version

The data and code supporting the trace-replay experiments are provided in an
anonymized review artifact.  The artifact contains the CommitmentTrace-LLM
records, schema, train/validation/test splits, validation reports, selected
policy configurations, locked test metrics, dominance checks, and scripts for
validating the release and reproducing the reported summary tables.  The
artifact is shared through an anonymous review link to preserve double-blind
review.  It should not be cited as a public DOI before acceptance.

## Camera-Ready Version Template

After acceptance, replace the paragraph above with:

```text
The CommitmentTrace-LLM dataset and replay code are publicly available at
[repository name and DOI], version [version].  The release includes claim
records, frozen role-agent responses, receiver transition labels, delayed
verifier outcomes, network-state records, policy replay events, train/validation
/test splits, validation reports, selected policy configurations, locked test
metrics, dominance checks, and scripts for validating the dataset and
reproducing the summary tables.  The dataset is released under [data licence],
and the code is released under [software licence].
```

## Repository and Citation Actions

- During review: use an anonymous repository or identity-stripped mirror.
- After acceptance: deposit a versioned archive with a DOI.
- Recommended public data licence, pending author confirmation: CC BY 4.0.
- Recommended code licence, pending author confirmation: MIT or Apache-2.0.
- Verify the upstream model and generated-output licence before public release.

## Missing Information / Risk Flags

- Final DOI is intentionally absent during double-blind review.
- Final creator list is intentionally absent during double-blind review.
- Final licence should be confirmed by the authors before public release.
- The paper should state that the dataset is controlled trace-replay evidence,
  not a live deployment trace.

