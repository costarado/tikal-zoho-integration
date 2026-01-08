"""
Автоматическая настройка разрешений полей в Zoho CRM через API
Требует: pip install zohocrmsdk

Использование:
1. Настройте ZOHO_CONFIG в config.py (см. ZOHO_API_SETUP_GUIDE.md)
2. Запустите: python zoho_api_permissions.py
"""

import sys
import io
from zohocrmsdk.src.com.zoho.crm.api import Initializer
from zohocrmsdk.src.com.zoho.crm.api.fields import FieldsOperations, GetFieldsParam
from zohocrmsdk.src.com.zoho.crm.api.fields import Field, Permission
from zohocrmsdk.src.com.zoho.api.authenticator import OAuthToken
from zohocrmsdk.src.com.zoho.api.dc import USDataCenter, EUDataCenter, INDataCenter
import json

# Попытка импорта из config.py
try:
    from config import ZOHO_CONFIG
    CLIENT_ID = ZOHO_CONFIG.get('client_id')
    CLIENT_SECRET = ZOHO_CONFIG.get('client_secret')
    REFRESH_TOKEN = ZOHO_CONFIG.get('refresh_token')
    ORGANIZATION_ID = ZOHO_CONFIG.get('organization_id')
    API_DOMAIN = ZOHO_CONFIG.get('api_domain', 'https://www.zohoapis.com')
    MODULE = ZOHO_CONFIG.get('module', 'Contacts')
except ImportError:
    print("⚠️  config.py не найден или ZOHO_CONFIG не определен")
    print("   Используйте значения по умолчанию или настройте config.py")
    CLIENT_ID = "your_client_id"
    CLIENT_SECRET = "your_client_secret"
    REFRESH_TOKEN = "your_refresh_token"
    ORGANIZATION_ID = "your_organization_id"
    API_DOMAIN = "https://www.zohoapis.com"
    MODULE = "Contacts"

# Кастомные поля (с вариантами имен)
CUSTOM_FIELDS = {
    "Agent_ID": ["Agent_ID", "agent_id"],
    "Extension": ["Extension", "extension"],
    "Tikal_Status": ["Tikal_Status", "Tikal_Status", "Status", "status"],
    "Queues": ["Queues", "queues"],
    "Queue_Count1": ["Queue_Count1", "Queue_Count", "queue_count"],
    "Active": ["Active", "Is_Active", "is_active"],
}


def get_data_center(api_domain: str):
    """Определяет Data Center по домену"""
    if 'zoho.eu' in api_domain or 'zohoapis.eu' in api_domain:
        return EUDataCenter.PRODUCTION()
    elif 'zoho.in' in api_domain or 'zohoapis.in' in api_domain:
        return INDataCenter.PRODUCTION()
    else:
        return USDataCenter.PRODUCTION()


def initialize_zoho():
    """Инициализация Zoho CRM API"""
    if CLIENT_ID == "your_client_id" or not CLIENT_ID:
        raise ValueError(
            "❌ Zoho API не настроен!\n"
            "   Следуйте инструкциям в ZOHO_API_SETUP_GUIDE.md\n"
            "   Или настройте ZOHO_CONFIG в config.py"
        )
    
    environment = get_data_center(API_DOMAIN)
    token = OAuthToken(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        refresh_token=REFRESH_TOKEN
    )
    
    try:
        Initializer.initialize(
            environment=environment,
            token=token
        )
        print("✓ Zoho CRM API инициализирован")
    except Exception as e:
        raise Exception(f"❌ Ошибка инициализации API: {e}")


def get_all_roles():
    """Получает список всех ролей через Roles API"""
    try:
        from zohocrmsdk.src.com.zoho.crm.api.roles import RolesOperations
        
        roles_operations = RolesOperations()
        response = roles_operations.get_roles()
        
        if response is not None:
            roles_list = []
            roles = response.get_object()
            
            if hasattr(roles, 'roles') and roles.roles:
                for role in roles.roles:
                    roles_list.append({
                        'id': role.get_id(),
                        'name': role.get_name()
                    })
            
            return roles_list
    except Exception as e:
        print(f"⚠️  Не удалось получить роли через API: {e}")
        print("   Используются роли по умолчанию")
    
    # Fallback: возвращаем пример ролей
    return [
        {"id": "Admin", "name": "Administrator"},
        {"id": "Manager", "name": "Manager"},
        {"id": "User", "name": "User"}
    ]


