import os
from pathlib import Path

class Config:
    # Пути
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Бот
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
    
    # YClients
    YCLIENTS_TOKEN = os.getenv("YCLIENTS_TOKEN")
    COMPANY_ID = os.getenv("COMPANY_ID")
    
    # Веб
    WEB_SECRET_KEY = os.getenv("WEB_SECRET_KEY", "default-secret-key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATA_DIR}/bookings.db"

    @classmethod
    def create_dirs(cls):
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
