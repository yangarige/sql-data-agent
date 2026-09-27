SELECT
    cohort_date,
    segment_name,
    MAX(cohort_users) AS cohort_users,
    ROUND(
        1.0 * MAX(CASE WHEN period_number = 1 THEN retained_users END)
        / NULLIF(MAX(cohort_users), 0),
        4
    ) AS day_1_retention,
    ROUND(
        1.0 * MAX(CASE WHEN period_number = 7 THEN retained_users END)
        / NULLIF(MAX(cohort_users), 0),
        4
    ) AS day_7_retention
FROM example_analytics.retention_cohorts
WHERE cohort_date >= '2026-01-01'
  AND cohort_date <= '2026-01-22'
  AND period_number IN (1, 7)
GROUP BY cohort_date, segment_name
ORDER BY cohort_date, segment_name
LIMIT 100;
