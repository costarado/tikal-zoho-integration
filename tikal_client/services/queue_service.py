"""
Сервис для работы с очередями через Tikal API
"""

import logging
from typing import Optional, Dict, Any, List
from ..api_client import TikalAPIClient

logger = logging.getLogger(__name__)


class QueueService:
    """Сервис для управления очередями"""
    
    def __init__(self, api_client: TikalAPIClient):
        """
        Инициализация сервиса
        
        Args:
            api_client: Экземпляр TikalAPIClient
        """
        self.api = api_client
    
    def create(
        self,
        queue_id: str,
        name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Создает новую очередь
        
        Args:
            queue_id: ID очереди
            name: Название очереди (опционально)
            **kwargs: Дополнительные параметры
        
        Returns:
            Результат создания очереди
        """
        params = {'id': queue_id}
        if name:
            params['name'] = name
        params.update(kwargs)
        
        return self.api.post('/api/queue/create/', params=params)
    
    def edit(
        self,
        queue_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Редактирует очередь
        
        Args:
            queue_id: ID очереди
            **kwargs: Параметры для редактирования
        
        Returns:
            Результат редактирования
        """
        params = {'id': queue_id}
        params.update(kwargs)
        
        return self.api.post('/api/queue/edit/', params=params)
    
    def delete(self, queue_id: str) -> Dict[str, Any]:
        """
        Удаляет очередь
        
        Args:
            queue_id: ID очереди
        
        Returns:
            Результат удаления
        """
        return self.api.post('/api/queue/delete/', params={'id': queue_id})
    
    def get_agents(self, queue_id: str) -> Dict[str, Any]:
        """
        Получает список агентов в очереди
        
        Args:
            queue_id: ID очереди
        
        Returns:
            Список агентов
        """
        return self.api.post('/api/queue/get_agents/', params={'id': queue_id})
    
    def members_update(
        self,
        queue_id: str,
        agents: List[str]
    ) -> Dict[str, Any]:
        """
        Обновляет список агентов в очереди
        
        Args:
            queue_id: ID очереди
            agents: Список ID агентов
        
        Returns:
            Результат обновления
        """
        # Формат может быть разным, нужно проверить документацию
        params = {'id': queue_id}
        # Возможно, агенты передаются как строка через запятую или отдельными параметрами
        if agents:
            params['agents'] = ','.join(agents) if isinstance(agents, list) else agents
        
        return self.api.post('/api/queue/members_update/', params=params)
    
    def get_waiting_time(self, queue_id: str) -> Dict[str, Any]:
        """
        Получает время ожидания в очереди
        
        Args:
            queue_id: ID очереди
        
        Returns:
            Время ожидания
        """
        return self.api.post('/api/queue/get_waiting_time/', params={'id': queue_id})

