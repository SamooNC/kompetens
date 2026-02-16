from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application Kompetens.

    All values are read from environment variables (or .env file).
    """

    # --- PostgreSQL ---
    DATABASE_URL: str = (
        "postgresql+asyncpg://kompetens:kompetens_dev@localhost:5432/kompetens"
    )
    DATABASE_URL_SYNC: str = (
        "postgresql+psycopg://kompetens:kompetens_dev@localhost:5432/kompetens"
    )

    # --- FastAPI ---
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # --- vLLM (local LLM) ---
    VLLM_BASE_URL: str = "http://localhost:8001/v1"
    VLLM_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.3"

    # --- Whisper STT (local) ---
    WHISPER_MODEL_SIZE: str = "large-v3"
    WHISPER_DEVICE: str = "cuda"
    WHISPER_COMPUTE_TYPE: str = "float16"

    # --- Piper TTS (local) ---
    PIPER_MODEL_PATH: str = "/models/piper/fr_FR-siwis-medium.onnx"
    PIPER_SAMPLE_RATE: int = 22050

    # --- Embeddings (local) ---
    EMBEDDING_MODEL: str = "intfloat/multilingual-e5-large"
    EMBEDDING_DIMENSION: int = 1024

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
