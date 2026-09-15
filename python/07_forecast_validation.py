import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load forecasting features
sales = pd.read_csv("forecast_features.csv")

print("Forecast features loaded successfully!")
print("Shape:", sales.shape)

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

# Time-series cross-validation
tscv = TimeSeriesSplit(n_splits=4)

mae_scores = []
rmse_scores = []

print("\nTime-Series Cross Validation:")

for fold, (train_index, test_index) in enumerate(tscv.split(X), start=1):

    X_train = X.iloc[train_index]
    X_test = X.iloc[test_index]

    y_train = y.iloc[train_index]
    y_test = y.iloc[test_index]

    # Train Random Forest
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        max_depth=5
    )

    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    mae_scores.append(mae)
    rmse_scores.append(rmse)

    print(f"\nFold {fold}:")
    print("Training samples:", len(train_index))
    print("Testing samples:", len(test_index))
    print("MAE:", round(mae, 2))
    print("RMSE:", round(rmse, 2))

# Average performance
average_mae = np.mean(mae_scores)
average_rmse = np.mean(rmse_scores)

print("\n==============================")
print("FINAL CROSS-VALIDATION RESULTS")
print("==============================")

print("Average MAE:", round(average_mae, 2))
print("Average RMSE:", round(average_rmse, 2))

# Save validation results
validation_results = pd.DataFrame({
    "fold": range(1, 5),
    "MAE": mae_scores,
    "RMSE": rmse_scores
})

validation_results.to_csv(
    "forecast_validation_results.csv",
    index=False
)

print("\nValidation results saved successfully!")
print("File: forecast_validation_results.csv")