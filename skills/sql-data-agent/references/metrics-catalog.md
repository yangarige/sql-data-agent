# Metrics catalog

Replace these examples with approved definitions. Every metric should name its numerator, denominator, population, time basis, exclusions, owner, freshness expectation, allowed dimensions, and approval status.

| Metric | Definition | Source | Status |
|---|---|---|---|
| Daily active users | Distinct eligible users with an approved activity event on a calendar date | `CUSTOMIZE` | Example only |
| Signup conversion | `signups / eligible_visitors` | `CUSTOMIZE` | Example only |
| Activation conversion | `activated_users / signups` | `CUSTOMIZE` | Example only |
| Day-N retention | Cohort users active on exactly day N divided by the original eligible cohort | `CUSTOMIZE` | Example only |

## Definition rules

- Ratios are computed from aggregated numerators and denominators, never averaged from row-level rates.
- State whether retention is exact-day, rolling-window, or bounded-window retention.
- State the timezone and whether periods are calendar or rolling periods.
- Do not add targets, alert thresholds, or commercial assumptions unless they are approved for public release.
