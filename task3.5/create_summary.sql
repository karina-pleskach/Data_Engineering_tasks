CREATE TABLE summary AS
SELECT 
	year, 
	COUNT(*),
	ROUND(
		AVG(
			CASE
				WHEN LEFT(price, 1) = '$' THEN RIGHT(price, -1)::numeric(4,2)
				ELSE RIGHT(price, -1)::numeric(4,2)*1.2
			END
		), 
		2) AS average_USD_price
FROM book
GROUP BY year
ORDER BY year;