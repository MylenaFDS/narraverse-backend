import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # ==========================
    # Banco
    # ==========================
    DATABASE_URL = os.getenv("DATABASE_URL")

    # ==========================
    # Segurança
    # ==========================
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "60",
        )
    )

    # ==========================
    # Ambiente
    # ==========================
    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development",
    )

    DEBUG = (
        os.getenv(
            "DEBUG",
            "true",
        ).lower()
        == "true"
    )

    # ==========================
    # Uploads
    # ==========================
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        "uploads",
    )

    # ==========================
    # IA
    # ==========================
    AI_PROVIDER = os.getenv(
        "AI_PROVIDER",
        "ollama",
    )

    # Ollama
    OLLAMA_URL = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434",
    )

    OLLAMA_MODEL = os.getenv(
        "OLLAMA_MODEL",
        "llama3",
    )

    # Gemini
    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY",
    )

    # OpenAI
    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY",
    )


settings = Settings()