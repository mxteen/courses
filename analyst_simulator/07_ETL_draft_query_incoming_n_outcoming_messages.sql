-- В message_actions для каждого юзера считаем, 
-- * сколько он получает сообщений 
-- * сколько он отсылает сообщений,
-- * скольким людям он пишет,
-- * сколько людей пишут ему


SELECT
	day,
	gender,
	age,
	user,
	os,
	messages_sent,
	users_sent,
	messages_received,
	users_received
FROM
	(
		-- сколько сообщений отправляет пользователь 
		-- скольким людям пишет пользователь
		SELECT
			user_id AS user,
			gender,
			age,
			os,
			DATE(time) as day,
			COUNT(reciever_id) AS messages_sent,
			COUNT(DISTINCT reciever_id) AS users_sent  -- uniq(reciever_id) AS distinct_message_recievers
		FROM 
			simulator_20230720.message_actions
		WHERE 
			day = today() - 1
		GROUP BY 
			user,
			gender,
			age,
			os,
			day
	) AS qry_sent_msgs
	FULL OUTER JOIN
	(
		-- сколько пользователь получает сообщений 
		-- сколько людей пишет пользователю
		SELECT
			reciever_id AS user,
			gender,
			age,
			os,
			DATE(time) as day,
			COUNT(user_id) AS messages_received,
			COUNT(DISTINCT user_id) AS users_received
		FROM 
			simulator_20230720.message_actions
		WHERE 
			day = today() - 1
		GROUP BY 
			user,
			gender,
			age,
			os,
			day	
	) AS qry_recieved_msgs
	USING user
LIMIT 10