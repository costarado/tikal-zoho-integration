"""
Сервис для работы со звонками через Tikal API
"""

import logging
from typing import Optional, Dict, Any
from ..api_client import TikalAPIClient

logger = logging.getLogger(__name__)


class CallService:
    """Сервис для управления звонками"""
    
    def __init__(self, api_client: TikalAPIClient):
        """
        Инициализация сервиса
        
        Args:
            api_client: Экземпляр TikalAPIClient
        """
        self.api = api_client
    
    def get_incoming(self, **filters) -> Dict[str, Any]:
        """
        Получает список входящих звонков
        
        Args:
            **filters: Фильтры (нужно проверить документацию для точных параметров)
        
        Returns:
            Список входящих звонков
        """
        return self.api.post('/api/call/get_incoming', params=filters)
    
    def get_outgoing(self, **filters) -> Dict[str, Any]:
        """
        Получает список исходящих звонков
        
        Args:
            **filters: Фильтры
        
        Returns:
            Список исходящих звонков
        """
        return self.api.post('/api/call/get_outgoing', params=filters)
    
    def originate(
        self,
        agent_id: str,
        dest_num: str,  # Исправлено: должно быть dest_num, а не phone_number
        custom1: Optional[str] = None,
        custom2: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Создает звонок между агентом и номером телефона (Originate API)
        
        Args:
            agent_id: ID агента
            dest_num: Номер телефона назначения - ТОЛЬКО ЦИФРЫ (без +, пробелов и других символов)
            custom1: Пользовательское поле 1 (будет в CDR)
            custom2: Пользовательское поле 2 (будет в CDR)
            **kwargs: Дополнительные параметры
        
        Returns:
            Результат создания звонка
        
        Пример:
            # Правильно: только цифры
            dest_num='1234567890'
            dest_num='0508155492'
            
            # Неправильно: содержит символы
            dest_num='+1234567890'  # содержит +
            dest_num='123-456-7890'  # содержит дефисы
        """
        # Убираем все нецифровые символы из номера
        dest_num_clean = ''.join(filter(str.isdigit, dest_num))
        
        params = {
            'agent_id': agent_id,
            'dest_num': dest_num_clean,  # Только цифры
        }
        
        if custom1:
            params['custom1'] = custom1
        if custom2:
            params['custom2'] = custom2
        
        params.update(kwargs)
        
        return self.api.post('/api/call/originate', params=params)
    
    def queue_dial(
        self,
        queue_id: str,
        phone_number: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Звонит в очередь
        
        Args:
            queue_id: ID очереди
            phone_number: Номер телефона
            **kwargs: Дополнительные параметры
        
        Returns:
            Результат звонка
        """
        params = {
            'queue_id': queue_id,
            'phone_number': phone_number,
        }
        params.update(kwargs)
        
        return self.api.post('/api/call/queue_dial', params=params)
    
    def get_cdr(self, unique_id: Optional[str] = None, **filters) -> Dict[str, Any]:
        """
        Получает CDR (Call Detail Records)
        
        Args:
            unique_id: Уникальный ID звонка (обязательный параметр)
            **filters: Дополнительные фильтры
        
        Returns:
            CDR данные
        """
        params = {}
        if unique_id:
            params['unique_id'] = unique_id
        params.update(filters)
        
        return self.api.post('/api/call/get_cdr', params=params)
    
    def start_new_recording(self, call_id: str) -> Dict[str, Any]:
        """Начинает новую запись звонка"""
        return self.api.post('/api/call/start_new_recording', params={'call_id': call_id})
    
    def stop_recording(self, call_id: str) -> Dict[str, Any]:
        """Останавливает запись звонка"""
        return self.api.post('/api/call/stop_recording', params={'call_id': call_id})
    
    def start_recording(self, call_id: str) -> Dict[str, Any]:
        """Начинает запись звонка"""
        return self.api.post('/api/call/start_recording', params={'call_id': call_id})

