from pydantic import BaseModel


class SpeakRequest(BaseModel):
    text: str
    speaker: int | None = None
    length_scale: float | None = None
    noise_scale: float | None = None
    noise_w: float | None = None
    sentence_silence: float | None = None


class SpeakSummaryResponse(BaseModel):
    ok: bool
    text: str
    filename: str