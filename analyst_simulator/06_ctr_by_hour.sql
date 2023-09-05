SELECT
  toStartOfHour(time) as day_hour,
  countIf(user_id, action = 'like') as likes,
  countIf(user_id, action = 'view') as views,
  likes / views as ctr
FROM
  simulator_20230720.feed_actions
WHERE
  day_hour between '2023-07-01' and '2023-07-20'
GROUP BY
  day_hour