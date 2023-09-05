-- В feed_actions для каждого юзера посчитаем число просмотров и лайков контента.

SELECT
    user_id,
    gender,
    age,
    DATE(time) as day,
    countIf(action='view') AS views,
    countIf(action='like') AS likes
FROM 
    simulator_20230720.feed_actions
GROUP BY 
     user_id, 
     day,
     gender,
     age

LIMIT 10