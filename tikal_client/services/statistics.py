"""
Сервис для работы со статистикой
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class StatisticsService:
    """Сервис для получения статистики"""
    
    def __init__(self, client):
        """
        Инициализация сервиса
        
        Args:
            client: Экземпляр TikalClient
        """
        self.client = client
    
    def calls(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        agent_id: Optional[str] = None,
        queue_id: Optional[str] = None,
        group_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Получает статистику по звонкам
        
        Args:
            start_date: Начальная дата для статистики
            end_date: Конечная дата для статистики
            agent_id: ID агента для фильтрации
            queue_id: ID очереди для фильтрации
            group_by: Группировка (day, hour, agent, queue и т.д.)
        
        Returns:
            Статистика по звонкам
        """
        params = {}
        
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        if agent_id:
            params['agent_id'] = agent_id
        if queue_id:
            params['queue_id'] = queue_id
        if group_by:
            params['group_by'] = group_by
        
        return self.client.get('/api/statistics/calls', params=params)
    
    def agents(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        agent_id: Optional[str] = None,
        queue_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Получает статистику по агентам
        
        Args:
            start_date: Начальная дата для статистики
            end_date: Конечная дата для статистики
            agent_id: ID агента для фильтрации
            queue_id: ID очереди для фильтрации
        
        Returns:
            Статистика по агентам
        """
        params = {}
        
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        if agent_id:
            params['agent_id'] = agent_id
        if queue_id:
            params['queue_id'] = queue_id
        
        return self.client.get('/api/statistics/agents', params=params)
    
    def queues(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        queue_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Получает статистику по очередям
        
        Args:
            start_date: Начальная дата для статистики
            end_date: Конечная дата для статистики
            queue_id: ID очереди для фильтрации
        
        Returns:
            Статистика по очередям
        """
        params = {}
        
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        if queue_id:
            params['queue_id'] = queue_id
        
        return self.client.get('/api/statistics/queues', params=params)
    
    def get_daily_summary(
        self,
        date: datetime,
        agent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Получает сводную статистику за день
        
        Args:
            date: Дата для статистики
            agent_id: ID агента для фильтрации (опционально)
        
        Returns:
            Сводная статистика за день
        """
        start_date = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_date = datetime(date.year, date.month, date.day, 23, 59, 59)
        
        return self.calls(
            start_date=start_date,
            end_date=end_date,
            agent_id=agent_id,
            group_by='hour'
        )

