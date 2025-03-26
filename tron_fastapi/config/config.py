from pathlib import Path
from pydantic_settings import BaseSettings
import logging

logging.basicConfig(level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    #DB_ECHO: bool = False
    DB_ECHO: bool = True

settings = Settings()


