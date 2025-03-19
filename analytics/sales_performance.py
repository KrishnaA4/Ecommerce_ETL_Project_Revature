import pymysql
import pandas as pd
from operations.create_schema import connect_db

def get_sales_performance():
    """Fetches sales performance metrics from the database."""
    connection = connect_db()
    query = """
        SELECT 
            o.customer_id,
            c.customer_city,
            c.customer_state,
            SUM(o.price) AS total_revenue,
            COUNT(o.order_id) AS total_orders
        FROM fact_orders o
        JOIN dim_customers c ON o.customer_id = c.customer_id
        GROUP BY o.customer_id, c.customer_city, c.customer_state
        ORDER BY total_revenue DESC;
    """
    df = pd.read_sql(query, connection)
    connection.close()
    return df

if __name__ == "__main__":
    df = get_sales_performance()
    print(df.head())  # For testing
