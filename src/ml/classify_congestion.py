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
df = pd.get_dummies(df, columns=["zone_name"], drop_first=True)
feature_cols += [col for col in df.columns if col.startswith("zone_name_")]
X = df[feature_cols]
y = df["high_congestion"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print(f"\nTraining set: {len(X_train)} readings")
print(f"Test set: {len(X_test)} readings")

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

# Baseline: what if we always predicted the majority class?
baseline_accuracy = max(y_test.mean(), 1 - y_test.mean())

print(f"\n=== Model Performance ===")
print(f"Model accuracy: {accuracy:.1%}")
print(f"Baseline accuracy (always guess majority class): {baseline_accuracy:.1%}")
print(
    f"Improvement over baseline: {(accuracy - baseline_accuracy)*100:+.1f} percentage points"
)
print("\nActual vs Predicted:")
print(pd.DataFrame({"actual": y_test.values, "predicted": predictions}))
