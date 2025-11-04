"""Data models shared across the FastAPI application."""

from typing import List, Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Raw user input text.")


class ChatResponse(BaseModel):
    summary: str
    history: List[Message]


class HealthResponse(BaseModel):
    status: str

