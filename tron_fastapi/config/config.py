from pathlib import Path
from pydantic_settings import BaseSettings
import logging

logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    This class is used to store the settings of the application
    """

    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    DB_ECHO: bool = False
    # DB_ECHO: bool = True
    API_KEY1: str = "d0be5201-e79d-48e9-853f-88fc2b3106d9"
    API_KEY2: str = "18ac5f55-bba2-4beb-a1bf-658564f8778a"
    API_KEY3: str = "b9815890-3363-4b80-8f3a-2b5499d8876a"


settings = Settings()
