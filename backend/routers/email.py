from fastapi import APIRouter
from models.email_models import EmailRequest, EmailResponse
from services.groq_client import analyze_with_groq

router = APIRouter()

@router.post("/analyze", response_model=EmailResponse)
async def analyze_email(req: EmailRequest):
    result = await analyze_with_groq(req.text)
    return EmailResponse(
        sentiment=result.get("sentiment", "neutral"),
        priority=result.get("priority", "low"),
        ai_response=result.get("ai_response", "No response generated.")
    )
