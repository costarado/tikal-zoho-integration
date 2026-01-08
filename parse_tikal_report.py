"""
Парсер для CSV отчетов Tikal Call Center
Формат: agents_report_1_05_01_2026_13_06_25.csv
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Optional


def parse_tikal_agents_report(file_path: str) -> List[Dict]:
    """
    Парсит CSV отчет об агентах из Tikal
    
    Args:
        file_path: Путь к CSV файлу
    
    Returns:
        Список словарей с данными агентов
    """
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return []
    
    agents = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Очищаем данные от лишних пробелов и BOM
                cleaned_row = {}
                for k, v in row.items():
                    # Убираем BOM (Byte Order Mark) если есть
                    key = k.strip() if k else ''
                    if key.startswith('\ufeff'):
                        key = key[1:]  # Убираем BOM
                    key = key.strip()
                    value = v.strip() if v else ''
                    cleaned_row[key] = value
                agents.append(cleaned_row)
        
        print(f"Loaded {len(agents)} records from {file_path}")
        return agents
    
    except Exception as e:
        print(f"Ошибка при парсинге CSV: {e}")
        return []


def parse_duration(duration_str: str) -> int:
    """
    Парсит строку времени в секунды
    
    Args:
        duration_str: Строка времени в формате HH:MM:SS или MM:SS
    
    Returns:
        Количество секунд
    """
    if not duration_str:
        return 0
    
    try:
        parts = duration_str.split(':')
        if len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:  # MM:SS
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        else:
            return 0
    except:
        return 0


def format_duration(seconds: int) -> str:
    """
    Форматирует секунды в строку HH:MM:SS
    
    Args:
        seconds: Количество секунд
    
    Returns:
        Строка в формате HH:MM:SS
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def analyze_tikal_report(agents: List[Dict]):
    """
    Анализирует отчет Tikal
    
    Args:
        agents: Список словарей с данными агентов
    """
    if not agents:
        print("No data to analyze")
        return
    
    print("\n" + "=" * 70)
    print("Tikal Call Center Report Analysis")
    print("=" * 70)
    
    # Обрабатываем каждую запись
    for i, agent in enumerate(agents, 1):
        agent_name = agent.get('Agent Name', 'N/A')
        total_calls = agent.get('Total Calls', '0')
        answered = agent.get('Answered', '0')
        unanswered = agent.get('Unanswered', '0')
        total_duration = agent.get('Total Duration', '00:00:00')
        avg_duration = agent.get('Average Call Duration', '00:00:00')
        calls_per_hour = agent.get('Calls per Hour', '0')
        login_duration = agent.get('LogIn Duration', '00:00:00')
        
        # Очищаем имя агента
        agent_name_clean = agent_name.strip() if agent_name else 'Total'
        
        print(f"\n{i}. {agent_name_clean}")
        print("-" * 70)
        print(f"  Total Calls: {total_calls}")
        print(f"  Answered: {answered}")
        print(f"  Unanswered: {unanswered}")
        
        # Парсим время
        total_sec = parse_duration(total_duration)
        avg_sec = parse_duration(avg_duration)
        login_sec = parse_duration(login_duration)
        
        print(f"  Total Duration: {total_duration} ({total_sec} seconds)")
        print(f"  Average Call Duration: {avg_duration} ({avg_sec} seconds)")
        print(f"  Calls per Hour: {calls_per_hour}")
        print(f"  Login Duration: {login_duration} ({login_sec // 3600} hours)")
        
        # Статистика
        if total_calls and total_calls != '0':
            try:
                total = int(total_calls)
                ans = int(answered)
                unans = int(unanswered)
                
                if total > 0:
                    answer_rate = (ans / total) * 100
                    print(f"  Answer Rate: {answer_rate:.1f}%")
                    
                    if ans > 0:
                        avg_per_answered = total_sec / ans if total_sec > 0 else 0
                        print(f"  Average Answered Call Duration: {format_duration(int(avg_per_answered))}")
                    
                    # Дополнительная статистика
                    if unans > 0:
                        unanswered_wait = parse_duration(agent.get('Unanswered Wait Time', '00:00:00'))
                        avg_wait = unanswered_wait / unans if unanswered_wait > 0 else 0
                        print(f"  Average Unanswered Wait Time: {format_duration(int(avg_wait))}")
            except:
                pass


