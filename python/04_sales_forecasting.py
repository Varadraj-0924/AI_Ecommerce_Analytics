import pandas as pd

# Load monthly sales data
sales = pd.read_csv("monthly_sales.csv")

print("Monthly sales data loaded successfully!")
print("Original shape:", sales.shape)

# Convert date column to datetime
sales["order_month"] = pd.to_datetime(sales["order_month"])

# Sort by month
sales = sales.sort_values("order_month")

# Remove September 2018 because it is a partial month
sales = sales[sales["order_month"] < "2018-09-01"]

# Create continuous monthly timeline
sales = sales.set_index("order_month")

sales = sales.asfreq("MS")

# Fill missing months with 0 revenue
sales["revenue"] = sales["revenue"].fillna(0)

# Reset index
sales = sales.reset_index()

print("\nForecasting data prepared successfully!")
print("Shape:", sales.shape)

print("\nPrepared dataset:")
print(sales)

# Save prepared dataset
sales.to_csv("forecasting_data.csv", index=False)

print("\nPrepared forecasting dataset saved successfully!")
print("File: forecasting_data.csv")