# Runnable demo

This demo uses deterministic fictional data. It has no network access, credentials, or production identifiers.

Build the ignored SQLite file:

```bash
python3 examples/demo/build_demo_db.py
```

Run a validated query:

```bash
python3 examples/demo/query_demo.py \
  examples/demo/demo.sqlite \
  examples/demo/queries/funnel_by_channel.sql
```

Try the four query files under `examples/demo/queries/`. The query runner opens the generated database through a read-only SQLite attachment, limits returned rows, and emits JSON containing columns, rows, truncation state, elapsed time, and validator warnings.

The database generator deletes and recreates only the output path explicitly passed to it. Do not point it at an existing database.
