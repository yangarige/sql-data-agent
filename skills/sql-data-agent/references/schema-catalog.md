# Schema catalog

This file is a public-safe placeholder. Replace examples with approved metadata only. Prefer table purpose, grain, keys, partitions, and non-sensitive column definitions. Never paste sample production rows.

## Core activity

Table: `CUSTOMIZE.analytics.daily_activity`

- Grain: one row per `activity_date`, `segment_name`
- Owner: `CUSTOMIZE`
- Partition: `activity_date`
- Measures: `active_users`, `sessions`
- Dimensions: `segment_name`
- Approved joins: `CUSTOMIZE`
- Sensitivity: synthetic example; replace with an approved classification
- Freshness expectation: `CUSTOMIZE`
- Known limitations: `CUSTOMIZE`

## Acquisition

Table: `CUSTOMIZE.analytics.acquisition_funnel`

- Grain: one row per `cohort_date`, `channel_name`
- Owner: `CUSTOMIZE`
- Partition: `cohort_date`
- Measures: `visitors`, `signups`, `activated_users`
- Dimensions: `channel_name`
- Approved joins: `CUSTOMIZE`
- Sensitivity: synthetic example; replace with an approved classification
- Freshness expectation: `CUSTOMIZE`
- Known limitations: `CUSTOMIZE`

## Retention

Table: `CUSTOMIZE.analytics.retention_cohorts`

- Grain: one row per `cohort_date`, `period_number`, `segment_name`
- Owner: `CUSTOMIZE`
- Partition: `cohort_date`
- Measures: `cohort_users`, `retained_users`
- Dimensions: `period_number`, `segment_name`
- Approved joins: `CUSTOMIZE`
- Sensitivity: synthetic example; replace with an approved classification
- Freshness expectation: `CUSTOMIZE`
- Known limitations: `CUSTOMIZE`

## Product events

Table: `CUSTOMIZE.events.product_events`

- Grain: one row per event
- Owner: `CUSTOMIZE`
- Partition: `event_date`
- Keys: `event_id`, `anonymous_user_key`
- Fields: `event_name`, `event_timestamp`, `event_date`
- Approved joins: `CUSTOMIZE`
- Sensitivity: `CUSTOMIZE`
- Freshness expectation: `CUSTOMIZE`
- Privacy note: document hashed or anonymous identifiers only; do not expose direct identifiers.
