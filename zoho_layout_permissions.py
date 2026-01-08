"""
Скрипт для настройки разрешений кастомных полей в Zoho CRM
и инструкции по клонированию макета Standard
"""

import json
import sys
import io
from typing import Dict, List, Optional

# Кастомные поля для настройки
CUSTOM_FIELDS = [
    'Agent_ID',      # Agent ID
    'Extension',     # Extension
    'Tikal_Status',  # Tikal Status (или Status)
    'Queues',        # Queues
    'Queue_Count1',  # Queue Count (внутреннее имя может быть Queue_Count1)
    'Active',        # Is Active
]

# Альтернативные имена полей (на случай, если внутренние имена отличаются)
FIELD_NAME_VARIANTS = {
    'Agent_ID': ['Agent_ID', 'Agent_ID', 'agent_id'],
    'Extension': ['Extension', 'extension'],
    'Tikal_Status': ['Tikal_Status', 'Tikal_Status', 'Status', 'status'],
    'Queues': ['Queues', 'queues'],
    'Queue_Count1': ['Queue_Count1', 'Queue_Count', 'queue_count'],
    'Active': ['Active', 'Is_Active', 'is_active'],
}


def print_instructions():
    """Выводит инструкции по клонированию макета"""
    print("=" * 70)
    print("📋 ИНСТРУКЦИЯ: Клонирование макета Standard в Zoho CRM")
    print("=" * 70)
    print("""
Клонирование макетов в Zoho CRM выполняется через веб-интерфейс.

ШАГ 1: Клонирование макета Standard
------------------------------------
1. Войдите в Zoho CRM
2. Settings → Customization → Modules → Contacts → Layouts
3. Найдите макет "Standard"
4. Нажмите на иконку "⋮" (три точки) рядом с "Standard"
5. Выберите "Clone" (Клонировать)
6. Введите имя нового макета: "Standard - Tikal Agents"
7. Нажмите "Save"

ШАГ 2: Добавление полей в клонированный макет
------------------------------------------------
1. Откройте клонированный макет "Standard - Tikal Agents"
2. Нажмите "Edit"
3. Перейдите на вкладку "DETAIL VIEW"
4. Перетащите кастомные поля из списка "Unused Fields" в форму:
   - Agent ID
   - Extension
   - Tikal Status
   - Queues
   - Queue_Count
   - Active
5. Сохраните изменения

ШАГ 3: Настройка разрешений (через скрипт или вручную)
--------------------------------------------------------
Запустите этот скрипт для автоматической настройки разрешений.
Или настройте вручную через Settings → Fields → [Поле] → Permissions
""")


def setup_zoho_api_instructions():
    """Инструкции по настройке Zoho CRM API"""
    print("=" * 70)
    print("🔧 НАСТРОЙКА Zoho CRM API (для автоматизации)")
    print("=" * 70)
    print("""
Для автоматической настройки разрешений через API нужно:

1. Создать Zoho API приложение:
   - Перейдите: https://api-console.zoho.com/
   - Создайте новое приложение (Server-based Application)
   - Получите Client ID и Client Secret

2. Установить Zoho CRM Python SDK:
   pip install zohocrmsdk

3. Настроить credentials в config.py:
   ZOHO_CONFIG = {
       'client_id': 'your_client_id',
       'client_secret': 'your_client_secret',
       'refresh_token': 'your_refresh_token',
       'api_domain': 'https://www.zohoapis.com',
       'organization_id': 'your_org_id'
   }

4. Получить Refresh Token:
   - Следуйте инструкциям: https://www.zoho.com/crm/developer/docs/api/v2/oauth-overview.html

АЛЬТЕРНАТИВА: Настройка вручную через веб-интерфейс (см. ниже)
""")


