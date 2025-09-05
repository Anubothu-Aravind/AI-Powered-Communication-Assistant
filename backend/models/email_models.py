from pydantic import BaseModel

class EmailRequest(BaseModel):
    text: str

class EmailResponse(BaseModel):
    sentiment: str
    priority: str
    ai_response: str
