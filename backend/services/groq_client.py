import httpx
from config import settings

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def analyze_with_groq(email_text: str):
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama3-70b-8192",  # Groq’s LLaMA 3 model
        "messages": [
            {"role": "system", "content": "You are an AI assistant that classifies emails and generates responses."},
            {"role": "user", "content": f"Analyze this email:\n\n{email_text}\n\nReturn JSON with fields: sentiment, priority, ai_response"}
        ],
        "temperature": 0.3
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # Try to parse AI’s structured output
        try:
            import json
            return json.loads(content)
        except Exception:
            return {"sentiment": "unknown", "priority": "low", "ai_response": content}
