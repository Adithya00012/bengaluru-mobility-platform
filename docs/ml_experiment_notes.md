# ML Experiment Notes

## Experiment 1: Travel-time regression, small dataset (28 trips)
- Features: all 6 base features + one-hot encoded zones (13 total features)
- Result: R² = -2.36, MAE = 13.8 min — severe overfitting (too many features for too little data)

## Experiment 2: Travel-time regression, small dataset, reduced features
- Features: distance_km, is_peak_hour (2 features)
- Result: R² = -0.72, MAE = 9.7 min — improved, but still unreliable given only 7 test rows

## Experiment 3: Travel-time regression, expanded dataset (480 synthetic trips)
- Features: distance_km, is_peak_hour (same 2 features as Experiment 2)
- Result: R² = 0.82, MAE = 5.8 min — strong result. Coefficient for is_peak_hour (+17.99 min) correctly recovered the peak-hour slowdown deliberately built into the data generator.
- **Conclusion:** the modeling approach was sound throughout; Experiment 1-2's poor results were a data volume problem, not a methodology problem.

## Experiment 4: Congestion classification, small dataset (10 readings)
- Model: Decision Tree, max_depth=2
- Result: 33% accuracy — worse than the 60% majority-class baseline

## Experiment 5: Congestion classification, expanded dataset (3,840 synthetic readings)
- Model: Decision Tree, max_depth=2 (unchanged)
- Result: 79.3% accuracy vs. 76.7% baseline — only marginal improvement; model too simple for the data volume now available

## Experiment 6: Congestion classification, expanded dataset, deeper tree
- Model: Decision Tree, max_depth=5
- Result: 86.0% accuracy vs. 76.7% baseline (+9.3pp) — genuinely strong result once model complexity was re-tuned to match data volume

## Key takeaway
Model complexity should scale with data volume. A model that's appropriately simple for 10 rows becomes too simple for 3,840 rows, and vice versa — this needs re-checking whenever the underlying dataset size changes meaningfully.