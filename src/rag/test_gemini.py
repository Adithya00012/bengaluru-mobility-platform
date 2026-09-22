import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found. Check your .env file.")
else:
    print("API key loaded successfully (not printing it, for safety)")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.6-flash", contents="In one sentence, what is a data warehouse?"
)

print("\nGemini's response:")
print(response.text)
