"""
Основной клиент для работы с Tikal Call Center API
"""

import logging
import requests
from typing import Optional, Dict, Any, List
from .auth import AuthenticationManager
from .exceptions import (
    TikalAPIError,
    TikalAuthenticationError,
    TikalConnectionError,
    TikalNotFoundError,
    TikalRateLimitError,
    TikalServerError,
    TikalValidationError
)
from .utils import format_url, retry_on_error, parse_response

logger = logging.getLogger(__name__)


class TikalClient:
    """
    Основной клиент для взаимодействия с Tikal Call Center API
    """
    
    def __init__(
        self,
        base_url: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 30,
        retry_attempts: int = 3
    ):
        """
        Инициализация клиента
        
        Args:
            base_url: Базовый URL API
            access_token: Токен доступа
            refresh_token: Токен обновления
            username: Имя пользователя
            password: Пароль
            timeout: Таймаут запросов в секундах
            retry_attempts: Количество попыток при ошибках
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        
        # Инициализация менеджера аутентификации
        self.auth = AuthenticationManager(
            base_url=self.base_url,
            access_token=access_token,
            refresh_token=refresh_token,
            username=username,
            password=password
        )
        
        # Создаем сессию для запросов
        self._session = requests.Session()
        
        # Импортируем сервисы (будет создано позже)
        from .services.calls import CallsService
        from .services.recordings import RecordingsService
        from .services.agents import AgentsService
        from .services.statistics import StatisticsService
        from .services.cdr import CDRService
        
        # Инициализируем сервисы
        self.calls = CallsService(self)
        self.recordings = RecordingsService(self)
        self.agents = AgentsService(self)
        self.statistics = StatisticsService(self)
        self.cdr = CDRService(self)
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **url_kwargs
    ) -> Dict[str, Any]:
        """
        Выполняет HTTP запрос к API
        
        Args:
            method: HTTP метод (GET, POST, PUT, DELETE)
            endpoint: Endpoint API
            params: Query параметры
            json_data: JSON данные для тела запроса
            headers: Дополнительные заголовки
            **url_kwargs: Параметры для форматирования URL
        
        Returns:
            Ответ API в виде словаря
        
        Raises:
            Различные TikalAPIError в зависимости от типа ошибки
        """
        # Убеждаемся, что токен валиден
        self.auth.ensure_valid_token()
        
        # Формируем URL
        url = format_url(self.base_url, endpoint, **url_kwargs)
        
        # Получаем заголовки аутентификации
        request_headers = self.auth.get_auth_headers()
        if headers:
            request_headers.update(headers)
        
        # Выполняем запрос с повторными попытками
        return self._execute_request_with_retry(
            method, url, params, json_data, request_headers
        )
    
    @retry_on_error(max_attempts=3, delay=1.0)
    def _execute_request_with_retry(
        self,
        method: str,
        url: str,
        params: Optional[Dict],
        json_data: Optional[Dict],
        headers: Dict
    ) -> Dict[str, Any]:
        """
        Выполняет запрос с обработкой ошибок и автоматическим обновлением токена
        """
        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=headers,
                timeout=self.timeout
            )
            
            # Обрабатываем ответ
            return self._handle_response(response)
        
        except requests.exceptions.Timeout:
            raise TikalConnectionError(
                f"Превышено время ожидания запроса ({self.timeout} сек)",
                url=url
            )
        except requests.exceptions.ConnectionError as e:
            error_msg = (
                f"Не удалось подключиться к серверу {self.base_url}. "
                f"Проверьте:\n"
                f"  1. Доступность сервера\n"
                f"  2. Правильность URL (возможно нужен другой порт или протокол)\n"
                f"  3. Настройки файрвола/сети\n"
                f"Детали: {str(e)}"
            )
            raise TikalConnectionError(error_msg, url=url)
        except requests.exceptions.RequestException as e:
            raise TikalConnectionError(f"Ошибка запроса: {str(e)}", url=url)
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Обрабатывает ответ API и выбрасывает соответствующие исключения
        """
        status_code = response.status_code
        
        # Успешные ответы
        if 200 <= status_code < 300:
            try:
                return parse_response(response.json())
            except ValueError:
                # Если ответ не JSON, возвращаем текст
                return {'content': response.text}
        
        # Ошибка аутентификации - пытаемся обновить токен
        if status_code == 401:
            logger.warning("Получен 401, пытаемся обновить токен...")
            try:
                self.auth.refresh_access_token()
                # Повторяем запрос с новым токеном
                headers = self.auth.get_auth_headers()
                retry_response = self._session.request(
                    method=response.request.method,
                    url=response.url,
                    params=response.request.params,
                    json=response.request.json if hasattr(response.request, 'json') else None,
                    headers=headers,
                    timeout=self.timeout
                )
                return self._handle_response(retry_response)
            except Exception as e:
                raise TikalAuthenticationError(
                    f"Ошибка аутентификации: {str(e)}",
                    status_code
                )
        
        # Ошибка валидации
        if status_code == 400:
            error_msg = "Ошибка валидации запроса"
            try:
                error_data = response.json()
                error_msg = error_data.get('message', error_msg)
            except:
                error_msg = f"{error_msg} - {response.text}"
            raise TikalValidationError(error_msg, status_code, response)
        
        # Доступ запрещен
        if status_code == 403:
            raise TikalAuthenticationError(
                "Доступ запрещен",
                status_code,
                response
            )
        
        # Ресурс не найден
        if status_code == 404:
            raise TikalNotFoundError(
                "Ресурс не найден",
                status_code,
                response
            )
        
        # Превышен лимит запросов
        if status_code == 429:
            raise TikalRateLimitError(
                "Превышен лимит запросов",
                status_code,
                response
            )
        
        # Ошибки сервера
        if 500 <= status_code < 600:
            error_msg = f"Ошибка сервера: {status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('message', error_msg)
            except:
                error_msg = f"{error_msg} - {response.text}"
            raise TikalServerError(error_msg, status_code, response)
        
        # Другие ошибки
        error_msg = f"Неожиданная ошибка: {status_code}"
        try:
            error_data = response.json()
            error_msg = error_data.get('message', error_msg)
        except:
            error_msg = f"{error_msg} - {response.text}"
        
        raise TikalAPIError(error_msg, status_code, response)
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **url_kwargs) -> Dict[str, Any]:
        """Выполняет GET запрос"""
        return self._make_request('GET', endpoint, params=params, **url_kwargs)
    
    def post(self, endpoint: str, json_data: Optional[Dict] = None, **url_kwargs) -> Dict[str, Any]:
        """Выполняет POST запрос"""
        return self._make_request('POST', endpoint, json_data=json_data, **url_kwargs)
    
    def put(self, endpoint: str, json_data: Optional[Dict] = None, **url_kwargs) -> Dict[str, Any]:
        """Выполняет PUT запрос"""
        return self._make_request('PUT', endpoint, json_data=json_data, **url_kwargs)
    
    def delete(self, endpoint: str, **url_kwargs) -> Dict[str, Any]:
        """Выполняет DELETE запрос"""
        return self._make_request('DELETE', endpoint, **url_kwargs)
    
    def close(self):
        """Закрывает сессию и выполняет выход"""
        self.auth.logout()
        self._session.close()
        logger.info("Клиент закрыт")

