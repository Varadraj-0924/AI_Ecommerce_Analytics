import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD DATASETS
# ============================================================

customers = pd.read_csv("../data/olist_customers_dataset.csv")
orders = pd.read_csv("../data/olist_orders_dataset.csv")
order_items = pd.read_csv("../data/olist_order_items_dataset.csv")
payments = pd.read_csv("../data/olist_order_payments_dataset.csv")
reviews = pd.read_csv("../data/olist_order_reviews_dataset.csv")
products = pd.read_csv("../data/olist_products_dataset.csv")
sellers = pd.read_csv("../data/olist_sellers_dataset.csv")
geolocation = pd.read_csv("../data/olist_geolocation_dataset.csv")
category_translation = pd.read_csv(
    "../data/product_category_name_translation.csv"
)

print("All datasets loaded successfully!")


# ============================================================
# 2. VIEW SAMPLE DATA
# ============================================================

print("\n--- CUSTOMERS ---")
print(customers.head())

print("\n--- ORDERS ---")
print(orders.head())

print("\n--- ORDER ITEMS ---")
print(order_items.head())

print("\n--- PRODUCTS ---")
print(products.head())


# ============================================================
# 3. DATASET SIZES
# ============================================================

print("\n--- DATASET SIZES ---")

print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Payments:", payments.shape)
print("Reviews:", reviews.shape)
print("Products:", products.shape)
print("Sellers:", sellers.shape)
print("Geolocation:", geolocation.shape)
print("Category Translation:", category_translation.shape)


# ============================================================
# 4. DATA INFORMATION
# ============================================================

print("\n--- ORDERS INFORMATION ---")
orders.info()

print("\n--- ORDER ITEMS INFORMATION ---")
order_items.info()

print("\n--- CUSTOMERS INFORMATION ---")
customers.info()

print("\n--- PRODUCTS INFORMATION ---")
products.info()


# ============================================================
# 5. MISSING VALUE ANALYSIS
# ============================================================

print("\n--- MISSING VALUES ---")

print("\nOrders:")
print(orders.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nCustomers:")
print(customers.isnull().sum())

print("\nOrder Items:")
print(order_items.isnull().sum())


# ============================================================
# 6. DUPLICATE ANALYSIS
# ============================================================

print("\n--- DUPLICATE RECORDS ---")

print("Customers:", customers.duplicated().sum())
print("Orders:", orders.duplicated().sum())
print("Order Items:", order_items.duplicated().sum())
print("Payments:", payments.duplicated().sum())
print("Reviews:", reviews.duplicated().sum())
print("Products:", products.duplicated().sum())
print("Sellers:", sellers.duplicated().sum())
print("Geolocation:", geolocation.duplicated().sum())
print("Category Translation:", category_translation.duplicated().sum())


# ============================================================
# 7. ID INTEGRITY CHECK
# ============================================================

print("\n--- ID INTEGRITY CHECK ---")

# Orders -> Customers
missing_customers = ~orders["customer_id"].isin(
    customers["customer_id"]
)

# Order Items -> Orders
missing_orders = ~order_items["order_id"].isin(
    orders["order_id"]
)

# Order Items -> Products
missing_products = ~order_items["product_id"].isin(
    products["product_id"]
)

# Order Items -> Sellers
missing_sellers = ~order_items["seller_id"].isin(
    sellers["seller_id"]
)

print(
    "Orders with missing customer:",
    missing_customers.sum()
)

print(
    "Order items with missing order:",
    missing_orders.sum()
)

print(
    "Order items with missing product:",
    missing_products.sum()
)

print(
    "Order items with missing seller:",
    missing_sellers.sum()
)


# ============================================================
# 8. DATE CONVERSION
# ============================================================

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"],
    errors="coerce"
)

print("\n--- DATE CONVERSION ---")
print(orders[date_columns].dtypes)

print("\nOrder item shipping date:")
print(order_items["shipping_limit_date"].dtype)


# ============================================================
# 9. REVENUE CALCULATION
# ============================================================

# IMPORTANT:
# order_item_id is NOT quantity.
# It is the sequence number of the item within an order.
# Therefore revenue = price.

order_items["revenue"] = order_items["price"]

# Product value + shipping cost
order_items["total_item_value"] = (
    order_items["price"]
    + order_items["freight_value"]
)

print("\n--- REVENUE CALCULATION ---")

print(
    order_items[
        [
            "order_id",
            "price",
            "freight_value",
            "revenue",
            "total_item_value"
        ]
    ].head()
)


# ============================================================
# 10. DELIVERY ANALYSIS
# ============================================================

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.days

print("\n--- DELIVERY ANALYSIS ---")

print(
    orders[
        [
            "order_id",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "delivery_days"
        ]
    ].head()
)


# ============================================================
# 11. LATE DELIVERY ANALYSIS
# ============================================================

orders["delivery_difference_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.days

orders["late_delivery"] = (
    orders["delivery_difference_days"] > 0
).astype(int)

print("\n--- LATE DELIVERY ANALYSIS ---")

print(
    orders[
        [
            "order_id",
            "order_estimated_delivery_date",
            "order_delivered_customer_date",
            "delivery_difference_days",
            "late_delivery"
        ]
    ].head()
)


# ============================================================
# 12. KPI SUMMARY
# ============================================================

total_orders = orders["order_id"].nunique()

total_customers = customers["customer_unique_id"].nunique()

total_revenue = order_items["revenue"].sum()

total_freight = order_items["freight_value"].sum()

average_order_value = (
    order_items
    .groupby("order_id")["total_item_value"]
    .sum()
    .mean()
)

average_delivery_days = orders["delivery_days"].mean()

late_delivery_rate = (
    orders["late_delivery"].mean() * 100
)

print("\n--- KPI SUMMARY ---")

print("Total Orders:", total_orders)

print("Total Customers:", total_customers)

print("Total Revenue:", round(total_revenue, 2))

print("Total Freight:", round(total_freight, 2))

print(
    "Average Order Value:",
    round(average_order_value, 2)
)

print(
    "Average Delivery Days:",
    round(average_delivery_days, 2)
)

print(
    "Late Delivery Rate:",
    round(late_delivery_rate, 2),
    "%"
)


# ============================================================
# 13. MONTHLY SALES ANALYSIS
# ============================================================

orders["order_month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M")
)

