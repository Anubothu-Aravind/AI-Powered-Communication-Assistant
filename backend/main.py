from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from textblob import TextBlob
import requests
import os
import asyncio
import time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ======================
# CORS setup
# ======================
origins = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# Groq configuration
# ======================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_ID = "openai/gpt-oss-120b"
# print(GROQ_API_KEY)
# ======================
# Priority classification
# ======================
def classify_priority(subject, body):
    keywords = ["urgent", "immediately", "critical", "down", "blocked", "cannot"]
    return (
        "Urgent"
        if any(k in (subject + body).lower() for k in keywords)
        else "Not urgent"
    )

# ======================
# AI Response with Retry
# ======================
def generate_ai_response(email, retries=3, backoff=2):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a professional, empathetic AI assistant."},
            {
                "role": "user",
                "content": (
                    f"Sender: {email['sender']}\n"
                    f"Subject: {email['subject']}\n"
                    f"Body: {email['body']}\n\n"
                    "Write a short, polite, helpful reply."
                ),
            },
        ],
        "temperature": 0.7,
        "max_completion_tokens": 200,
    }

    for attempt in range(retries):
        try:
            res = requests.post(GROQ_URL, headers=headers, json=payload)
            res.raise_for_status()
            data = res.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            if res is not None and res.status_code == 429 and attempt < retries - 1:
                wait_time = backoff * (2 ** attempt)
                time.sleep(wait_time)
                continue
            return f"(AI Error: {str(e)} — {res.text if 'res' in locals() else ''})"

# ======================
# Async Queue + Workers
# ======================
queue = asyncio.Queue()

async def worker(worker_id: int):
    while True:
        email, future = await queue.get()
        try:
            response = generate_ai_response(email)
            future.set_result(response)
        except Exception as e:
            future.set_result(f"(Worker {worker_id} Error: {str(e)})")
        finally:
            queue.task_done()

@app.on_event("startup")
async def startup_event():
    # Start 3 workers
    for i in range(3):
        asyncio.create_task(worker(i + 1))

# ======================
# Upload Endpoint
# ======================
@app.post("/upload")
async def upload_csv(file: UploadFile):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    processed = []

    for _, row in df.iterrows():
        sentiment = TextBlob(str(row["body"])).sentiment.polarity
        sentiment_label = (
            "Positive" if sentiment > 0.1 else "Negative" if sentiment < -0.1 else "Neutral"
        )

        email = {
            "sender": row["sender"],
            "subject": row["subject"],
            "body": row["body"],
            "sent_date": row.get("sent_date", ""),
            "priority": classify_priority(row["subject"], row["body"]),
            "sentiment": sentiment_label,
        }

        # Use async queue for AI response
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        await queue.put((email, future))
        email["ai_response"] = await future

        processed.append(email)

    return {"emails": processed}
