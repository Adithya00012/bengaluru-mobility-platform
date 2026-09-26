import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

conn = sqlite3.connect("data/processed/mobility.db")
df = pd.read_sql("SELECT * FROM fact_trips_enriched", conn)
conn.close()

print("Loaded trips:", df.shape)

df["is_weekend"] = df["is_weekend"].astype(int)
df["is_peak_hour"] = df["is_peak_hour"].astype(int)
df["is_rain"] = df["is_rain"].astype(int)

feature_cols = ["distance_km", "is_peak_hour"]

X = df[feature_cols]
y = df["duration_min"]

print(f"\nUsing {len(feature_cols)} features:", feature_cols)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

print(f"\nTraining set: {len(X_train)} trips")
print(f"Test set: {len(X_test)} trips")

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"\n=== Model Performance ===")
print(f"Mean Absolute Error: {mae:.1f} minutes")
print(f"R² score: {r2:.2f}")

comparison = pd.DataFrame({
    "actual_duration": y_test.values,
    "predicted_duration": predictions.round(1)
})
print("\nActual vs Predicted (test set):")
print(comparison)

print("\n=== Model coefficients (feature importance) ===")
for feature, coef in zip(feature_cols, model.coef_):
    print(f"{feature}: {coef:.2f}")
print(f"Baseline (intercept): {model.intercept_:.2f}")

export_df = X_test.copy()
export_df["actual_duration"] = y_test.values
export_df["predicted_duration"] = predictions.round(1)
export_df["prediction_error"] = (
    export_df["actual_duration"] - export_df["predicted_duration"]
).round(1)
export_df.to_csv("data/processed/travel_time_predictions.csv", index=False)
print(
    f"\nExported {len(export_df)} predictions to data/processed/travel_time_predictions.csv"
)
