# Connector contract

The plugin intentionally does not ship production connection code. Implement this contract through an approved MCP server, CLI, or service in the deployment environment.

## Minimum capabilities

### List data sources

Return only sources the current identity is allowed to query.

```json
{
  "sources": [
    {
      "name": "analytics",
      "dialect": "postgres",
      "read_only": true
    }
  ]
}
```

### Describe a table

Return schema metadata, not production rows.

```json
{
  "source": "analytics",
  "table": "daily_activity",
  "grain": "one row per date and segment",
  "columns": [
    {"name": "activity_date", "type": "date", "nullable": false},
    {"name": "segment_name", "type": "text", "nullable": false},
    {"name": "active_users", "type": "integer", "nullable": false}
  ],
  "partition_columns": ["activity_date"],
  "freshness": "daily"
}
```

### Run read-only SQL

Suggested inputs:

```json
{
  "source": "analytics",
  "sql": "SELECT ...",
  "timeout_seconds": 30,
  "max_rows": 1000
}
```

Suggested output:

```json
{
  "ok": true,
  "columns": ["activity_date", "active_users"],
  "rows": [],
  "row_count": 0,
  "truncated": false,
  "elapsed_ms": 0,
  "query_id": "opaque-query-id",
  "data_freshness": "2026-01-31",
  "warnings": []
}
```

Errors should be returned as structured data so the agent can make a bounded correction:

```json
{
  "ok": false,
  "error_code": "UNKNOWN_COLUMN",
  "message": "The requested column is not available.",
  "retryable": true
}
```

## Required controls

- Use a database account with SELECT-only permissions.
- Start database sessions or transactions in read-only mode where supported.
- Enforce time, row, byte, and scan limits outside the model prompt.
- Validate the parsed SQL for the target dialect.
- Reject multiple statements, locking reads, file access, network functions, and stored procedures.
- Mask or deny sensitive columns before results reach the model.
- Preserve an audit record containing source, query hash, tables, runtime, row count, truncation state, and actor.
- Keep credentials out of model messages, tool outputs, repository files, and logs.

## Retry policy

Allow at most two targeted corrections after an execution error. A correction may fix syntax, an unknown identifier, or an unsupported function. It must not silently widen the date range, switch to a different source, remove an eligibility filter, or change the requested metric.

After the retry limit, return the error and the unverified SQL to the user.

## Dialect profile

For each supported source, document:

- Date arithmetic and timezone behavior
- Identifier quoting
- Safe division
- Approximate distinct functions
- Partition filtering
- Result limiting
- Read-only transaction configuration
- Functions that can access files, networks, or external services
