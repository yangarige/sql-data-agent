# Quality checks

Before presenting a result, verify as applicable:

- The latest expected partition or refresh timestamp exists.
- Current and comparison windows have equal duration.
- Result grain matches the intended grain.
- Join keys do not multiply rows unexpectedly.
- Overall values reconcile with dimension totals within explained limits.
- Nulls, zero denominators, duplicates, and small samples are handled.
- Ratios are rebuilt from aggregate components.
- Facts, interpretations, assumptions, and recommendations are distinct.
- The answer identifies the query source and any unverified limitations.
