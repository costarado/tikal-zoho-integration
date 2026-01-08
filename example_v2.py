"""
Примеры использования обновленного Tikal API Client v2
"""

import logging
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def example_agent_operations(client: TikalClientV2):
    """Примеры работы с агентами"""
    print("\n=== Пример: Работа с агентами ===")
    
    try:
        # Создание агента
        print("\n1. Создание агента...")
        # Используем правильные параметры: name только буквы/дефисы/пробелы, department только цифры
        new_agent = client.agents.create(
            agent_id='2012',
            name='bisly agent',  # Исправлено: убрали подчеркивание, добавили пробел
            password='1234',
            department=1  # Исправлено: только цифры, не строка
        )
        print(f"   Результат: {new_agent}")
        
        # Редактирование агента
        print("\n2. Редактирование агента...")
        # name должен содержать только буквы, дефисы или пробелы
        updated = client.agents.edit(
            agent_id='2012',
            name='bisly updated',  # Исправлено: пробел вместо подчеркивания
            wrapuptime=30
        )
        print(f"   Результат: {updated}")
        
        # Получение состояния агента (нужен существующий ID)
        print("\n3. Получение состояния агента...")
        # Используем реальный ID из системы (например, из вывода get_outgoing)
        # state = client.agents.get_state('8011')  # Пример из вывода
        # print(f"   Состояние: {state}")
        print("   (пропущено - нужен существующий ID агента)")
        
        # Логин агента (требует ag_exten)
        print("\n4. Логин агента...")
        # login_result = client.agents.login('2012', ag_exten='2012')  # Пример
        # print(f"   Результат: {login_result}")
        print("   (пропущено - нужен ag_exten - extension агента)")
        
    except Exception as e:
        print(f"   Ошибка: {e}")


def example_queue_operations(client: TikalClientV2):
    """Примеры работы с очередями"""
    print("\n=== Пример: Работа с очередями ===")
    
    try:
        # Создание очереди
        print("\n1. Создание очереди...")
        new_queue = client.queues.create(
            queue_id='3000',
            name='Sales Queue'
        )
        print(f"   Результат: {new_queue}")
        
        # Получение агентов в очереди
        print("\n2. Получение агентов в очереди...")
        agents = client.queues.get_agents('3000')
        print(f"   Агенты: {agents}")
        
        # Удаление очереди
        print("\n3. Удаление очереди...")
        # Раскомментируйте для реального удаления:
        # result = client.queues.delete('3000')
        # print(f"   Результат: {result}")
        print("   (закомментировано для безопасности)")
        
    except Exception as e:
        print(f"   Ошибка: {e}")


def example_call_operations(client: TikalClientV2):
    """Примеры работы со звонками"""
    print("\n=== Пример: Работа со звонками ===")
    
    try:
        # Создание звонка (Originate)
        print("\n1. Создание звонка (Originate)...")
        # Исправлено: dest_num должен содержать ТОЛЬКО ЦИФРЫ (без +, пробелов и т.д.)
        # Используем реальный номер из предыдущего вывода
        call = client.calls.originate(
            agent_id='8011',  # Используем существующий ID из get_outgoing
            dest_num='0508155492',  # Исправлено: только цифры, без +
            custom1='campaign_123',
            custom2='lead_456'
        )
        print(f"   Результат: {call}")
        
        # Получение входящих звонков
        print("\n2. Получение входящих звонков...")
        incoming = client.calls.get_incoming()
        print(f"   Входящие: {incoming}")
        
        # Получение исходящих звонков
        print("\n3. Получение исходящих звонков...")
        outgoing = client.calls.get_outgoing()
        print(f"   Исходящие: {outgoing}")
        
        # Получение CDR (требует unique_id)
        print("\n4. Получение CDR...")
        # Используем unique_id из предыдущего вызова get_outgoing
        # Пример: uniqueid из вывода '1740053479.1105665'
        # cdr = client.calls.get_cdr(unique_id='1740053479.1105665')
        # print(f"   CDR: {cdr}")
        print("   (пропущено - нужен unique_id звонка)")
        print("   Используйте uniqueid из get_outgoing или get_incoming")
        
    except Exception as e:
        print(f"   Ошибка: {e}")


def main():
    """Основная функция с примерами"""
    print("=" * 70)
    print("Примеры использования Tikal API Client v2")
    print("=" * 70)
    
    # Проверяем наличие api_key
    api_key = TIKAL_CONFIG.get('api_key')
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        print("\n⚠ ВНИМАНИЕ: Необходимо установить api_key в config.py")
        print("   Получите api_key при установке API в Tikal")
        print("\n⚠ אזהרה: יש להגדיר api_key בקובץ config.py")
        print("   קבל את api_key בעת התקנת ה-API ב-Tikal")
        return
    
    # Инициализация клиента
    try:
        client = TikalClientV2(
            base_url=TIKAL_CONFIG['base_url'],
            api_key=api_key,
            format=TIKAL_CONFIG.get('format', 'json')
        )
        
        print(f"\n✓ Клиент инициализирован")
        print(f"  Base URL: {TIKAL_CONFIG['base_url']}")
        print(f"  Format: {TIKAL_CONFIG.get('format', 'json')}")
        
        # Примеры использования
        example_agent_operations(client)
        example_queue_operations(client)
        example_call_operations(client)
        
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        print(f"\n✗ Ошибка: {e}")
    
    finally:
        try:
            client.close()
            print("\n✓ Клиент закрыт")
        except:
            pass


if __name__ == '__main__':
    main()

