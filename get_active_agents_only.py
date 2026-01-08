"""
Получение ТОЛЬКО активных агентов для импорта в Zoho CRM
Фильтрует неактивных агентов и неактивные очереди
"""

import csv
from datetime import datetime
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG


def is_agent_active(client: TikalClientV2, agent_id: str) -> tuple[bool, dict]:
    """
    Проверяет, активен ли агент
    Критерии активности:
    1. Агент существует в системе (get_state возвращает данные)
    2. Агент находится хотя бы в одной активной очереди
    
    Returns:
        (is_active, agent_info)
    """
    agent_info = {
        'id': agent_id,
        'name': '',
        'extension': '',
        'status': '',
        'is_active': False
    }
    
    try:
        state_result = client.agents.get_state(agent_id)
        if state_result.get('data', {}).get('status', {}).get('code') == '200':
            info = state_result.get('data', {}).get('info', {})
            agent_info['name'] = info.get('name', '')
            agent_info['extension'] = info.get('extension', '')
            agent_info['status'] = info.get('status', '')
            
            # Если агент существует и находится в активных очередях - считаем активным
            # (наличие в очереди уже проверено на предыдущем этапе)
            agent_info['is_active'] = True
            return True, agent_info
    except Exception as e:
        # Если не удалось получить данные - агент неактивен
        pass
    
    return False, agent_info


def get_active_queues_only(client: TikalClientV2) -> dict:
    """
    Получает только активные очереди (с агентами)
    
    Returns:
        Словарь {queue_id: [agent_ids]}
    """
    active_queues = {}
    
    # Расширенный список очередей
    queue_ids = [
        '1005', '1007', '1011', '1012', '1014', '1015', '1016', '1018', 
        '1020', '1021', '1066', '1135', '1146', '1155', '1163', '1164',
        '1140', '1141', '1142', '1143', '1148', '1149', '1150', '1151',
        '1152', '1153', '1154', '1156', '1157', '1159', '1161', '1162', '1167',
        '3000', '1067', '1068', '1136', '1137', '1138', '1139', '1144',
        '1145', '1147', '1165', '1166'
    ]
    
    print(f"Проверка {len(queue_ids)} очередей...")
    
    for queue_id in queue_ids:
        try:
            result = client.queues.get_agents(queue_id)
            if result.get('data', {}).get('status', {}).get('code') == '200':
                agents_str = result.get('data', {}).get('info', {}).get('assigned_agents', '')
                if agents_str:
                    agent_ids = [a.strip() for a in agents_str.split(',') if a.strip()]
                    if agent_ids:  # Только очереди с агентами
                        active_queues[queue_id] = agent_ids
                        print(f"  ✓ Очередь {queue_id}: {len(agent_ids)} агентов")
        except:
            pass
    
    return active_queues


def get_active_agents(client: TikalClientV2) -> list:
    """
    Получает только активных агентов из активных очередей
    
    Returns:
        Список активных агентов с полной информацией
    """
    print("=" * 70)
    print("Получение АКТИВНЫХ агентов для Zoho CRM")
    print("=" * 70)
    
    # Шаг 1: Получаем активные очереди
    print("\n1. Поиск активных очередей...")
    active_queues = get_active_queues_only(client)
    print(f"\n✓ Найдено {len(active_queues)} активных очередей")
    
    # Шаг 2: Собираем уникальных агентов
    print("\n2. Сбор уникальных агентов из активных очередей...")
    all_agent_ids = set()
    agent_queues_map = {}  # agent_id -> [queue_ids]
    
    for queue_id, agent_ids in active_queues.items():
        for agent_id in agent_ids:
            all_agent_ids.add(agent_id)
            if agent_id not in agent_queues_map:
                agent_queues_map[agent_id] = []
            agent_queues_map[agent_id].append(queue_id)
    
    print(f"✓ Найдено {len(all_agent_ids)} уникальных агентов")
    
    # Шаг 3: Проверяем статус каждого агента
    print("\n3. Проверка статуса агентов...")
    active_agents = []
    inactive_count = 0
    
    for i, agent_id in enumerate(sorted(all_agent_ids, key=int), 1):
        is_active, agent_info = is_agent_active(client, agent_id)
        
        if is_active:
            agent_info['queues'] = agent_queues_map.get(agent_id, [])
            active_agents.append(agent_info)
            status_icon = "✓"
        else:
            inactive_count += 1
            status_icon = "✗"
        
        name = agent_info.get('name', 'N/A')
        status = agent_info.get('status', 'N/A')
        print(f"  {status_icon} {i}/{len(all_agent_ids)}: {agent_id} - {name} [{status}]")
    
    print(f"\n✓ Активных агентов: {len(active_agents)}")
    print(f"✗ Неактивных агентов: {inactive_count}")
    
    return active_agents


def export_active_agents_to_zoho(agents: list, output_file: str = None) -> str:
    """
    Экспортирует активных агентов в формат Zoho CRM
    """
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'zoho_agents_ACTIVE_{timestamp}.csv'
    
    zoho_fields = [
        'First Name',
        'Last Name',
        'Email',
        'Phone',
        'Mobile',
        'Title',
        'Department',
        'Lead Source',
        'Description',
        'Agent ID',
        'Extension',
        'Status',
        'Queues',
        'Queue Count',
        'Is Active',
    ]
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=zoho_fields)
            writer.writeheader()
            
            for agent in agents:
                name = agent.get('name', '').strip()
                if not name:
                    name = f"Agent {agent.get('id', '')}"
                
                name_parts = name.split(' ', 1)
                first_name = name_parts[0] if name_parts else name
                last_name = name_parts[1] if len(name_parts) > 1 else ''
                
                queues = agent.get('queues', [])
                queues_str = ', '.join(queues)
                
                description = f"Tikal Call Center Agent (ACTIVE)\n"
                description += f"Agent ID: {agent.get('id', '')}\n"
                description += f"Extension: {agent.get('extension', '')}\n"
                description += f"Status: {agent.get('status', '')}\n"
                description += f"Queues: {queues_str}\n"
                description += f"Queue Count: {len(queues)}\n"
                description += f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                row = {
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Email': '',
                    'Phone': agent.get('extension', ''),
                    'Mobile': '',
                    'Title': 'Call Center Agent',
                    'Department': 'Call Center',
                    'Lead Source': 'Tikal Call Center',
                    'Description': description,
                    'Agent ID': agent.get('id', ''),
                    'Extension': agent.get('extension', ''),
                    'Status': agent.get('status', ''),
                    'Queues': queues_str,
                    'Queue Count': str(len(queues)),
                    'Is Active': 'Yes',
                }
                writer.writerow(row)
        
        print(f"\n✓ Экспортировано {len(agents)} АКТИВНЫХ агентов в {output_file}")
        return output_file
    
    except Exception as e:
        print(f"✗ Ошибка экспорта: {e}")
        return None


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
        
        # Получаем только активных агентов
        active_agents = get_active_agents(client)
        
        if active_agents:
            # Экспортируем
            output_file = export_active_agents_to_zoho(active_agents)
            
            if output_file:
                print("\n" + "=" * 70)
                print("✅ Экспорт завершен успешно!")
                print("=" * 70)
                print(f"\n📁 Файл: {output_file}")
                print(f"👥 Активных агентов: {len(active_agents)}")
                print(f"\n💡 Рекомендация: Импортируйте ТОЛЬКО этот файл в Zoho CRM")
                print(f"   Это исключит неактивных агентов и неактивные очереди")
        else:
            print("\n⚠️ Активных агентов не найдено")
        
        client.close()
    
    except Exception as e:
        print(f"\n✗ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

