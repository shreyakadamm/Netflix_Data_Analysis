
DROP DATABASE IF EXISTS netflix_db;
CREATE DATABASE netflix_db;

USE netflix_db;



CREATE TABLE netflix (

show_id VARCHAR(20) PRIMARY KEY,

type VARCHAR(20),

title VARCHAR(300),

director TEXT,

cast TEXT,

country TEXT,

date_added DATE,

release_year INT,

rating VARCHAR(20),

duration VARCHAR(30),

listed_in TEXT,

description TEXT,

year_added INT,

month_added VARCHAR(20),

day_added INT,

duration_num INT,

duration_type VARCHAR(20),

primary_genre VARCHAR(100),

primary_country VARCHAR(100),

decade INT,

content_age INT

);


/*

OPTION 1

Use MySQL Workbench

Table Data Import Wizard

Import

output/netflix_cleaned.csv

-------------------------------------------------

OPTION 2

LOAD DATA INFILE

(Change path according to your PC)

*/

LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/netflix_cleaned.csv'
INTO TABLE netflix
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



SELECT * FROM netflix
LIMIT 10;



SELECT COUNT(*) AS Total_Titles
FROM netflix;



SELECT COUNT(*) AS Total_Movies
FROM netflix
WHERE type='Movie';



SELECT COUNT(*) AS Total_TV_Shows
FROM netflix
WHERE type='TV Show';



SELECT COUNT(DISTINCT primary_country) AS Countries
FROM netflix;



SELECT COUNT(DISTINCT primary_genre) AS Genres
FROM netflix;



SELECT COUNT(DISTINCT director) AS Directors
FROM netflix;


SELECT MAX(release_year)
AS Latest_Release
FROM netflix;



SELECT MIN(release_year)
AS Oldest_Release
FROM netflix;



SELECT

primary_country,

COUNT(*) AS Total

FROM netflix

GROUP BY primary_country

ORDER BY Total DESC

LIMIT 10;



SELECT

primary_genre,

COUNT(*) AS Total

FROM netflix

GROUP BY primary_genre

ORDER BY Total DESC

LIMIT 10;



SELECT

rating,

COUNT(*) AS Total

FROM netflix

GROUP BY rating

ORDER BY Total DESC;



SELECT *

FROM netflix

WHERE primary_country='India'

AND type='Movie';



SELECT

title,

release_year

FROM netflix

WHERE release_year>=2020

ORDER BY release_year DESC;


SELECT

title,

duration_num

FROM netflix

WHERE type='Movie'

ORDER BY duration_num DESC

LIMIT 10;



SELECT

director,

COUNT(*) AS Movies

FROM netflix

WHERE director<>'Unknown'

GROUP BY director

ORDER BY Movies DESC

LIMIT 10;



SELECT
    cast,
    COUNT(*) AS total_titles
FROM netflix
WHERE cast <> 'Not Available'
GROUP BY cast
ORDER BY total_titles DESC
LIMIT 10;



SELECT
    ROUND(AVG(duration_num),2) AS average_movie_duration
FROM netflix
WHERE type='Movie';



SELECT
    ROUND(AVG(duration_num),2) AS average_seasons
FROM netflix
WHERE type='TV Show';


SELECT
    year_added,
    COUNT(*) AS total_titles
FROM netflix
GROUP BY year_added
ORDER BY year_added;



SELECT
    month_added,
    COUNT(*) AS total_titles
FROM netflix
GROUP BY month_added
ORDER BY total_titles DESC;



SELECT
    decade,
    COUNT(*) AS total_titles
FROM netflix
GROUP BY decade
ORDER BY decade;



SELECT
    primary_country,
    COUNT(*) AS total_titles
FROM netflix
GROUP BY primary_country
HAVING COUNT(*) > 100
ORDER BY total_titles DESC;



SELECT
    primary_genre,
    COUNT(*) AS total_titles
FROM netflix
GROUP BY primary_genre
HAVING COUNT(*) > 50
ORDER BY total_titles DESC;



SELECT
    type,
    COUNT(*) AS total
FROM netflix
GROUP BY type;



SELECT
ROUND(
100 * SUM(type='Movie') / COUNT(*),2
) AS movie_percentage
FROM netflix;


SELECT
ROUND(
100 * SUM(type='TV Show') / COUNT(*),2
) AS tv_show_percentage
FROM netflix;




SELECT
title,
release_year
FROM netflix
WHERE release_year>2015
ORDER BY release_year DESC;



SELECT
rating,
COUNT(*) AS total
FROM netflix
GROUP BY rating
ORDER BY total DESC;



SELECT
primary_country,
COUNT(*) AS total_movies
FROM netflix
WHERE type='Movie'
GROUP BY primary_country
ORDER BY total_movies DESC;


SELECT
primary_country,
COUNT(*) AS total_tvshows
FROM netflix
WHERE type='TV Show'
GROUP BY primary_country
ORDER BY total_tvshows DESC;



SELECT
    director,
    total_movies,
    RANK() OVER(ORDER BY total_movies DESC) AS director_rank
FROM
(
    SELECT
        director,
        COUNT(*) AS total_movies
    FROM netflix
    WHERE director <> 'Unknown'
    GROUP BY director
) t
LIMIT 5;


SELECT
    primary_genre,
    total_titles,
    DENSE_RANK() OVER(ORDER BY total_titles DESC) AS genre_rank
FROM
(
    SELECT
        primary_genre,
        COUNT(*) AS total_titles
    FROM netflix
    GROUP BY primary_genre
) g;



SELECT
title,

CASE

WHEN content_age <= 5 THEN 'New'

WHEN content_age BETWEEN 6 AND 10 THEN 'Recent'

WHEN content_age BETWEEN 11 AND 20 THEN 'Old'

ELSE 'Classic'

END AS Content_Category

FROM netflix;



SELECT
title,
duration_num
FROM netflix
WHERE type='Movie'
AND duration_num >
(
SELECT AVG(duration_num)
FROM netflix
WHERE type='Movie'
);


WITH CountryCount AS
(
SELECT
primary_country,
COUNT(*) AS total_titles
FROM netflix
GROUP BY primary_country
)

SELECT *
FROM CountryCount
ORDER BY total_titles DESC
LIMIT 1;



WITH GenreCount AS
(
SELECT
primary_genre,
COUNT(*) AS total_titles
FROM netflix
GROUP BY primary_genre
)

SELECT *
FROM GenreCount
ORDER BY total_titles DESC
LIMIT 1;



SELECT

title,

release_year,

ROW_NUMBER() OVER(
ORDER BY release_year DESC
) AS Row_No

FROM netflix;



SELECT

release_year,

COUNT(*) AS yearly_titles,

SUM(COUNT(*))
OVER(
ORDER BY release_year
) AS running_total

FROM netflix

GROUP BY release_year;



SELECT

director,

COUNT(*) AS total_titles,

SUM(type='Movie') AS movies,

SUM(type='TV Show') AS tv_shows

FROM netflix

WHERE director<>'Unknown'

GROUP BY director

ORDER BY total_titles DESC;



SELECT

COUNT(*) AS Total_Titles,

SUM(type='Movie') AS Movies,

SUM(type='TV Show') AS TV_Shows,

COUNT(DISTINCT primary_country) AS Countries,

COUNT(DISTINCT primary_genre) AS Genres,

COUNT(DISTINCT director) AS Directors,

ROUND(AVG(
CASE
WHEN type='Movie'
THEN duration_num
END
),2) AS Avg_Movie_Duration,

MIN(release_year) AS Oldest_Release,

MAX(release_year) AS Latest_Release

FROM netflix;
