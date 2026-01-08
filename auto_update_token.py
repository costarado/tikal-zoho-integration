"""
Автоматическое обновление Access Token в config.py
Без интерактивного запроса
"""

import sys
import io
import requests
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from config import ZOHO_CONFIG
except ImportError:
    print("❌ config.py не найден")
    sys.exit(1)


def refresh_and_update_token():
    """Обновляет токен и автоматически обновляет config.py"""
    client_id = ZOHO_CONFIG.get('client_id')
    client_secret = ZOHO_CONFIG.get('client_secret')
    refresh_token = ZOHO_CONFIG.get('refresh_token')
    
    if not all([client_id, client_secret, refresh_token]):
        print("❌ Не настроены Client ID, Client Secret или Refresh Token")
        return False
    
    # Обновляем токен
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
            new_access_token = result.get('access_token')
            
            if not new_access_token:
                print("❌ Не удалось получить новый токен")
                return False
            
            # Обновляем config.py
            try:
                with open('config.py', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Заменяем access_token
                pattern = r"('access_token':\s*')([^']+)(')"
                replacement = f"\\1{new_access_token}\\3"
                new_content = re.sub(pattern, replacement, content)
                
                # Записываем обратно
                with open('config.py', 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("=" * 70)
                print("✅ Токен успешно обновлен и сохранен в config.py!")
                print("=" * 70)
                print(f"\n🔑 Новый Access Token: {new_access_token[:50]}...")
                print(f"⏱️  Действителен: 3600 секунд (~1 час)")
                print(f"\n✅ config.py автоматически обновлен!")
                return True
            except Exception as e:
                print(f"❌ Ошибка при обновлении config.py: {e}")
                print(f"\n💡 Обновите вручную:")
                print(f"   'access_token': '{new_access_token}'")
                return False
        else:
            print(f"❌ Ошибка обновления токена: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


if __name__ == '__main__':
    refresh_and_update_token()
