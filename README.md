# SQL Data Agent Template

A public-safe, skill-only plugin template for answering data questions, writing read-only SQL, validating query results, and producing evidence-backed conclusions.

Use it as a starting point for an internal analytics assistant: add your approved schema metadata and metric definitions, connect a read-only data tool, and keep credentials and production data outside the repository.

This repository intentionally contains no organization-specific schemas, URLs, credentials, production SQL, query results, business thresholds, customer data, or private Git history.

## What it does

- Routes a question to the relevant dataset and metric definition.
- Writes conservative read-only SQL.
- Uses a connected query tool when one is available.
- Checks freshness, grain, joins, denominators, and reconciliation.
- Separates verified facts from interpretations and hypotheses.
- Supports quick lookups, funnels, cohorts, anomaly diagnosis, and SQL review.

It does not include a database connector or credentials. Connection details differ by environment and should be configured through an approved MCP server, CLI, or secret manager.

## Distribution modes

- Plugin installation: use the repository root, which contains `plugin.json` and `.codex-plugin/plugin.json`.
- Project-local use: copy `skills/sql-data-agent` into `.codex/skills/` in another project.
- Skill installation: install the `skills/sql-data-agent` subdirectory with a compatible Skill installer.

The repository does not bundle a production database connection. Connectors and credentials remain environment-specific.

After publishing, the Skill subdirectory can be installed from its GitHub directory URL with a compatible Skill installer, for example:

```text
$skill-installer install https://github.com/yangarige/sql-data-agent/tree/main/skills/sql-data-agent
```

Replace `OWNER/REPOSITORY` with the public repository path. Restart the client after installation when required by the client.

## Structure

```text
plugin.json                     Portable plugin manifest
.codex-plugin/plugin.json       Codex compatibility manifest
skills/sql-data-agent/
  SKILL.md                     Agent instructions and routing
  agents/openai.yaml           Codex UI metadata
  references/
    query-map.md               Business subject to data-source routing
    schema-catalog.md          Approved schemas, grains, and keys
    metrics-catalog.md         Governed metric definitions
    analysis-workflows.md      Analysis modes and diagnostic sequence
    query-safety.md            Read-only policy
    quality-checks.md          Data and conclusion checks
  scripts/validate_sql.py      Read-only SQL guardrail
examples/
  example_schema.sql           Synthetic schema only
  example_query.sql            Synthetic query only
  queries/                     End-to-end synthetic query examples
  demo/                        Runnable SQLite demonstration
evals/
  cases.json                   Behavioral evaluation contract
tests/
  test_validate_sql.py         SQL guard regression tests
  test_demo.py                 Demo execution tests
docs/
  BUILD_YOUR_OWN_AGENT.md      Step-by-step customization guide
  CONNECTORS.md                Connector contract and safety boundary
  EVALUATION.md                Agent behavior evaluation guide
  USE_CASES.md                 Example prompts, SQL, and expected behavior
```

## Five-minute start

1. Clone or copy this repository into a new, empty project.
2. Replace `CUSTOMIZE` entries in `query-map.md`, `schema-catalog.md`, and `metrics-catalog.md` with approved metadata.
3. Connect Codex to a database identity that is technically read-only.
4. Open the repository in Codex.
5. Ask a question such as:

```text
Use $sql-data-agent to compare daily active users for the last seven complete days with the previous seven days. Show the SQL and state any data-quality limitations.
```

See [Build your own agent](docs/BUILD_YOUR_OWN_AGENT.md) for the full setup and [Use cases](docs/USE_CASES.md) for end-to-end examples.

## Run the synthetic demo

The demo contains generated fictional data only:

```bash
python3 examples/demo/build_demo_db.py
python3 examples/demo/query_demo.py \
  examples/demo/demo.sqlite \
  examples/demo/queries/funnel_by_channel.sql
```

The query command opens SQLite in read-only mode and emits structured JSON. Generated `.sqlite` files are ignored by Git.

## Customize before use

1. Replace every `CUSTOMIZE` placeholder with metadata approved for the intended audience.
2. Keep credentials and private endpoints outside Git, preferably in the connector or secret manager.
3. Configure a technically read-only database identity.
4. Connect Codex to your database through an approved MCP server, CLI, or local adapter.
5. Add only non-sensitive metric definitions and schema descriptions.
6. Run the SQL validator and tests.
7. Copy `audit-denylist.example.txt` to the ignored `audit-denylist.local.txt` and add private organization terms before every public release.

Search for unfinished placeholders:

```bash
rg --hidden --no-ignore -n 'CUSTOMIZE|TODO|REPLACE_ME' .
```

Validate a query:

```bash
python3 skills/sql-data-agent/scripts/validate_sql.py examples/example_query.sql
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_eval_cases.py
python3 scripts/audit_public_repo.py .
```

No license is included by default. Choose one deliberately before public distribution; see `docs/LICENSING.md`.
