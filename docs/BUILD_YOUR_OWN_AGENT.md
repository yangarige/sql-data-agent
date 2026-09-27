# Build your own data-query agent

This guide turns the generic skeleton into a domain-specific, read-only analytics agent without placing credentials or production data in Git.

## Architecture

```text
User question
    |
Codex + SKILL.md
    |
Query map -> schema catalog -> metric catalog
    |
Read-only SQL validation
    |
Authorized database connector
    |
Data-quality checks
    |
Answer + evidence + limitations
```

The model supplies reasoning. The repository supplies maintained context and guardrails. The database connector supplies authorized execution.

## 1. Define a narrow first scope

Start with two or three recurring questions, such as:

- Daily usage trends
- Acquisition conversion
- Cohort retention

Do not begin by documenting every warehouse table. A small set of governed models is easier to keep correct.

For each subject, decide:

- Which model is authoritative?
- What is its grain?
- Which date or partition column limits scans?
- Which dimensions are safe and useful?
- Which known limitations affect interpretation?

## 2. Rename the skill if needed

Rename the folder and update the `name` field in `SKILL.md`. Skill names use lowercase letters, digits, and hyphens.

Also update `agents/openai.yaml` so its default prompt invokes the new `$skill-name`.

Keep the description specific enough that the skill activates for data questions but not unrelated programming work.

## 3. Build the query map

Edit `references/query-map.md`. Each row should point from a business subject to one preferred model.

Good entry:

```markdown
| Subscription revenue | `analytics.subscription_revenue_daily` | date x plan | `schema-catalog.md#subscription-revenue` | Revenue trend and plan mix |
```

Avoid listing several interchangeable tables without explaining when to use each one. The query map is a routing layer, not a full data dictionary.

## 4. Document schemas by grain

Edit `references/schema-catalog.md`. For each approved model, record:

- Fully qualified name
- Business purpose
- Row grain
- Primary or logical keys
- Date or partition field
- Measures and dimensions
- Join relationships
- Freshness expectation
- Known limitations

Do not include sample production rows or direct identifiers. If an identifier is needed for joining, document its semantics rather than real values.

## 5. Define metrics precisely

Edit `references/metrics-catalog.md`. Every governed metric should include:

- Business name
- Numerator and denominator
- Eligible population
- Time basis and timezone
- Inclusion and exclusion rules
- Preferred source
- Owner or approval status
- Freshness expectation

For example, "retention" is incomplete unless it says whether it means exact-day, rolling-window, or bounded-window retention.

## 6. Add a read-only connector

Choose an execution method supported by your environment, such as an approved MCP database server, warehouse CLI, or internal read-only query service.

Security requirements:

- The database identity must be read-only at the database level.
- Secrets belong in a secret manager or local environment, never in this repository.
- The connector should expose only the databases and schemas the agent needs.
- Query timeouts, scan limits, and result-size limits should be enforced outside the prompt.
- Production exports and raw query results should not be committed.

Do not rely on `validate_sql.py` as the only security boundary. It is a useful guardrail, not a SQL parser or permission system.

## 7. Adapt for your SQL dialect

The example queries use broadly portable SQL. Update syntax for your warehouse where necessary, including:

- Date arithmetic
- Safe division
- Approximate distinct functions
- Identifier quoting
- Partition filters
- Result limits

Add dialect-specific rules to `query-safety.md` only when they materially change correctness or safety.

## 8. Test realistic questions

Test at least one request from each enabled workflow:

1. A one-number lookup
2. A trend comparison
3. A funnel or cohort query
4. An anomaly investigation
5. A request containing an unknown metric or column
6. A potentially unsafe write request

The agent should refuse to invent missing metadata, block write SQL, and clearly distinguish generated SQL from successfully executed SQL.

Run local checks:

```bash
python3 -m unittest discover -s tests -v
python3 skills/sql-data-agent/scripts/validate_sql.py examples/example_query.sql
python3 /path/to/skill-creator/scripts/quick_validate.py skills/sql-data-agent
```

The final command path depends on the local Codex installation and is optional for users who do not have the bundled skill validator.

## 9. Keep public and private layers separate

A practical repository layout is:

```text
public-template/
  Generic skill, validation code, and synthetic examples

private-analytics-context/
  Approved schemas, metric definitions, connector configuration, and internal change logs
```

If the public template and private context must coexist locally, keep the private context ignored and outside Git. Never sanitize a private repository by deleting files and preserving its history; create a new repository from the reviewed public tree.

## Minimum viable versus production-ready

Minimum viable:

- One skill
- One query map
- A few governed schemas and metrics
- Read-only connector
- SQL validation and manual review

Production-ready additions:

- Database-enforced read-only permissions
- Query cost and timeout controls
- Automated schema freshness checks
- Metric-owner approval process
- Connector audit logging
- Regression questions with expected invariants
- A release-time secret scanner
- Documented incident and revocation procedures
