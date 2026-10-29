CREATE OR REPLACE FUNCTION get_random_gender_values(
    user_seed NUMERIC,
    user_locale_id SMALLINT,
    user_page_number INTEGER,
    user_page_size SMALLINT,
    table_name VARCHAR(20),
	user_gender CHAR(1) DEFAULT NULL
)
RETURNS TABLE(row_num BIGINT, value VARCHAR(50), gender CHAR(1))
LANGUAGE plpgsql
AS $$
BEGIN
    PERFORM setseed(user_seed);
    RETURN QUERY EXECUTE format(
		'SELECT row_number() OVER () AS row_num, value, gender
		 FROM (
		     SELECT INITCAP(value)::VARCHAR(50) as value, gender
		     FROM %I
		     WHERE locale_id = $1
		       AND ($4 IS NULL OR gender = $4)
		     ORDER BY random()
		     LIMIT $2
		 ) AS shuffled',
        table_name
    )
    USING user_locale_id, user_page_size, user_page_number, user_gender;
END;
$$;
