"""
Попытка извлечь информацию об API из PDF документации
"""

import os
import re

def extract_api_info_from_pdf():
    """Пытается извлечь информацию об API из PDF"""
    import sys
    import io
    
    # Устанавливаем UTF-8 для вывода
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    pdf_path = "API Documentation Guide for Tikal's Call Center (V1).pdf"
    
    if not os.path.exists(pdf_path):
        print(f"File {pdf_path} not found")
        return
    
    print("=" * 70)
    print("Extracting API information from PDF documentation")
    print("=" * 70)
    print(f"\nFile: {pdf_path}\n")
    
    # Пробуем использовать различные библиотеки
    try:
        import PyPDF2
        print("Используется PyPDF2...")
        extract_with_pypdf2(pdf_path)
    except ImportError:
        try:
            import pypdf
            print("Используется pypdf...")
            extract_with_pypdf(pdf_path)
        except ImportError:
            print("⚠ Библиотеки для работы с PDF не установлены")
            print("\nУстановите одну из библиотек:")
            print("  pip install PyPDF2")
            print("  или")
            print("  pip install pypdf")
            print("\nАльтернатива: Откройте PDF вручную и найдите раздел с API endpoints")
            print("Обычно это разделы типа:")
            print("  - API Endpoints")
            print("  - REST API")
            print("  - API Reference")
            print("  - Authentication")
            return

def extract_with_pypdf2(pdf_path):
    """Извлекает текст используя PyPDF2"""
    import PyPDF2
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        print(f"Всего страниц: {total_pages}\n")
        
        # Ищем ключевые слова
        keywords = [
            'api', 'endpoint', 'url', 'http', 'rest', 'json',
            'agent', 'call', 'recording', 'statistic',
            'authentication', 'token', 'login'
        ]
        
        found_sections = []
        
        for page_num in range(min(50, total_pages)):  # Проверяем первые 50 страниц
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            # Ищем строки с URL или endpoints
            lines = text.split('\n')
            for line in lines:
                line_lower = line.lower()
                
                # Проверяем наличие ключевых слов
                has_keyword = any(kw in line_lower for kw in keywords)
                
                # Ищем URL паттерны
                url_patterns = [
                    r'http[s]?://[^\s]+',
                    r'/api/[^\s]+',
                    r'/cc3/[^\s]+',
                    r'api/[^\s]+',
                ]
                
                has_url = any(re.search(pattern, line, re.IGNORECASE) for pattern in url_patterns)
                
                if has_keyword or has_url:
                    # Проверяем, не дублируется ли
                    if line.strip() and line not in [s['text'] for s in found_sections]:
                        found_sections.append({
                            'page': page_num + 1,
                            'text': line.strip()
                        })
        
        # Выводим найденную информацию
        if found_sections:
            print("Найдена информация об API:\n")
            for section in found_sections[:30]:  # Показываем первые 30
                print(f"Страница {section['page']}: {section['text']}")
        else:
            print("⚠ Информация об API не найдена в первых 50 страницах")
            print("\nПопробуйте:")
            print("1. Открыть PDF вручную")
            print("2. Найти раздел 'API Documentation' или 'API Reference'")
            print("3. Скопировать endpoints из документации")

def extract_with_pypdf(pdf_path):
    """Извлекает текст используя pypdf"""
    import pypdf
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = pypdf.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        print(f"Всего страниц: {total_pages}\n")
        
        keywords = [
            'api', 'endpoint', 'url', 'http', 'rest', 'json',
            'agent', 'call', 'recording', 'statistic',
            'authentication', 'token', 'login'
        ]
        
        found_sections = []
        
        for page_num in range(min(50, total_pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            lines = text.split('\n')
            for line in lines:
                line_lower = line.lower()
                has_keyword = any(kw in line_lower for kw in keywords)
                
                url_patterns = [
                    r'http[s]?://[^\s]+',
                    r'/api/[^\s]+',
                    r'/cc3/[^\s]+',
                    r'api/[^\s]+',
                ]
                
                has_url = any(re.search(pattern, line, re.IGNORECASE) for pattern in url_patterns)
                
                if has_keyword or has_url:
                    if line.strip() and line not in [s['text'] for s in found_sections]:
                        found_sections.append({
                            'page': page_num + 1,
                            'text': line.strip()
                        })
        
        if found_sections:
            print("Найдена информация об API:\n")
            for section in found_sections[:30]:
                print(f"Страница {section['page']}: {section['text']}")
        else:
            print("⚠ Информация об API не найдена")
            print("\nОткройте PDF вручную и найдите раздел с API endpoints")


if __name__ == '__main__':
    extract_api_info_from_pdf()

