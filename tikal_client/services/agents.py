"""
Сервис для работы с агентами
"""

import logging
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)


class AgentsService:
    """Сервис для работы с агентами"""
    
    def __init__(self, client):
        """
        Инициализация сервиса
        
        Args:
            client: Экземпляр TikalClient
        """
        self.client = client
    
    def list(
        self,
        status: Optional[str] = None,
        queue_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Получает список агентов
        
        Args:
            status: Статус агента для фильтрации (online, offline, busy и т.д.)
            queue_id: ID очереди для фильтрации
            limit: Лимит количества результатов
            offset: Смещение для пагинации
        
        Returns:
            Словарь со списком агентов
        """
        params = {}
        
        if status:
            params['status'] = status
        if queue_id:
            params['queue_id'] = queue_id
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        
        return self.client.get('/api/agents', params=params)
    
    def get(self, agent_id: str) -> Dict[str, Any]:
        """
        Получает детальную информацию об агенте
        
        Args:
            agent_id: ID агента
        
        Returns:
            Информация об агенте
        """
        return self.client.get('/api/agents/{id}', id=agent_id)
    
    def get_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Получает текущий статус агента
        
        Args:
            agent_id: ID агента
        
        Returns:
            Статус агента
        """
        return self.client.get('/api/agents/{id}/status', id=agent_id)
    
    def get_all(self, **filters) -> List[Dict[str, Any]]:
        """
        Получает всех агентов с фильтрами
        
        Args:
            **filters: Дополнительные фильтры
        
        Returns:
            Список агентов
        """
        result = self.list(**filters)
        
        # Если результат - список, возвращаем его
        if isinstance(result, list):
            return result
        
        # Если результат - словарь с полем 'agents' или 'data'
        if isinstance(result, dict):
            return result.get('agents', result.get('data', []))
        
        return []
    
    def get_online(self) -> List[Dict[str, Any]]:
        """
        Получает список онлайн агентов
        
        Returns:
            Список онлайн агентов
        """
        return self.get_all(status='online')
    
    def get_offline(self) -> List[Dict[str, Any]]:
        """
        Получает список офлайн агентов
        
        Returns:
            Список офлайн агентов
        """
        return self.get_all(status='offline')

