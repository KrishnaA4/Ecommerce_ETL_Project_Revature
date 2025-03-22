import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px

# Database connection function
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Krishna@3002",
        database="ecommerce_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to fetch data from MySQL
def fetch_data(query):
    connection = get_connection()
    df = pd.DataFrame()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            df = pd.DataFrame(data)
    finally:
        connection.close()
    return df

# Streamlit App Layout
st.set_page_config(page_title="Retail Data Analytics Dashboard", layout="wide")
st.sidebar.title("Retail Data Analytics Dashboard")

# Sidebar Navigation
option = st.sidebar.radio("Select Analysis:", [
    "Data Mart Analysis",
    "Aggregation Analysis",
    "KPI Analysis",
    "View Schema",
    "Project Summary"
])

if option == "Data Mart Analysis":
    option = st.selectbox("Choose one..", ("Sales Performance", "Product Category"))
    if option == "Sales Performance":
        st.title("Sales Performance Data Mart")
        df = fetch_data("SELECT * FROM dm_sales_performance order by total_revenue")
        st.dataframe(df)
        df1 = fetch_data("select customer_state,sum(total_revenue) as total_revenue from dm_sales_performance group by customer_state")
        fig = px.bar(df1, x='customer_state', y='total_revenue', title='Total Revenue by State')
        st.plotly_chart(fig, use_container_width=True)

    elif option == "Product Category":
         st.title("Product Category Analysis")
         df = fetch_data("SELECT * FROM dm_product_category_analysis order by product_category_name")
         st.dataframe(df)
         df1 = fetch_data("select product_category_name,sum(total_orders)  as  total_sales from dm_product_category_analysis group by product_category_name limit 20")
         fig = px.bar(df1, x='product_category_name', y='total_sales', title='Sales by Product Category')
         st.plotly_chart(fig, use_container_width=True)

elif option == "Aggregation Analysis":
    option = st.selectbox("Select one..", ("Total Sales by Customer", "Revenue by Category", "Monthly sales summary", "Daily sales summary"))
    if option == "Daily sales summary":
        df = fetch_data("SELECT * FROM daily_sales_summary order by date")
        st.dataframe(df)
        df1 = fetch_data("SELECT * FROM daily_sales_summary where date between '2017-01-01' and '2017-01-31' order by date")
        fig = px.line(df1, x='date', y='total_revenue', title='Daily Sales Trend of Jan-2017')
        st.plotly_chart(fig, use_container_width=True)

    elif option == "Monthly sales summary":
         df = fetch_data("SELECT * FROM monthly_sales_summary where year=2017 order by month desc")
         st.dataframe(df)
         fig = px.line(df, x='month', y='total_revenue', title='Monthly Sales Trend of 2017')
         st.plotly_chart(fig, use_container_width=True)

    elif option == "Revenue by Category":
        df = fetch_data("SELECT * FROM revenue_by_category order by total_revenue desc limit 20")
        st.dataframe(df)
        fig = px.line(df, x='product_category_name', y='total_revenue', title='Revenue By Category')
        st.plotly_chart(fig, use_container_width=True)
        

    elif option == "Total Sales by Customer":
        df = fetch_data("SELECT * FROM total_sales_by_customer")
        st.dataframe(df)
elif option == "KPI Analysis":
    option = st.selectbox("Select one..", ("Revenue by Payment Method", " Top 5 Best-Selling Product Categories", "Sales By State", "Number of Orders per Year"))
    if option == "Revenue by Payment Method":
        df = fetch_data("SELECT dp.payment_type,  SUM(dp.payment_value) AS total_revenue FROM dim_payments dp GROUP BY dp.payment_type ORDER BY total_revenue DESC")
        st.dataframe(df)
        fig = px.pie(df, names='payment_type', values='total_revenue', title='Revenue by Payment Method')
        st.plotly_chart(fig, use_container_width=True)

    elif option == " Top 5 Best-Selling Product Categories":
         df = fetch_data("SELECT dpc.product_category_name, SUM(dpc.total_orders) AS total_sales FROM dm_product_category_analysis dpc GROUP BY dpc.product_category_name ORDER BY total_sales DESC LIMIT 5;")
         st.dataframe(df)
         fig = px.bar(df, x='product_category_name', y='total_sales', title='Top 5 Best-Selling Product categories')
         st.plotly_chart(fig, use_container_width=True)

    elif option == "Sales By State":
        df = fetch_data("SELECT customer_state, sum(total_orders) as total_sales from dm_sales_performance group by customer_state order by customer_state")
        st.dataframe(df)
        fig = px.bar(df, x='customer_state', y='total_sales', title='Sales By State')
        st.plotly_chart(fig, use_container_width=True)
        

    elif option == "Number of Orders per Year":
        df = fetch_data("SELECT dd.year AS year, COUNT(fo.order_id) AS total_orders FROM fact_orders fo JOIN dim_dates dd ON fo.purchase_date_id = dd.date_id GROUP BY year")
        st.dataframe(df)
        fig = px.pie(df, names='year', values='total_orders', title='Number of Orders per Year')
        st.plotly_chart(fig, use_container_width=True)

elif option == "View Schema":
    st.title("Star Schema of Sales Project")
    st.image("dashboard/star_schema.png", use_container_width=True)


elif option == "Project Summary":
    st.title("Project Summary Report")

    st.markdown("""
    ## **1. Project Overview**  
    This project focuses on building a **Retail Data Analytics Dashboard** to analyze and visualize e-commerce retail data.  
    It integrates **MySQL** for data storage and **Streamlit** for interactive reporting. The dashboard provides key insights  
    on **sales performance, product trends, and business KPIs** using a **star schema-based data warehouse**.

    ## **2. Data Processing & Storage**  
    - **Data Cleaning & Transformation:** Missing values handled, optimized data types.  
    - **Star Schema Implementation:** Fact & Dimension tables for efficient querying.  
    - **Data Insertion into MySQL:** Used INSERT IGNORE to prevent duplicate records.  

    ## **3. Dashboard Features & Analysis**  
    - **Data Mart Analysis:** Sales performance, product category trends.  
    - **Aggregation Analysis:** Revenue trends, customer & category-wise sales.  
    - **KPI Analysis:** Payment methods, best-selling categories, sales by state.  
    - **Schema View:** Visual representation of the data model.  

    ## **4. Technologies Used**  
    - **Python & Streamlit** for dashboard development.  
    - **MySQL & pymysql** for database management.  
    - **Pandas & Plotly** for data processing & visualization.  

    ## **5. Key Outcomes**  
    - Fully interactive **Retail Data analytics dashboard**.  
    - **Optimized database structure** for fast querying.  
    - **Data-driven insights** into sales trends & business KPIs.  
    """)

st.sidebar.markdown("---")
