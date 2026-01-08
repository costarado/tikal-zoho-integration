"""
Обновленный клиент для работы с Tikal API
Использует api_key и form-data вместо Bearer token
"""

import logging
import requests
from typing import Optional, Dict, Any
from .exceptions import (
    TikalAPIError,
    TikalAuthenticationError,
    TikalConnectionError,
    TikalNotFoundError,
    TikalRateLimitError,
    TikalServerError,
    TikalValidationError
)
from .utils import format_url, retry_on_error

logger = logging.getLogger(__name__)


class TikalAPIClient:
    """
    Клиент для работы с Tikal Call Center API
    Использует api_key и form-data формат
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        format: str = 'json',
        timeout: int = 30,
        retry_attempts: int = 3
    ):
        """
        Инициализация клиента
        
        Args:
            base_url: Базовый URL сервера (например, http://arielsip.com)
            api_key: API ключ (special key, выданный при установке)
            format: Формат ответа ('json' или 'xml')
            timeout: Таймаут запросов в секундах
            retry_attempts: Количество попыток при ошибках
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.format = format
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        
        # Создаем сессию для запросов
        self._session = requests.Session()
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        **url_kwargs
    ) -> Dict[str, Any]:
        """
        Выполняет HTTP запрос к API
        
        Args:
            method: HTTP метод (GET или POST)
            endpoint: Endpoint API (например, '/api/agent/create')
            params: Параметры запроса (будут отправлены как form-data)
            **url_kwargs: Параметры для форматирования URL
        
        Returns:
            Ответ API в виде словаря
        """
        # Формируем URL
        url = format_url(self.base_url, endpoint, **url_kwargs)
        
        # Добавляем обязательные параметры
        request_params = {
            'api_key': self.api_key,
            'format': self.format,
        }
        
        # Добавляем пользовательские параметры
        if params:
            request_params.update(params)
        
        # Выполняем запрос с повторными попытками
        return self._execute_request_with_retry(method, url, request_params)
    
    @retry_on_error(max_attempts=3, delay=1.0)
    def _execute_request_with_retry(
        self,
        method: str,
        url: str,
        params: Dict
    ) -> Dict[str, Any]:
        """
        Выполняет запрос с обработкой ошибок
        """
        try:
            # Tikal API использует POST с form-data (application/x-www-form-urlencoded)
            # Некоторые методы поддерживают GET, но POST стабильнее
            if method.upper() == 'GET':
                response = self._session.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )
            else:
                # POST с form-data
                response = self._session.post(
                    url,
                    data=params,  # form-data, не JSON
                    timeout=self.timeout
                )
            
            # Обрабатываем ответ
            return self._handle_response(response)
        
        except requests.exceptions.Timeout:
            raise TikalConnectionError("Request timeout exceeded")
        except requests.exceptions.ConnectionError as e:
            raise TikalConnectionError(f"Connection error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise TikalConnectionError(f"Request error: {str(e)}")
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Обрабатывает ответ API и выбрасывает соответствующие исключения
        """
        status_code = response.status_code
        
        # Успешные ответы
        if 200 <= status_code < 300:
            try:
                # Пытаемся распарсить как JSON
                if self.format == 'json':
                    return response.json()
                else:
                    # XML формат - возвращаем текст для дальнейшей обработки
                    return {'xml': response.text}
            except ValueError:
                # Если не JSON, возвращаем текст
                return {'text': response.text}
        
        # Ошибка валидации
        if status_code == 400:
            error_msg = "Validation error"
            try:
                error_data = response.json() if self.format == 'json' else {'text': response.text}
                error_msg = error_data.get('message', error_data.get('error', error_msg))
            except:
                error_msg = f"{error_msg} - {response.text}"
            raise TikalValidationError(error_msg, status_code, response)
        
        # Доступ запрещен (неверный api_key)
        if status_code == 401 or status_code == 403:
            raise TikalAuthenticationError(
                "Authentication failed. Check your api_key.",
                status_code,
                response
            )
        
        # Ресурс не найден
        if status_code == 404:
            raise TikalNotFoundError(
                "Resource not found",
                status_code,
                response
            )
        
        # Превышен лимит запросов
        if status_code == 429:
            raise TikalRateLimitError(
                "Rate limit exceeded",
                status_code,
                response
            )
        
        # Ошибки сервера
        if 500 <= status_code < 600:
            error_msg = f"Server error: {status_code}"
            try:
                error_data = response.json() if self.format == 'json' else {'text': response.text}
                error_msg = error_data.get('message', error_msg)
            except:
                error_msg = f"{error_msg} - {response.text}"
            raise TikalServerError(error_msg, status_code, response)
        
        # Другие ошибки
        error_msg = f"Unexpected error: {status_code}"
        try:
            error_data = response.json() if self.format == 'json' else {'text': response.text}
            error_msg = error_data.get('message', error_msg)
        except:
            error_msg = f"{error_msg} - {response.text}"
        
        raise TikalAPIError(error_msg, status_code, response)
    
    def post(self, endpoint: str, params: Optional[Dict] = None, **url_kwargs) -> Dict[str, Any]:
        """Выполняет POST запрос"""
        return self._make_request('POST', endpoint, params=params, **url_kwargs)
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **url_kwargs) -> Dict[str, Any]:
        """Выполняет GET запрос (не рекомендуется, но поддерживается)"""
        return self._make_request('GET', endpoint, params=params, **url_kwargs)
    
    def close(self):
        """Закрывает сессию"""
        self._session.close()
        logger.info("API client closed")

