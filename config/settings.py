"""Application setting for CustomerAI (FastAPI)."""

from dataclasses import dataclass


@dataclass
class Settings:
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    data_path: str = "customerai/data/events.csv"


settings = Settings()