monthly_sales = (
    order_items
    .merge(
        orders[["order_id", "order_month"]],
        on="order_id",
        how="left"
    )
    .groupby("order_month")["revenue"]
    .sum()
    .reset_index()
)

print("\n--- MONTHLY SALES ---")
print(monthly_sales)


# ============================================================
# 14. MONTHLY REVENUE CHART
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["order_month"].astype(str),
    monthly_sales["revenue"],
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Revenue")
plt.title("Monthly Revenue Trend")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "../screenshots/monthly_revenue_trend.png",
    dpi=300
)

plt.show()


# ============================================================
# 15. TOP PRODUCT CATEGORIES
# ============================================================

category_sales = (
    order_items
    .merge(
        products[
            [
                "product_id",
                "product_category_name"
            ]
        ],
        on="product_id",
        how="left"
    )
)

category_sales = category_sales.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

category_sales["category"] = (
    category_sales[
        "product_category_name_english"
    ]
    .fillna(
        category_sales["product_category_name"]
    )
)

top_categories = (
    category_sales
    .groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

print("\n--- TOP 10 PRODUCT CATEGORIES ---")
print(top_categories)


# ============================================================
# 16. TOP PRODUCT CATEGORY CHART
# ============================================================

plt.figure(figsize=(10, 6))

plt.barh(
    top_categories["category"],
    top_categories["revenue"]
)

plt.xlabel("Revenue")
plt.ylabel("Product Category")
plt.title("Top 10 Product Categories by Revenue")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "../screenshots/top_10_product_categories.png",
    dpi=300
)

plt.show()


# ============================================================
# 17. CUSTOMER STATE ANALYSIS
# ============================================================

state_customers = (
    customers
    .groupby("customer_state")
    .size()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="customers")
)

print("\n--- TOP 10 CUSTOMER STATES ---")
print(state_customers)


# ============================================================
# 18. PAYMENT ANALYSIS
# ============================================================

payment_analysis = (
    payments
    .groupby("payment_type")["payment_value"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

print("\n--- PAYMENT TYPE ANALYSIS ---")
print(payment_analysis)


# ============================================================
# 19. ORDER STATUS ANALYSIS
# ============================================================

order_status_analysis = (
    orders
    .groupby("order_status")
    .size()
    .sort_values(ascending=False)
    .reset_index(name="orders")
)

print("\n--- ORDER STATUS ANALYSIS ---")
print(order_status_analysis)


# ============================================================
# END OF ANALYSIS
# ============================================================

print("\n========================================")
print("PYTHON EDA COMPLETED SUCCESSFULLY!")
print("========================================")


# ========================================
# BUSINESS INSIGHTS
# ========================================

print("\n--- BUSINESS INSIGHTS ---")


# 1. Top 10 product categories by revenue
category_data = order_items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

category_revenue = (
    category_data
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Categories by Revenue:")
print(category_revenue)


# 2. Top 10 sellers by revenue
seller_revenue = (
    order_items
    .groupby("seller_id")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Sellers by Revenue:")
print(seller_revenue)


# 3. Top 10 states by customers
state_orders = (
    customers
    .groupby("customer_state")["customer_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 States by Customers:")
print(state_orders)


# 4. Average Order Value by Payment Type

order_values = (
    order_items
    .groupby("order_id")["total_item_value"]
    .sum()
    .reset_index()
)

payment_order = payments[
    ["order_id", "payment_type"]
].drop_duplicates("order_id")

payment_aov = order_values.merge(
    payment_order,
    on="order_id",
    how="left"
)

payment_aov_result = (
    payment_aov
    .groupby("payment_type")["total_item_value"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Order Value by Payment Type:")
print(payment_aov_result)


# 5. Delivery performance by state

delivery_state = (
    orders
    .merge(
        customers[["customer_id", "customer_state"]],
        on="customer_id",
        how="left"
    )
    .groupby("customer_state")["delivery_days"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\nStates with Highest Average Delivery Time:")
print(delivery_state)


print("\n========================================")
print("BUSINESS INSIGHTS COMPLETED!")
print("========================================")


# ========================================
# MONTHLY REVENUE GROWTH
# ========================================

print("\n--- MONTHLY REVENUE GROWTH ---")

monthly_revenue = (
    order_items
    .merge(
        orders[["order_id", "order_purchase_timestamp"]],
        on="order_id",
        how="left"
    )
)

monthly_revenue["order_month"] = (
    monthly_revenue["order_purchase_timestamp"]
    .dt.to_period("M")
)

monthly_revenue = (
    monthly_revenue
    .groupby("order_month")["price"]
    .sum()
    .reset_index()
)

monthly_revenue["growth_percent"] = (
    monthly_revenue["price"]
    .pct_change() * 100
)

print(monthly_revenue)

print("\n========================================")
print("DAY 1 PYTHON ANALYSIS COMPLETED!")
print("========================================")