def export_to_json(agents: List[Dict], output_file: str):
    """
    Экспортирует данные в JSON
    
    Args:
        agents: Список словарей с данными агентов
        output_file: Путь к выходному файлу
    """
    import json
    
    # Обрабатываем данные для JSON
    processed_data = []
    for agent in agents:
        processed_agent = {
            'agent_name': agent.get('Agent Name', '').strip(),
            'total_calls': int(agent.get('Total Calls', 0)) if agent.get('Total Calls', '0').isdigit() else 0,
            'answered': int(agent.get('Answered', 0)) if agent.get('Answered', '0').isdigit() else 0,
            'unanswered': int(agent.get('Unanswered', 0)) if agent.get('Unanswered', '0').isdigit() else 0,
            'total_duration': agent.get('Total Duration', '00:00:00'),
            'total_duration_seconds': parse_duration(agent.get('Total Duration', '00:00:00')),
            'average_call_duration': agent.get('Average Call Duration', '00:00:00'),
            'average_call_duration_seconds': parse_duration(agent.get('Average Call Duration', '00:00:00')),
            'unanswered_wait_time': agent.get('Unanswered Wait Time', '00:00:00'),
            'average': agent.get('Average', '00:00:00'),
            'calls_per_hour': float(agent.get('Calls per Hour', 0)) if agent.get('Calls per Hour', '0').replace('.', '').isdigit() else 0,
            'login_duration': agent.get('LogIn Duration', '00:00:00'),
            'login_duration_seconds': parse_duration(agent.get('LogIn Duration', '00:00:00')),
        }
        
        # Добавляем вычисляемые поля
        if processed_agent['total_calls'] > 0:
            processed_agent['answer_rate'] = (processed_agent['answered'] / processed_agent['total_calls']) * 100
        else:
            processed_agent['answer_rate'] = 0
        
        processed_data.append(processed_agent)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nExported to JSON: {output_file}")
        return output_file
    except Exception as e:
        print(f"Ошибка при экспорте в JSON: {e}")
        return None


def export_to_formatted_csv(agents: List[Dict], output_file: str):
    """
    Экспортирует данные в отформатированный CSV с дополнительными полями
    
    Args:
        agents: Список словарей с данными агентов
        output_file: Путь к выходному файлу
    """
    if not agents:
        print("No data to export")
        return
    
    fieldnames = [
        'Agent Name', 'Total Calls', 'Answered', 'Unanswered',
        'Answer Rate %', 'Total Duration', 'Total Duration (seconds)',
        'Average Call Duration', 'Average Call Duration (seconds)',
        'Calls per Hour', 'LogIn Duration', 'LogIn Duration (hours)'
    ]
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for agent in agents:
                total_calls = int(agent.get('Total Calls', 0)) if agent.get('Total Calls', '0').isdigit() else 0
                answered = int(agent.get('Answered', 0)) if agent.get('Answered', '0').isdigit() else 0
                
                answer_rate = (answered / total_calls * 100) if total_calls > 0 else 0
                total_duration = agent.get('Total Duration', '00:00:00')
                login_duration = agent.get('LogIn Duration', '00:00:00')
                
                row = {
                    'Agent Name': agent.get('Agent Name', ''),
                    'Total Calls': total_calls,
                    'Answered': answered,
                    'Unanswered': agent.get('Unanswered', '0'),
                    'Answer Rate %': f"{answer_rate:.1f}",
                    'Total Duration': total_duration,
                    'Total Duration (seconds)': parse_duration(total_duration),
                    'Average Call Duration': agent.get('Average Call Duration', '00:00:00'),
                    'Average Call Duration (seconds)': parse_duration(agent.get('Average Call Duration', '00:00:00')),
                    'Calls per Hour': agent.get('Calls per Hour', '0'),
                    'LogIn Duration': login_duration,
                    'LogIn Duration (hours)': parse_duration(login_duration) // 3600,
                }
                writer.writerow(row)
        
        print(f"Exported to CSV: {output_file}")
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
    print("Tikal Call Center Report Parser")
    print("=" * 70)
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Пробуем найти файл на рабочем столе
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        default_file = os.path.join(desktop_path, 'agents_report_1_05_01_2026_13_06_25.csv')
        
        if os.path.exists(default_file):
            file_path = default_file
            print(f"\nИспользуется файл: {file_path}")
        else:
            print("\nИспользование: python parse_tikal_report.py <путь_к_файлу.csv>")
            print(f"Или поместите файл на рабочий стол: {default_file}")
            return
    
    # Парсим файл
    agents = parse_tikal_agents_report(file_path)
    
    if agents:
        # Анализируем
        analyze_tikal_report(agents)
        
        # Экспортируем в разные форматы
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        json_file = f"{base_name}_processed.json"
        csv_file = f"{base_name}_processed.csv"
        
        export_to_json(agents, json_file)
        export_to_formatted_csv(agents, csv_file)
        
        print("\n" + "=" * 70)
        print("Processing completed")
        print("=" * 70)
        print(f"Source file: {file_path}")
        print(f"JSON: {json_file}")
        print(f"CSV: {csv_file}")


if __name__ == '__main__':
    main()

