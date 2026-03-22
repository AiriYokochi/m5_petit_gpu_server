from fastapi import APIRouter, File, UploadFile

from m5_petit_voice_recognition.schemas import HealthResponse, TranscribeResponse
from m5_petit_voice_recognition.services.whisper_service import WhisperService

router = APIRouter()
whisper_service = WhisperService()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(file: UploadFile = File(...)) -> TranscribeResponse:
    result = await whisper_service.transcribe_upload(file)
    return TranscribeResponse(**result)