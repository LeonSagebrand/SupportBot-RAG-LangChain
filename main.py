from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import Chatbot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

chatbot = Chatbot()

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    user_message = chat_message.message
    try:
        response = await chatbot.chat_with_bot(user_message)
        return {"response": response}
    
    except Exception as e:
        print(f"Error during chatbot conversation: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")
