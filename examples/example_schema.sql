CREATE TABLE example_analytics.daily_activity (
    activity_date DATE NOT NULL,
    segment_name VARCHAR(100) NOT NULL,
    active_users BIGINT NOT NULL,
    sessions BIGINT NOT NULL
);

CREATE TABLE example_analytics.acquisition_funnel (
    cohort_date DATE NOT NULL,
    channel_name VARCHAR(100) NOT NULL,
    visitors BIGINT NOT NULL,
    signups BIGINT NOT NULL,
    activated_users BIGINT NOT NULL
);

CREATE TABLE example_analytics.retention_cohorts (
    cohort_date DATE NOT NULL,
    period_number INTEGER NOT NULL,
    segment_name VARCHAR(100) NOT NULL,
    cohort_users BIGINT NOT NULL,
    retained_users BIGINT NOT NULL
);
