SELECT
    cohort_date,
    segment_name,
    MAX(cohort_users) AS cohort_users,
    MAX(
        CASE
            WHEN period_number = 1 AND cohort_users > 0
            THEN 1.0 * retained_users / cohort_users
        END
    ) AS day_1_retention,
    MAX(
        CASE
            WHEN period_number = 7 AND cohort_users > 0
            THEN 1.0 * retained_users / cohort_users
        END
    ) AS day_7_retention
FROM example_analytics.retention_cohorts
WHERE cohort_date >= DATE '{{first_fully_observed_cohort}}'
  AND cohort_date <= DATE '{{last_fully_observed_cohort}}'
  AND period_number IN (1, 7)
GROUP BY cohort_date, segment_name
ORDER BY cohort_date, segment_name
LIMIT 1000;
