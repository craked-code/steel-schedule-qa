from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    ocr_backend : Literal["tesseract", "google_vision"] = "tesseract" # 'pytessaract' is the default value if none is provided

settings = Settings()