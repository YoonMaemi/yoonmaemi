"""FastAPI application entrypoint for the demo summarizer."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .chat_state import ChatState
from .config import get_settings
from .gemini_client import GeminiClient
from .models import ChatRequest, ChatResponse, HealthResponse, Message

app = FastAPI(title="Three-Line Summary Demo", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()
chat_state = ChatState()
gemini_client: GeminiClient | None = None


@app.on_event("startup")
async def startup_event() -> None:
    global gemini_client
    gemini_client = GeminiClient(settings=settings)


@app.get("/healthz", response_model=HealthResponse)
async def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/api/history", response_model=list[Message])
async def get_history() -> list[Message]:
    return chat_state.snapshot()


@app.post("/api/chat", response_model=ChatResponse)
async def create_summary(request: ChatRequest) -> ChatResponse:
    if gemini_client is None:
        raise HTTPException(status_code=503, detail="Gemini client not initialized.")

    user_message = Message(role="user", content=request.message.strip())
    chat_state.append(user_message)

    try:
        summary = gemini_client.summarize(request.message)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=502, detail=f"Gemini API error: {exc}") from exc

    assistant_message = Message(role="assistant", content=summary)
    chat_state.append(assistant_message)

    return ChatResponse(summary=summary, history=chat_state.snapshot())
