"""
Тестирование создания звонка через Tikal API
Имитация запроса из Zoho CRM
"""

import sys
import io
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from tikal_client.tikal_client_v2 import TikalClientV2
    from config import TIKAL_CONFIG
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)


def test_create_call(agent_id: str, phone_number: str):
    """Тестирование создания звонка"""
    print("=" * 70)
    print("📞 Тестирование создания звонка через Tikal API")
    print("=" * 70)
    
    print(f"\n📋 Параметры:")
    print(f"   Agent ID: {agent_id}")
    print(f"   Phone: {phone_number}")
    
    try:
        # Создаем клиент
        client = TikalClientV2(
            base_url=TIKAL_CONFIG['base_url'],
            api_key=TIKAL_CONFIG['api_key'],
            format=TIKAL_CONFIG.get('format', 'json')
        )
        
        # Очищаем номер (только цифры)
        phone_clean = ''.join(filter(str.isdigit, phone_number))
        print(f"   Phone (cleaned): {phone_clean}")
        
        # Создаем звонок
        print(f"\n🔄 Создание звонка...")
        result = client.calls.originate(
            agent_id=agent_id,
            dest_num=phone_clean,
            custom1='test_from_zoho',
            custom2='python_script'
        )
        
        # Проверяем результат
        if result.get('data', {}).get('status', {}).get('code') == '200':
            print(f"\n✅ Звонок успешно создан!")
            print(f"   Результат: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            error_msg = result.get('data', {}).get('status', {}).get('message', 'Unknown error')
            print(f"\n❌ Ошибка создания звонка:")
            print(f"   {error_msg}")
            print(f"   Полный ответ: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Основная функция"""
    print("=" * 70)
    print("🧪 Тест создания звонка из Zoho через Tikal")
    print("=" * 70)
    
    # Параметры для теста (можно изменить)
    agent_id = input("\nВведите Agent ID (или нажмите Enter для '6701'): ").strip()
    if not agent_id:
        agent_id = '6701'
    
    phone_number = input("Введите номер телефона (или нажмите Enter для '0508155492'): ").strip()
    if not phone_number:
        phone_number = '0508155492'
    
    test_create_call(agent_id, phone_number)
    
    print("\n" + "=" * 70)
    print("💡 Для использования из Zoho:")
    print("   1. Запустите веб-сервис: python zoho_call_service.py")
    print("   2. Настройте Zoho Workflow (см. ZOHO_CALL_INTEGRATION.md)")
    print("=" * 70)


if __name__ == '__main__':
    main()
