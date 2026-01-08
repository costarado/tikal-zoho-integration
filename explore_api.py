"""
Утилита для исследования структуры Tikal API
Проверяет различные варианты endpoints
"""

import requests
import json
from config import TIKAL_CONFIG

def test_endpoint(url, method='GET', headers=None, data=None):
    """Тестирует endpoint и возвращает результат"""
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10, verify=False)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
        else:
            return None
        
        return {
            'status': response.status_code,
            'headers': dict(response.headers),
            'content_type': response.headers.get('Content-Type', ''),
            'text': response.text[:500] if len(response.text) > 500 else response.text,
            'is_json': False
        }
    except Exception as e:
        return {'error': str(e)}

def try_parse_json(text):
    """Пытается распарсить JSON"""
    try:
        return json.loads(text)
    except:
        return None

def explore_api():
    """Исследует структуру API"""
    base_url = TIKAL_CONFIG['base_url'].rstrip('/')
    access_token = TIKAL_CONFIG.get('access_token', '')
    
    print("=" * 70)
    print("Исследование структуры Tikal API")
    print("=" * 70)
    print(f"\nБазовый URL: {base_url}")
    print(f"Токен доступа: {'Установлен' if access_token else 'Не установлен'}\n")
    
    # Заголовки с токеном
    headers_with_token = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Заголовки без токена
    headers_without_token = {
        'Content-Type': 'application/json'
    }
    
    # Варианты endpoints для проверки
    # ВАЖНО: Из скриншота видно, что веб-интерфейс использует /cc3/index.php
    # Поэтому API, скорее всего, находится в /cc3/api/ или /cc3/rest/
    endpoints_to_test = [
        # Базовые пути
        ('/', 'Корневой путь'),
        ('/cc3', 'CC3 корень'),
        ('/cc3/index.php', 'CC3 index'),
        ('/cc3/api', 'CC3 API корень'),
        ('/cc3/rest', 'CC3 REST'),
        ('/cc3/api/v1', 'CC3 API v1'),
        
        # Старые варианты (на случай если API не в /cc3/)
        ('/api', 'API корень'),
        ('/api/v1', 'API v1'),
        
        # Агенты - CC3 пути
        ('/cc3/api/agents', 'Агенты CC3 API'),
        ('/cc3/api/agent', 'Агент CC3 API'),
        ('/cc3/rest/agents', 'Агенты CC3 REST'),
        ('/cc3/index.php?action=agents', 'Агенты через index.php'),
        ('/cc3/index.php?cat=agents', 'Агенты через cat=agents'),
        ('/cc3/api/v1/agents', 'Агенты CC3 API v1'),
        
        # Агенты - старые пути
        ('/api/agents', 'Агенты (текущий)'),
        ('/api/v1/agents', 'Агенты v1'),
        ('/agents', 'Агенты (без /api)'),
        
        # Звонки - CC3 пути
        ('/cc3/api/calls', 'Звонки CC3 API'),
        ('/cc3/api/call', 'Звонок CC3 API'),
        ('/cc3/rest/calls', 'Звонки CC3 REST'),
        ('/cc3/index.php?action=calls', 'Звонки через index.php'),
        ('/cc3/api/v1/calls', 'Звонки CC3 API v1'),
        
        # Звонки - старые пути
        ('/api/calls', 'Звонки (текущий)'),
        ('/api/v1/calls', 'Звонки v1'),
        
        # Записи - CC3 пути
        ('/cc3/api/recordings', 'Записи CC3 API'),
        ('/cc3/api/recording', 'Запись CC3 API'),
        ('/cc3/rest/recordings', 'Записи CC3 REST'),
        ('/cc3/api/v1/recordings', 'Записи CC3 API v1'),
        
        # Записи - старые пути
        ('/api/recordings', 'Записи (текущий)'),
        ('/api/v1/recordings', 'Записи v1'),
        
        # Статистика - CC3 пути
        ('/cc3/api/statistics', 'Статистика CC3 API'),
        ('/cc3/api/stats', 'Статистика CC3 API (короткий)'),
        ('/cc3/rest/statistics', 'Статистика CC3 REST'),
        ('/cc3/api/v1/statistics', 'Статистика CC3 API v1'),
        
        # Статистика - старые пути
        ('/api/statistics', 'Статистика (текущий)'),
        ('/api/v1/statistics', 'Статистика v1'),
        
        # Аутентификация - CC3 пути
        ('/cc3/api/auth/login', 'Логин CC3 API'),
        ('/cc3/api/login', 'Логин CC3 API (короткий)'),
        ('/cc3/rest/auth/login', 'Логин CC3 REST'),
        ('/cc3/index.php?action=login', 'Логин через index.php'),
        ('/cc3/api/v1/auth/login', 'Логин CC3 API v1'),
        
        # Аутентификация - старые пути
        ('/api/auth/login', 'Логин'),
        ('/api/v1/auth/login', 'Логин v1'),
        ('/auth/login', 'Логин (без /api)'),
        
        # Другие возможные пути
        ('/cc3/api/health', 'Health check CC3'),
        ('/cc3/api/status', 'Status CC3'),
        ('/api/health', 'Health check'),
        ('/api/status', 'Status'),
    ]
    
    print("Проверка endpoints...\n")
    print("-" * 70)
    
    found_endpoints = []
    
    for endpoint, description in endpoints_to_test:
        url = f"{base_url}{endpoint}"
        
        # Пробуем с токеном
        result = test_endpoint(url, headers=headers_with_token)
        
        if result and 'error' not in result:
            status = result['status']
            
            # Показываем только интересные результаты
            if status != 404:
                print(f"\n✓ {description}")
                print(f"  URL: {url}")
                print(f"  Статус: {status}")
                print(f"  Content-Type: {result['content_type']}")
                
                if status == 200:
                    json_data = try_parse_json(result['text'])
                    if json_data:
                        print(f"  JSON ответ: {json.dumps(json_data, indent=2, ensure_ascii=False)[:200]}...")
                    else:
                        print(f"  Текст ответа: {result['text'][:200]}...")
                
                if status in [200, 201, 401, 403]:
                    found_endpoints.append({
                        'endpoint': endpoint,
                        'description': description,
                        'status': status,
                        'url': url
                    })
        else:
            # Если с токеном ошибка, пробуем без токена
            result_no_token = test_endpoint(url, headers=headers_without_token)
            if result_no_token and 'error' not in result_no_token:
                status = result_no_token['status']
                if status != 404:
                    print(f"\n⚠ {description} (без токена)")
                    print(f"  URL: {url}")
                    print(f"  Статус: {status}")
    
    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ")
    print("=" * 70)
    
    if found_endpoints:
        print(f"\n✓ Найдено {len(found_endpoints)} доступных endpoints:\n")
        for ep in found_endpoints:
            print(f"  {ep['status']} - {ep['endpoint']} ({ep['description']})")
        
        print("\n" + "=" * 70)
        print("РЕКОМЕНДАЦИИ")
        print("=" * 70)
        print("\nОбновите endpoints в config.py на основе найденных путей.")
        print("Например, если найден /api/v1/agents, используйте:")
        print("  'agents': { 'list': '/api/v1/agents' }")
    else:
        print("\n⚠ Не найдено доступных endpoints с текущими путями.")
        print("\nВозможные причины:")
        print("1. API требует другую структуру путей")
        print("2. Необходима аутентификация через другой метод")
        print("3. API использует другую версию или формат")
        print("\nПроверьте документацию API или свяжитесь с поддержкой Tikal.")
    
    # Проверка корневого пути
    print("\n" + "-" * 70)
    print("Проверка корневого пути...")
    root_result = test_endpoint(base_url, headers=headers_with_token)
    if root_result and 'error' not in root_result:
        print(f"Статус корня: {root_result['status']}")
        if root_result['status'] == 200:
            json_data = try_parse_json(root_result['text'])
            if json_data:
                print(f"Корневой ответ (может содержать информацию об API):")
                print(json.dumps(json_data, indent=2, ensure_ascii=False)[:500])


if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    explore_api()

