USE refined;

SELECT
    s.customer_id,
    s.date,
    p.quantity,
    p.price
FROM
    sales s
JOIN
    products p ON s.product_id = p.product_id
ORDER BY
    s.customer_id,
    s.date;