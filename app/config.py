from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    ocr_backend : Literal["tesseract", "google_vision"] = "tesseract" # 'pytessaract' is the default value if none is provided
    table_detection_conf_threshold : float = 0.5
    pixel_density_threshold : float = 70.0

settings = Settings()