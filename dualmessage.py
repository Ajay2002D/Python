from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from openai import AzureOpenAI
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enum for message type
class MessageType(str, Enum):
    whatsapp = "whatsapp"
    sms = "sms"

# Request schema
class MessageRequest(BaseModel):
    content: str
    type: MessageType

# Azure OpenAI client
client = AzureOpenAI(
    api_key="",
    api_version="",  # Replace with your API version
    azure_endpoint=''
)

# API endpoint
@app.post("/generate-message")
def generate_message(request: MessageRequest):
    # System instructions based on type
    if request.type == MessageType.whatsapp:
        instructions = (
            "Format the following message for WhatsApp. "
            "Use bold for important words using asterisks, and add a friendly tone with emojis if suitable."
        )
    elif request.type == MessageType.sms:
        instructions = (
            "Format the following message for SMS. "
            "Keep it short, clear, and professional with no emojis or formatting."
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid message type.")

    try:
        response = client.chat.completions.create(
            model="gpt-35-turbo",  # Or the name of your deployed model
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": request.content}
            ]
        )

        res = response.choices[0].message.content
        return {"formatted_message": res}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
