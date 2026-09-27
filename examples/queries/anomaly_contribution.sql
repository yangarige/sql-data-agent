WITH segment_daily AS (
    SELECT
        activity_date,
        segment_name,
        SUM(active_users) AS active_users
    FROM example_analytics.daily_activity
    WHERE activity_date >= DATE '{{baseline_start_date}}'
      AND activity_date <= DATE '{{target_date}}'
    GROUP BY activity_date, segment_name
),
baseline AS (
    SELECT
        segment_name,
        AVG(active_users) AS baseline_active_users
    FROM segment_daily
    WHERE activity_date < DATE '{{target_date}}'
    GROUP BY segment_name
),
target AS (
    SELECT
        segment_name,
        active_users AS target_active_users
    FROM segment_daily
    WHERE activity_date = DATE '{{target_date}}'
)
SELECT
    target.segment_name,
    target.target_active_users,
    baseline.baseline_active_users,
    target.target_active_users - baseline.baseline_active_users AS absolute_change
FROM target
JOIN baseline
  ON target.segment_name = baseline.segment_name
ORDER BY absolute_change
LIMIT 100;
