"""
Обновление Access Token через Refresh Token
Использует Client ID и Client Secret из config.py
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


def refresh_access_token():
    """Обновляет Access Token через Refresh Token"""
    print("=" * 70)
    print("🔄 Обновление Access Token через Refresh Token")
    print("=" * 70)
    
    client_id = ZOHO_CONFIG.get('client_id')
    client_secret = ZOHO_CONFIG.get('client_secret')
    refresh_token = ZOHO_CONFIG.get('refresh_token')
    
    # Проверка настроек
    if client_id == 'your_client_id_here' or not client_id:
        print("\n❌ Client ID не настроен!")
        print("\n📋 Инструкция:")
        print("   1. Перейдите: https://api-console.zoho.com/")
        print("   2. Найдите или создайте приложение")
        print("   3. Скопируйте Client ID и Client Secret")
        print("   4. Обновите config.py:")
        print("      'client_id': 'ваш_client_id'")
        print("      'client_secret': 'ваш_client_secret'")
        return False
    
    if not refresh_token or refresh_token == 'your_refresh_token_here':
        print("\n❌ Refresh Token не настроен!")
        return False
    
    print(f"\n📋 Параметры:")
    print(f"   Client ID: {client_id[:20]}...")
    print(f"   Refresh Token: {refresh_token[:30]}...")
    print()
    
    # Запрос на обновление токена
    url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
    
    try:
        print("🔄 Отправка запроса...")
        response = requests.post(url, data=data)
        result = response.json()
        
        if response.status_code == 200:
            new_access_token = result.get('access_token')
            expires_in = result.get('expires_in', 3600)
            
            print("\n" + "=" * 70)
            print("✅ Токен успешно обновлен!")
            print("=" * 70)
            print(f"\n🔑 Новый Access Token:")
            print(f"   {new_access_token}")
            print(f"\n⏱️  Действителен: {expires_in} секунд (~{expires_in // 3600} часов)")
            print()
            print("=" * 70)
            print("📝 ОБНОВИТЕ config.py:")
            print("=" * 70)
            print(f"\nZOHO_CONFIG = {{")
            print(f"    # ...")
            print(f"    'access_token': '{new_access_token}',")
            print(f"    'refresh_token': '{refresh_token}',")
            print(f"    # ...")
            print(f"}}")
            print()
            print("💡 Или скопируйте токен выше и вставьте в config.py вручную")
            print()
            
            # Предложение автоматического обновления
            print("=" * 70)
            print("🤖 Автоматическое обновление config.py?")
            print("=" * 70)
            answer = input("Обновить config.py автоматически? (y/n): ").strip().lower()
            
            if answer == 'y' or answer == 'yes' or answer == 'да':
                try:
                    # Читаем config.py
                    with open('config.py', 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Заменяем access_token
                    import re
                    pattern = r"('access_token':\s*')([^']+)(')"
                    replacement = f"\\1{new_access_token}\\3"
                    new_content = re.sub(pattern, replacement, content)
                    
                    # Записываем обратно
                    with open('config.py', 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print("\n✅ config.py успешно обновлен!")
                    print("   Теперь можно запустить: python test_zoho_connection.py")
                except Exception as e:
                    print(f"\n⚠️  Не удалось обновить config.py автоматически: {e}")
                    print("   Обновите вручную, используя токен выше")
            
            return True
        else:
            print(f"\n❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {json.dumps(result, indent=2, ensure_ascii=False)}")
            print()
            
            if 'error' in result:
                error = result['error']
                print("💡 Возможные причины:")
                if error == 'invalid_client':
                    print("   - Неверный Client ID или Client Secret")
                elif error == 'invalid_refresh_token':
                    print("   - Refresh Token истек или отозван")
                    print("   - Получите новый Refresh Token через авторизацию")
                else:
                    print(f"   - {error}")
            
            return False
    
    except Exception as e:
        print(f"\n❌ Ошибка при запросе: {e}")
        return False


if __name__ == '__main__':
    refresh_access_token()
