"""
Фильтрация активных агентов и улучшение данных для Zoho
"""

import csv
from datetime import datetime
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG


def get_active_agents_only(client: TikalClientV2, min_queues: int = 1) -> list:
    """
    Получает только активных агентов (с статусом online или в активных очередях)
    
    Args:
        client: Экземпляр TikalClientV2
        min_queues: Минимальное количество очередей для включения агента
    
    Returns:
        Список активных агентов
    """
    all_agents = {}
    
    print("Получение активных агентов...")
    
    # Получаем из всех очередей
    queue_ids = [
        '1005', '1007', '1011', '1012', '1014', '1015', '1016', '1018', 
        '1020', '1021', '1066', '1135', '1146', '1155', '1163', '1164',
        '1140', '1141', '1142', '1143', '1148', '1149', '1150', '1151',
        '1152', '1153', '1154', '1156', '1157', '1159', '1161', '1162', '1167'
    ]
    
    print(f"Проверка {len(queue_ids)} очередей...")
    
    for queue_id in queue_ids:
        try:
            result = client.queues.get_agents(queue_id)
            if result.get('data', {}).get('status', {}).get('code') == '200':
                agents_str = result.get('data', {}).get('info', {}).get('assigned_agents', '')
                if agents_str:
                    agent_ids = [a.strip() for a in agents_str.split(',') if a.strip()]
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
        except:
            pass
    
    # Фильтруем по количеству очередей
    filtered_agents = {
        agent_id: agent for agent_id, agent in all_agents.items()
        if len(agent['queues']) >= min_queues
    }
    
    print(f"Найдено {len(all_agents)} агентов, после фильтрации: {len(filtered_agents)}")
    
    # Получаем детальную информацию
    agents_list = list(filtered_agents.values())
    print(f"\nПолучение детальной информации о {len(agents_list)} агентах...")
    
    for i, agent in enumerate(agents_list, 1):
        agent_id = agent['id']
        try:
            state_result = client.agents.get_state(agent_id)
            if state_result.get('data', {}).get('status', {}).get('code') == '200':
                info = state_result.get('data', {}).get('info', {})
                agent['name'] = info.get('name', '')
                agent['extension'] = info.get('extension', '')
                agent['status'] = info.get('status', '')
        except:
            pass
        
        if i % 20 == 0:
            print(f"  Обработано {i}/{len(agents_list)}...")
    
    return agents_list


def export_to_zoho_with_stats(agents: list, output_file: str = None) -> str:
    """
    Экспортирует агентов в Zoho с дополнительной статистикой
    """
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'zoho_agents_active_{timestamp}.csv'
    
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
                
                description = f"Tikal Call Center Agent\n"
                description += f"Agent ID: {agent.get('id', '')}\n"
                description += f"Extension: {agent.get('extension', '')}\n"
                description += f"Status: {agent.get('status', '')}\n"
                description += f"Queues: {queues_str}\n"
                description += f"Queue Count: {len(queues)}"
                
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
                }
                writer.writerow(row)
        
        print(f"\n✓ Экспортировано {len(agents)} агентов в {output_file}")
        return output_file
    
    except Exception as e:
        print(f"Ошибка: {e}")
        return None


def main():
    """Основная функция"""
    import sys
    import io
    
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 70)
    print("Get Active Agents for Zoho CRM")
    print("=" * 70)
    
    try:
        client = TikalClientV2(
            base_url=TIKAL_CONFIG['base_url'],
            api_key=TIKAL_CONFIG['api_key'],
            format=TIKAL_CONFIG.get('format', 'json')
        )
        
        # Получаем активных агентов
        agents = get_active_agents_only(client, min_queues=1)
        
        if agents:
            print(f"\n✓ Найдено {len(agents)} активных агентов")
            
            # Статистика
            agents_with_names = [a for a in agents if a.get('name')]
            agents_with_status = [a for a in agents if a.get('status')]
            
            print(f"  С именами: {len(agents_with_names)}")
            print(f"  Со статусом: {len(agents_with_status)}")
            
            # Экспортируем
            output_file = export_to_zoho_with_stats(agents)
            
            if output_file:
                print("\n" + "=" * 70)
                print("Export completed!")
                print("=" * 70)
                print(f"\nFile: {output_file}")
                print(f"Total agents: {len(agents)}")
        
        client.close()
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

