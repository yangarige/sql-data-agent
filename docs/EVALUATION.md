# Evaluation guide

Unit tests for the SQL validator are necessary but do not measure whether the agent selects the right source or answers correctly. Use `evals/cases.json` as a behavioral contract.

## Evaluation layers

### Static safety

Verify that generated SQL:

- Is one read-only statement
- Uses known tables and columns
- Contains required date or partition filters
- Avoids `SELECT *` in final analytical queries
- Recomputes ratios from aggregate components
- Avoids locking, side-effect functions, and external access

### Execution correctness

For deterministic synthetic data, execute the generated SQL and compare result sets with an approved reference result. Prefer result-set equality over exact SQL-string equality because different valid queries can produce the same answer.

### Source selection

Measure whether the agent loaded all necessary tables without loading unrelated schemas:

- Schema recall: required tables found / required tables
- Schema precision: required tables found / tables loaded

### Behavioral safety

Verify that the agent:

- Refuses write requests
- Does not invent missing metrics or columns
- Does not claim a query ran when no connector returned a result
- Reports freshness, truncation, and small-sample limitations
- Stops after the configured retry limit

## Case file

Each case contains:

- `id`: stable identifier
- `category`: workflow group
- `prompt`: synthetic user request
- `expected_behaviors`: observable requirements
- `forbidden_behaviors`: observable failures

Validate the case file:

```bash
python3 scripts/check_eval_cases.py
```

## Suggested metrics

| Metric | Purpose |
|---|---|
| Execution accuracy | Correct result set on executable cases |
| SQL success rate | Syntactically valid and executable SQL |
| Schema recall | Required tables were discovered |
| Schema precision | Irrelevant schema context was avoided |
| Unsafe-query rejection | Dangerous requests were refused |
| Unsupported-claim rate | Unverified facts were not presented as verified |
| Retry-limit compliance | Failures stopped within the configured bound |

Store evaluation outputs outside Git if they include proprietary schemas, questions, SQL, or results.
