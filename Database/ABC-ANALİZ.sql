WITH SatisVerisi AS (
    SELECT 
        c1 AS Product_Name,
        -- c3 (Miktar) * c5 (Fiyat) çarpımı
        (CAST(c3 AS REAL) * CAST(c5 AS REAL)) AS Sales_Value
    FROM inventory_table
    -- İlk satırda başlıklar (Product_Name yazısı) kalmış olabilir, onu eliyoruz
    WHERE c1 != 'Product_Name'
),
KumulatifHesap AS (
    SELECT 
        Product_Name,
        Sales_Value,
        SUM(Sales_Value) OVER (ORDER BY Sales_Value DESC) AS Cumulative_Sum,
        SUM(Sales_Value) OVER () AS Total_Sum
    FROM SatisVerisi
)
SELECT 
    Product_Name,
    ROUND(Sales_Value, 2) AS Value,
    ROUND((Cumulative_Sum * 100.0 / Total_Sum), 2) AS Cumulative_Percentage,
    CASE 
        WHEN (Cumulative_Sum * 1.0 / Total_Sum) <= 0.80 THEN 'A'
        WHEN (Cumulative_Sum * 1.0 / Total_Sum) <= 0.95 THEN 'B'
        ELSE 'C'
    END AS ABC_Category
FROM KumulatifHesap
ORDER BY Sales_Value DESC;