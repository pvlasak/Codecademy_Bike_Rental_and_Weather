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

CREATE TABLE weather (
	date date PRIMARY KEY, 
  avg_wind_speed_ms float, 
  precipitation_mm float, 
  snowfall_mm float, 
  snowdepth_mm float, 
  avg_temp_f integer, 
  max_temp_f integer, 
  min_temp_f integer, 
  sunshine_min float
  );  
  
  
ALTER TABLE users
ADD UNIQUE (type, gender, birth_year);

/* --------------------------------------------------------------*/
/* View containing average trip duration in each month. */
/* --------------------------------------------------------------*/
CREATE OR REPLACE VIEW v_time_duration_per_month AS (
SELECT EXTRACT(MONTH FROM start_datetime) AS Month, 
AVG(time_duration) AS average_duration
FROM bike_trips
GROUP BY Month
ORDER BY Month
  );


/* --------------------------------------------------------------*/
/* View shows the most typical category of user that use bike rental service.
/* --------------------------------------------------------------*/
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

/* --------------------------------------------------------------*/
/* Number of trips in relationship to weather conditions such as average monthly
/* temperature and wind speed.
/* --------------------------------------------------------------*/
CREATE OR REPLACE VIEW v_number_of_trips_vs_weather AS (
WITH temporary_table AS (
  SELECT date(start_datetime) AS datum,
  		 EXTRACT(MONTH FROM start_datetime) AS month
  FROM bike_trips)
SELECT temporary_table.month, 
	   ROUND(CAST(AVG(weather.avg_wind_speed_ms) AS numeric),2) AS Average_monthly_windspeed, 
       ROUND(AVG(weather.avg_temp_f),1) AS Average_monthly_temperature_F,
       ROUND(AVG((weather.avg_temp_f - 32)*0.5556),1) AS Average_monthly_temperature_C,
       COUNT(*) as number_of_trips
FROM temporary_table
LEFT JOIN weather
	ON weather.date = temporary_table.datum
GROUP BY temporary_table.month
ORDER BY temporary_table.month
);


/* --------------------------------------------------------------*/
/* Daily change of bike trip counts with respect to weekday (week/weekend)
/* and weather conditions like average daily temperature, wind speed and 
/* daily precipitation in mm. 
/* --------------------------------------------------------------*/

CREATE OR REPLACE VIEW v_daily_change_vs_weather AS (
WITH trip_count_change AS(
SELECT base.datum, 
  	   MAX(base.weekend) as Weekend,
	   COUNT(*) AS trip_count,
       COUNT(*) - LAG(COUNT(*), 1,0) OVER (
       ORDER BY base.datum) as daily_change
FROM
	(SELECT date(start_datetime) AS datum, 
   		    CASE WHEN (EXTRACT(DOW FROM start_datetime)) in (0,6) THEN 1 ELSE 0 END AS weekend
    FROM bike_trips
    ORDER BY datum
    ) base
GROUP BY base.datum
),
weather_join AS(
SELECT trip_count_change.*, 
	   (weather.avg_temp_f - 32)*0.5556 AS Avg_temp_celsius,
  	   weather.avg_wind_speed_ms,
  	   weather.precipitation_mm
FROM trip_count_change
	LEFT JOIN weather
	ON trip_count_change.datum = weather.date
)
SELECT *
FROM weather_join
ORDER BY daily_change ASC
);
  
/* --------------------------------------------------------------*/
/* Monthly running total count of bike trips
/* --------------------------------------------------------------*/  
CREATE OR REPLACE VIEW v_running_total_count AS (
WITH monthly_counts AS (
  SELECT  EXTRACT(MONTH FROM start_datetime) AS month,
          COUNT(*) as counts
	FROM bike_trips
	GROUP BY month
	ORDER BY month
  ) 
SELECT *, 
  	   SUM(counts) OVER (
           ORDER BY month) AS running_total
FROM monthly_counts
 );
 
/* --------------------------------------------------------------*/
/* Monthly running total count per stations
/* --------------------------------------------------------------*/  
CREATE OR REPLACE VIEW v_running_total_per_month_and_stations AS (
WITH month_and_stations AS (
  SELECT  start_datetime, 
  		  EXTRACT(MONTH FROM start_datetime) AS month,
          start_station_id
	FROM bike_trips
), counts_per_station AS (
SELECT month, 
  	   start_station_id, 
  	   COUNT(*) AS trip_counts
FROM month_and_stations
GROUP BY month, start_station_id
ORDER BY start_station_id
  ), 
running_total AS (
SELECT *, 
	   SUM(trip_counts) OVER (
       PARTITION BY start_station_id
       ORDER BY month) AS running_total
FROM counts_per_station
)
SELECT stations.name,
	   running_total.month, 
	   running_total.trip_counts, 
       running_total.running_total
FROM running_total
LEFT JOIN stations
	ON running_total.start_station_id = stations.id
);