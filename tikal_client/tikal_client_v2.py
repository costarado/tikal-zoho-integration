"""
Обновленный клиент Tikal API v2
Использует правильный формат: api_key и form-data
"""

import logging
from typing import Optional
from .api_client import TikalAPIClient
from .services.agent_service import AgentService
from .services.queue_service import QueueService
from .services.call_service_new import CallService
from .services.cdr import CDRService

logger = logging.getLogger(__name__)


class TikalClientV2:
    """
    Обновленный клиент для работы с Tikal Call Center API
    Использует api_key и form-data формат запросов
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        format: str = 'json',
        timeout: int = 30
    ):
        """
        Инициализация клиента
        
        Args:
            base_url: Базовый URL сервера (например, http://arielsip.com)
            api_key: API ключ (special key, выданный при установке)
            format: Формат ответа ('json' или 'xml')
            timeout: Таймаут запросов в секундах
        """
        # Создаем API клиент
        self.api = TikalAPIClient(
            base_url=base_url,
            api_key=api_key,
            format=format,
            timeout=timeout
        )
        
        # Инициализируем сервисы
        self.agents = AgentService(self.api)
        self.queues = QueueService(self.api)
        self.calls = CallService(self.api)
        self.cdr = CDRService(None)  # CDR не требует API клиента
    
    def close(self):
        """Закрывает клиент"""
        self.api.close()
        logger.info("Tikal client closed")

