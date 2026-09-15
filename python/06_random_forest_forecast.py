import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Load forecasting features
sales = pd.read_csv("forecast_features.csv")

print("Forecast features loaded successfully!")

# Features
features = [
    "month_number",
    "year",
    "month",
    "lag_1",
    "lag_2",
    "lag_3",
    "rolling_mean_3"
]

X = sales[features]
y = sales["revenue"]

# Train final model on all available data
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    max_depth=5
)

model.fit(X, y)

print("\nFinal Random Forest model trained successfully!")

# Last available month
last_month_number = sales["month_number"].iloc[-1]

print("Last historical month:", sales["order_month"].iloc[-1])
print("Last month number:", last_month_number)

# Generate future month numbers
future_month_numbers = np.arange(
    last_month_number + 1,
    last_month_number + 7
)

# We need future predictions sequentially
history = sales["revenue"].tolist()

forecast_rows = []

for month_number in future_month_numbers:

    # Calculate future year and month
    last_date = pd.to_datetime(sales["order_month"].iloc[-1])
    future_date = last_date + pd.DateOffset(
        months=int(month_number - last_month_number)
    )

    month = future_date.month
    year = future_date.year

    # Lag values
    lag_1 = history[-1]
    lag_2 = history[-2]
    lag_3 = history[-3]

    # Rolling average of previous 3 months
    rolling_mean_3 = np.mean(history[-3:])

    # Create feature row
    future_X = pd.DataFrame([{
        "month_number": month_number,
        "year": year,
        "month": month,
        "lag_1": lag_1,
        "lag_2": lag_2,
        "lag_3": lag_3,
        "rolling_mean_3": rolling_mean_3
    }])

    # Predict revenue
    prediction = model.predict(future_X)[0]

    # Prevent negative forecast
    prediction = max(0, prediction)

    # Store prediction
    forecast_rows.append({
        "order_month": future_date,
        "forecast_revenue": prediction
    })

    # Add prediction to history for next month's lag
    history.append(prediction)

# Create forecast dataframe
forecast = pd.DataFrame(forecast_rows)

print("\nNext 6 Months Revenue Forecast:")
print(forecast)

# Save final forecast
forecast.to_csv(
    "final_revenue_forecast.csv",
    index=False
)

print("\nFinal revenue forecast saved successfully!")
print("File: final_revenue_forecast.csv")