WITH silver AS (
    SELECT *
    FROM {{ ref('silver_real_estate') }}
),

price_brackets AS (
    SELECT
        *,
        CASE
            WHEN price_brl < 300000 THEN 'Up to R$ 300,000'
            WHEN price_brl BETWEEN 300000 AND 600000 THEN 'R$ 300,000 - R$ 600,000'
            WHEN price_brl BETWEEN 600000 AND 1000000 THEN 'R$ 600,000 - R$ 1,000,000'
            ELSE 'Above R$ 1,000,000'
        END AS price_range,
        
        CASE
            WHEN size_sqm < 50 THEN 'Less than 50 m²'
            WHEN size_sqm BETWEEN 50 AND 80 THEN '50 - 80 m²'
            WHEN size_sqm BETWEEN 80 AND 120 THEN '80 - 120 m²'
            ELSE 'Above 120 m²'
        END AS size_range
    FROM silver
)

SELECT
    pb.price_range AS "Price Range",
    pb.size_range AS "Size Range",
    COUNT(*) AS "Total Apartments",
    SUM(CASE WHEN parking_spaces > 0 THEN 1 ELSE 0 END) AS "With Parking",
    SUM(CASE WHEN parking_spaces = 0 OR parking_spaces IS NULL THEN 1 ELSE 0 END) AS "Without Parking",
    SUM(CASE WHEN bathrooms > 1 THEN 1 ELSE 0 END) AS "With More Than 1 Bathroom",
    SUM(CASE WHEN bedrooms > 1 THEN 1 ELSE 0 END) AS "With More Than 1 Bedroom",
    ROUND(AVG(pb.price_brl), 0) AS "Average Price (R$)",
    ROUND(AVG(pb.size_sqm), 1) AS "Average Size (m²)",
    ROUND(AVG(pb.bedrooms), 1) AS "Average Bedrooms",
    ROUND(AVG(pb.bathrooms), 1) AS "Average Bathrooms",
    ROUND(AVG(pb.parking_spaces), 1) AS "Average Parking Spaces"
FROM price_brackets pb
GROUP BY pb.price_range, pb.size_range
ORDER BY pb.price_range, pb.size_range
