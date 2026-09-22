import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

conn = sqlite3.connect("data/processed/mobility.db")
df = pd.read_sql("SELECT * FROM fact_traffic_enriched", conn)
conn.close()

print("Loaded traffic readings:", df.shape)
print(df[["zone_name", "hour", "congestion_index"]])

df["high_congestion"] = (df["congestion_index"] >= 0.6).astype(int)

print(f"\nHigh congestion readings: {df['high_congestion'].sum()} of {len(df)}")

df["is_weekend"] = df["is_weekend"].astype(int)
df["is_peak_hour"] = df["is_peak_hour"].astype(int)

feature_cols = ["hour", "is_weekend", "is_peak_hour"]
X = df[feature_cols]
y = df["high_congestion"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print(f"\nTraining set: {len(X_train)} readings")
print(f"Test set: {len(X_test)} readings")

model = DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\n=== Model Performance ===")
print(f"Accuracy: {accuracy:.0%}")
print("\nActual vs Predicted:")
print(pd.DataFrame({"actual": y_test.values, "predicted": predictions}))
