CREATE TABLE stations(
  id integer PRIMARY KEY, 
  name varchar(50),
  latitude float, 
  longitude float
  );

CREATE TABLE users (
	id integer PRIMARY KEY, 
  type varchar(50), 
  gender integer, 
  birth_year integer
  );
 
CREATE TABLE bike_trips (
  id integer PRIMARY KEY, 
  time_duration integer, 
  start_datetime timestamp, 
  end_datetime timestamp,
  start_station_id integer REFERENCES stations(id), 
  end_station_id integer REFERENCES stations(id), 
  bike_id integer, 
  user_id integer REFERENCES users(id)
);

ALTER TABLE users
ADD UNIQUE (type, gender, birth_year);


CREATE OR REPLACE VIEW v_time_duration_per_month AS (
SELECT EXTRACT(MONTH FROM start_datetime) AS Month, 
AVG(time_duration) AS average_duration
FROM bike_trips
GROUP BY Month
ORDER BY Month
  );

CREATE OR REPLACE VIEW v_most_common_users AS (
SELECT users.type, 
			 users.birth_year, 
       users.gender, 
       user_counts.number_of_users
FROM users
LEFT JOIN 
(
SELECT user_id, 
		   COUNT(user_id) AS number_of_users
FROM bike_trips
GROUP BY user_id) user_counts
ON users.id = user_counts.user_id
ORDER BY user_counts.number_of_users DESC
  );

