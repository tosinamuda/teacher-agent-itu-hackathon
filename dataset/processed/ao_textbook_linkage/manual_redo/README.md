# Manual AO-Textbook Linkage Redo Workspace

This workspace is for the new manual linkage pass. The previous generated pass has been quarantined and must not be treated as trusted evidence.

## Trusted Active State

- The active manual linkage folder keeps only the original trusted pilot row:
  `dataset/processed/ao_textbook_linkage/manual/jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa.json`
- The active manifest now lists only that pilot row.

## Redo Protocol

Work in small review batches. Do not create one curriculum-wide audit file.

For each subtopic:

1. Render a structured evidence packet into `evidence_packets/`.
2. Manually inspect the atomic objectives and every textbook record in that packet.
3. Write the linkage row into `linkage_rows/` only after manual judgment.
4. Write candidate AO proposals into `candidate_atomic_objectives/` only when a record teaches a measurable skill not covered by an existing AO.
5. Keep each source record accounted for exactly once in the linkage row as a shared foundation record, AO record link, excluded record, or review item. Candidate AO proposals do not become a new accounting bucket.
6. Validate each subtopic before moving to the next batch.

Scripts may extract records, render evidence packets, count records, and validate schemas. Scripts must not decide semantic linkage, review categories, or candidate AOs.
