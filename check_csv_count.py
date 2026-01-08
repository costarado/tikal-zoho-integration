"""Проверка количества записей в CSV файле"""
import csv
import sys
import io

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

file_path = 'zoho_import_FIXED_20260108_131553.csv'

try:
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"Всего записей (без заголовка): {len(rows)}")
        print(f"Первая запись: {rows[0] if rows else 'Нет данных'}")
        print(f"Последняя запись: {rows[-1] if rows else 'Нет данных'}")
except Exception as e:
    print(f"Ошибка: {e}")
