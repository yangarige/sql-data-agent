WITH daily AS (
    SELECT
        activity_date,
        SUM(active_users) AS active_users
    FROM example_analytics.daily_activity
    WHERE activity_date >= DATE '{{comparison_start_date}}'
      AND activity_date < DATE '{{current_end_date_exclusive}}'
    GROUP BY activity_date
)
SELECT
    activity_date,
    active_users
FROM daily
ORDER BY activity_date
LIMIT 100;
