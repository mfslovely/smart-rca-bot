from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from parser import parse_logs
from rca_agent import get_root_cause
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ollama import Client

app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    logs = content.decode()
    events = parse_logs(logs)
    rca = get_root_cause(events)
    return {"events": events, "rca_report": rca, "logs": logs}


class ChatRequest(BaseModel):
    message: str

# Chat endpoint with Ollama
@app.post("/chat/")
async def chat_with_bot(chat: ChatRequest):
    client = Client(host='http://localhost:11434')  # default Ollama host
    response = client.chat(
        model="llama3",  # or mistral, phi, etc.
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": chat.message},
        ]
    )
    return {"reply": response['message']['content']}