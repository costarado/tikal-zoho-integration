"""
Подготовка CSV файла для импорта в Zoho CRM
Исправляет форматирование и проверяет структуру данных
"""

import csv
import sys
import io
from datetime import datetime


def prepare_zoho_csv(input_file: str, output_file: str = None) -> str:
    """
    Подготавливает CSV файл для импорта в Zoho CRM
    
    Args:
        input_file: Путь к исходному CSV файлу
        output_file: Путь к выходному файлу (если не указан, создаст автоматически)
    
    Returns:
        Путь к подготовленному файлу
    """
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'zoho_import_READY_{timestamp}.csv'
    
    # Поля для Zoho CRM (стандартные + кастомные)
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
        'Agent ID',      # Кастомное поле
        'Extension',     # Кастомное поле
        'Status',        # Кастомное поле
        'Queues',        # Кастомное поле
        'Queue Count',   # Кастомное поле
        'Is Active',     # Кастомное поле
    ]
    
    try:
        # Читаем исходный файл
        with open(input_file, 'r', encoding='utf-8-sig') as infile:
            reader = csv.DictReader(infile)
            
            # Собираем все строки
            rows = []
            for row in reader:
                # Очищаем и нормализуем данные
                cleaned_row = {}
                for field in zoho_fields:
                    value = row.get(field, '').strip()
                    
                    # Исправляем многострочный Description - заменяем переносы строк на пробелы
                    if field == 'Description':
                        value = value.replace('\n', ' | ').replace('\r', '')
                    
                    # Убеждаемся, что числовые поля не содержат лишних символов
                    if field in ['Agent ID', 'Extension', 'Queue Count']:
                        value = ''.join(c for c in value if c.isdigit() or c == '-')
                    
                    # Нормализуем Is Active
                    if field == 'Is Active':
                        if value.lower() in ['yes', 'true', '1', 'да']:
                            value = 'Yes'
                        else:
                            value = 'No'
                    
                    cleaned_row[field] = value
                
                rows.append(cleaned_row)
        
        # Записываем подготовленный файл
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=zoho_fields)
            writer.writeheader()
            writer.writerows(rows)
        
        print("=" * 70)
        print("✅ Файл подготовлен для импорта в Zoho CRM")
        print("=" * 70)
        print(f"\n📁 Исходный файл: {input_file}")
        print(f"📁 Подготовленный файл: {output_file}")
        print(f"👥 Записей: {len(rows)}")
        print(f"\n📋 Поля в файле:")
        for i, field in enumerate(zoho_fields, 1):
            marker = "🔹" if field in ['Agent ID', 'Extension', 'Status', 'Queues', 'Queue Count', 'Is Active'] else "✓"
            print(f"   {marker} {i}. {field}")
        
        print(f"\n⚠️  ВАЖНО: Кастомные поля (🔹) нужно создать в Zoho перед импортом!")
        print(f"   См. инструкцию: ZOHO_CUSTOM_FIELDS_INSTRUCTIONS.md")
        
        return output_file
    
    except FileNotFoundError:
        print(f"✗ Ошибка: Файл {input_file} не найден")
        return None
    except Exception as e:
        print(f"✗ Ошибка при подготовке файла: {e}")
        import traceback
        traceback.print_exc()
        return None


def validate_csv_structure(file_path: str) -> bool:
    """
    Проверяет структуру CSV файла
    """
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            required_fields = ['First Name', 'Agent ID']
            
            # Проверяем заголовки
            headers = reader.fieldnames
            if not headers:
                print("✗ Ошибка: Файл не содержит заголовков")
                return False
            
            missing_fields = [f for f in required_fields if f not in headers]
            if missing_fields:
                print(f"✗ Ошибка: Отсутствуют обязательные поля: {', '.join(missing_fields)}")
                return False
            
            # Подсчитываем записи
            row_count = sum(1 for _ in reader)
            print(f"✓ Файл валиден: {row_count} записей, {len(headers)} полей")
            return True
    
    except Exception as e:
        print(f"✗ Ошибка валидации: {e}")
        return False


def main():
    """Основная функция"""
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Файл для подготовки
    input_file = 'zoho_agents_ACTIVE_20260105_140957.csv'
    
    print("=" * 70)
    print("Подготовка файла для импорта в Zoho CRM")
    print("=" * 70)
    print(f"\n📂 Обработка файла: {input_file}\n")
    
    # Валидация
    if not validate_csv_structure(input_file):
        print("\n✗ Файл не прошел валидацию. Проверьте структуру.")
        return
    
    # Подготовка
    output_file = prepare_zoho_csv(input_file)
    
    if output_file:
        print("\n" + "=" * 70)
        print("✅ Готово! Файл готов к импорту в Zoho CRM")
        print("=" * 70)
        print(f"\n📌 Следующие шаги:")
        print(f"   1. Создайте кастомные поля в Zoho (см. ZOHO_CUSTOM_FIELDS_INSTRUCTIONS.md)")
        print(f"   2. Импортируйте файл: {output_file}")
        print(f"   3. Сопоставьте поля при импорте")
    else:
        print("\n✗ Не удалось подготовить файл")


if __name__ == '__main__':
    main()
