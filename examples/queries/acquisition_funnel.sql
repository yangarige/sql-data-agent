SELECT
    channel_name,
    SUM(visitors) AS visitors,
    SUM(signups) AS signups,
    SUM(activated_users) AS activated_users,
    CASE
        WHEN SUM(visitors) > 0
        THEN 1.0 * SUM(signups) / SUM(visitors)
    END AS visitor_to_signup_rate,
    CASE
        WHEN SUM(signups) > 0
        THEN 1.0 * SUM(activated_users) / SUM(signups)
    END AS signup_to_activation_rate
FROM example_analytics.acquisition_funnel
WHERE cohort_date >= DATE '{{month_start}}'
  AND cohort_date < DATE '{{next_month_start}}'
GROUP BY channel_name
ORDER BY visitors DESC
LIMIT 100;
