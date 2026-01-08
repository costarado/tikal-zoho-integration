"""
Утилита для экспорта данных агентов Tikal в формат Zoho CRM
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG


def get_agents_from_api(client: TikalClientV2) -> List[Dict]:
    """
    Получает данные агентов через API
    
    Args:
        client: Экземпляр TikalClientV2
    
    Returns:
        Список словарей с данными агентов
    """
    agents = []
    
    try:
        # Получаем данные из очередей
        queue_ids = ['3000', '1066', '1135', '1067', '1068']  # Расширьте список по необходимости
        
        for queue_id in queue_ids:
            try:
                result = client.queues.get_agents(queue_id)
                if result.get('data', {}).get('status', {}).get('code') == '200':
                    agents_str = result.get('data', {}).get('info', {}).get('assigned_agents', '')
                    if agents_str:
                        agent_ids = [a.strip() for a in agents_str.split(',') if a.strip()]
                        for agent_id in agent_ids:
                            if agent_id not in [a.get('id') for a in agents]:
                                # Получаем детальную информацию об агенте
                                try:
                                    state_result = client.agents.get_state(agent_id)
                                    if state_result.get('data', {}).get('status', {}).get('code') == '200':
                                        info = state_result.get('data', {}).get('info', {})
                                        agents.append({
                                            'id': agent_id,
                                            'name': info.get('name', ''),
                                            'extension': info.get('extension', ''),
                                            'status': info.get('status', ''),
                                            'queue': queue_id
                                        })
                                except:
                                    # Если не удалось получить детали, добавляем базовую информацию
                                    agents.append({
                                        'id': agent_id,
                                        'name': '',
                                        'extension': '',
                                        'status': '',
                                        'queue': queue_id
                                    })
            except Exception as e:
                print(f"  Ошибка при получении агентов из очереди {queue_id}: {e}")
        
        # Также получаем из звонков
        try:
            outgoing = client.calls.get_outgoing()
            if outgoing.get('data', {}).get('status', {}).get('code') == '200':
                calls = outgoing.get('data', {}).get('info', {}).get('calls', [])
                for call in calls:
                    agent_id = call.get('agent_id')
                    if agent_id and agent_id not in [a.get('id') for a in agents]:
                        agents.append({
                            'id': agent_id,
                            'name': '',
                            'extension': '',
                            'status': '',
                            'queue': call.get('queue', '')
                        })
        except Exception as e:
            print(f"  Ошибка при получении из звонков: {e}")
    
    except Exception as e:
        print(f"Ошибка при получении агентов: {e}")
    
    return agents


def parse_agents_from_csv(csv_file: str) -> List[Dict]:
    """
    Парсит CSV файл с данными агентов
    
    Args:
        csv_file: Путь к CSV файлу
    
    Returns:
        Список словарей с данными агентов
    """
    agents = []
    
    if not os.path.exists(csv_file):
        print(f"Файл {csv_file} не найден")
        return agents
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Обрабатываем BOM если есть
                cleaned_row = {}
                for k, v in row.items():
                    key = k.strip()
                    if key.startswith('\ufeff'):
                        key = key[1:]
                    cleaned_row[key] = v.strip() if v else ''
                
                # Извлекаем данные агента
                agent_name = cleaned_row.get('Agent Name', '').strip()
                if agent_name and agent_name.lower() != 'total':
                    agents.append({
                        'name': agent_name,
                        'total_calls': cleaned_row.get('Total Calls', '0'),
                        'answered': cleaned_row.get('Answered', '0'),
                        'unanswered': cleaned_row.get('Unanswered', '0'),
                        'total_duration': cleaned_row.get('Total Duration', '00:00:00'),
                        'calls_per_hour': cleaned_row.get('Calls per Hour', '0'),
                        'login_duration': cleaned_row.get('LogIn Duration', '00:00:00'),
                    })
    except Exception as e:
        print(f"Ошибка при парсинге CSV: {e}")
    
    return agents


def export_to_zoho_format(agents: List[Dict], output_file: str = None) -> str:
    """
    Экспортирует данные агентов в формат Zoho CRM
    
    Args:
        agents: Список словарей с данными агентов
        output_file: Путь к выходному файлу
    
    Returns:
        Путь к созданному файлу
    """
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'zoho_import_agents_{timestamp}.csv'
    
    # Формат Zoho CRM для импорта контактов/лидов
    # Стандартные поля Zoho
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
        'Custom Field 1',  # Agent ID
        'Custom Field 2',  # Extension
        'Custom Field 3',  # Status
        'Custom Field 4',  # Total Calls
        'Custom Field 5',  # Answer Rate
        'Custom Field 6',  # Calls per Hour
    ]
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:  # utf-8-sig для Excel
            writer = csv.DictWriter(csvfile, fieldnames=zoho_fields)
            writer.writeheader()
            
            for agent in agents:
                # Разделяем имя на First Name и Last Name
                name = agent.get('name', '').strip()
                name_parts = name.split(' ', 1)
                first_name = name_parts[0] if name_parts else ''
                last_name = name_parts[1] if len(name_parts) > 1 else ''
                
                # Вычисляем процент ответов
                total_calls = int(agent.get('total_calls', 0)) if str(agent.get('total_calls', '0')).isdigit() else 0
                answered = int(agent.get('answered', 0)) if str(agent.get('answered', '0')).isdigit() else 0
                answer_rate = (answered / total_calls * 100) if total_calls > 0 else 0
                
                # Формируем описание
                description = f"Tikal Call Center Agent\n"
                description += f"Total Calls: {total_calls}\n"
                description += f"Answered: {answered}\n"
                description += f"Answer Rate: {answer_rate:.1f}%\n"
                description += f"Calls per Hour: {agent.get('calls_per_hour', '0')}\n"
                description += f"Login Duration: {agent.get('login_duration', '00:00:00')}"
                
                row = {
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Email': '',  # Заполните если есть
                    'Phone': agent.get('extension', ''),  # Extension как телефон
                    'Mobile': '',
                    'Title': 'Call Center Agent',
                    'Department': 'Call Center',
                    'Lead Source': 'Tikal Call Center',
                    'Description': description,
                    'Custom Field 1': agent.get('id', ''),  # Agent ID
                    'Custom Field 2': agent.get('extension', ''),  # Extension
                    'Custom Field 3': agent.get('status', ''),  # Status
                    'Custom Field 4': str(total_calls),  # Total Calls
                    'Custom Field 5': f"{answer_rate:.1f}%",  # Answer Rate
                    'Custom Field 6': agent.get('calls_per_hour', '0'),  # Calls per Hour
                }
                writer.writerow(row)
        
        print(f"Exported {len(agents)} agents to {output_file}")
        print(f"  File ready for Zoho CRM import")
        return output_file
    
    except Exception as e:
        print(f"Ошибка при экспорте: {e}")
        return None


def export_to_zoho_simple_format(agents: List[Dict], output_file: str = None) -> str:
    """
    Экспортирует в упрощенный формат Zoho (только основные поля)
    
    Args:
        agents: Список словарей с данными агентов
        output_file: Путь к выходному файлу
    
    Returns:
        Путь к созданному файлу
    """
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'zoho_import_simple_{timestamp}.csv'
    
    # Упрощенный формат - только основные поля
    simple_fields = [
        'First Name',
        'Last Name',
        'Phone',
        'Title',
        'Department',
        'Lead Source',
        'Agent ID',
        'Extension',
        'Total Calls',
        'Answer Rate %',
    ]
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=simple_fields)
            writer.writeheader()
            
            for agent in agents:
                name = agent.get('name', '').strip()
                name_parts = name.split(' ', 1)
                first_name = name_parts[0] if name_parts else ''
                last_name = name_parts[1] if len(name_parts) > 1 else ''
                
                total_calls = int(agent.get('total_calls', 0)) if str(agent.get('total_calls', '0')).isdigit() else 0
                answered = int(agent.get('answered', 0)) if str(agent.get('answered', '0')).isdigit() else 0
                answer_rate = (answered / total_calls * 100) if total_calls > 0 else 0
                
                row = {
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Phone': agent.get('extension', ''),
                    'Title': 'Call Center Agent',
                    'Department': 'Call Center',
                    'Lead Source': 'Tikal Call Center',
                    'Agent ID': agent.get('id', ''),
                    'Extension': agent.get('extension', ''),
                    'Total Calls': str(total_calls),
                    'Answer Rate %': f"{answer_rate:.1f}",
                }
                writer.writerow(row)
        
        print(f"Exported {len(agents)} agents in simple format: {output_file}")
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
    print("Export Tikal Agents Data to Zoho CRM Format")
    print("=" * 70)
    
    # Варианты получения данных
    agents = []
    
    # Вариант 1: Из CSV файлов
    if len(sys.argv) > 1:
        csv_files = sys.argv[1:]
        print(f"\nОбработка {len(csv_files)} CSV файлов...")
        for csv_file in csv_files:
            print(f"  Парсинг: {csv_file}")
            csv_agents = parse_agents_from_csv(csv_file)
            agents.extend(csv_agents)
    else:
        # Вариант 2: Через API
        print("\nПолучение данных через API...")
        try:
            client = TikalClientV2(
                base_url=TIKAL_CONFIG['base_url'],
                api_key=TIKAL_CONFIG['api_key'],
                format=TIKAL_CONFIG.get('format', 'json')
            )
            api_agents = get_agents_from_api(client)
            agents.extend(api_agents)
            client.close()
        except Exception as e:
            print(f"Ошибка при получении через API: {e}")
        
        # Вариант 3: Поиск CSV на рабочем столе
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        csv_files = [f for f in os.listdir(desktop_path) if f.endswith('.csv') and 'agent' in f.lower()]
        if csv_files:
            print(f"\nНайдены CSV файлы на рабочем столе:")
            for f in csv_files:
                print(f"  - {f}")
                csv_agents = parse_agents_from_csv(os.path.join(desktop_path, f))
                agents.extend(csv_agents)
    
    if not agents:
        print("\n⚠ Не найдено данных об агентах")
        print("\nИспользование:")
        print("  python export_to_zoho.py <файл1.csv> <файл2.csv> ...")
        print("  или")
        print("  python export_to_zoho.py  (автоматический поиск)")
        return
    
    # Удаляем дубликаты по имени
    unique_agents = {}
    for agent in agents:
        key = agent.get('name', '') or agent.get('id', '')
        if key and key not in unique_agents:
            unique_agents[key] = agent
    
    agents = list(unique_agents.values())
    print(f"\n✓ Найдено {len(agents)} уникальных агентов")
    
    # Экспортируем в форматы Zoho
    print("\n" + "=" * 70)
    print("Exporting to Zoho formats")
    print("=" * 70)
    
    # Полный формат
    full_file = export_to_zoho_format(agents)
    
    # Упрощенный формат
    simple_file = export_to_zoho_simple_format(agents)
    
    print("\n" + "=" * 70)
    print("Export completed")
    print("=" * 70)
    print(f"\nCreated files:")
    if full_file:
        print(f"  Full format: {full_file}")
    if simple_file:
        print(f"  Simple format: {simple_file}")
    
    print("\nZoho CRM Import Instructions:")
    print("1. Login to Zoho CRM")
    print("2. Go to Contacts or Leads section")
    print("3. Click Import")
    print("4. Upload the created CSV file")
    print("5. Map fields (Zoho will auto-detect most)")
    print("6. Complete import")


if __name__ == '__main__':
    main()

