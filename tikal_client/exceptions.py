"""
Кастомные исключения для Tikal API Client
"""


class TikalAPIError(Exception):
    """Базовое исключение для всех ошибок API"""
    
    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)
    
    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class TikalAuthenticationError(TikalAPIError):
    """Ошибка аутентификации (401, 403)"""
    pass


class TikalConnectionError(TikalAPIError):
    """Ошибка подключения к серверу"""
    
    def __init__(self, message, status_code=None, response=None, url=None):
        super().__init__(message, status_code, response)
        self.url = url
    
    def __str__(self):
        base_msg = super().__str__()
        if self.url:
            return f"{base_msg} (URL: {self.url})"
        return base_msg


class TikalNotFoundError(TikalAPIError):
    """Ресурс не найден (404)"""
    pass


class TikalRateLimitError(TikalAPIError):
    """Превышен лимит запросов (429)"""
    pass


class TikalValidationError(TikalAPIError):
    """Ошибка валидации данных (400)"""
    pass


class TikalServerError(TikalAPIError):
    """Ошибка сервера (5xx)"""
    pass

