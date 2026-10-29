CREATE TABLE temp_male_names (
    name VARCHAR(50),
    occurrences INTEGER
);

CREATE TABLE temp_female_names (
    name VARCHAR(50),
    occurrences INTEGER
);

INSERT INTO last_name (locale_id, value, gender)
SELECT 
	(SELECT locale_id
	FROM locale
	WHERE language_code = 'pl'
  		AND country_code = 'PL'), 
	name, 
	'M'
FROM temp_male_names;

INSERT INTO last_name (locale_id, value, gender)
SELECT 
	(SELECT locale_id
	FROM locale
	WHERE language_code = 'pl'
  		AND country_code = 'PL'), 
	name, 
	'F'
FROM temp_female_names;

DROP TABLE temp_male_names;
DROP TABLE temp_female_names;
