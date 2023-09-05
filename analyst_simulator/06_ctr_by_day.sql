SELECT 
    DATE(time) AS day,
    countIf(user_id, action='like') as likes,
    countIf(user_id, action='view') as views,
    likes / views as CTR
FROM 
    simulator_20230720.feed_actions
GROUP BY 
    day