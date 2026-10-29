CREATE OR REPLACE FUNCTION generate_full_names(
    user_seed NUMERIC,
    user_locale_id SMALLINT,
    user_page_number INTEGER,
    user_page_size SMALLINT
)
RETURNS TABLE(full_name VARCHAR(200))
LANGUAGE SQL
AS $$
    SELECT
        CONCAT_WS(' ', title, first_name, middle_name, last_name, name_suffix)::VARCHAR(600) AS full_name
    FROM get_random_full_names(user_seed, user_locale_id, user_page_number, user_page_size);
$$;


SELECT *
FROM generate_full_names(0.42, 2::SMALLINT, 1, 100::SMALLINT);