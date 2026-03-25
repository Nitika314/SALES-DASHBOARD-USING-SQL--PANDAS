
import os
import pandas as pd
import numpy as np
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

password = quote_plus(os.getenv("DB_PASS"))

url = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{password}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(url)



# -----------------------------
# Extract Data
# -----------------------------
customers = pd.read_sql("SELECT * FROM customers", engine)
products = pd.read_sql("SELECT * FROM products", engine)
orders = pd.read_sql("SELECT * FROM orders", engine)
details = pd.read_sql("SELECT * FROM order_details", engine)

print("Data Extracted")

# -----------------------------
# Cleaning: Customers
# -----------------------------

# Remove duplicates
customers = customers.drop_duplicates(subset=["email"], keep="first")

# Fill missing values
customers["city"] = customers["city"].fillna("Unknown")
customers["email"] = customers["email"].fillna("no_email@unknown.com")

# -----------------------------
# Cleaning: Products
# -----------------------------

# Fill missing price with mean
products["price"] = products["price"].fillna(products["price"].mean())

# Remove invalid prices
products = products[products["price"] > 0]

# -----------------------------
# Cleaning: Orders
# -----------------------------

# Convert date
orders["order_date"] = pd.to_datetime(orders["order_date"])

# Keep only valid orders
valid_status = ["paid", "delivered", "shipped"]
orders = orders[orders["order_status"].isin(valid_status)]

# Remove negative/zero orders
orders = orders[orders["total_amount"] > 0]

# -----------------------------
# Cleaning: Order Details
# -----------------------------

# Remove invalid subtotal
details = details[details["subtotal"] > 0]

# Merge price for recalculation
details = details.merge(
    products[["id", "price"]],
    left_on="product_id",
    right_on="id",
    how="left"
)

# Recalculate subtotal
details["clean_subtotal"] = details["quantity"] * details["price"]

details = details.drop(columns=["id_y"])
details = details.rename(columns={"id_x": "id"})

# -----------------------------
# Feature Engineering
# -----------------------------

# Add month column
orders["month"] = orders["order_date"].dt.to_period("M").astype(str)

# Customer Lifetime Value
clv = orders.groupby("customer_id")["total_amount"].sum().reset_index()
clv.columns = ["customer_id", "lifetime_value"]

# -----------------------------
# Load Clean Data Back
# -----------------------------

customers.to_sql("customers_clean", engine, if_exists="replace", index=False)
products.to_sql("products_clean", engine, if_exists="replace", index=False)
orders.to_sql("orders_clean", engine, if_exists="replace", index=False)
details.to_sql("order_details_clean", engine, if_exists="replace", index=False)
clv.to_sql("customer_ltv", engine, if_exists="replace", index=False)

print("Clean Data Loaded Successfully")
