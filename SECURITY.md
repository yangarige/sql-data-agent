# Security policy

## Public-release checklist

Before every release, verify that the repository contains none of the following:

- Git history copied from a private repository
- Credentials, tokens, cookies, certificates, or connection strings
- Private domains, IP addresses, usernames, or filesystem paths
- Internal database, schema, table, column, event, project, or experiment names
- Production SQL, query history, results, logs, exports, screenshots, or reports
- Customer, employee, account, device, or other direct identifiers
- Proprietary business rules, targets, thresholds, costs, or strategy notes
- Local agent permission files or tool allowlists

Use a database identity that enforces read-only access. Application-level SQL validation does not replace database permissions.

For a local organization-specific scan, copy `audit-denylist.example.txt` to `audit-denylist.local.txt`, add private names, domains, schema prefixes, and project identifiers, then run:

```bash
python3 scripts/audit_public_repo.py .
```

The local denylist is ignored by Git and must never be committed.

Report security issues privately to the repository owner. Do not open a public issue containing sensitive evidence.
