"""
Получение данных агентов из Tikal API для экспорта в Zoho CRM
"""

import csv
from datetime import datetime
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG


def get_all_agents_from_system(client: TikalClientV2) -> list:
    """
    Получает всех агентов из системы через различные методы
    
    Args:
        client: Экземпляр TikalClientV2
    
    Returns:
        Список словарей с данными агентов
    """
    all_agents = {}
    
    print("Получение данных агентов из системы...")
    
    # Метод 1: Из очередей
    print("\n1. Получение из очередей...")
    # Расширенный список очередей из интерфейса (видимых на скриншоте)
    queue_ids = [
        # Очереди из интерфейса
        '1005', '1007', '1011', '1012', '1014', '1015', '1016', '1018', 
        '1020', '1021', '1066', '1135', '1146', '1155', '1163', '1164',
        # Дополнительные очереди
        '3000', '1067', '1068', '1136', '1137', '1138', '1139', '1140',
        '1141', '1142', '1143', '1144', '1145', '1147', '1148', '1149',
        '1150', '1151', '1152', '1153', '1154', '1156', '1157', '1158',
        '1159', '1160', '1161', '1162', '1165', '1166', '1167', '1168',
        '1169', '1170', '1171', '1172', '1173', '1174', '1175'
    ]
    
    print(f"  Проверка {len(queue_ids)} очередей...")
    
    found_queues = []
    for queue_id in queue_ids:
        try:
            result = client.queues.get_agents(queue_id)
            status_code = result.get('data', {}).get('status', {}).get('code')
            
            if status_code == '200':
                agents_str = result.get('data', {}).get('info', {}).get('assigned_agents', '')
                agent_ids = [a.strip() for a in agents_str.split(',') if a.strip()] if agents_str else []
                print(f"  ✓ Очередь {queue_id}: {len(agent_ids)} агентов")
                found_queues.append(queue_id)
                
                for agent_id in agent_ids:
                    if agent_id not in all_agents:
                        all_agents[agent_id] = {
                            'id': agent_id,
                            'queues': [queue_id],
                            'name': '',
                            'extension': '',
                            'status': ''
                        }
                    else:
                        if queue_id not in all_agents[agent_id]['queues']:
                            all_agents[agent_id]['queues'].append(queue_id)
        except Exception as e:
            pass
    
    print(f"\n  Найдено {len(found_queues)} активных очередей: {', '.join(found_queues)}")
    
    # Метод 2: Из звонков
    print("\n2. Получение из звонков...")
    try:
        outgoing = client.calls.get_outgoing()
        if outgoing.get('data', {}).get('status', {}).get('code') == '200':
            calls = outgoing.get('data', {}).get('info', {}).get('calls', [])
            agent_ids_from_calls = set()
            for call in calls:
                agent_id = call.get('agent_id')
                if agent_id:
                    agent_ids_from_calls.add(agent_id)
            
            print(f"  Найдено {len(agent_ids_from_calls)} уникальных агентов в звонках")
            
            for agent_id in agent_ids_from_calls:
                if agent_id not in all_agents:
                    all_agents[agent_id] = {
                        'id': agent_id,
                        'queues': [],
                        'name': '',
                        'extension': '',
                        'status': ''
                    }
    except Exception as e:
        print(f"  Ошибка: {e}")
    
    # Получаем детальную информацию об агентах
    print("\n3. Получение детальной информации об агентах...")
    agents_list = list(all_agents.values())
    
    for i, agent in enumerate(agents_list, 1):
        agent_id = agent['id']
        try:
            state_result = client.agents.get_state(agent_id)
            if state_result.get('data', {}).get('status', {}).get('code') == '200':
                info = state_result.get('data', {}).get('info', {})
                agent['name'] = info.get('name', '')
                agent['extension'] = info.get('extension', '')
                agent['status'] = info.get('status', '')
                print(f"  {i}/{len(agents_list)}: {agent_id} - {agent.get('name', 'N/A')}")
            else:
                print(f"  {i}/{len(agents_list)}: {agent_id} - не удалось получить данные")
        except Exception as e:
            print(f"  {i}/{len(agents_list)}: {agent_id} - ошибка: {e}")
    
    return agents_list


def export_to_zoho_format(agents: list, output_file: str = None) -> str:
    """
    Экспортирует агентов в формат Zoho CRM
    
    Args:
        agents: Список словарей с данными агентов
        output_file: Путь к выходному файлу
    
    Returns:
        Путь к созданному файлу
    """
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'zoho_agents_import_{timestamp}.csv'
    
    # Стандартные поля Zoho CRM
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
                
                queues_str = ', '.join(agent.get('queues', []))
                
                description = f"Tikal Call Center Agent\n"
                description += f"Agent ID: {agent.get('id', '')}\n"
                description += f"Extension: {agent.get('extension', '')}\n"
                description += f"Status: {agent.get('status', '')}\n"
                if queues_str:
                    description += f"Queues: {queues_str}"
                
                row = {
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Email': '',  # Заполните если есть
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
                }
                writer.writerow(row)
        
        print(f"\n✓ Экспортировано {len(agents)} агентов в {output_file}")
        return output_file
    
    except Exception as e:
        print(f"Ошибка при экспорте: {e}")
        return None


def main():
    """Основная функция"""
    import sys
    import io
    
    # Устанавливаем UTF-8 для вывода
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 70)
    print("Get Agents from Tikal for Zoho CRM Import")
    print("=" * 70)
    
    try:
        client = TikalClientV2(
            base_url=TIKAL_CONFIG['base_url'],
            api_key=TIKAL_CONFIG['api_key'],
            format=TIKAL_CONFIG.get('format', 'json')
        )
        
        # Получаем всех агентов
        agents = get_all_agents_from_system(client)
        
        if agents:
            print(f"\n✓ Найдено {len(agents)} агентов")
            
            # Экспортируем в Zoho формат
            output_file = export_to_zoho_format(agents)
            
            if output_file:
                print("\n" + "=" * 70)
                print("Export completed successfully!")
                print("=" * 70)
                print(f"\nFile: {output_file}")
                print("\nNext steps:")
                print("1. Open Zoho CRM")
                print("2. Go to Contacts > Import")
                print("3. Upload the CSV file")
                print("4. Map fields and import")
        else:
            print("\n⚠ No agents found")
            print("Try checking queue IDs or agent IDs in the system")
        
        client.close()
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

