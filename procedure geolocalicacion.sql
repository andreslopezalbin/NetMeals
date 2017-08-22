USE netmeals;
DELIMITER $$
DROP PROCEDURE IF EXISTS geodist $$
CREATE PROCEDURE geodist(IN init_lat float, IN init_lon float, IN dist int)	
BEGIN
	declare lon1 float; 
	declare lon2 float;
	declare lat1 float; 
	declare lat2 float;

	-- calculate lon and lat for the rectangle:
	set lon1 = init_lon - dist/abs(cos(radians(init_lat))*69);
	set lon2 = init_lon + dist/abs(cos(radians(init_lat))*69);
	set lat1 = init_lat - (dist/69); 
	set lat2 = init_lat + (dist/69);
	 -- run the query:
	 
	(SELECT 'activity', a_t.id,
		3956 * 2 * ASIN(SQRT( POWER(SIN((init_lat - latitude) * pi()/180 / 2), 2) +COS(init_lat * pi()/180) * COS(latitude * pi()/180) *POWER(SIN((init_lon - longitude) * pi()/180 / 2), 2) )) as distance 
	FROM activities_activity a
	RIGHT JOIN activities_activitytime a_t ON(a_t.activity_id = a.id)
	WHERE longitude between lon1 and lon2 and latitude between lat1 and lat2 
		AND a_t.date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
	having distance < dist)
	
	UNION
	
	(SELECT 'dish', id,
		3956 * 2 * ASIN(SQRT( POWER(SIN((init_lat - latitude) * pi()/180 / 2), 2) +COS(init_lat * pi()/180) * COS(latitude * pi()/180) *POWER(SIN((init_lon - longitude) * pi()/180 / 2), 2) )) as distance 
	FROM activities_dish
	WHERE longitude between lon1 and lon2 and latitude between lat1 and lat2 
		AND date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
	having distance < dist)
	
	ORDER BY distance
    limit 100;
END $$
DELIMITER ;