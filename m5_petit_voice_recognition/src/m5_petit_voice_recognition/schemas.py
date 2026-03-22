from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class TranscribeResponse(BaseModel):
    text: str
    language: str | None = None
    duration_sec: float | None = None