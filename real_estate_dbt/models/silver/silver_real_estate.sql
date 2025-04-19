WITH raw AS (
    SELECT * FROM {{ ref('bronze_real_estate') }}
)
SELECT
    title,
    price::numeric AS price_brl, -- Use NUMERIC para cálculos futuros
    size::numeric AS size_sqm,
    bedrooms::integer AS bedrooms,
    bathrooms::integer AS bathrooms,
    parking_spaces::integer AS parking_spaces,
    link,
    CASE
        WHEN size IS NULL THEN 'Size not available'
        ELSE CAST(size AS TEXT)
    END AS size_display,
    CASE
        WHEN bedrooms IS NULL THEN 'Number of bedrooms not available'
        ELSE CAST(bedrooms AS TEXT)
    END AS bedrooms_display,
    CASE
        WHEN bathrooms IS NULL THEN 'Number of bathrooms not available'
        ELSE CAST(bathrooms AS TEXT)
    END AS bathrooms_display,
    CASE
        WHEN parking_spaces IS NULL THEN 'Number of parking spaces not available'
        ELSE CAST(parking_spaces AS TEXT)
    END AS parking_spaces_display
FROM raw
WHERE link IS NOT NULL