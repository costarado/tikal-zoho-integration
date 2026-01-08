"""
Поиск JSON API endpoints
Проверяет различные параметры для получения JSON вместо HTML
"""

import requests
import json
from config import TIKAL_CONFIG

def test_json_format():
    """Тестирует различные параметры для получения JSON"""
    base_url = TIKAL_CONFIG['base_url'].rstrip('/')
    access_token = TIKAL_CONFIG.get('access_token', '')
    
    print("=" * 70)
    print("Поиск JSON API endpoints")
    print("=" * 70)
    print(f"\nБазовый URL: {base_url}\n")
    
    headers_with_token = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Базовые endpoints, которые возвращают HTML
    base_endpoints = [
        '/cc3/index.php?action=agents',
        '/cc3/index.php?cat=agents',
        '/cc3/index.php?action=calls',
        '/cc3/index.php?cat=board',
    ]
    
    # Параметры для получения JSON
    json_params = [
        {'format': 'json'},
        {'api': '1'},
        {'api': 'true'},
        {'json': '1'},
        {'output': 'json'},
        {'response': 'json'},
        {'type': 'json'},
        {'format': 'json', 'api': '1'},
        {'format': 'json', 'action': 'agents'},
    ]
    
    print("1. Проверка параметров для получения JSON:\n")
    
    found_json_endpoints = []
    
    for base_endpoint in base_endpoints:
        url = base_endpoint.split('?')[0]
        existing_params = {}
        if '?' in base_endpoint:
            # Извлекаем существующие параметры
            params_str = base_endpoint.split('?')[1]
            for param in params_str.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    existing_params[key] = value
        
        for json_param in json_params:
            # Объединяем существующие параметры с JSON параметрами
            all_params = {**existing_params, **json_param}
            
            try:
                response = requests.get(
                    url,
                    params=all_params,
                    headers=headers_with_token,
                    timeout=10,
                    verify=False
                )
                
                content_type = response.headers.get('Content-Type', '').lower()
                is_json_response = 'json' in content_type
                
                # Пытаемся распарсить как JSON
                try:
                    json_data = response.json()
                    is_json_data = True
                except:
                    is_json_data = False
                
                if is_json_response or is_json_data:
                    print(f"  ✓ {url}?{requests.compat.urlencode(all_params)}")
                    print(f"    Статус: {response.status_code}")
                    print(f"    Content-Type: {content_type}")
                    if is_json_data:
                        print(f"    ✓ JSON данные получены!")
                        print(f"    Ключи: {list(json_data.keys())[:10]}")
                        found_json_endpoints.append({
                            'url': url,
                            'params': all_params,
                            'data': json_data
                        })
                    print()
            except Exception as e:
                pass
    
    # Проверка специальных API endpoints
    print("\n2. Проверка специальных API endpoints:\n")
    
    api_endpoints = [
        '/cc3/api.php',
        '/cc3/api/index.php',
        '/cc3/api/agents.php',
        '/cc3/api/calls.php',
        '/cc3/api/rest.php',
        '/cc3/rest.php',
        '/cc3/rest/index.php',
        '/cc3/json.php',
        '/cc3/api/json.php',
    ]
    
    for endpoint in api_endpoints:
        url = f"{base_url}{endpoint}"
        try:
            # GET с различными параметрами
            for params in [None, {'action': 'agents'}, {'format': 'json'}]:
                response = requests.get(
                    url,
                    params=params,
                    headers=headers_with_token,
                    timeout=10,
                    verify=False
                )
                
                if response.status_code != 404:
                    content_type = response.headers.get('Content-Type', '').lower()
                    try:
                        json_data = response.json()
                        print(f"  ✓ {url}")
                        if params:
                            print(f"    Параметры: {params}")
                        print(f"    Статус: {response.status_code}")
                        print(f"    ✓ JSON данные получены!")
                        print(f"    Ключи: {list(json_data.keys())[:10]}")
                        found_json_endpoints.append({
                            'url': url,
                            'params': params,
                            'data': json_data
                        })
                        print()
                        break
                    except:
                        if 'json' in content_type:
                            print(f"  ⚠ {url} - JSON Content-Type, но не парсится")
                            print(f"    Ответ: {response.text[:200]}")
        except Exception as e:
            pass
    
    # Проверка через POST
    print("\n3. Проверка через POST с JSON:\n")
    
    post_endpoints = [
        '/cc3/index.php',
        '/cc3/api.php',
        '/cc3/api/index.php',
    ]
    
    for endpoint in post_endpoints:
        url = f"{base_url}{endpoint}"
        try:
            # POST с JSON body
            post_data = {
                'action': 'get_agents',
                'format': 'json'
            }
            
            response = requests.post(
                url,
                json=post_data,
                headers=headers_with_token,
                timeout=10,
                verify=False
            )
            
            if response.status_code not in [404, 405]:
                content_type = response.headers.get('Content-Type', '').lower()
                try:
                    json_data = response.json()
                    print(f"  ✓ POST {url}")
                    print(f"    Статус: {response.status_code}")
                    print(f"    ✓ JSON данные получены!")
                    print(f"    Ключи: {list(json_data.keys())[:10]}")
                    found_json_endpoints.append({
                        'url': url,
                        'method': 'POST',
                        'data': json_data
                    })
                    print()
                except:
                    if 'json' in content_type:
                        print(f"  ⚠ POST {url} - JSON Content-Type")
                        print(f"    Ответ: {response.text[:200]}")
        except Exception as e:
            pass
    
    # Итоги
    print("\n" + "=" * 70)
    print("ИТОГИ")
    print("=" * 70)
    
    if found_json_endpoints:
        print(f"\n✓ Найдено {len(found_json_endpoints)} JSON API endpoints:\n")
        for i, ep in enumerate(found_json_endpoints, 1):
            print(f"{i}. {ep['url']}")
            if ep.get('params'):
                print(f"   Параметры: {ep['params']}")
            if ep.get('method'):
                print(f"   Метод: {ep['method']}")
            print()
        
        print("\n" + "=" * 70)
        print("РЕКОМЕНДАЦИИ")
        print("=" * 70)
        print("\nОбновите config.py с найденными endpoints.")
        print("Пример:")
        print("  API_ENDPOINTS = {")
        print("    'agents': {")
        print(f"      'list': '{found_json_endpoints[0]['url']}'")
        if found_json_endpoints[0].get('params'):
            print(f"      # Параметры: {found_json_endpoints[0]['params']}")
        print("    }")
        print("  }")
    else:
        print("\n⚠ JSON API endpoints не найдены.")
        print("\nВозможные причины:")
        print("1. API требует специальную настройку в админ-панели")
        print("2. API использует другой формат (XML, SOAP и т.д.)")
        print("3. API доступен только через веб-интерфейс")
        print("4. Нужно проверить вкладку 'API Edit API key' в веб-интерфейсе")
        print("\nПопробуйте:")
        print("- Открыть вкладку 'API Edit API key' в веб-интерфейсе")
        print("- Проверить документацию Tikal (PDF файл)")
        print("- Связаться с поддержкой Tikal")


if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    test_json_format()

