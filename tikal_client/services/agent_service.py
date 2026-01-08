"""
Сервис для работы с агентами через Tikal API
"""

import logging
from typing import Optional, Dict, Any
from ..api_client import TikalAPIClient

logger = logging.getLogger(__name__)


class AgentService:
    """Сервис для управления агентами"""
    
    def __init__(self, api_client: TikalAPIClient):
        """
        Инициализация сервиса
        
        Args:
            api_client: Экземпляр TikalAPIClient
        """
        self.api = api_client
    
    def create(
        self,
        agent_id: str,
        name: str,
        password: str,
        out_q: Optional[str] = None,
        wrapuptime: Optional[int] = None,
        department: Optional[int] = None,  # Исправлено: только цифры
        mon1_queue: Optional[str] = None,
        mon2_queue: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Создает нового агента
        
        Args:
            agent_id: ID агента
            name: Имя агента (только буквы, дефисы или пробелы)
            password: Пароль агента
            out_q: Исходящая очередь (опционально)
            wrapuptime: Время wrap-up в секундах (опционально)
            department: ID отдела - только цифры (опционально)
            mon1_queue: Мониторинг очереди 1 (опционально)
            mon2_queue: Мониторинг очереди 2 (опционально)
        
        Returns:
            Результат создания агента
        """
        params = {
            'id': agent_id,
            'name': name,
            'password': password,
        }
        
        if out_q:
            params['out_q'] = out_q
        if wrapuptime is not None:
            params['wrapuptime'] = str(wrapuptime)
        if department is not None:
            params['department'] = str(department)  # Только цифры
        if mon1_queue:
            params['mon1_queue'] = mon1_queue
        if mon2_queue:
            params['mon2_queue'] = mon2_queue
        
        return self.api.post('/api/agent/create', params=params)
    
    def edit(
        self,
        agent_id: str,
        name: Optional[str] = None,
        password: Optional[str] = None,
        out_q: Optional[str] = None,
        wrapuptime: Optional[int] = None,
        department: Optional[str] = None,
        mon1_queue: Optional[str] = None,
        mon2_queue: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Редактирует агента
        
        Args:
            agent_id: ID агента
            name: Новое имя (опционально)
            password: Новый пароль (опционально)
            out_q: Исходящая очередь (опционально)
            wrapuptime: Время wrap-up (опционально)
            department: Отдел (опционально)
            mon1_queue: Мониторинг очереди 1 (опционально)
            mon2_queue: Мониторинг очереди 2 (опционально)
        
        Returns:
            Результат редактирования
        """
        params = {'id': agent_id}
        
        if name:
            params['name'] = name
        if password:
            params['password'] = password
        if out_q:
            params['out_q'] = out_q
        if wrapuptime is not None:
            params['wrapuptime'] = str(wrapuptime)
        if department:
            params['department'] = department
        if mon1_queue:
            params['mon1_queue'] = mon1_queue
        if mon2_queue:
            params['mon2_queue'] = mon2_queue
        
        return self.api.post('/api/agent/edit', params=params)
    
    def delete(self, agent_id: str) -> Dict[str, Any]:
        """
        Удаляет агента
        
        Args:
            agent_id: ID агента
        
        Returns:
            Результат удаления
        """
        return self.api.post('/api/agent/delete/', params={'id': agent_id})
    
    def assign(self, agent_id: str, queue_id: str) -> Dict[str, Any]:
        """Назначает агента в очередь"""
        return self.api.post('/api/agent/assign/', params={
            'id': agent_id,
            'queue_id': queue_id
        })
    
    def release(self, agent_id: str, queue_id: str) -> Dict[str, Any]:
        """Освобождает агента из очереди"""
        return self.api.post('/api/agent/release/', params={
            'id': agent_id,
            'queue_id': queue_id
        })
    
    def login(self, agent_id: str, ag_exten: str) -> Dict[str, Any]:
        """
        Логинит агента в систему
        
        Args:
            agent_id: ID агента
            ag_exten: Extension (внутренний номер) агента
        """
        return self.api.post('/api/agent/login/', params={
            'id': agent_id,
            'ag_exten': ag_exten
        })
    
    def logoff(self, agent_id: str) -> Dict[str, Any]:
        """Логаутит агента из системы"""
        return self.api.post('/api/agent/logoff/', params={'id': agent_id})
    
    def set_state(self, agent_id: str, state: str) -> Dict[str, Any]:
        """Устанавливает состояние агента"""
        return self.api.post('/api/agent/set_state/', params={
            'id': agent_id,
            'state': state
        })
    
    def get_state(self, agent_id: str) -> Dict[str, Any]:
        """Получает состояние агента"""
        return self.api.post('/api/agent/get_state/', params={'id': agent_id})
    
    def get_answered_calls(self, agent_id: str) -> Dict[str, Any]:
        """Получает список отвеченных звонков агента"""
        return self.api.post('/api/agent/get_answered_calls/', params={'id': agent_id})
    
    def send_msg(self, agent_id: str, message: str) -> Dict[str, Any]:
        """Отправляет сообщение агенту"""
        return self.api.post('/api/agent/send_msg/', params={
            'id': agent_id,
            'msg': message
        })
    
    def screen_capture(self, agent_id: str) -> Dict[str, Any]:
        """Делает скриншот экрана агента"""
        return self.api.post('/api/agent/screen_capture/', params={'id': agent_id})

