# Connector contract

Use only an authorized connector that provides schema inspection and read-only SQL execution.

Before querying, confirm:

- The selected source and SQL dialect
- Database-enforced read-only access
- Query timeout and maximum returned rows
- Whether the connector reports truncation and freshness

Expected result metadata should include columns, rows, row count, truncation state, elapsed time, and warnings. Treat missing truncation or freshness metadata as a limitation.

On an execution error, make at most two targeted corrections. A correction may fix syntax or a verified identifier. It must not change the requested population, metric, time range, or source without telling the user.

Never expose connector credentials or private connection details in SQL, responses, files, or logs.
