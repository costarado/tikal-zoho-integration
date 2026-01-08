"""
Утилиты для Tikal API Client
"""

import time
import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)


def retry_on_error(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Декоратор для повторных попыток при ошибках
    
    Args:
        max_attempts: Максимальное количество попыток
        delay: Начальная задержка между попытками (секунды)
        backoff: Множитель для увеличения задержки
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Импорт здесь, чтобы избежать циклических зависимостей
            from .exceptions import TikalConnectionError, TikalServerError
            
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (TikalConnectionError, TikalServerError) as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Попытка {attempt + 1}/{max_attempts} не удалась. "
                            f"Повтор через {current_delay:.2f} сек. Ошибка: {e}"
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"Все {max_attempts} попыток исчерпаны")
                except Exception as e:
                    # Для других ошибок не делаем повторные попытки
                    raise
            
            raise last_exception
        
        return wrapper
    return decorator


def format_url(base_url: str, endpoint: str, **kwargs) -> str:
    """
    Форматирует URL с параметрами
    
    Args:
        base_url: Базовый URL
        endpoint: Endpoint с плейсхолдерами (например, /api/calls/{id})
        **kwargs: Параметры для подстановки
    
    Returns:
        Отформатированный URL
    """
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    if kwargs:
        url = url.format(**kwargs)
    return url


def parse_response(response_data: dict) -> dict:
    """
    Парсит ответ API и извлекает данные
    
    Args:
        response_data: Сырые данные ответа
    
    Returns:
        Распарсенные данные
    """
    # Стандартные форматы ответов API
    if isinstance(response_data, dict):
        # Если есть поле 'data', возвращаем его
        if 'data' in response_data:
            return response_data['data']
        # Если есть поле 'result', возвращаем его
        if 'result' in response_data:
            return response_data['result']
        # Иначе возвращаем весь ответ
        return response_data
    
    return response_data

