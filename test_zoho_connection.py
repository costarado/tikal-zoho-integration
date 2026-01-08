"""
Тестирование подключения к Zoho CRM API
Использует токены из config.py
"""

import sys
import io
import requests
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from config import ZOHO_CONFIG
except ImportError:
    print("❌ Ошибка: config.py не найден")
    sys.exit(1)


def test_with_access_token():
    """Тестирование подключения через Access Token"""
    print("=" * 70)
    print("🔍 Тестирование подключения к Zoho CRM через Access Token")
    print("=" * 70)
    
    access_token = ZOHO_CONFIG.get('access_token')
    api_domain = ZOHO_CONFIG.get('api_domain', 'https://www.zohoapis.com')
    module = ZOHO_CONFIG.get('module', 'Contacts')
    
    if not access_token or access_token == 'your_access_token_here':
        print("❌ Access Token не настроен в config.py")
        return False
    
    # Тест 1: Получение информации об организации (может требовать специальных scope)
    print("\n📋 Тест 1: Получение информации об организации...")
    try:
        url = f"{api_domain}/crm/v2/org"
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            org_data = response.json()
            if 'org' in org_data and len(org_data['org']) > 0:
                org = org_data['org'][0]
                print(f"   ✅ Подключение успешно!")
                print(f"   📌 Organization Name: {org.get('company_name', 'N/A')}")
                print(f"   📌 Organization ID: {org.get('zgid', 'N/A')}")
                
                # Сохраняем Organization ID в config (если не указан)
                if ZOHO_CONFIG.get('organization_id') == 'your_organization_id_here':
                    print(f"\n   💡 Сохраните Organization ID в config.py:")
                    print(f"      'organization_id': '{org.get('zgid', '')}'")
            else:
                print(f"   ⚠️  Ответ получен, но данные организации не найдены")
                print(f"   Ответ: {org_data}")
        elif response.status_code == 401:
            error_data = response.json()
            if 'OAUTH_SCOPE_MISMATCH' in str(error_data):
                print(f"   ⚠️  Endpoint требует специальных разрешений (scope)")
                print(f"   Пропускаем этот тест, переходим к тесту полей...")
            else:
                print(f"   ❌ Ошибка: {response.status_code}")
                print(f"   Ответ: {response.text}")
                return False
        else:
            print(f"   ⚠️  Ошибка: {response.status_code}")
            print(f"   Ответ: {response.text}")
            # Не возвращаем False, продолжаем тестирование
    
    except Exception as e:
        print(f"   ❌ Ошибка при запросе: {e}")
        return False
    
    # Тест 2: Получение списка полей модуля Contacts
    print(f"\n📋 Тест 2: Получение списка полей модуля {module}...")
    try:
        url = f"{api_domain}/crm/v2/settings/fields"
        params = {"module": module}
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            fields_data = response.json()
            if 'fields' in fields_data:
                fields = fields_data['fields']
                print(f"   ✅ Получено полей: {len(fields)}")
                
                # Ищем кастомные поля
                custom_fields = [
                    'Agent_ID', 'Extension', 'Tikal_Status', 
                    'Queues', 'Queue_Count1', 'Active'
                ]
                
                print(f"\n   🔍 Поиск кастомных полей...")
                found_fields = []
                for field in fields:
                    api_name = field.get('api_name', '')
                    if api_name in custom_fields:
                        found_fields.append(api_name)
                        print(f"      ✅ {api_name} - {field.get('display_label', 'N/A')}")
                
                if len(found_fields) < len(custom_fields):
                    missing = set(custom_fields) - set(found_fields)
                    print(f"\n   ⚠️  Не найдены поля: {', '.join(missing)}")
                    print(f"      Возможно, поля имеют другие API имена")
                
                return True
            else:
                print(f"   ⚠️  Поля не найдены в ответе")
                print(f"   Ответ: {fields_data}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
    
    except Exception as e:
        print(f"   ❌ Ошибка при запросе: {e}")
        return False


def test_with_refresh_token():
    """Тестирование обновления Access Token через Refresh Token"""
    print("\n" + "=" * 70)
    print("🔄 Тестирование обновления Access Token")
    print("=" * 70)
    
    refresh_token = ZOHO_CONFIG.get('refresh_token')
    client_id = ZOHO_CONFIG.get('client_id')
    client_secret = ZOHO_CONFIG.get('client_secret')
    
    if not refresh_token or refresh_token == 'your_refresh_token_here':
        print("❌ Refresh Token не настроен в config.py")
        return False
    
    if client_id == 'your_client_id_here' or not client_id:
        print("⚠️  Client ID и Client Secret не настроены")
        print("   Для обновления токена нужны Client ID и Client Secret")
        print("   Получите их из: https://api-console.zoho.com/")
        return False
    
    try:
        url = "https://accounts.zoho.com/oauth/v2/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            new_access_token = token_data.get('access_token')
            print(f"   ✅ Токен успешно обновлен!")
            print(f"   💡 Новый Access Token: {new_access_token[:50]}...")
            print(f"\n   ⚠️  Обновите access_token в config.py")
            return True
        else:
            print(f"   ❌ Ошибка обновления: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
    
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False


def main():
    """Основная функция"""
    print("=" * 70)
    print("🧪 Тестирование подключения к Zoho CRM")
    print("=" * 70)
    
    # Тест с текущим Access Token
    success = test_with_access_token()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ Подключение работает!")
        print("=" * 70)
        print("\n💡 Следующие шаги:")
        print("   1. Если Organization ID не найден - найдите его в URL Zoho CRM")
        print("   2. Обновите organization_id в config.py")
        print("   3. Запустите: python zoho_api_permissions.py")
    else:
        print("\n" + "=" * 70)
        print("⚠️  Проблемы с подключением")
        print("=" * 70)
        print("\n💡 Возможные причины:")
        print("   1. Access Token истек (действителен ~1 час)")
        print("   2. Неверный API домен (проверьте регион)")
        print("   3. Токен не имеет нужных разрешений")
        print("\n📚 Решение:")
        print("   - Настройте Client ID и Client Secret")
        print("   - Обновите токен через test_with_refresh_token()")
        print("   - См. инструкции: ZOHO_API_SETUP_GUIDE.md")
    
    # Тест обновления токена (если настроены credentials)
    if ZOHO_CONFIG.get('client_id') != 'your_client_id_here':
        test_with_refresh_token()


if __name__ == '__main__':
    main()
