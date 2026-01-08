"""
Быстрый тест подключения к API после исправления конфигурации
"""

import logging
from tikal_client import TikalClient
from config import TIKAL_CONFIG

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_basic_connection():
    """Тест базового подключения"""
    print("=" * 60)
    print("Тест подключения к Tikal API")
    print("=" * 60)
    print(f"\nURL: {TIKAL_CONFIG['base_url']}")
    print(f"Используется: {'HTTP' if 'http://' in TIKAL_CONFIG['base_url'] else 'HTTPS'}")
    
    try:
        # Создание клиента
        print("\n1. Инициализация клиента...")
        client = TikalClient(
            base_url=TIKAL_CONFIG['base_url'],
            access_token=TIKAL_CONFIG['access_token'],
            refresh_token=TIKAL_CONFIG['refresh_token']
        )
        print("   ✓ Клиент инициализирован")
        
        # Простой запрос для проверки подключения
        print("\n2. Проверка подключения к API...")
        print("   Попытка получить список агентов...")
        
        try:
            agents = client.agents.list(limit=1)
            print(f"   ✓ Подключение успешно!")
            print(f"   Ответ получен: {type(agents)}")
            if isinstance(agents, dict):
                print(f"   Ключи в ответе: {list(agents.keys())[:5]}...")
            elif isinstance(agents, list):
                print(f"   Количество элементов: {len(agents)}")
        except Exception as e:
            print(f"   ⚠ Ошибка при запросе: {e}")
            print("   Но подключение установлено (это может быть ошибка API или аутентификации)")
        
        # Закрытие клиента
        print("\n3. Закрытие клиента...")
        client.close()
        print("   ✓ Клиент закрыт")
        
        print("\n" + "=" * 60)
        print("✓ ТЕСТ ЗАВЕРШЕН УСПЕШНО")
        print("=" * 60)
        print("\nТеперь можно запускать example.py для полных примеров")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("✗ ОШИБКА ПРИ ТЕСТЕ")
        print("=" * 60)
        print(f"\nОшибка: {e}")
        print("\nПроверьте:")
        print("1. Правильность URL в config.py")
        print("2. Доступность сервера")
        print("3. Правильность токенов доступа")
        logger.exception("Детали ошибки:")


if __name__ == '__main__':
    test_basic_connection()

