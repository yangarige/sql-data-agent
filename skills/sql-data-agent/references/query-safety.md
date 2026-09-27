# Query safety

## Allowed by default

- A single `SELECT` or `WITH ... SELECT` statement
- Metadata inspection with `SHOW`, `DESCRIBE`, or `EXPLAIN`
- Read-only queries through an authorized connector

## Blocked by default

- `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `UPSERT`
- `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `REPLACE`
- `GRANT`, `REVOKE`, role or permission changes
- `CALL`, `EXECUTE`, stored procedures, external exports
- Multiple SQL statements

Run `scripts/validate_sql.py` before execution. The validator is a guardrail, not a substitute for database permissions. Use a database account that is technically read-only.

Do not commit credentials, access tokens, private hostnames, connection strings, direct identifiers, production result files, or query history.
