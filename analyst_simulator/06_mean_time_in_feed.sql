SELECT
  day,
  median(duration_minutes),
  AVG(duration_minutes)
FROM
  (
    SELECT
      user_id,
      DATE(time) as day,
      MIN(time) as min_time,
      MAX(time) as max_time,
      (max_time - min_time) / 60 as duration_minutes
    FROM
      simulator_20230720.feed_actions
    GROUP BY
      user_id,
      day
  )
GROUP BY day