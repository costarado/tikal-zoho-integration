"""
Пример скрипта для синхронизации агентов Tikal с Zoho CRM
Требует установки Zoho CRM API SDK
"""

from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG
import json
from datetime import datetime


def sync_agents_to_zoho():
    """
    Синхронизирует агентов из Tikal в Zoho CRM
    
    Требования:
    1. Установить Zoho CRM Python SDK: pip install zohocrmsdk
    2. Настроить Zoho API credentials
    3. Создать кастомные поля в Zoho CRM
    """
    
    print("=" * 70)
    print("Синхронизация агентов Tikal → Zoho CRM")
    print("=" * 70)
    
    # Шаг 1: Получаем агентов из Tikal
    print("\n1. Получение агентов из Tikal...")
    try:
        client = TikalClientV2(
            base_url=TIKAL_CONFIG['base_url'],
            api_key=TIKAL_CONFIG['api_key'],
            format=TIKAL_CONFIG.get('format', 'json')
        )
        
        # Получаем активных агентов
        from get_active_agents_only import get_active_agents
        agents = get_active_agents(client)
        
        print(f"✓ Получено {len(agents)} агентов из Tikal")
        
        client.close()
    
    except Exception as e:
        print(f"✗ Ошибка получения агентов: {e}")
        return
    
    # Шаг 2: Подключение к Zoho CRM
    print("\n2. Подключение к Zoho CRM...")
    try:
        # Пример использования Zoho CRM API
        # from zohocrmsdk.src.com.zoho.crm.api import Initializer
        # from zohocrmsdk.src.com.zoho.crm.api.contacts import ContactsOperations
        
        # Настройка Zoho API
        # Initializer.initialize(
        #     environment="production",
        #     token=zoho_token,
        #     store=token_store
        # )
        
        print("⚠ Zoho CRM API SDK не установлен")
        print("   Для полной интеграции установите: pip install zohocrmsdk")
        print("   И настройте Zoho API credentials")
        
        # Вместо реальной синхронизации, создаем JSON файл для ручного импорта
        sync_data = {
            'timestamp': datetime.now().isoformat(),
            'agents': agents,
            'summary': {
                'total': len(agents),
                'with_names': len([a for a in agents if a.get('name')]),
                'with_status': len([a for a in agents if a.get('status')]),
            }
        }
        
        output_file = f'zoho_sync_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sync_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Данные сохранены в {output_file}")
        print("   Используйте этот файл для ручной синхронизации или")
        print("   настройте Zoho API для автоматической синхронизации")
        
    except Exception as e:
        print(f"✗ Ошибка подключения к Zoho: {e}")
        return
    
    # Шаг 3: Обновление контактов в Zoho
    print("\n3. Обновление контактов в Zoho...")
    print("   (требует настройки Zoho API)")
    
    # Пример кода для обновления:
    # contacts_operations = ContactsOperations()
    # for agent in agents:
    #     contact = {
    #         'Agent_ID': agent['id'],
    #         'Extension': agent.get('extension', ''),
    #         'Tikal_Status': agent.get('status', ''),
    #         'Queues': ', '.join(agent.get('queues', [])),
    #         'Is_Active': True,
    #         'Last_Sync': datetime.now().isoformat()
    #     }
    #     # Обновление или создание контакта
    #     # contacts_operations.update_contact(contact_id, contact)
    
    print("\n" + "=" * 70)
    print("Синхронизация завершена")
    print("=" * 70)


def create_zoho_custom_fields_guide():
    """
    Создает руководство по созданию кастомных полей в Zoho
    """
    guide = """
# Руководство по созданию кастомных полей в Zoho CRM

## Шаг 1: Откройте настройки модуля Contacts

1. Войдите в Zoho CRM
2. Перейдите в **Settings** (⚙️) → **Customization** → **Modules**
3. Найдите модуль **Contacts** и нажмите на него

## Шаг 2: Создайте кастомные поля

Нажмите **Fields** → **Add Fields** и создайте следующие поля:

### 1. Agent ID
- **Field Type:** Text
- **Field Label:** Agent ID
- **Field Name:** Agent_ID
- **Length:** 50
- **Required:** No
- **Unique:** Yes (рекомендуется)

### 2. Extension
- **Field Type:** Text
- **Field Label:** Extension
- **Field Name:** Extension
- **Length:** 20
- **Required:** No

### 3. Tikal Status
- **Field Type:** Picklist
- **Field Label:** Tikal Status
- **Field Name:** Tikal_Status
- **Values:** 
  - Online
  - Offline
  - Ready
  - Busy
  - Not Available

### 4. Queues
- **Field Type:** Multi-Select Picklist
- **Field Label:** Queues
- **Field Name:** Queues
- **Values:** (добавьте ID ваших очередей)
  - 1005
  - 1012
  - 1142
  - ... (и т.д.)

### 5. Is Active
- **Field Type:** Checkbox
- **Field Label:** Is Active
- **Field Name:** Is_Active
- **Default Value:** Checked

### 6. Last Sync
- **Field Type:** Date and Time
- **Field Label:** Last Sync
- **Field Name:** Last_Sync
- **Required:** No

## Шаг 3: Настройте маппинг при импорте

При импорте CSV файла:
1. Zoho автоматически определит стандартные поля
2. Для кастомных полей выберите вручную:
   - Agent ID → Agent_ID
   - Extension → Extension
   - Status → Tikal_Status
   - Queues → Queues

## Шаг 4: Сохраните настройки

После создания всех полей:
1. Нажмите **Save**
2. Проверьте, что поля отображаются в форме контакта
3. Настройте видимость полей (если нужно)

## Готово!

Теперь при импорте агентов все данные будут правильно сопоставлены.
"""
    
    with open('ZOHO_CUSTOM_FIELDS_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✓ Создано руководство: ZOHO_CUSTOM_FIELDS_GUIDE.md")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--create-guide':
        create_zoho_custom_fields_guide()
    else:
        sync_agents_to_zoho()

