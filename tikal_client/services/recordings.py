"""
Сервис для работы с записями звонков
"""

import logging
from typing import Optional, Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class RecordingsService:
    """Сервис для работы с записями звонков"""
    
    def __init__(self, client):
        """
        Инициализация сервиса
        
        Args:
            client: Экземпляр TikalClient
        """
        self.client = client
    
    def list(
        self,
        call_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        agent_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Получает список записей
        
        Args:
            call_id: ID звонка для фильтрации
            start_date: Начальная дата для фильтрации
            end_date: Конечная дата для фильтрации
            agent_id: ID агента для фильтрации
            limit: Лимит количества результатов
            offset: Смещение для пагинации
        
        Returns:
            Словарь со списком записей
        """
        params = {}
        
        if call_id:
            params['call_id'] = call_id
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        if agent_id:
            params['agent_id'] = agent_id
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        
        return self.client.get('/api/recordings', params=params)
    
    def get(self, recording_id: str) -> Dict[str, Any]:
        """
        Получает детальную информацию о записи
        
        Args:
            recording_id: ID записи
        
        Returns:
            Информация о записи
        """
        return self.client.get('/api/recordings/{id}', id=recording_id)
    
    def download_url(self, recording_id: str) -> str:
        """
        Получает URL для скачивания записи
        
        Args:
            recording_id: ID записи
        
        Returns:
            URL для скачивания
        """
        result = self.client.get('/api/recordings/{id}/download', id=recording_id)
        
        # Если результат содержит URL, возвращаем его
        if isinstance(result, dict):
            return result.get('url', result.get('download_url', ''))
        
        return ''
    
    def get_by_call(self, call_id: str) -> List[Dict[str, Any]]:
        """
        Получает все записи для конкретного звонка
        
        Args:
            call_id: ID звонка
        
        Returns:
            Список записей
        """
        result = self.list(call_id=call_id)
        
        # Если результат - список, возвращаем его
        if isinstance(result, list):
            return result
        
        # Если результат - словарь с полем 'recordings' или 'data'
        if isinstance(result, dict):
            return result.get('recordings', result.get('data', []))
        
        return []
    
    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        **filters
    ) -> List[Dict[str, Any]]:
        """
        Получает записи за период с дополнительными фильтрами
        
        Args:
            start_date: Начальная дата
            end_date: Конечная дата
            **filters: Дополнительные фильтры
        
        Returns:
            Список записей
        """
        result = self.list(
            start_date=start_date,
            end_date=end_date,
            **filters
        )
        
        # Если результат - список, возвращаем его
        if isinstance(result, list):
            return result
        
        # Если результат - словарь с полем 'recordings' или 'data'
        if isinstance(result, dict):
            return result.get('recordings', result.get('data', []))
        
        return []

