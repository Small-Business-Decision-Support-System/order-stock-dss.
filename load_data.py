import pandas as pd
from database import get_connection

def load_csv():
    df = pd.read_csv("inventory_dataset.csv")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO products (
                product_name,
                initial_stock,
                daily_sales_rate,
                lead_time_days,
                unit_cost,
                ordering_cost,
                holding_cost
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row["Product_Name"],
            row["Initial_Stock"],
            row["Daily_Sales_Rate"],
            row["Lead_Time_Days"],
            row["Unit_Cost"],
            row["Ordering_Cost"],
            row["Holding_Cost"]
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("CSV data loaded successfully!")

load_csv()