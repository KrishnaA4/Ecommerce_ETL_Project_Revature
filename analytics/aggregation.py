import pymysql
from operations.create_schema import connect_db

def create_aggregation_tables():
    """Creates aggregation tables for faster analytics."""
    connection = connect_db()
    cursor = connection.cursor()

    # Aggregate total sales per month
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agg_monthly_sales AS
        SELECT 
            d.year, d.month, 
            SUM(o.price) AS total_revenue,
            COUNT(o.order_id) AS total_orders
        FROM fact_orders o
        JOIN dim_dates d ON o.purchase_date_id = d.date_id
        GROUP BY d.year, d.month;
    """)

    # Aggregate top-selling products
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agg_top_products AS
        SELECT 
            p.product_category_name,
            COUNT(o.order_id) AS total_orders,
            SUM(o.price) AS total_revenue
        FROM fact_orders o
        JOIN dim_products p ON o.product_id = p.product_id
        GROUP BY p.product_category_name
        ORDER BY total_revenue DESC
        LIMIT 10;
    """)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Aggregation tables created successfully!")

if __name__ == "__main__":
    create_aggregation_tables()
