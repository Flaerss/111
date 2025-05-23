from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class Client(Base):
    """Клиенты фотостудии"""
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    yclients_id = Column(Integer, unique=True, comment="ID из YClients")
    telegram_id = Column(Integer, unique=True, index=True)
    phone = Column(String(20), comment="Формат: +79991234567", unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Client {self.phone}>"

    def validate(self):
        if not self.phone:
            raise ValueError("Поле телефона не должно быть пустым")
        if len(self.phone) != 12:
            raise ValueError("Неверный формат телефона")

class Booking(Base):
    """Записи на фотосессии"""
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), index=True)
    session_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='active')  # active/canceled/changed

    client = relationship("Client", back_populates="bookings")

    def __repr__(self):
        return f"<Booking {self.session_date}>"

    def validate(self):
        if not self.session_date:
            raise ValueError("Поле даты сессии не должно быть пустым")

# Логирование операций с базой данных
Base.metadata.create_all(logging=logging)
