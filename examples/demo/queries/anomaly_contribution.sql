WITH segment_daily AS (
    SELECT
        activity_date,
        segment_name,
        SUM(active_users) AS active_users
    FROM example_analytics.daily_activity
    WHERE activity_date >= '2026-01-21'
      AND activity_date <= '2026-01-28'
    GROUP BY activity_date, segment_name
),
baseline AS (
    SELECT
        segment_name,
        AVG(active_users) AS baseline_active_users
    FROM segment_daily
    WHERE activity_date < '2026-01-28'
    GROUP BY segment_name
),
target AS (
    SELECT
        segment_name,
        active_users AS target_active_users
    FROM segment_daily
    WHERE activity_date = '2026-01-28'
)
SELECT
    target.segment_name,
    target.target_active_users,
    ROUND(baseline.baseline_active_users, 2) AS baseline_active_users,
    ROUND(target.target_active_users - baseline.baseline_active_users, 2) AS absolute_change
FROM target
JOIN baseline
  ON target.segment_name = baseline.segment_name
ORDER BY absolute_change
LIMIT 20;
