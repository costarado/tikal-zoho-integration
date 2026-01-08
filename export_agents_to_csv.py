"""
Утилита для экспорта данных агентов в CSV формат
"""

import csv
import os
from datetime import datetime
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG


def export_agents_to_csv(client: TikalClientV2, output_file: str = None):
    """
    Экспортирует данные агентов в CSV файл
    
    Args:
        client: Экземпляр TikalClientV2
        output_file: Путь к выходному файлу (если None, создается автоматически)
    
    Returns:
        Путь к созданному файлу
    """
    if output_file is None:
        timestamp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        output_file = f'agents_report_1_{timestamp}.csv'
    
    print(f"Экспорт данных агентов в {output_file}...")
    
    # Получаем данные из системы
    # Примечание: Tikal API может не иметь прямого метода для получения списка всех агентов
    # Используем доступные методы
    
    agents_data = []
    
    # Попробуем получить данные через очереди
    try:
        # Получаем агентов из очередей
        print("Получение данных из очередей...")
        
        # Пример: получаем агентов из очереди 3000 (или других)
        queue_ids = ['3000', '1066', '1135']  # Можно расширить список
        
        for queue_id in queue_ids:
            try:
                result = client.queues.get_agents(queue_id)
                if result.get('data', {}).get('status', {}).get('code') == '200':
                    agents_str = result.get('data', {}).get('info', {}).get('assigned_agents', '')
                    if agents_str:
                        # Парсим строку агентов (формат может быть разным)
                        agent_ids = [a.strip() for a in agents_str.split(',') if a.strip()]
                        for agent_id in agent_ids:
                            if agent_id not in [a.get('id') for a in agents_data]:
                                agents_data.append({
                                    'id': agent_id,
                                    'queue': queue_id,
                                    'source': 'queue'
                                })
            except Exception as e:
                print(f"  Ошибка при получении агентов из очереди {queue_id}: {e}")
    
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
    
    # Если нет данных из очередей, используем данные из исходящих звонков
    if not agents_data:
        print("Получение данных из звонков...")
        try:
            outgoing = client.calls.get_outgoing()
            if outgoing.get('data', {}).get('status', {}).get('code') == '200':
                calls = outgoing.get('data', {}).get('info', {}).get('calls', [])
                for call in calls:
                    agent_id = call.get('agent_id')
                    if agent_id and agent_id not in [a.get('id') for a in agents_data]:
                        agents_data.append({
                            'id': agent_id,
                            'queue': call.get('queue', ''),
                            'source': 'calls'
                        })
        except Exception as e:
            print(f"Ошибка при получении данных из звонков: {e}")
    
    # Записываем в CSV
    if agents_data:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'queue', 'source', 'name', 'status', 'extension']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for agent in agents_data:
                # Пытаемся получить дополнительную информацию об агенте
                try:
                    state_result = client.agents.get_state(agent['id'])
                    if state_result.get('data', {}).get('status', {}).get('code') == '200':
                        info = state_result.get('data', {}).get('info', {})
                        agent['status'] = info.get('status', '')
                        agent['extension'] = info.get('extension', '')
                        agent['name'] = info.get('name', '')
                except:
                    pass
                
                writer.writerow(agent)
        
        print(f"✓ Экспортировано {len(agents_data)} агентов в {output_file}")
        return output_file
    else:
        print("⚠ Не найдено данных об агентах для экспорта")
        return None


def export_calls_to_csv(client: TikalClientV2, call_type: str = 'outgoing', output_file: str = None):
    """
    Экспортирует данные звонков в CSV
    
    Args:
        client: Экземпляр TikalClientV2
        call_type: Тип звонков ('incoming' или 'outgoing')
        output_file: Путь к выходному файлу
    """
    if output_file is None:
        timestamp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        output_file = f'calls_{call_type}_{timestamp}.csv'
    
    print(f"Экспорт {call_type} звонков в {output_file}...")
    
    try:
        if call_type == 'outgoing':
            result = client.calls.get_outgoing()
        else:
            result = client.calls.get_incoming()
        
        if result.get('data', {}).get('status', {}).get('code') == '200':
            calls = result.get('data', {}).get('info', {}).get('calls', [])
            
            if calls:
                with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['order', 'uniqueid', 'queue', 'start_time', 'number', 'agent_id']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for call in calls:
                        writer.writerow(call)
                
                print(f"✓ Экспортировано {len(calls)} звонков в {output_file}")
                return output_file
            else:
                print(f"Нет {call_type} звонков для экспорта")
                return None
        else:
            print(f"Ошибка: {result.get('data', {}).get('status', {}).get('description')}")
            return None
    
    except Exception as e:
        print(f"Ошибка при экспорте: {e}")
        return None


def main():
    """Основная функция"""
    print("=" * 70)
    print("Экспорт данных Tikal в CSV")
    print("=" * 70)
    
    client = TikalClientV2(
        base_url=TIKAL_CONFIG['base_url'],
        api_key=TIKAL_CONFIG['api_key'],
        format=TIKAL_CONFIG.get('format', 'json')
    )
    
    try:
        # Экспорт агентов
        print("\n1. Экспорт агентов...")
        agents_file = export_agents_to_csv(client)
        
        # Экспорт исходящих звонков
        print("\n2. Экспорт исходящих звонков...")
        outgoing_file = export_calls_to_csv(client, 'outgoing')
        
        # Экспорт входящих звонков
        print("\n3. Экспорт входящих звонков...")
        incoming_file = export_calls_to_csv(client, 'incoming')
        
        print("\n" + "=" * 70)
        print("Экспорт завершен")
        print("=" * 70)
        if agents_file:
            print(f"Агенты: {agents_file}")
        if outgoing_file:
            print(f"Исходящие звонки: {outgoing_file}")
        if incoming_file:
            print(f"Входящие звонки: {incoming_file}")
    
    except Exception as e:
        print(f"\n✗ Ошибка: {e}")
    
    finally:
        client.close()


if __name__ == '__main__':
    main()

