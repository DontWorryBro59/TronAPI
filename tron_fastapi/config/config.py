from pathlib import Path
from pydantic_settings import BaseSettings
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Настройка для корректного пути к файлу базы данных
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    This class is used to store the settings of the application
    """

    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    DB_ECHO: bool = False
    # DB_ECHO: bool = True
    # Прописываем ключи для обращения к API сервиса Tron, default - тестовая
    API_KEY1: str = "d0be5201-e79d-48e9-853f-88fc2b3106d9"


settings = Settings()
