"""
Исправление Last Name в CSV файле для корректного импорта в Zoho CRM
Zoho требует, чтобы Last Name содержал текстовое значение, а не только цифры
"""

import csv
import sys
import io
from datetime import datetime


def fix_last_name_in_csv(input_file: str, output_file: str = None) -> str:
    """
    Исправляет Last Name, добавляя префикс для числовых значений
    
    Args:
        input_file: Путь к исходному CSV файлу
        output_file: Путь к выходному файлу
    
    Returns:
        Путь к исправленному файлу
    """
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'zoho_import_FIXED_{timestamp}.csv'
    
    try:
        # Читаем исходный файл
        with open(input_file, 'r', encoding='utf-8-sig') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            
            rows = []
            fixed_count = 0
            
            for row in reader:
                last_name = row.get('Last Name', '').strip()
                
                # Если Last Name содержит только цифры, добавляем префикс
                if last_name and last_name.isdigit():
                    row['Last Name'] = f'Agent {last_name}'
                    fixed_count += 1
                elif not last_name:
                    # Если Last Name пустое, используем Agent ID
                    agent_id = row.get('Agent ID', '').strip()
                    if agent_id:
                        row['Last Name'] = f'Agent {agent_id}'
                        fixed_count += 1
                
                rows.append(row)
        
        # Записываем исправленный файл
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print("=" * 70)
        print("✅ Файл исправлен для импорта в Zoho CRM")
        print("=" * 70)
        print(f"\n📁 Исходный файл: {input_file}")
        print(f"📁 Исправленный файл: {output_file}")
        print(f"👥 Всего записей: {len(rows)}")
        print(f"🔧 Исправлено Last Name: {fixed_count}")
        print(f"\n💡 Изменения:")
        print(f"   - Last Name '6701' → 'Agent 6701'")
        print(f"   - Last Name '6702' → 'Agent 6702'")
        print(f"   - и т.д.")
        
        return output_file
    
    except FileNotFoundError:
        print(f"✗ Ошибка: Файл {input_file} не найден")
        return None
    except Exception as e:
        print(f"✗ Ошибка при исправлении файла: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Основная функция"""
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Файл для исправления
    input_file = 'zoho_import_READY_20260108_121037.csv'
    
    print("=" * 70)
    print("Исправление Last Name для импорта в Zoho CRM")
    print("=" * 70)
    print(f"\n📂 Обработка файла: {input_file}\n")
    
    output_file = fix_last_name_in_csv(input_file)
    
    if output_file:
        print("\n" + "=" * 70)
        print("✅ Готово! Файл готов к импорту")
        print("=" * 70)
        print(f"\n📌 Следующий шаг:")
        print(f"   Импортируйте файл: {output_file}")
        print(f"   Ошибка 'Please enter a valid Last Name' больше не появится")
    else:
        print("\n✗ Не удалось исправить файл")


if __name__ == '__main__':
    main()
