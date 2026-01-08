"""
Утилита для получения всех очередей из системы
"""

from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG


def get_all_queues(client: TikalClientV2):
    """
    Пытается получить список всех очередей
    """
    print("=" * 70)
    print("Поиск всех очередей в системе")
    print("=" * 70)
    
    # Проверяем широкий диапазон ID очередей
    found_queues = []
    
    # Диапазон для проверки
    ranges = [
        (1000, 1200),  # Основной диапазон
        (3000, 3100),  # Дополнительный диапазон
    ]
    
    print("\nПроверка очередей...")
    
    for start, end in ranges:
        for queue_id in range(start, end):
            try:
                result = client.queues.get_agents(str(queue_id))
                status = result.get('data', {}).get('status', {})
                
                if status.get('code') == '200':
                    # Очередь существует
                    agents_str = result.get('data', {}).get('info', {}).get('assigned_agents', '')
                    agent_count = len([a for a in agents_str.split(',') if a.strip()]) if agents_str else 0
                    
                    found_queues.append({
                        'id': str(queue_id),
                        'agent_count': agent_count,
                        'agents': agents_str
                    })
                    print(f"  ✓ Очередь {queue_id}: {agent_count} агентов")
                elif status.get('code') == '205':
                    # Очередь не существует - пропускаем
                    pass
            except Exception as e:
                pass
    
    print(f"\n✓ Найдено {len(found_queues)} очередей")
    
    # Выводим список
    print("\nСписок найденных очередей:")
    for queue in found_queues:
        print(f"  {queue['id']}: {queue['agent_count']} агентов")
    
    # Сохраняем в файл
    import json
    with open('all_queues.json', 'w', encoding='utf-8') as f:
        json.dump(found_queues, f, indent=2, ensure_ascii=False)
    
    print(f"\nСписок сохранен в all_queues.json")
    
    return found_queues


def main():
    """Основная функция"""
    import sys
    import io
    
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    try:
        client = TikalClientV2(
            base_url=TIKAL_CONFIG['base_url'],
            api_key=TIKAL_CONFIG['api_key'],
            format=TIKAL_CONFIG.get('format', 'json')
        )
        
        queues = get_all_queues(client)
        
        # Теперь получаем всех агентов из найденных очередей
        print("\n" + "=" * 70)
        print("Получение всех агентов из найденных очередей")
        print("=" * 70)
        
        all_agents = {}
        for queue in queues:
            queue_id = queue['id']
            agents_str = queue.get('agents', '')
            if agents_str:
                agent_ids = [a.strip() for a in agents_str.split(',') if a.strip()]
                for agent_id in agent_ids:
                    if agent_id not in all_agents:
                        all_agents[agent_id] = {
                            'id': agent_id,
                            'queues': [queue_id]
                        }
                    else:
                        if queue_id not in all_agents[agent_id]['queues']:
                            all_agents[agent_id]['queues'].append(queue_id)
        
        print(f"\n✓ Найдено {len(all_agents)} уникальных агентов")
        print("\nСписок агентов:")
        for agent_id in sorted(all_agents.keys(), key=int):
            queues = ', '.join(all_agents[agent_id]['queues'])
            print(f"  {agent_id}: очереди {queues}")
        
        client.close()
    
    except Exception as e:
        print(f"\n✗ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

