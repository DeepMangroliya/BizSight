SELECT
    s.customer_id,
    s.date,
    p.quantity,
    p.price
FROM
    refined.sales s
JOIN
    refined.products p ON s.product_id = p.product_id
ORDER BY
    s.customer_id,
    s.date;