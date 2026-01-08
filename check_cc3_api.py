"""
Специальная проверка CC3 API структуры
Основано на структуре веб-интерфейса: /cc3/index.php?cat=board
"""

import requests
import json
from config import TIKAL_CONFIG

def test_cc3_api():
    """Тестирует CC3 API структуру"""
    base_url = TIKAL_CONFIG['base_url'].rstrip('/')
    access_token = TIKAL_CONFIG.get('access_token', '')
    
    print("=" * 70)
    print("Проверка CC3 API структуры")
    print("=" * 70)
    print(f"\nБазовый URL: {base_url}")
    print(f"Веб-интерфейс: {base_url}/cc3/index.php?cat=board\n")
    
    headers_with_token = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    headers_form = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Проверка index.php с различными параметрами
    print("1. Проверка index.php с параметрами:\n")
    
    index_params = [
        {'cat': 'api'},
        {'cat': 'rest'},
        {'action': 'api'},
        {'action': 'agents'},
        {'action': 'calls'},
        {'module': 'api'},
        {'module': 'rest'},
        {'page': 'api'},
        {'api': 'agents'},
        {'api': 'calls'},
        {'format': 'json'},
        {'format': 'json', 'action': 'agents'},
    ]
    
    for params in index_params:
        url = f"{base_url}/cc3/index.php"
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers_with_token,
                timeout=10,
                verify=False
            )
            
            if response.status_code != 404:
                print(f"  {url}?{requests.compat.urlencode(params)}")
                print(f"    Статус: {response.status_code}")
                print(f"    Content-Type: {response.headers.get('Content-Type', '')}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"    ✓ JSON ответ получен!")
                        print(f"    Ключи: {list(data.keys())[:5]}")
                        return url, params, data
                    except:
                        text = response.text[:200]
                        if 'json' in text.lower() or 'api' in text.lower():
                            print(f"    ⚠ Текст ответа: {text}")
                print()
        except Exception as e:
            pass
    
    # Проверка прямых API путей
    print("\n2. Проверка прямых API путей:\n")
    
    api_paths = [
        '/cc3/api',
        '/cc3/api/',
        '/cc3/api/index.php',
        '/cc3/rest',
        '/cc3/rest/',
        '/cc3/api.php',
        '/cc3/rest.php',
        '/cc3/api/agents.php',
        '/cc3/api/calls.php',
    ]
    
    for path in api_paths:
        url = f"{base_url}{path}"
        try:
            # GET запрос
            response = requests.get(
                url,
                headers=headers_with_token,
                timeout=10,
                verify=False
            )
            
            if response.status_code != 404:
                print(f"  {url}")
                print(f"    Статус: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"    ✓ JSON ответ получен!")
                        return url, None, data
                    except:
                        text = response.text[:200]
                        if 'api' in text.lower() or 'json' in text.lower():
                            print(f"    ⚠ Текст: {text[:100]}")
                print()
        except Exception as e:
            pass
    
    # Проверка через POST
    print("\n3. Проверка через POST запросы:\n")
    
    post_endpoints = [
        '/cc3/api/agents',
        '/cc3/api/calls',
        '/cc3/index.php',
    ]
    
    for endpoint in post_endpoints:
        url = f"{base_url}{endpoint}"
        try:
            # POST с JSON
            response = requests.post(
                url,
                json={'action': 'get_agents'},
                headers=headers_with_token,
                timeout=10,
                verify=False
            )
            
            if response.status_code not in [404, 405]:
                print(f"  POST {url}")
                print(f"    Статус: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"    ✓ JSON ответ получен!")
                        return url, {'method': 'POST'}, data
                    except:
                        pass
                print()
        except Exception as e:
            pass
    
    print("\n" + "=" * 70)
    print("РЕКОМЕНДАЦИИ")
    print("=" * 70)
    print("\nЕсли не найдено рабочих endpoints:")
    print("1. Проверьте вкладку 'API Edit API key' в веб-интерфейсе")
    print("2. Там может быть документация по API endpoints")
    print("3. Или примеры использования API")
    print("4. Возможно, API требует специальную настройку в админ-панели")


if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    test_cc3_api()

