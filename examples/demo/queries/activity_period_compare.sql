SELECT
    CASE
        WHEN activity_date < '2026-01-22' THEN 'previous_7_days'
        ELSE 'current_7_days'
    END AS period_name,
    SUM(active_users) AS active_user_days,
    ROUND(AVG(active_users), 2) AS average_daily_active_users
FROM example_analytics.daily_activity
WHERE activity_date >= '2026-01-15'
  AND activity_date <= '2026-01-28'
GROUP BY period_name
ORDER BY period_name
LIMIT 10;
