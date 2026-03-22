from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8766, alias="PORT")

    piper_bin: Path = Field(alias="PIPER_BIN")
    piper_ld_library_path: str = Field(alias="PIPER_LD_LIBRARY_PATH")
    piper_model_path: Path = Field(alias="PIPER_MODEL_PATH")
    output_dir: Path = Field(default=Path("./outputs"), alias="OUTPUT_DIR")

    piper_speaker: int = Field(default=0, alias="PIPER_SPEAKER")
    piper_length_scale: float = Field(default=1.0, alias="PIPER_LENGTH_SCALE")
    piper_noise_scale: float = Field(default=0.5, alias="PIPER_NOISE_SCALE")
    piper_noise_w: float = Field(default=0.8, alias="PIPER_NOISE_W")
    piper_sentence_silence: float = Field(default=0.2, alias="PIPER_SENTENCE_SILENCE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        extra="ignore",
    )


settings = Settings()
settings.output_dir.mkdir(parents=True, exist_ok=True)
