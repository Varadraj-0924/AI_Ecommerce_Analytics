import pandas as pd
import numpy as np

# Load forecasting data
sales = pd.read_csv("forecasting_data.csv")

print("Forecasting data loaded successfully!")

# Convert date column
sales["order_month"] = pd.to_datetime(sales["order_month"])

# Sort by date
sales = sales.sort_values("order_month").reset_index(drop=True)

# Create time-based features
sales["month_number"] = np.arange(len(sales))
sales["year"] = sales["order_month"].dt.year
sales["month"] = sales["order_month"].dt.month

# Create lag features
sales["lag_1"] = sales["revenue"].shift(1)
sales["lag_2"] = sales["revenue"].shift(2)
sales["lag_3"] = sales["revenue"].shift(3)

# Create rolling average
sales["rolling_mean_3"] = sales["revenue"].shift(1).rolling(3).mean()

print("\nForecasting features created successfully!")

print("\nFeature dataset:")
print(sales)

# Remove rows with missing lag values
model_data = sales.dropna().reset_index(drop=True)

print("\nModel-ready dataset:")
print(model_data)

print("\nModel-ready shape:", model_data.shape)

# Save feature dataset
model_data.to_csv("forecast_features.csv", index=False)

print("\nForecast features saved successfully!")
print("File: forecast_features.csv")