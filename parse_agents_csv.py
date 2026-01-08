"""
Утилита для парсинга и анализа CSV отчетов об агентах
"""

import csv
import os
from typing import List, Dict, Optional


def parse_agents_csv(file_path: str) -> List[Dict]:
    """
    Парсит CSV файл с данными об агентах
    
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
            # Автоматическое определение разделителя
            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            
            for row in reader:
                agents.append(dict(row))
        
        print(f"✓ Загружено {len(agents)} агентов из {file_path}")
        return agents
    
    except Exception as e:
        print(f"Ошибка при парсинге CSV: {e}")
        return []


def analyze_agents(agents: List[Dict]):
    """
    Анализирует данные агентов
    
    Args:
        agents: Список словарей с данными агентов
    """
    if not agents:
        print("Нет данных для анализа")
        return
    
    print("\n" + "=" * 70)
    print("Анализ данных агентов")
    print("=" * 70)
    
    # Статистика
    print(f"\nВсего агентов: {len(agents)}")
    
    # Уникальные ID
    unique_ids = set(a.get('id', '') for a in agents if a.get('id'))
    print(f"Уникальных ID: {len(unique_ids)}")
    
    # Группировка по очередям
    queues = {}
    for agent in agents:
        queue = agent.get('queue', 'N/A')
        if queue not in queues:
            queues[queue] = []
        queues[queue].append(agent.get('id', 'N/A'))
    
    print(f"\nРаспределение по очередям:")
    for queue, agent_ids in queues.items():
        print(f"  Очередь {queue}: {len(agent_ids)} агентов")
        if len(agent_ids) <= 10:
            print(f"    Агенты: {', '.join(agent_ids)}")
    
    # Статусы (если есть)
    statuses = {}
    for agent in agents:
        status = agent.get('status', 'N/A')
        if status not in statuses:
            statuses[status] = 0
        statuses[status] += 1
    
    if len(statuses) > 1:
        print(f"\nРаспределение по статусам:")
        for status, count in statuses.items():
            print(f"  {status}: {count}")


def export_to_formatted_csv(agents: List[Dict], output_file: str):
    """
    Экспортирует данные в отформатированный CSV
    
    Args:
        agents: Список словарей с данными агентов
        output_file: Путь к выходному файлу
    """
    if not agents:
        print("Нет данных для экспорта")
        return
    
    # Определяем все возможные поля
    all_fields = set()
    for agent in agents:
        all_fields.update(agent.keys())
    
    fieldnames = sorted(all_fields)
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for agent in agents:
                # Заполняем отсутствующие поля пустыми значениями
                row = {field: agent.get(field, '') for field in fieldnames}
                writer.writerow(row)
        
        print(f"✓ Экспортировано {len(agents)} агентов в {output_file}")
    
    except Exception as e:
        print(f"Ошибка при экспорте: {e}")


def main():
    """Основная функция"""
    import sys
    
    print("=" * 70)
    print("Парсинг CSV отчетов об агентах")
    print("=" * 70)
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Ищем CSV файлы в текущей директории
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'agent' in f.lower()]
        
        if csv_files:
            print(f"\nНайдены CSV файлы:")
            for i, f in enumerate(csv_files, 1):
                print(f"  {i}. {f}")
            
            if len(csv_files) == 1:
                file_path = csv_files[0]
                print(f"\nИспользуется: {file_path}")
            else:
                choice = input(f"\nВыберите файл (1-{len(csv_files)}): ")
                try:
                    file_path = csv_files[int(choice) - 1]
                except:
                    print("Неверный выбор")
                    return
        else:
            print("\nНе найдено CSV файлов с агентами")
            print("Использование: python parse_agents_csv.py <путь_к_файлу.csv>")
            return
    
    # Парсим файл
    agents = parse_agents_csv(file_path)
    
    if agents:
        # Анализируем
        analyze_agents(agents)
        
        # Экспортируем в отформатированный вид
        output_file = f"formatted_{os.path.basename(file_path)}"
        export_to_formatted_csv(agents, output_file)


if __name__ == '__main__':
    main()

