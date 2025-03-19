import pymysql
import pandas as pd
from operations.create_schema import connect_db

def get_product_category_sales():
    """Fetches total sales by product category."""
    connection = connect_db()
    query = """
        SELECT 
            p.product_category_name,
            COUNT(o.order_id) AS total_orders,
            SUM(o.price) AS total_revenue
        FROM fact_orders o
        JOIN dim_products p ON o.product_id = p.product_id
        GROUP BY p.product_category_name
        ORDER BY total_revenue DESC;
    """
    df = pd.read_sql(query, connection)
    connection.close()
    return df

if __name__ == "__main__":
    df = get_product_category_sales()
    print(df.head())  # For testing
