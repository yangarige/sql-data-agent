# Use cases

All names and schemas in these examples are synthetic. The SQL illustrates the expected shape; adapt date functions and safe-division syntax to the connected warehouse.

## 1. Quick metric lookup

User prompt:

```text
Use $sql-data-agent to show daily active users for the last seven complete days and compare them with the previous seven days.
```

Expected agent behavior:

1. Resolve "daily active users" in the metric catalog.
2. Select the governed daily activity model from the query map.
3. Confirm the latest complete date.
4. Query two equal seven-day windows.
5. Report both totals or averages, the change, freshness, and definition.

Starting SQL: `examples/queries/daily_activity_trend.sql`

## 2. Acquisition funnel

User prompt:

```text
Use $sql-data-agent to compare visitor-to-signup and signup-to-activation conversion by channel for January. Sort by eligible visitors and show the SQL.
```

Expected agent behavior:

1. Confirm the funnel population and calendar month.
2. Aggregate numerators and denominators before calculating rates.
3. Check for zero denominators and missing channel values.
4. Present volume and conversion together so small channels are not overinterpreted.

Starting SQL: `examples/queries/acquisition_funnel.sql`

## 3. Cohort retention

User prompt:

```text
Use $sql-data-agent to compare day-1 and day-7 retention for the last four fully observed signup cohorts by segment.
```

Expected agent behavior:

1. Resolve whether retention is exact-day or windowed.
2. Exclude cohorts that have not had a full seven-day observation window.
3. Report cohort size beside retention.
4. Avoid strong conclusions for small cohorts.

Starting SQL: `examples/queries/retention_cohort.sql`

## 4. Anomaly diagnosis

User prompt:

```text
Use $sql-data-agent to investigate why active users fell yesterday. First rule out freshness problems, then identify the segments contributing most to the decline.
```

Expected agent behavior:

1. Check whether yesterday is complete and whether expected partitions exist.
2. Compare yesterday with a suitable baseline, such as the same weekday average.
3. Calculate each segment's absolute contribution to the total change.
4. Separate the observed contribution from unverified causal explanations.

Starting SQL: `examples/queries/anomaly_contribution.sql`

## 5. SQL review without execution

User prompt:

```text
Use $sql-data-agent to review this SQL for correctness and cost. Do not execute it. Check grain, joins, filters, ratio calculations, and whether it is read-only.
```

Expected agent behavior:

1. Run the local validator.
2. Inspect each source grain and join key.
3. Identify one-to-many amplification risks.
4. Verify partition filters and denominator handling.
5. Return a corrected query and explain every material change.

This mode works even when no database connector is configured, although schema-dependent claims remain unverified.

## 6. Missing metadata

User prompt:

```text
Use $sql-data-agent to calculate qualified pipeline efficiency by territory.
```

If the repositories do not define "qualified pipeline efficiency," the agent should not invent a formula. It should identify the missing definition, ask for the smallest necessary clarification, or provide a clearly labeled draft definition for approval.

## 7. Unsafe write request

User prompt:

```text
Use $sql-data-agent to delete duplicate event rows and rebuild the table.
```

Expected agent behavior:

- Explain that this skill is read-only.
- Do not generate executable destructive SQL.
- Offer a diagnostic query that identifies duplicates.
- State that remediation requires a separately authorized write workflow and database controls.

## What a good answer looks like

For most analytical questions, prefer this order:

1. Direct answer
2. Small evidence table
3. Interpretation supported by the evidence
4. Definitions and freshness
5. Limitations or unresolved hypotheses
6. SQL, when requested

Do not present generated example numbers as query results, and never say a query ran unless a connector returned a result.
