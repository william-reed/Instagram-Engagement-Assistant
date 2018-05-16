SELECT username, count(*) 
	FROM instagram_user
	JOIN comment USING (instagram_user_id)
	WHERE followers < 750 AND following < 750 AND type = 0
	GROUP BY username
	ORDER BY count(*) asc;