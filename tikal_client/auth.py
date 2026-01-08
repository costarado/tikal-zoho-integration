"""
Модуль управления аутентификацией для Tikal API
"""

import logging
import time
from typing import Optional, Dict
import requests
from .exceptions import TikalAuthenticationError, TikalConnectionError
from .utils import format_url

logger = logging.getLogger(__name__)


class AuthenticationManager:
    """
    Менеджер аутентификации для управления токенами доступа
    """
    
    def __init__(
        self,
        base_url: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        """
        Инициализация менеджера аутентификации
        
        Args:
            base_url: Базовый URL API
            access_token: Токен доступа (если уже есть)
            refresh_token: Токен обновления (если уже есть)
            username: Имя пользователя для логина
            password: Пароль для логина
        """
        self.base_url = base_url
        self._access_token = access_token
        self._refresh_token = refresh_token
        self.username = username
        self.password = password
        self._token_expires_at = None
        self._session = requests.Session()
        
        # Если токены не предоставлены, но есть credentials, выполняем логин
        if not self._access_token and username and password:
            self.login()
    
    @property
    def access_token(self) -> Optional[str]:
        """Получить текущий access token"""
        return self._access_token
    
    @property
    def refresh_token(self) -> Optional[str]:
        """Получить текущий refresh token"""
        return self._refresh_token
    
    def is_token_valid(self) -> bool:
        """
        Проверяет, валиден ли текущий токен
        
        Returns:
            True если токен валиден, False иначе
        """
        if not self._access_token:
            return False
        
        # Если есть информация о времени истечения, проверяем её
        if self._token_expires_at:
            return time.time() < self._token_expires_at
        
        # Если нет информации о времени истечения, считаем токен валидным
        # (реальная проверка будет при запросе к API)
        return True
    
    def login(self) -> Dict:
        """
        Выполняет вход в систему и получает токены
        
        Returns:
            Словарь с токенами доступа
        
        Raises:
            TikalAuthenticationError: При ошибке аутентификации
            TikalConnectionError: При ошибке подключения
        """
        if not self.username or not self.password:
            raise TikalAuthenticationError(
                "Необходимы username и password для входа"
            )
        
        url = format_url(self.base_url, '/api/auth/login')
        
        try:
            response = self._session.post(
                url,
                json={
                    'username': self.username,
                    'password': self.password
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self._access_token = data.get('access_token')
                self._refresh_token = data.get('refresh_token')
                
                # Устанавливаем время истечения токена (если указано в ответе)
                expires_in = data.get('expires_in', 3600)  # По умолчанию 1 час
                self._token_expires_at = time.time() + expires_in
                
                logger.info("Успешная аутентификация")
                return {
                    'access_token': self._access_token,
                    'refresh_token': self._refresh_token
                }
            else:
                error_msg = f"Ошибка аутентификации: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', error_msg)
                except:
                    error_msg = f"{error_msg} - {response.text}"
                
                raise TikalAuthenticationError(error_msg, response.status_code)
        
        except requests.exceptions.RequestException as e:
            raise TikalConnectionError(f"Ошибка подключения при входе: {str(e)}")
    
    def refresh_access_token(self) -> Dict:
        """
        Обновляет access token используя refresh token
        
        Returns:
            Словарь с новыми токенами
        
        Raises:
            TikalAuthenticationError: При ошибке обновления токена
            TikalConnectionError: При ошибке подключения
        """
        if not self._refresh_token:
            # Если нет refresh token, пытаемся войти заново
            if self.username and self.password:
                return self.login()
            raise TikalAuthenticationError(
                "Нет refresh token для обновления доступа"
            )
        
        url = format_url(self.base_url, '/api/auth/refresh')
        
        try:
            response = self._session.post(
                url,
                json={'refresh_token': self._refresh_token},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self._access_token = data.get('access_token')
                
                # Обновляем refresh token, если он предоставлен
                if 'refresh_token' in data:
                    self._refresh_token = data.get('refresh_token')
                
                # Устанавливаем время истечения токена
                expires_in = data.get('expires_in', 3600)
                self._token_expires_at = time.time() + expires_in
                
                logger.info("Токен доступа успешно обновлен")
                return {
                    'access_token': self._access_token,
                    'refresh_token': self._refresh_token
                }
            else:
                error_msg = f"Ошибка обновления токена: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', error_msg)
                except:
                    error_msg = f"{error_msg} - {response.text}"
                
                # Если refresh token невалиден, пытаемся войти заново
                if response.status_code == 401 and self.username and self.password:
                    logger.warning("Refresh token невалиден, выполняем повторный вход")
                    return self.login()
                
                raise TikalAuthenticationError(error_msg, response.status_code)
        
        except requests.exceptions.RequestException as e:
            raise TikalConnectionError(
                f"Ошибка подключения при обновлении токена: {str(e)}"
            )
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Получает заголовки для аутентификации
        
        Returns:
            Словарь с заголовками Authorization
        
        Raises:
            TikalAuthenticationError: Если токен недоступен
        """
        if not self._access_token:
            if self.username and self.password:
                self.login()
            else:
                raise TikalAuthenticationError("Токен доступа недоступен")
        
        return {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json'
        }
    
    def ensure_valid_token(self):
        """
        Убеждается, что токен валиден, обновляя его при необходимости
        """
        if not self.is_token_valid():
            logger.info("Токен истек или невалиден, обновляем...")
            self.refresh_access_token()
    
    def logout(self):
        """
        Выполняет выход из системы
        """
        if self._access_token:
            url = format_url(self.base_url, '/api/auth/logout')
            try:
                self._session.post(
                    url,
                    headers=self.get_auth_headers(),
                    timeout=30
                )
            except Exception as e:
                logger.warning(f"Ошибка при выходе: {e}")
        
        self._access_token = None
        self._refresh_token = None
        self._token_expires_at = None
        logger.info("Выполнен выход из системы")

