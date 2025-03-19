import pymysql
from operations.create_schema import connect_db

def create_views():
    """Creates SQL views for simplified data access."""
    connection = connect_db()
    cursor = connection.cursor()

    # View for sales per customer
    cursor.execute("""
        CREATE OR REPLACE VIEW view_customer_sales AS
        SELECT 
            o.customer_id,
            c.customer_city,
            c.customer_state,
            SUM(o.price) AS total_revenue,
            COUNT(o.order_id) AS total_orders
        FROM fact_orders o
        JOIN dim_customers c ON o.customer_id = c.customer_id
        GROUP BY o.customer_id, c.customer_city, c.customer_state;
    """)

    # View for sales per product category
    cursor.execute("""
        CREATE OR REPLACE VIEW view_product_sales AS
        SELECT 
            p.product_category_name,
            COUNT(o.order_id) AS total_orders,
            SUM(o.price) AS total_revenue
        FROM fact_orders o
        JOIN dim_products p ON o.product_id = p.product_id
        GROUP BY p.product_category_name;
    """)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Views created successfully!")

if __name__ == "__main__":
    create_views()
