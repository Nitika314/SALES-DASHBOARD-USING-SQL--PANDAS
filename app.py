import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


# ---------------- CONFIG ---------------- #

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Password@123",
    "database": "sales"

}


# ---------------- DB CONNECTION ---------------- #

@st.cache_resource
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    return df


# ---------------- PAGE SETUP ---------------- #

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Analytics Dashboard")
st.markdown("ETL + MySQL + Streamlit Project")

st.divider()


# ---------------- KPI SECTION ---------------- #

st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

# Total Orders
orders_df = fetch_data(
    "SELECT COUNT(*) AS total_orders FROM orders_clean"
)
total_orders = orders_df["total_orders"][0]


# Total Revenue
revenue_df = fetch_data(
    "SELECT SUM(total_amount) AS revenue FROM orders_clean"
)
total_revenue = revenue_df["revenue"][0]


# Total Customers
customers_df = fetch_data("SELECT COUNT(*) AS total_customers FROM customers_clean")
total_customers = customers_df["total_customers"][0]

col1.metric("Total Orders", total_orders)
col2.metric("Total Revenue", f"₹ {round(total_revenue or 0,2)}")
col3.metric("Total Customers", total_customers)

st.divider()


# ---------------- ORDERS ANALYSIS ---------------- #

st.subheader("📦 Orders Analysis")

col1, col2 = st.columns(2)

# Orders by Status
status_df = fetch_data("""
SELECT order_status, COUNT(*) AS count
FROM orders_clean
GROUP BY order_status
""")

if not status_df.empty:

    fig, ax = plt.subplots()
    ax.bar(status_df["order_status"], status_df["count"])
    ax.set_title("Orders by Status")
    ax.set_xlabel("Status")
    ax.set_ylabel("Count")

    col1.pyplot(fig)

else:
    col1.info("No order status data available")


# Revenue Over Time
date_df = fetch_data("""
SELECT order_date, SUM(total_amount) AS revenue
FROM orders_clean
GROUP BY order_date
ORDER BY order_date
""")

if not date_df.empty:

    fig, ax = plt.subplots()
    ax.plot(date_df["order_date"], date_df["revenue"], marker="o")
    ax.set_title("Revenue Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")

    col2.pyplot(fig)

else:
    col2.info("No revenue date data available")

st.divider()


# ---------------- CUSTOMER ANALYSIS ---------------- #

st.subheader("👥 Customer Analysis")

col1, col2 = st.columns(2)

# Top Customers
top_customers = fetch_data("""
SELECT c.name, SUM(o.total_amount) AS total_spent
FROM orders_clean o
JOIN customers_clean c ON o.customer_id = c.id
GROUP BY c.name
ORDER BY total_spent DESC
LIMIT 5
""")


if not top_customers.empty:

    col1.markdown("### 💰 Top Customers")
    col1.dataframe(top_customers)

else:
    col1.info("No customer spending data")


# Customers by City
city_df = fetch_data("""
SELECT city, COUNT(*) AS count
FROM customers_clean
GROUP BY city
""")


if not city_df.empty:

    fig, ax = plt.subplots()
    ax.pie(city_df["count"], labels=city_df["city"], autopct="%1.1f%%")
    ax.set_title("Customers by City")

    col2.pyplot(fig)

else:
    col2.info("No city data available")

st.divider()


# ---------------- PRODUCT ANALYSIS ---------------- #

st.subheader("📦 Product Analysis")

col1, col2 = st.columns(2)
#Products by Category
category_df = fetch_data("""
SELECT category, COUNT(*) AS count
FROM products_clean
GROUP BY category
""")


if not category_df.empty:

    fig, ax = plt.subplots()
    ax.bar(category_df["category"], category_df["count"])
    ax.set_title("Products by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Count")

    col1.pyplot(fig)

else:
    col1.info("No category data available")


# Product Price Stats
price_df = fetch_data("""
SELECT
    MIN(price) AS min_price,
    MAX(price) AS max_price,
    AVG(price) AS avg_price
FROM products_clean
""")


if not price_df.empty:

    col2.markdown("### 💲 Product Price Summary")
    col2.dataframe(price_df)

else:
    col2.info("No price data available")

st.divider()


# ---------------- RAW DATA ---------------- #

st.subheader("📄 Raw Tables")

with st.expander("View Orders Table"):
    st.dataframe(fetch_data("SELECT * FROM orders_clean"))

with st.expander("View Customers Table"):
    st.dataframe(fetch_data("SELECT * FROM customers_clean"))

with st.expander("View Products Table"):
    st.dataframe(fetch_data("SELECT * FROM products_clean"))