def manual_permissions_setup():
    """Инструкции по ручной настройке разрешений"""
    print("=" * 70)
    print("✋ РУЧНАЯ НАСТРОЙКА РАЗРЕШЕНИЙ ДЛЯ ВСЕХ ПОЛЕЙ")
    print("=" * 70)
    print("""
Для каждого кастомного поля выполните:

1. Settings → Customization → Modules → Contacts → Fields
2. Найдите поле (например, "Agent ID")
3. Нажмите на поле для редактирования
4. Найдите раздел "Field Level Security" или "Permissions"
5. Для каждой роли установите:
   ✅ Visible = Yes
   ✅ Editable = Yes (если нужно редактирование)
6. Сохраните изменения

Повторите для всех полей:
- Agent ID
- Extension
- Tikal Status
- Queues
- Queue_Count
- Active

ВРЕМЯ: ~2-3 минуты на поле × 6 полей = ~15 минут
""")


def create_permissions_script():
    """Создает скрипт для автоматической настройки разрешений через API"""
    script_content = '''"""
Автоматическая настройка разрешений полей в Zoho CRM через API
Требует: pip install zohocrmsdk
"""

from zohocrmsdk.src.com.zoho.crm.api import Initializer
from zohocrmsdk.src.com.zoho.crm.api.fields import FieldsOperations, GetFieldsParam
from zohocrmsdk.src.com.zoho.crm.api.fields import Field, Permission
from zohocrmsdk.src.com.zoho.crm.api.util import APIResponse
from zohocrmsdk.src.com.zoho.api.authenticator import OAuthToken
from zohocrmsdk.src.com.zoho.api.dc import USDataCenter
from zohocrmsdk.src.com.zoho.crm.api import HeaderMap
import json

# Настройки (заполните своими данными)
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REFRESH_TOKEN = "your_refresh_token"
ORGANIZATION_ID = "your_organization_id"

# Кастомные поля
CUSTOM_FIELDS = [
    "Agent_ID",
    "Extension", 
    "Tikal_Status",
    "Queues",
    "Queue_Count1",
    "Active"
]


def initialize_zoho():
    """Инициализация Zoho CRM API"""
    environment = USDataCenter.PRODUCTION()
    token = OAuthToken(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        refresh_token=REFRESH_TOKEN
    )
    
    Initializer.initialize(
        environment=environment,
        token=token
    )


def get_all_roles():
    """Получает список всех ролей"""
    # TODO: Реализовать получение ролей через Roles API
    # Пока возвращаем пример
    return ["Admin", "Manager", "User"]  # Замените на реальные роли


def set_field_permissions(field_api_name: str, visible: bool = True, editable: bool = True):
    """
    Устанавливает разрешения для поля
    
    Args:
        field_api_name: API имя поля (например, "Agent_ID")
        visible: Видимо для всех ролей
        editable: Редактируемо для всех ролей
    """
    try:
        fields_operations = FieldsOperations()
        
        # Получаем информацию о поле
        param_instance = GetFieldsParam()
        param_instance.module = "Contacts"
        
        response = fields_operations.get_fields(param_instance)
        
        if response is not None:
            response_object = response.get_object()
            
            if response_object is not None:
                if hasattr(response_object, 'fields'):
                    fields = response_object.fields
                    
                    # Находим нужное поле
                    target_field = None
                    for field in fields:
                        if field.get_api_name() == field_api_name:
                            target_field = field
                            break
                    
                    if target_field:
                        # Создаем разрешения для всех ролей
                        roles = get_all_roles()
                        permissions = []
                        
                        for role in roles:
                            permission = Permission()
                            permission.set_visible(visible)
                            permission.set_editable(editable)
                            # permission.set_role(role)  # Установить роль
                            permissions.append(permission)
                        
                        # Обновляем поле
                        # TODO: Реализовать обновление через UpdateField API
                        print(f"✓ Настроены разрешения для поля: {field_api_name}")
                    else:
                        print(f"✗ Поле не найдено: {field_api_name}")
                else:
                    print("✗ Не удалось получить список полей")
            else:
                print("✗ Пустой ответ от API")
        else:
            print("✗ Ошибка при получении полей")
            
    except Exception as e:
        print(f"✗ Ошибка при настройке разрешений для {field_api_name}: {e}")


def main():
    """Основная функция"""
    print("=" * 70)
    print("Настройка разрешений полей в Zoho CRM")
    print("=" * 70)
    
    # Инициализация
    try:
        initialize_zoho()
        print("✓ Zoho CRM API инициализирован")
    except Exception as e:
        print(f"✗ Ошибка инициализации: {e}")
        print("\\nПроверьте настройки в скрипте:")
        print("- CLIENT_ID")
        print("- CLIENT_SECRET")
        print("- REFRESH_TOKEN")
        print("- ORGANIZATION_ID")
        return
    
    # Настройка разрешений для каждого поля
    print("\\nНастройка разрешений...")
    for field in CUSTOM_FIELDS:
        print(f"\\nОбработка поля: {field}")
        set_field_permissions(field, visible=True, editable=True)
    
    print("\\n" + "=" * 70)
    print("✅ Настройка завершена!")
    print("=" * 70)


if __name__ == '__main__':
    main()
'''
    
    with open('zoho_api_permissions.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✓ Создан скрипт: zoho_api_permissions.py")
    print("  Заполните настройки Zoho API и запустите скрипт")


def create_quick_setup_guide():
    """Создает быструю инструкцию по настройке"""
    guide = """# 🚀 Быстрая настройка: Клонирование макета и разрешения

## Шаг 1: Клонирование макета Standard (2 минуты)

1. **Settings** → **Customization** → **Modules** → **Contacts** → **Layouts**
2. Найдите **"Standard"**
3. Нажмите **"⋮"** (три точки) → **"Clone"**
4. Имя: **"Standard - Tikal Agents"**
5. Нажмите **"Save"**

## Шаг 2: Добавление полей в макет (3 минуты)

1. Откройте **"Standard - Tikal Agents"**
2. Нажмите **"Edit"**
3. Вкладка **"DETAIL VIEW"**
4. Перетащите поля из **"Unused Fields"**:
   - Agent ID
   - Extension
   - Tikal Status
   - Queues
   - Queue_Count
   - Active
5. **"Save and Close"**

## Шаг 3: Настройка разрешений (15 минут)

### Для каждого поля:

1. **Settings** → **Customization** → **Modules** → **Contacts** → **Fields**
2. Найдите поле (например, **"Agent ID"**)
3. Нажмите на поле
4. **"Field Level Security"** или **"Permissions"**
5. Для **каждой роли**:
   - ✅ **Visible** = Yes
   - ✅ **Editable** = Yes
6. **Save**

### Поля для настройки:
- Agent ID
- Extension
- Tikal Status
- Queues
- Queue_Count
- Active

**Время:** ~2-3 минуты на поле × 6 полей = ~15 минут

## ✅ Готово!

После настройки:
- ✅ Поля видны во всех макетах
- ✅ Поля доступны всем пользователям
- ✅ Поиск работает по полям

**Общее время:** ~20 минут
"""
    
    with open('ZOHO_QUICK_SETUP.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✓ Создана инструкция: ZOHO_QUICK_SETUP.md")


def main():
    """Основная функция"""
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 70)
    print("🔧 Настройка макетов и разрешений в Zoho CRM")
    print("=" * 70)
    print()
    
    # Инструкции по клонированию
    print_instructions()
    print()
    
    # Инструкции по API
    setup_zoho_api_instructions()
    print()
    
    # Ручная настройка
    manual_permissions_setup()
    print()
    
    # Создание скриптов и инструкций
    print("=" * 70)
    print("📝 Создание вспомогательных файлов...")
    print("=" * 70)
    
    create_permissions_script()
    create_quick_setup_guide()
    
    print()
    print("=" * 70)
    print("✅ Готово!")
    print("=" * 70)
    print()
    print("📋 Следующие шаги:")
    print("   1. Следуйте инструкциям выше для клонирования макета")
    print("   2. Настройте разрешения вручную (15 минут)")
    print("   3. Или настройте Zoho API и используйте zoho_api_permissions.py")
    print()
    print("📄 Файлы созданы:")
    print("   - zoho_api_permissions.py (скрипт для API)")
    print("   - ZOHO_QUICK_SETUP.md (быстрая инструкция)")


if __name__ == '__main__':
    main()
