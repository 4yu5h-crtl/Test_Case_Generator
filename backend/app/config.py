import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables from .env file with robust encoding handling
logger = logging.getLogger(__name__)

def _load_env_file():
    # Prefer backend/.env next to this file's parent directory
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        # Try UTF-8 first, then UTF-16 as fallback (common on Windows)
        try:
            load_dotenv(dotenv_path=env_path, encoding="utf-8")
            return
        except UnicodeDecodeError:
            try:
                load_dotenv(dotenv_path=env_path, encoding="utf-16")
                logger.warning("Loaded .env using UTF-16 encoding. Consider saving as UTF-8.")
                return
            except Exception as e:
                logger.error(f"Failed to load .env with UTF-16: {e}")
    # Fallback to default search
    try:
        load_dotenv()
    except Exception as e:
        logger.error(f"Failed to load .env: {e}")

_load_env_file()

class Settings:
    # GitHub API Configuration
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_API_BASE_URL: str = "https://api.github.com"
    
    # OpenRouter API Configuration (for future phases)
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_API_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_DEFAULT_MODEL: str = os.getenv("OPENROUTER_DEFAULT_MODEL", "openrouter/auto")
    
    # Gemini API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # Provider selection: 'gemini' or 'openrouter'
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openrouter").lower()
    # AI Mock Mode (set AI_MOCK_MODE=true to force mock responses)
    AI_MOCK_MODE: bool = os.getenv("AI_MOCK_MODE", "false").lower() == "true"
    
    # App Configuration
    APP_NAME: str = "Test Case Generator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

# Global settings instance
settings = Settings()
