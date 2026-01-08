"""
Сервис для работы с CDR (Call Detail Records)
Сервис SEND CDR для получения уведомлений о звонках
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class CDRService:
    """Сервис для работы с CDR (Call Detail Records)"""
    
    def __init__(self, client):
        """
        Инициализация сервиса
        
        Args:
            client: Экземпляр TikalClient
        """
        self.client = client
    
    def parse_cdr_data(self, data_string: str, format_type: str = 'json') -> Dict[str, Any]:
        """
        Парсит данные CDR из строки
        
        Args:
            data_string: Строка с данными CDR (XML, JSON или key-value)
            format_type: Формат данных ('json', 'xml', 'keyvalue')
        
        Returns:
            Распарсенные данные CDR
        """
        if format_type == 'json':
            import json
            return json.loads(data_string)
        elif format_type == 'xml':
            try:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(data_string)
                return {child.tag: child.text for child in root}
            except Exception as e:
                logger.error(f"Ошибка парсинга XML: {e}")
                return {}
        elif format_type == 'keyvalue':
            # Парсинг key-value пар
            result = {}
            for pair in data_string.split('&'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    result[key] = value
            return result
        else:
            raise ValueError(f"Неподдерживаемый формат: {format_type}")
    
    def extract_cdr_fields(self, cdr_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Извлекает стандартные поля CDR
        
        Args:
            cdr_data: Данные CDR
        
        Returns:
            Стандартизированные поля CDR
        """
        return {
            'agent_id': cdr_data.get('agent_id'),
            'queue_id': cdr_data.get('queue_id'),
            'caller_id': cdr_data.get('caller_id'),
            'answer_time': cdr_data.get('answer_time'),
            'end_time': cdr_data.get('end_time'),
            'waiting_time': cdr_data.get('waiting_time'),
            'duration': cdr_data.get('duration'),
            'direction': cdr_data.get('direction'),  # incoming or outgoing
            'recording_link': cdr_data.get('recording_link'),
            'call_status': cdr_data.get('call_status'),  # answered, unanswered, asterisk status
            'custom1': cdr_data.get('custom1'),
            'custom2': cdr_data.get('custom2'),
        }


class CDRWebhookHandler:
    """
    Обработчик webhook для получения CDR данных
    Используется для создания сервера, который принимает CDR от Tikal
    """
    
    @staticmethod
    def handle_webhook_request(request_data: Dict[str, Any], format_type: str = 'json') -> Dict[str, Any]:
        """
        Обрабатывает webhook запрос от Tikal с CDR данными
        
        Args:
            request_data: Данные запроса (обычно содержит поле 'data')
            format_type: Формат данных в поле 'data'
        
        Returns:
            Распарсенные данные CDR
        """
        # Извлекаем поле 'data' из запроса
        data_string = request_data.get('data', '')
        
        if not data_string:
            # Если нет поля 'data', возможно данные уже распарсены
            return request_data
        
        # Парсим данные
        cdr_service = CDRService(None)
        parsed_data = cdr_service.parse_cdr_data(data_string, format_type)
        
        # Извлекаем стандартные поля
        return cdr_service.extract_cdr_fields(parsed_data)

