import subprocess
import sys

steps = [
    "src/ingestion/load_trips.py",
    "src/ingestion/load_to_sql.py",
    "src/ingestion/export_for_powerbi.py",
]

print("=== Starting Bengaluru Mobility Pipeline ===\n")

for step in steps:
    print(f"--- Running {step} ---")
    result = subprocess.run([sys.executable, step])

    if result.returncode != 0:
        print(f"\nPipeline FAILED at step: {step}")
        sys.exit(1)

    print()  # blank line for readability

print("=== Pipeline completed successfully ===")
