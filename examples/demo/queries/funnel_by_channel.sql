SELECT
    channel_name,
    SUM(visitors) AS visitors,
    SUM(signups) AS signups,
    SUM(activated_users) AS activated_users,
    ROUND(1.0 * SUM(signups) / NULLIF(SUM(visitors), 0), 4) AS signup_rate,
    ROUND(1.0 * SUM(activated_users) / NULLIF(SUM(signups), 0), 4) AS activation_rate
FROM example_analytics.acquisition_funnel
WHERE cohort_date >= '2026-01-01'
  AND cohort_date < '2026-02-01'
GROUP BY channel_name
ORDER BY visitors DESC
LIMIT 20;
