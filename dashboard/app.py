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
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")
st.sidebar.title("📊 Sales Analytics Dashboard")

# Sidebar Navigation
option = st.sidebar.radio("Select Analysis:", [
    "Sales Performance Data Mart",
    "Product Category Analysis",
    "Aggregation Tables",
    "Views for Business Metrics",
    "Date-Based Sales Trends"
])

if option == "Sales Performance Data Mart":
    st.title("📊 Sales Performance Data Mart")
    df = fetch_data("SELECT * FROM dm_sales_performance order by total_revenue desc limit 20")
    st.dataframe(df)
    fig = px.bar(df, x='customer_state', y='total_revenue', title='Total Sales by State')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Product Category Analysis":
    st.title("📦 Product Category Analysis")
    df = fetch_data("SELECT * FROM dm_product_category_analysis order by total_revenue desc limit 10")
    st.dataframe(df)
    fig = px.pie(df, names='product_category_name', values='total_revenue', title='Revenue by Product Category')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Aggregation Tables":
    st.title("📈 Aggregation Tables Analysis")
    option = st.selectbox("Type of Table to display ?", ("Total Sales by Customer", "Revenue by Category", "Monthly sales summary", "Daily sales summary"))
    if option == "Daily sales summary":
        df = fetch_data("SELECT * FROM daily_sales_summary")
        st.dataframe(df)

    elif option == "Monthly sales summary":
         df = fetch_data("SELECT * FROM monthly_sales_summary where year=2017")
         st.dataframe(df)
         fig = px.line(df, x='month', y='total_revenue', title='Monthly Sales Trend')
         st.plotly_chart(fig, use_container_width=True)

    elif option == "Revenue by Category":
        df = fetch_data("SELECT * FROM revenue_by_category")
        st.dataframe(df)
        fig = px.line(df, x='product_category_name', y='total_revenue', title='Revenue By Category')
        st.plotly_chart(fig, use_container_width=True)
        

    elif option == "Total Sales by Customer":
        df = fetch_data("SELECT * FROM total_sales_by_customer")
        st.dataframe(df)
        
        

elif option == "Views for Business Metrics":
    st.title("📑 Business Metrics Overview")
    df = fetch_data("SELECT * FROM business_metrics_view")
    st.dataframe(df)
    fig = px.scatter(df, x='metric_name', y='metric_value', title='Business Metrics')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Date-Based Sales Trends":
    st.title("📆 Date-Based Sales Trends")
    df = fetch_data("SELECT * FROM date_sales_trends")
    st.dataframe(df)
    fig = px.area(df, x='date', y='total_sales', title='Daily Sales Trend')
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Developed for Sales Data Insights 📊")
