"""
Тест различных методов аутентификации
"""

import requests
import json
from config import TIKAL_CONFIG

def test_auth_methods():
    """Тестирует различные методы аутентификации"""
    base_url = TIKAL_CONFIG['base_url'].rstrip('/')
    username = TIKAL_CONFIG['username']
    password = TIKAL_CONFIG['password']
    access_token = TIKAL_CONFIG.get('access_token', '')
    
    print("=" * 70)
    print("Тест методов аутентификации")
    print("=" * 70)
    
    # Варианты endpoints для логина
    # ВАЖНО: Учитываем структуру /cc3/ из веб-интерфейса
    login_endpoints = [
        # CC3 пути (приоритет)
        '/cc3/api/auth/login',
        '/cc3/api/login',
        '/cc3/rest/auth/login',
        '/cc3/index.php?action=login',
        '/cc3/api/v1/auth/login',
        '/cc3/api/authenticate',
        
        # Старые пути
        '/api/auth/login',
        '/api/v1/auth/login',
        '/auth/login',
        '/login',
        '/api/login',
        '/api/authenticate',
        '/authenticate',
    ]
    
    print("\n1. Проверка endpoints для логина:\n")
    
    for endpoint in login_endpoints:
        url = f"{base_url}{endpoint}"
        print(f"Тестирую: {url}")
        
        try:
            # Пробуем POST с credentials
            response = requests.post(
                url,
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json'},
                timeout=10,
                verify=False
            )
            
            print(f"  Статус: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  ✓ Успешно! Ответ: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}")
                    return endpoint, data
                except:
                    print(f"  ✓ Успешно! Текст: {response.text[:200]}")
                    return endpoint, response.text
            elif response.status_code == 401:
                print(f"  ⚠ Требуется аутентификация (возможно правильный endpoint)")
            elif response.status_code == 404:
                print(f"  ✗ Не найден")
            else:
                print(f"  ? Неожиданный статус: {response.status_code}")
                print(f"    Ответ: {response.text[:200]}")
        
        except Exception as e:
            print(f"  ✗ Ошибка: {e}")
        
        print()
    
    # Проверка использования токена
    print("\n2. Проверка использования токена:\n")
    
    test_endpoints = [
        # CC3 пути (приоритет)
        '/cc3/api/agents',
        '/cc3/api/agent',
        '/cc3/rest/agents',
        '/cc3/index.php?action=agents',
        '/cc3/api/v1/agents',
        '/cc3/api/user',
        '/cc3/api/v1/user',
        
        # Старые пути
        '/api/agents',
        '/api/v1/agents',
        '/agents',
        '/api/user',
        '/api/v1/user',
        '/user',
    ]
    
    auth_headers_variants = [
        ('Bearer', f'Bearer {access_token}'),
        ('Token', f'Token {access_token}'),
        ('Authorization', f'Authorization: {access_token}'),
        ('X-Auth-Token', access_token),
        ('X-Access-Token', access_token),
        ('X-API-Key', access_token),
    ]
    
    for endpoint in test_endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\nТестирую: {url}")
        
        for header_name, header_value in auth_headers_variants:
            try:
                headers = {header_name: header_value, 'Content-Type': 'application/json'}
                response = requests.get(url, headers=headers, timeout=10, verify=False)
                
                if response.status_code != 404:
                    print(f"  {header_name}: {header_value[:50]}... → {response.status_code}")
                    if response.status_code == 200:
                        print(f"    ✓ Успешно!")
                        try:
                            data = response.json()
                            print(f"    Данные: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}")
                        except:
                            print(f"    Текст: {response.text[:200]}")
            except Exception as e:
                pass
    
    print("\n" + "=" * 70)
    print("РЕКОМЕНДАЦИИ")
    print("=" * 70)
    print("\nЕсли найден рабочий endpoint для логина, обновите config.py")
    print("Если найден рабочий формат заголовков, обновите auth.py")


if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    test_auth_methods()