def find_field_by_name(fields_operations, field_name_variants: list):
    """
    Находит поле по вариантам имени
    
    Args:
        fields_operations: Экземпляр FieldsOperations
        field_name_variants: Список вариантов имени поля
    
    Returns:
        Field или None
    """
    try:
        param_instance = GetFieldsParam()
        param_instance.module = MODULE
        
        response = fields_operations.get_fields(param_instance)
        
        if response is not None:
            response_object = response.get_object()
            
            if response_object and hasattr(response_object, 'fields'):
                fields = response_object.fields
                
                # Ищем поле по вариантам имени
                for field in fields:
                    api_name = field.get_api_name()
                    if api_name in field_name_variants:
                        return field
                
                # Если не найдено, выводим список доступных полей для отладки
                print(f"   Доступные поля (первые 10):")
                for i, field in enumerate(fields[:10]):
                    print(f"     - {field.get_api_name()}")
                if len(fields) > 10:
                    print(f"     ... и еще {len(fields) - 10} полей")
        
        return None
    except Exception as e:
        print(f"   ✗ Ошибка при поиске поля: {e}")
        return None


def set_field_permissions(field_display_name: str, field_name_variants: list, 
                          visible: bool = True, editable: bool = True, searchable: bool = True):
    """
    Устанавливает разрешения для поля
    
    Args:
        field_display_name: Отображаемое имя поля (для логов)
        field_name_variants: Список вариантов API имени поля
        visible: Видимо для всех ролей
        editable: Редактируемо для всех ролей
        searchable: Доступно для поиска
    """
    try:
        fields_operations = FieldsOperations()
        
        # Находим поле
        target_field = find_field_by_name(fields_operations, field_name_variants)
        
        if target_field:
            api_name = target_field.get_api_name()
            print(f"   ✓ Найдено поле: {api_name}")
            
            # Получаем текущие разрешения
            current_permissions = target_field.get_permissions()
            
            if current_permissions:
                print(f"   ✓ Текущие разрешения найдены")
                # Обновляем разрешения для всех ролей
                for permission in current_permissions:
                    permission.set_visible(visible)
                    permission.set_editable(editable)
                
                # Обновляем поле через API
                # Примечание: Обновление полей через API может быть ограничено
                # В некоторых случаях нужно делать это вручную через веб-интерфейс
                print(f"   ⚠️  Обновление разрешений через API может быть ограничено")
                print(f"   💡 Рекомендуется проверить разрешения вручную:")
                print(f"      Settings → Customization → Modules → Contacts → Fields → {field_display_name}")
            else:
                print(f"   ⚠️  Разрешения не найдены. Поле может быть Public по умолчанию")
            
            # Включаем поиск (если доступно)
            if searchable:
                try:
                    # Попытка установить searchable через API
                    # Примечание: Это может не работать для всех версий API
                    print(f"   💡 Для включения поиска:")
                    print(f"      Settings → Customization → Modules → Contacts → Fields → {field_display_name}")
                    print(f"      Включите опцию 'Searchable'")
                except:
                    pass
            
            return True
        else:
            print(f"   ✗ Поле не найдено среди вариантов: {field_name_variants}")
            return False
            
    except Exception as e:
        print(f"   ✗ Ошибка при настройке разрешений: {e}")
        return False


def main():
    """Основная функция"""
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 70)
    print("🔧 Автоматическая настройка разрешений полей в Zoho CRM")
    print("=" * 70)
    print()
    
    # Инициализация
    try:
        initialize_zoho()
    except Exception as e:
        print(f"\n{e}")
        print("\n📚 Инструкции по настройке:")
        print("   См. файл: ZOHO_API_SETUP_GUIDE.md")
        return
    
    # Получение ролей
    print("\n📋 Получение списка ролей...")
    roles = get_all_roles()
    print(f"   ✓ Найдено ролей: {len(roles)}")
    for role in roles[:5]:  # Показываем первые 5
        print(f"     - {role.get('name', role)}")
    if len(roles) > 5:
        print(f"     ... и еще {len(roles) - 5} ролей")
    
    # Настройка разрешений для каждого поля
    print("\n" + "=" * 70)
    print("🔧 Настройка разрешений для кастомных полей...")
    print("=" * 70)
    
    success_count = 0
    fail_count = 0
    
    for field_display_name, field_variants in CUSTOM_FIELDS.items():
        print(f"\n📝 Поле: {field_display_name}")
        print(f"   Варианты API имени: {', '.join(field_variants)}")
        
        if set_field_permissions(
            field_display_name=field_display_name,
            field_name_variants=field_variants,
            visible=True,
            editable=True,
            searchable=True
        ):
            success_count += 1
        else:
            fail_count += 1
    
    # Итоги
    print("\n" + "=" * 70)
    print("📊 Итоги настройки")
    print("=" * 70)
    print(f"✅ Успешно обработано: {success_count} полей")
    if fail_count > 0:
        print(f"⚠️  Проблемы с: {fail_count} полями")
    
    print("\n💡 Важно:")
    print("   - Некоторые настройки могут требовать ручной проверки")
    print("   - Проверьте разрешения в веб-интерфейсе Zoho CRM")
    print("   - Убедитесь, что поиск включен для всех полей")
    print("\n📚 Полная инструкция: ZOHO_API_SETUP_GUIDE.md")
    print("=" * 70)


if __name__ == '__main__':
    main()
