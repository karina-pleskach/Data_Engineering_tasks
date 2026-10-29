CREATE OR REPLACE FUNCTION get_random_name(
    user_seed NUMERIC,
    user_locale_id SMALLINT,
    user_page_number INTEGER,
    user_page_size SMALLINT,
	table_name VARCHAR(20),
    user_gender CHAR(1) DEFAULT NULL
)
RETURNS TABLE(row_num BIGINT, value VARCHAR, gender CHAR(1))
LANGUAGE SQL
AS $$
    SELECT row_num, value, gender
    FROM get_random_gender_values(((user_seed + (user_page_number - 1) * 0.01 ) % 1), user_locale_id, user_page_number, user_page_size, table_name, user_gender);
$$;

SELECT *
FROM get_random_name(0.42, 2::SMALLINT, 1, 3::SMALLINT, 'first_name');