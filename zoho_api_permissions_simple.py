"""
Автоматическая настройка разрешений полей в Zoho CRM через API
Использует прямые HTTP запросы (не требует SDK)

Использование:
1. Настройте ZOHO_CONFIG в config.py
2. Запустите: python zoho_api_permissions_simple.py
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
    print("❌ config.py не найден")
    sys.exit(1)

# Кастомные поля
CUSTOM_FIELDS = {
    "Agent_ID": ["Agent_ID", "agent_id"],
    "Extension": ["Extension", "extension"],
    "Tikal_Status": ["Tikal_Status", "Tikal_Status", "Status", "status"],
    "Queues": ["Queues", "queues"],
    "Queue_Count1": ["Queue_Count1", "Queue_Count", "queue_count"],
    "Active": ["Active", "Is_Active", "is_active"],
}


def refresh_access_token():
    """Обновляет Access Token через Refresh Token"""
    client_id = ZOHO_CONFIG.get('client_id')
    client_secret = ZOHO_CONFIG.get('client_secret')
    refresh_token = ZOHO_CONFIG.get('refresh_token')
    
    if not all([client_id, client_secret, refresh_token]):
        print("❌ Не настроены Client ID, Client Secret или Refresh Token")
        return None
    
    url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            return result.get('access_token')
        else:
            print(f"❌ Ошибка обновления токена: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None


def get_access_token():
    """Получает актуальный Access Token"""
    access_token = ZOHO_CONFIG.get('access_token')
    
    # Проверяем, не истек ли токен (попробуем использовать)
    # Если не работает, обновим
    return access_token


def get_fields(access_token: str):
    """Получает список полей модуля Contacts"""
    api_domain = ZOHO_CONFIG.get('api_domain', 'https://www.zohoapis.com')
    module = ZOHO_CONFIG.get('module', 'Contacts')
    
    url = f"{api_domain}/crm/v2/settings/fields"
    params = {"module": module}
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('fields', [])
        elif response.status_code == 401:
            # Токен истек, обновляем
            print("   ⚠️  Токен истек, обновляем...")
            new_token = refresh_access_token()
            if new_token:
                headers["Authorization"] = f"Zoho-oauthtoken {new_token}"
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return data.get('fields', [])
        return []
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return []


def find_custom_fields(fields: list):
    """Находит кастомные поля по вариантам имен"""
    found_fields = {}
    
    for field_display_name, variants in CUSTOM_FIELDS.items():
        for field in fields:
            api_name = field.get('api_name', '')
            if api_name in variants:
                found_fields[field_display_name] = field
                break
    
    return found_fields


def check_field_permissions(field: dict):
    """Проверяет настройки разрешений поля"""
    permissions = field.get('permissions', [])
    
    if not permissions:
        return {
            'has_permissions': False,
            'visible_count': 0,
            'editable_count': 0,
            'total_roles': 0
        }
    
    visible_count = sum(1 for p in permissions if p.get('visible', False))
    editable_count = sum(1 for p in permissions if p.get('editable', False))
    
    return {
        'has_permissions': True,
        'visible_count': visible_count,
        'editable_count': editable_count,
        'total_roles': len(permissions)
    }


def main():
    """Основная функция"""
    print("=" * 70)
    print("🔧 Настройка разрешений полей в Zoho CRM")
    print("=" * 70)
    print()
    
    # Получаем токен
    print("📋 Получение Access Token...")
    access_token = get_access_token()
    if not access_token:
        print("❌ Access Token не настроен")
        return
    
    # Получаем список полей
    print("📋 Получение списка полей модуля Contacts...")
    fields = get_fields(access_token)
    
    if not fields:
        print("❌ Не удалось получить список полей")
        print("   Проверьте настройки в config.py")
        return
    
    print(f"   ✅ Получено полей: {len(fields)}")
    
    # Ищем кастомные поля
    print("\n" + "=" * 70)
    print("🔍 Поиск кастомных полей...")
    print("=" * 70)
    
    found_fields = find_custom_fields(fields)
    
    if not found_fields:
        print("❌ Кастомные поля не найдены")
        return
    
    print(f"\n✅ Найдено кастомных полей: {len(found_fields)}")
    
    # Проверяем разрешения для каждого поля
    print("\n" + "=" * 70)
    print("📊 Проверка разрешений полей")
    print("=" * 70)
    
    for field_display_name, field in found_fields.items():
        api_name = field.get('api_name', 'N/A')
        display_label = field.get('display_label', 'N/A')
        
        print(f"\n📝 Поле: {display_label} ({api_name})")
        
        # Проверяем разрешения
        perm_info = check_field_permissions(field)
        
        if perm_info['has_permissions']:
            print(f"   ✅ Разрешения настроены:")
            print(f"      - Видимо для ролей: {perm_info['visible_count']}/{perm_info['total_roles']}")
            print(f"      - Редактируемо для ролей: {perm_info['editable_count']}/{perm_info['total_roles']}")
            
            if perm_info['visible_count'] < perm_info['total_roles']:
                print(f"   ⚠️  Не все роли имеют доступ к просмотру")
        else:
            print(f"   ⚠️  Разрешения не настроены (поле может быть Public по умолчанию)")
        
        # Проверяем поиск
        searchable = field.get('searchable', False)
        if searchable:
            print(f"   ✅ Поиск включен")
        else:
            print(f"   ⚠️  Поиск не включен")
            print(f"      💡 Включите вручную: Settings → Fields → {display_label} → Searchable")
    
    # Итоги
    print("\n" + "=" * 70)
    print("📊 Итоги")
    print("=" * 70)
    print(f"✅ Найдено полей: {len(found_fields)}")
    print(f"📋 Всего полей в модуле: {len(fields)}")
    
    print("\n💡 Важно:")
    print("   - Настройка разрешений через REST API ограничена")
    print("   - Для полной настройки используйте веб-интерфейс Zoho CRM:")
    print("     Settings → Customization → Modules → Contacts → Fields")
    print("   - Для каждого поля:")
    print("     • Field Level Security → Visible/Editable для всех ролей")
    print("     • Searchable → включить для поиска")
    
    print("\n📚 Инструкции:")
    print("   - ZOHO_FIELDS_ALL_LAYOUTS_USERS.md - настройка для всех пользователей")
    print("   - ZOHO_CUSTOM_FIELDS_INSTRUCTIONS.md - создание полей")


if __name__ == '__main__':
    main()
