SELECT
    activity_date,
    SUM(active_users) AS active_users
FROM example_analytics.daily_activity
WHERE activity_date >= DATE '2026-01-01'
  AND activity_date < DATE '2026-01-08'
GROUP BY activity_date
ORDER BY activity_date
LIMIT 100;
