"""
Сервис для работы со звонками
"""

import logging
from typing import Optional, Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class CallsService:
    """Сервис для управления звонками"""
    
    def __init__(self, client):
        """
        Инициализация сервиса
        
        Args:
            client: Экземпляр TikalClient
        """
        self.client = client
    
    def list(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Получает список звонков
        
        Args:
            start_date: Начальная дата для фильтрации
            end_date: Конечная дата для фильтрации
            agent_id: ID агента для фильтрации
            status: Статус звонка для фильтрации
            limit: Лимит количества результатов
            offset: Смещение для пагинации
        
        Returns:
            Словарь со списком звонков
        """
        params = {}
        
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        if agent_id:
            params['agent_id'] = agent_id
        if status:
            params['status'] = status
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        
        return self.client.get('/api/calls', params=params)
    
    def get(self, call_id: str) -> Dict[str, Any]:
        """
        Получает детальную информацию о звонке
        
        Args:
            call_id: ID звонка
        
        Returns:
            Информация о звонке
        """
        return self.client.get('/api/calls/{id}', id=call_id)
    
    def create(
        self,
        phone_number: str,
        agent_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Создает исходящий звонок
        
        Args:
            phone_number: Номер телефона для звонка
            agent_id: ID агента (опционально)
            campaign_id: ID кампании (опционально)
            **kwargs: Дополнительные параметры
        
        Returns:
            Информация о созданном звонке
        """
        data = {
            'phone_number': phone_number,
            **kwargs
        }
        
        if agent_id:
            data['agent_id'] = agent_id
        if campaign_id:
            data['campaign_id'] = campaign_id
        
        return self.client.post('/api/calls', json_data=data)
    
    def originate(
        self,
        agent_id: str,
        phone_number: str,
        custom1: Optional[str] = None,
        custom2: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Создает звонок между агентом и номером телефона (Originate API)
        
        Согласно документации, это основной способ создания звонков через API.
        Параметры custom1 и custom2 будут возвращены в CDR.
        
        Args:
            agent_id: ID агента для звонка
            phone_number: Номер телефона для звонка
            custom1: Пользовательское поле 1 (будет в CDR)
            custom2: Пользовательское поле 2 (будет в CDR)
            **kwargs: Дополнительные параметры
        
        Returns:
            Информация о созданном звонке
        """
        data = {
            'agent_id': agent_id,
            'phone_number': phone_number,
            **kwargs
        }
        
        if custom1:
            data['custom1'] = custom1
        if custom2:
            data['custom2'] = custom2
        
        # Пробуем различные возможные endpoints для originate
        endpoints = [
            '/api/originate',
            '/api/calls/originate',
            '/cc3/api/originate',
            '/cc3/api/calls/originate',
        ]
        
        # Пробуем первый endpoint, если не работает - будет ошибка
        return self.client.post('/api/originate', json_data=data)
    
    def update(self, call_id: str, **kwargs) -> Dict[str, Any]:
        """
        Обновляет информацию о звонке
        
        Args:
            call_id: ID звонка
            **kwargs: Поля для обновления
        
        Returns:
            Обновленная информация о звонке
        """
        return self.client.put('/api/calls/{id}', json_data=kwargs, id=call_id)
    
    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        **filters
    ) -> List[Dict[str, Any]]:
        """
        Получает звонки за период с дополнительными фильтрами
        
        Args:
            start_date: Начальная дата
            end_date: Конечная дата
            **filters: Дополнительные фильтры
        
        Returns:
            Список звонков
        """
        result = self.list(
            start_date=start_date,
            end_date=end_date,
            **filters
        )
        
        # Если результат - список, возвращаем его
        if isinstance(result, list):
            return result
        
        # Если результат - словарь с полем 'calls' или 'data'
        if isinstance(result, dict):
            return result.get('calls', result.get('data', []))
        
        return []

