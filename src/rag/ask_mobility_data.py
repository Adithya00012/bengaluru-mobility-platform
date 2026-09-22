import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SCHEMA_DESCRIPTION = """
You have access to a SQLite database with these tables:

fact_trips_enriched (one row per trip):
  - full_date (date), day_of_week (text), is_weekend (0/1)
  - hour (integer 0-23), period_of_day (text), is_peak_hour (0/1)
  - pickup_zone (text - zone name)
  - is_rain (0/1), temperature_c (float)
  - distance_km, duration_min, speed_kmh, fare (all numeric)

fact_traffic_enriched (one row per traffic reading):
  - full_date (date), day_of_week (text), is_weekend (0/1)
  - hour (integer 0-23), period_of_day (text), is_peak_hour (0/1)
  - zone_name (text)
  - avg_speed_kmh, congestion_index (numeric, 0 to 1, higher = more congested)
"""


def ask_question(question):
    sql_prompt = f"""{SCHEMA_DESCRIPTION}

Convert this question into a single valid SQLite SELECT query.
Only output the raw SQL query, nothing else - no explanation, no markdown formatting, no code fences.

Question: {question}
"""
    sql_response = client.models.generate_content(
        model="gemini-3.6-flash", contents=sql_prompt
    )
    sql_query = sql_response.text.strip()

    print(f"\n[Generated SQL]:\n{sql_query}\n")

    conn = sqlite3.connect("data/processed/mobility.db")
    try:
        result_df = pd.read_sql(sql_query, conn)
    except Exception as e:
        conn.close()
        return f"Error running generated SQL: {e}"
    conn.close()

    answer_prompt = f"""The user asked: "{question}"

The query returned this data:
{result_df.to_string()}

Answer the user's question in one or two clear, natural sentences based on this data.
"""
    answer_response = client.models.generate_content(
        model="gemini-3.6-flash", contents=answer_prompt
    )

    return answer_response.text


if __name__ == "__main__":
    questions = [
        "What were the peak travel hours based on trip data?",
        "How did rain affect average trip speed?",
        "Which zone has the most traffic readings recorded?",
    ]
    for q in questions:
        print(f"\n{'='*60}")
        print(f"Q: {q}")
        answer = ask_question(q)
        print(f"A: {answer}")
