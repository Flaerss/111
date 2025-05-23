import logging
import aiohttp
from datetime import datetime
from typing import Optional, Dict, List
from config import Config

logger = logging.getLogger(__name__)

class YClientsAPI:
    """Сервис для работы с API YClients"""
    
    BASE_URL = "https://api.yclients.com/api/v1"
    
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {Config.YCLIENTS_TOKEN}",
            "Accept": "application/vnd.yclients.v2+json",
            "Content-Type": "application/json"
        }
        self.company_id = Config.COMPANY_ID
        
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[dict] = None
    ) -> Dict:
        """Базовый метод для выполнения запросов"""
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data
                ) as response:
                    response.raise_for_status()
                    return await response.json()
                    
        except aiohttp.ClientError as e:
            logger.error(f"API Request Failed: {str(e)}")
            return {"success": False, "error": str(e)}
            
    async def create_booking(
        self,
        client_id: int,
        date: datetime,
        services: List[int] = [0000],  # ID услуг фотостудии
        worker_id: int = 0000           # ID фотографа
    ) -> Dict:
        """Создание новой записи"""
        endpoint = f"bookings/{self.company_id}"
        data = {
            "client": {"id": client_id},
            "services": [{"id": service} for service in services],
            "staff_id": worker_id,
            "datetime": date.isoformat()
        }
        return await self._make_request("POST", endpoint, data)
    
    async def get_booking(self, booking_id: int) -> Dict:
        """Получение информации о записи"""
        endpoint = f"bookings/{self.company_id}/{booking_id}"
        return await self._make_request("GET", endpoint)
    
    async def update_booking(
        self, 
        booking_id: int, 
        new_date: datetime
    ) -> Dict:
        """Перенос записи"""
        endpoint = f"bookings/{self.company_id}/{booking_id}"
        data = {"datetime": new_date.isoformat()}
        return await self._make_request("PUT", endpoint, data)
    
    async def cancel_booking(self, booking_id: int) -> Dict:
        """Отмена записи"""
        endpoint = f"bookings/{self.company_id}/{booking_id}"
        return await self._make_request("DELETE", endpoint)
    
    async def setup_webhooks(self, webhook_url: str) -> Dict:
        """Настройка вебхуков для получения событий"""
        endpoint = f"company/{self.company_id}/webhooks"
        data = {
            "url": webhook_url,
            "events": [
                "bookings.create",
                "bookings.update",
                "bookings.delete"
            ]
        }
        return await self._make_request("POST", endpoint, data)
    
    async def sync_clients(self) -> List[Dict]:
        """Синхронизация клиентов из YClients"""
        endpoint = f"company/{self.company_id}/clients"
        response = await self._make_request("GET", endpoint)
        return response.get("data", [])