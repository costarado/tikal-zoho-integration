"""
Рабочие примеры использования Tikal API
С использованием реальных данных из системы
"""

import logging
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Примеры с реальными данными"""
    print("=" * 70)
    print("Рабочие примеры Tikal API")
    print("=" * 70)
    
    client = TikalClientV2(
        base_url=TIKAL_CONFIG['base_url'],
        api_key=TIKAL_CONFIG['api_key'],
        format=TIKAL_CONFIG.get('format', 'json')
    )
    
    try:
        # 1. Получение исходящих звонков (работает)
        print("\n1. Получение исходящих звонков...")
        outgoing = client.calls.get_outgoing()
        
        if outgoing.get('data', {}).get('status', {}).get('code') == '200':
            calls = outgoing.get('data', {}).get('info', {}).get('calls', [])
            if calls:
                print(f"   ✓ Найдено {len(calls)} исходящих звонков")
                first_call = calls[0]
                print(f"   Первый звонок:")
                print(f"     - Unique ID: {first_call.get('uniqueid')}")
                print(f"     - Номер: {first_call.get('number')}")
                print(f"     - Агент: {first_call.get('agent_id')}")
                print(f"     - Очередь: {first_call.get('queue')}")
                
                # Используем эти данные для дальнейших операций
                unique_id = first_call.get('uniqueid')
                agent_id = first_call.get('agent_id')
                phone_number = first_call.get('number')
                
                # 2. Получение CDR для конкретного звонка
                print(f"\n2. Получение CDR для звонка {unique_id}...")
                cdr = client.calls.get_cdr(unique_id=unique_id)
                print(f"   Результат: {cdr.get('data', {}).get('status', {}).get('description')}")
                
                # 3. Создание нового звонка с правильными параметрами
                print(f"\n3. Создание звонка (Originate)...")
                print(f"   Агент: {agent_id}, Номер: {phone_number}")
                # dest_num должен содержать только цифры
                new_call = client.calls.originate(
                    agent_id=agent_id,
                    dest_num=phone_number,  # Уже только цифры из системы
                    custom1='test_campaign',
                    custom2='test_lead'
                )
                status = new_call.get('data', {}).get('status', {})
                print(f"   Статус: {status.get('code')} - {status.get('description')}")
            else:
                print("   Нет исходящих звонков")
        else:
            print(f"   Ошибка: {outgoing}")
        
        # 4. Получение агентов в очереди (работает)
        print("\n4. Получение агентов в очереди 3000...")
        queue_agents = client.queues.get_agents('3000')
        status = queue_agents.get('data', {}).get('status', {})
        if status.get('code') == '200':
            agents = queue_agents.get('data', {}).get('info', {}).get('assigned_agents', '')
            print(f"   ✓ Статус: {status.get('description')}")
            print(f"   Агенты: {agents if agents else 'Нет назначенных агентов'}")
        
        # 5. Получение входящих звонков
        print("\n5. Получение входящих звонков...")
        incoming = client.calls.get_incoming()
        status = incoming.get('data', {}).get('status', {})
        if status.get('code') == '200':
            calls = incoming.get('data', {}).get('info', {}).get('calls')
            if calls:
                print(f"   ✓ Найдено {len(calls)} входящих звонков")
            else:
                print(f"   ✓ Нет входящих звонков в данный момент")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        print(f"\n✗ Ошибка: {e}")
    
    finally:
        client.close()
        print("\n✓ Клиент закрыт")


if __name__ == '__main__':
    main()

