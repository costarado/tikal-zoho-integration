"""
Примеры использования Tikal Call Center API Client
"""

import logging
from datetime import datetime, timedelta
from config import TIKAL_CONFIG
from tikal_client import TikalClient

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def example_initialization():
    """Пример инициализации клиента"""
    print("\n=== Пример 1: Инициализация клиента ===")
    
    # Инициализация с токенами
    client = TikalClient(
        base_url=TIKAL_CONFIG['base_url'],
        access_token=TIKAL_CONFIG['access_token'],
        refresh_token=TIKAL_CONFIG['refresh_token']
    )
    
    print("Клиент успешно инициализирован")
    return client


def example_calls(client: TikalClient):
    """Примеры работы со звонками"""
    print("\n=== Пример 2: Работа со звонками ===")
    
    try:
        print("Попытка подключения к API...")
        # Получение списка звонков за последние 7 дней
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        calls = client.calls.list(
            start_date=start_date,
            end_date=end_date,
            limit=10
        )
        
        print(f"Найдено звонков: {len(calls) if isinstance(calls, list) else 'N/A'}")
        
        # Если есть звонки, получаем детали первого
        if isinstance(calls, list) and len(calls) > 0:
            first_call_id = calls[0].get('id')
            if first_call_id:
                call_details = client.calls.get(first_call_id)
                print(f"Детали звонка {first_call_id}: {call_details}")
        
        # Получение звонков за период
        recent_calls = client.calls.get_by_date_range(
            start_date=start_date,
            end_date=end_date
        )
        print(f"Звонков за период: {len(recent_calls)}")
        
    except Exception as e:
        print(f"Ошибка при работе со звонками: {e}")
        print("\n💡 Совет: Запустите 'python check_connection.py' для диагностики подключения")


def example_recordings(client: TikalClient):
    """Примеры работы с записями"""
    print("\n=== Пример 3: Работа с записями ===")
    
    try:
        # Получение списка записей за последние 7 дней
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        recordings = client.recordings.list(
            start_date=start_date,
            end_date=end_date,
            limit=10
        )
        
        print(f"Найдено записей: {len(recordings) if isinstance(recordings, list) else 'N/A'}")
        
        # Если есть записи, получаем детали первой
        if isinstance(recordings, list) and len(recordings) > 0:
            first_recording_id = recordings[0].get('id')
            if first_recording_id:
                recording_details = client.recordings.get(first_recording_id)
                print(f"Детали записи {first_recording_id}: {recording_details}")
                
                # Получение URL для скачивания
                download_url = client.recordings.download_url(first_recording_id)
                if download_url:
                    print(f"URL для скачивания: {download_url}")
        
    except Exception as e:
        print(f"Ошибка при работе с записями: {e}")


def example_agents(client: TikalClient):
    """Примеры работы с агентами"""
    print("\n=== Пример 4: Работа с агентами ===")
    
    try:
        # Получение списка всех агентов
        agents = client.agents.list()
        print(f"Найдено агентов: {len(agents) if isinstance(agents, list) else 'N/A'}")
        
        # Получение онлайн агентов
        online_agents = client.agents.get_online()
        print(f"Онлайн агентов: {len(online_agents)}")
        
        # Получение офлайн агентов
        offline_agents = client.agents.get_offline()
        print(f"Офлайн агентов: {len(offline_agents)}")
        
        # Если есть агенты, получаем детали первого
        if isinstance(agents, list) and len(agents) > 0:
            first_agent_id = agents[0].get('id')
            if first_agent_id:
                agent_details = client.agents.get(first_agent_id)
                print(f"Детали агента {first_agent_id}: {agent_details}")
                
                # Получение статуса агента
                agent_status = client.agents.get_status(first_agent_id)
                print(f"Статус агента: {agent_status}")
        
    except Exception as e:
        print(f"Ошибка при работе с агентами: {e}")


def example_statistics(client: TikalClient):
    """Примеры работы со статистикой"""
    print("\n=== Пример 5: Работа со статистикой ===")
    
    try:
        # Статистика по звонкам за последние 7 дней
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        calls_stats = client.statistics.calls(
            start_date=start_date,
            end_date=end_date,
            group_by='day'
        )
        print(f"Статистика по звонкам: {calls_stats}")
        
        # Статистика по агентам
        agents_stats = client.statistics.agents(
            start_date=start_date,
            end_date=end_date
        )
        print(f"Статистика по агентам: {agents_stats}")
        
        # Статистика по очередям
        queues_stats = client.statistics.queues(
            start_date=start_date,
            end_date=end_date
        )
        print(f"Статистика по очередям: {queues_stats}")
        
        # Сводная статистика за сегодня
        today_summary = client.statistics.get_daily_summary(datetime.now())
        print(f"Сводная статистика за сегодня: {today_summary}")
        
    except Exception as e:
        print(f"Ошибка при работе со статистикой: {e}")


def example_create_call(client: TikalClient):
    """Пример создания исходящего звонка"""
    print("\n=== Пример 6: Создание исходящего звонка ===")
    
    try:
        # Создание звонка (закомментировано, чтобы не создавать реальный звонок)
        # new_call = client.calls.create(
        #     phone_number='+1234567890',
        #     agent_id='agent_123'
        # )
        # print(f"Создан звонок: {new_call}")
        
        print("Пример создания звонка (закомментирован)")
        print("Раскомментируйте код для реального создания звонка")
        
    except Exception as e:
        print(f"Ошибка при создании звонка: {e}")


def main():
    """Основная функция с примерами"""
    print("=" * 60)
    print("Примеры использования Tikal Call Center API Client")
    print("=" * 60)
    print("\n⚠ Примечание: Для работы примеров необходим доступ к API серверу.")
    print("   Если возникают ошибки подключения, запустите:")
    print("   python check_connection.py\n")
    
    # Инициализация клиента
    client = example_initialization()
    
    try:
        # Примеры использования различных сервисов
        example_calls(client)
        example_recordings(client)
        example_agents(client)
        example_statistics(client)
        example_create_call(client)
        
    except Exception as e:
        logger.error(f"Общая ошибка: {e}", exc_info=True)
    
    finally:
        # Закрытие клиента
        client.close()
        print("\n=== Клиент закрыт ===")


if __name__ == '__main__':
    main()

