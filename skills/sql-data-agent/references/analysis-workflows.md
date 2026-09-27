# Analysis workflows

## Quick lookup

Use a governed aggregate model, the smallest date range, and only required columns. Return the value, definition, freshness, and one concise interpretation.

## Structured output

Preserve the requested columns and grain. If a requested field is unsupported, keep the column visible and explain the limitation rather than silently changing its meaning.

## Funnel or cohort analysis

Define the eligible population first and reuse that fixed population throughout the analysis. Report population size before rates. Keep comparison populations aligned on definitions and observation windows.

## Anomaly diagnosis

Check in this order:

1. Data freshness, missing partitions, duplicates, and schema changes.
2. Calendar effects and unequal comparison windows.
3. Overall magnitude and start time.
4. Contribution by meaningful dimensions.
5. Funnel denominator changes versus conversion changes.
6. Known product, marketing, or operational changes supplied by the user.

## Deep dive

Start with the total, identify the largest contributor, then drill down only where the evidence changes the decision. Separate observed facts from causal hypotheses.
