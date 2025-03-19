import pymysql
import pandas as pd
from operations.create_schema import connect_db

def get_sales_trends():
    """Fetches monthly and yearly sales trends."""
    connection = connect_db()
    query = """
        SELECT 
            d.year, d.month, 
            SUM(o.price) AS total_revenue,
            COUNT(o.order_id) AS total_orders
        FROM fact_orders o
        JOIN dim_dates d ON o.purchase_date_id = d.date_id
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month;
    """
    df = pd.read_sql(query, connection)
    connection.close()
    return df

if __name__ == "__main__":
    df = get_sales_trends()
    print(df.head())  # For testing
