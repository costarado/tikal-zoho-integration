"""
Поиск API endpoints через анализ веб-интерфейса
Проверяет различные места, где может быть информация об API
"""

import requests
from bs4 import BeautifulSoup
from config import TIKAL_CONFIG
import re

def find_api_in_interface():
    """Ищет информацию об API в веб-интерфейсе"""
    import sys
    import io
    
    # Устанавливаем UTF-8 для вывода
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    base_url = TIKAL_CONFIG['base_url'].rstrip('/')
    
    print("=" * 70)
    print("Searching for API in Tikal web interface")
    print("=" * 70)
    print(f"\nBase URL: {base_url}\n")
    
    # Страницы для проверки
    pages_to_check = [
        '/cc3/index.php?cat=board',
        '/cc3/index.php?cat=settings',
        '/cc3/index.php?cat=config',
        '/cc3/index.php?cat=admin',
        '/cc3/index.php?cat=modules',
        '/cc3/index.php?cat=api',
        '/cc3/index.php?cat=integration',
        '/cc3/index.php?action=api',
        '/cc3/index.php?action=settings',
        '/cc3/index.php?action=config',
        '/cc3/settings.php',
        '/cc3/config.php',
        '/cc3/admin.php',
    ]
    
    print("1. Проверка страниц настроек и конфигурации:\n")
    
    for page in pages_to_check:
        url = f"{base_url}{page}"
        try:
            response = requests.get(url, timeout=10, verify=False)
            if response.status_code == 200:
                # Ищем упоминания API в HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text().lower()
                
                # Ключевые слова для поиска
                api_keywords = ['api', 'rest', 'json', 'endpoint', 'integration', 'webhook']
                
                if any(keyword in text for keyword in api_keywords):
                    print(f"  ✓ {url}")
                    print(f"    Найдены упоминания API")
                    
                    # Ищем ссылки на API
                    links = soup.find_all('a', href=True)
                    api_links = [link for link in links if any(kw in link.get('href', '').lower() for kw in ['api', 'rest', 'json'])]
                    
                    if api_links:
                        print(f"    Найдено {len(api_links)} ссылок, связанных с API:")
                        for link in api_links[:5]:
                            print(f"      - {link.get('href')}")
                    print()
        except Exception as e:
            pass
    
    # Поиск в JavaScript файлах
    print("\n2. Поиск API endpoints в JavaScript файлах:\n")
    
    js_patterns = [
        r'/api/[^\s"\']+',
        r'/cc3/api/[^\s"\']+',
        r'api/[^\s"\']+',
        r'endpoint["\']?\s*[:=]\s*["\']([^"\']+)["\']',
        r'url["\']?\s*[:=]\s*["\']([^"\']+api[^"\']+)["\']',
    ]
    
    # Получаем главную страницу и ищем JS файлы
    try:
        main_page = requests.get(f"{base_url}/cc3/index.php", timeout=10, verify=False)
        soup = BeautifulSoup(main_page.text, 'html.parser')
        
        # Ищем script теги
        scripts = soup.find_all('script', src=True)
        for script in scripts[:10]:  # Проверяем первые 10
            js_url = script.get('src')
            if not js_url.startswith('http'):
                js_url = f"{base_url}/cc3/{js_url.lstrip('/')}"
            
            try:
                js_response = requests.get(js_url, timeout=5, verify=False)
                js_content = js_response.text
                
                for pattern in js_patterns:
                    matches = re.findall(pattern, js_content, re.IGNORECASE)
                    if matches:
                        print(f"  ✓ Найдено в {js_url}:")
                        for match in matches[:5]:
                            print(f"    {match}")
                        print()
                        break
            except:
                pass
    except Exception as e:
        pass
    
    # Поиск в исходном коде страницы
    print("\n3. Поиск API endpoints в исходном коде страницы:\n")
    
    try:
        main_page = requests.get(f"{base_url}/cc3/index.php?cat=board", timeout=10, verify=False)
        page_content = main_page.text
        
        # Ищем паттерны URL
        url_patterns = [
            r'["\'](/cc3/[^"\']*api[^"\']*)["\']',
            r'["\'](/api/[^"\']+)["\']',
            r'url\s*[:=]\s*["\']([^"\']*api[^"\']*)["\']',
            r'endpoint\s*[:=]\s*["\']([^"\']+)["\']',
        ]
        
        found_urls = set()
        for pattern in url_patterns:
            matches = re.findall(pattern, page_content, re.IGNORECASE)
            for match in matches:
                if 'api' in match.lower():
                    found_urls.add(match)
        
        if found_urls:
            print("  Найдены возможные API endpoints:")
            for url in sorted(found_urls)[:10]:
                print(f"    {url}")
        else:
            print("  API endpoints не найдены в исходном коде")
    except Exception as e:
        print(f"  Ошибка: {e}")
    
    print("\n" + "=" * 70)
    print("РЕКОМЕНДАЦИИ")
    print("=" * 70)
    print("\n1. Проверьте разделы 'Settings', 'Config', 'Modules' в веб-интерфейсе")
    print("2. Ищите разделы с названиями:")
    print("   - API")
    print("   - Integration")
    print("   - Webhooks")
    print("   - External Access")
    print("   - Developer")
    print("3. Проверьте документацию Tikal (PDF файл)")
    print("4. Свяжитесь с поддержкой Tikal для получения API документации")


if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    try:
        from bs4 import BeautifulSoup
        find_api_in_interface()
    except ImportError:
        print("Установите BeautifulSoup4:")
        print("  pip install beautifulsoup4")
        print("\nЗатем запустите скрипт снова")

