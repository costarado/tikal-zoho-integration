"""
Скрипт для получения Refresh Token из Zoho CRM API
Используйте после получения Authorization Code из браузера
"""

import requests
import sys
import io

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Настройки (заполните своими данными)
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
AUTHORIZATION_CODE = "code_from_browser_url"  # Получите из URL после авторизации
REDIRECT_URI = "http://localhost:8080"  # Должен совпадать с настройками приложения


def get_refresh_token():
    """Получает Refresh Token из Authorization Code"""
    
    if CLIENT_ID == "your_client_id" or not CLIENT_ID:
        print("❌ Ошибка: Настройте CLIENT_ID, CLIENT_SECRET и AUTHORIZATION_CODE в скрипте")
        return
    
    url = "https://accounts.zoho.com/oauth/v2/token"
    
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": AUTHORIZATION_CODE
    }
    
    print("=" * 70)
    print("🔑 Получение Refresh Token из Zoho CRM")
    print("=" * 70)
    print(f"\n📋 Параметры:")
    print(f"   Client ID: {CLIENT_ID[:20]}...")
    print(f"   Redirect URI: {REDIRECT_URI}")
    print(f"   Authorization Code: {AUTHORIZATION_CODE[:30]}...")
    print()
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        
        if response.status_code == 200:
            print("✅ Успешно получены токены!")
            print()
            print("=" * 70)
            print("📝 СОХРАНИТЕ ЭТИ ДАННЫЕ:")
            print("=" * 70)
            print(f"\n🔄 Refresh Token:")
            print(f"   {result.get('refresh_token')}")
            print(f"\n🔑 Access Token (временный):")
            print(f"   {result.get('access_token')}")
            print(f"\n⏱️  Expires In: {result.get('expires_in')} секунд")
            print()
            print("=" * 70)
            print("⚠️  ВАЖНО:")
            print("=" * 70)
            print("   1. Сохраните Refresh Token в безопасном месте")
            print("   2. Добавьте его в config.py как ZOHO_CONFIG['refresh_token']")
            print("   3. Refresh Token действует бессрочно (пока не отозван)")
            print("   4. Access Token временный, не сохраняйте его")
            print()
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {result}")
            print()
            if 'error' in result:
                print("💡 Возможные причины:")
                if result['error'] == 'invalid_client':
                    print("   - Неверный Client ID или Client Secret")
                elif result['error'] == 'invalid_grant':
                    print("   - Authorization Code истек (действителен 1 минуту)")
                    print("   - Получите новый код из браузера")
                elif result['error'] == 'invalid_redirect_uri':
                    print("   - Redirect URI не совпадает с настройками приложения")
    
    except Exception as e:
        print(f"❌ Ошибка при запросе: {e}")


if __name__ == '__main__':
    get_refresh_token()
