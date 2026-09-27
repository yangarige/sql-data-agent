# Query map

Replace every `CUSTOMIZE` value before relying on this map. Do not add credentials, private URLs, customer data, or production query results to this repository.

| Subject | Preferred model | Grain | Schema reference | Typical use |
|---|---|---|---|---|
| Core activity | `CUSTOMIZE.analytics.daily_activity` | one row per date and segment | `schema-catalog.md#core-activity` | Daily trends and comparisons |
| Acquisition | `CUSTOMIZE.analytics.acquisition_funnel` | one row per cohort and channel | `schema-catalog.md#acquisition` | Signup and activation funnel |
| Retention | `CUSTOMIZE.analytics.retention_cohorts` | one row per cohort and period | `schema-catalog.md#retention` | D1, D7, and weekly retention |
| Product events | `CUSTOMIZE.events.product_events` | one row per event | `schema-catalog.md#product-events` | Detailed validation and drill-down |

## Source preference

1. Use governed aggregate models for routine answers.
2. Use user-level or event-level models only when the aggregate cannot answer the question.
3. Use raw ingestion tables only for source validation.
4. When two sources disagree, report the disagreement instead of silently choosing one.
