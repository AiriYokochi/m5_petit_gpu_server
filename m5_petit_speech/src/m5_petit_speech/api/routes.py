from fastapi import APIRouter
from fastapi.responses import FileResponse, PlainTextResponse

from m5_petit_speech.schemas import SpeakRequest, SpeakSummaryResponse
from m5_petit_speech.services.piper_service import piper_service

router = APIRouter()


@router.get("/help", response_class=PlainTextResponse)
async def help_text() -> str:
    return """m5_petit_speech API

GET /help
POST /speak
POST /speak_summary

JSON example:
{
  "text": "こんにちは",
  "speaker": 0,
  "length_scale": 1.0,
  "noise_scale": 0.5,
  "noise_w": 0.8,
  "sentence_silence": 0.2
}

Notes:
- length_scale: smaller=faster, larger=slower
- noise_scale: voice variation
- noise_w: phoneme duration variation
- sentence_silence: silence between sentences
- speaker: speaker id for multi-speaker models
"""


@router.post("/speak")
async def speak(req: SpeakRequest):
    wav_path = piper_service.synthesize(
        text=req.text,
        speaker=req.speaker,
        length_scale=req.length_scale,
        noise_scale=req.noise_scale,
        noise_w=req.noise_w,
        sentence_silence=req.sentence_silence,
    )

    return FileResponse(
        path=wav_path,
        media_type="audio/wav",
        filename="speech.wav",
    )


@router.post("/speak_summary", response_model=SpeakSummaryResponse)
async def speak_summary(req: SpeakRequest):
    wav_path = piper_service.synthesize(
        text=req.text,
        speaker=req.speaker,
        length_scale=req.length_scale,
        noise_scale=req.noise_scale,
        noise_w=req.noise_w,
        sentence_silence=req.sentence_silence,
    )

    return SpeakSummaryResponse(
        ok=True,
        text=req.text,
        filename=wav_path.name,
    )