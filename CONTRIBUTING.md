# Contributing

Contributions should keep this repository generic, read-only by default, and safe to publish.

## Before opening a pull request

1. Use fictional schemas, identifiers, and data only.
2. Do not include credentials, private endpoints, production SQL, query results, screenshots, or copied internal documentation.
3. Keep `SKILL.md` concise and route detailed guidance to focused references.
4. Add or update tests for changes to deterministic scripts.
5. Add an evaluation case when changing agent behavior.
6. Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_eval_cases.py
python3 scripts/audit_public_repo.py .
```

## Pull request description

Explain:

- The user problem being solved
- The observable behavior change
- How the change was tested
- Any security, privacy, dialect, or compatibility implications

Do not attach private logs or data when reporting a bug. Reproduce the issue with a minimal fictional schema.
