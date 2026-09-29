# API Documentation

## Gemini API (Google Generative AI)

Used by the RAG system (`src/rag/ask_mobility_data.py`) to power natural language querying over the mobility database.

### Authentication
- Requires a free API key from https://aistudio.google.com/apikey
- Stored in `.env` as `GEMINI_API_KEY` (never committed to Git — see `.gitignore`)
- Loaded at runtime via `python-dotenv`

### Model used
- `gemini-3.6-flash` — Google's fast, free-tier-friendly model

### How the integration works (two-call pattern)
1. **Call 1 (text-to-SQL):** the user's plain-English question, plus a schema description, is sent to Gemini. Gemini returns a raw SQL SELECT query as text.
2. **Local execution:** that SQL is run directly against `mobility.db` using `sqlite3`/`pandas` — Gemini never touches the actual data at this step.
3. **Call 2 (answer generation):** the real query results are sent back to Gemini, which converts them into a natural-language answer.

### Request/response shape
```python
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="<prompt text>"
)
# response.text contains the model's reply
```

### Rate limits and cost
- Free tier: subject to Google's published per-minute/per-day request limits (check https://ai.google.dev/pricing for current limits, as these change over time)
- No cost incurred as long as usage stays within free tier limits

### Known limitations
- The model can write technically-correct SQL that produces a misleading answer if the underlying data doesn't have the pattern implied by the question (see `docs/troubleshooting.md` for a documented example)