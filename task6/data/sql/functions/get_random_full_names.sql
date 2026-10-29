CREATE OR REPLACE FUNCTION get_random_full_names(
    user_seed NUMERIC,
    user_locale_id SMALLINT,
    user_page_number INTEGER,
    user_page_size SMALLINT
)
RETURNS TABLE(
	row_num BIGINT, 
	first_name VARCHAR(50), 
	last_name VARCHAR(50), 
	middle_name VARCHAR(50), 
	title VARCHAR(20), 
	name_suffix VARCHAR(10),
	gender CHAR(1)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
		n.row_num, 
		n.value as first_name,
		COALESCE(s_f.value, s_m.value)::VARCHAR(120) as last_name, 
		CASE
			WHEN random() < 0.3 THEN COALESCE(m_n_f.value, m_n_m.value)::VARCHAR(120)
			ELSE NULL
		END as middle_name,
		CASE
			WHEN random() < 0.2 THEN (SELECT value
								    FROM title t
								    WHERE t.locale_id = user_locale_id AND t.gender = n.gender
								    ORDER BY random()
								    LIMIT 1)::VARCHAR(120)
			ELSE NULL
		END as title,
		CASE
			WHEN random() < 0.2 
				THEN (SELECT value
				    FROM name_suffix ns
				    WHERE ns.locale_id = user_locale_id AND ns.gender = n.gender
				    ORDER BY random()
				    LIMIT 1)::VARCHAR(120)
			ELSE NULL
		END as name_suffix,
		n.gender
	FROM get_random_name(user_seed, user_locale_id, user_page_number, user_page_size, 'first_name') as n
	LEFT JOIN get_random_name(user_seed, user_locale_id, user_page_number, user_page_size, 'last_name', 'F') as s_f
		ON n.row_num = s_f.row_num AND n.gender = s_f.gender
	LEFT JOIN get_random_name(user_seed, user_locale_id, user_page_number, user_page_size, 'last_name', 'M') as s_m
		ON n.row_num = s_m.row_num AND n.gender = s_m.gender
	LEFT JOIN get_random_name(user_seed+0.1, user_locale_id, user_page_number, user_page_size, 'first_name', 'F') as m_n_f
		ON n.row_num = m_n_f.row_num AND n.gender = m_n_f.gender
	LEFT JOIN get_random_name(user_seed+0.1, user_locale_id, user_page_number, user_page_size, 'first_name', 'M') as m_n_m
		ON n.row_num = m_n_m.row_num AND n.gender = m_n_m.gender;
END;
$$;

SELECT *
FROM get_random_full_names(0.42, 2::SMALLINT, 1, 100::SMALLINT);