"""
Утилита для проверки подключения к Tikal API
"""

import sys
import socket
import requests
from urllib.parse import urlparse
from config import TIKAL_CONFIG


def check_dns(hostname):
    """Проверяет разрешение DNS"""
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✓ DNS разрешен: {hostname} -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"✗ Ошибка DNS: {hostname} - {e}")
        return False


def check_port(hostname, port, timeout=5):
    """Проверяет доступность порта"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((hostname, port))
        sock.close()
        
        if result == 0:
            print(f"✓ Порт {port} доступен")
            return True
        else:
            print(f"✗ Порт {port} недоступен (код: {result})")
            return False
    except Exception as e:
        print(f"✗ Ошибка проверки порта {port}: {e}")
        return False


def check_http(url, timeout=10):
    """Проверяет HTTP/HTTPS подключение"""
    try:
        print(f"\nПроверка HTTP подключения к {url}...")
        response = requests.get(url, timeout=timeout, verify=False)
        print(f"✓ HTTP подключение успешно: {response.status_code}")
        return True
    except requests.exceptions.SSLError as e:
        print(f"⚠ SSL ошибка (возможно самоподписанный сертификат): {e}")
        print("   Попробуйте использовать HTTP или добавить сертификат")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"✗ Ошибка подключения: {e}")
        return False
    except requests.exceptions.Timeout:
        print(f"✗ Превышено время ожидания ({timeout} сек)")
        return False
    except Exception as e:
        print(f"✗ Неожиданная ошибка: {e}")
        return False


def check_alternative_urls(base_url):
    """Проверяет альтернативные варианты URL"""
    parsed = urlparse(base_url)
    hostname = parsed.hostname
    scheme = parsed.scheme
    port = parsed.port or (443 if scheme == 'https' else 80)
    
    alternatives = []
    
    # Проверяем HTTP вместо HTTPS
    if scheme == 'https':
        http_url = f"http://{hostname}:{port}"
        alternatives.append(http_url)
        if port == 443:
            alternatives.append(f"http://{hostname}")
    
    # Проверяем другие порты
    common_ports = [8080, 8443, 8000, 3000]
    for p in common_ports:
        if p != port:
            if scheme == 'https':
                alternatives.append(f"https://{hostname}:{p}")
            alternatives.append(f"http://{hostname}:{p}")
    
    print(f"\nПроверка альтернативных URL...")
    for alt_url in alternatives:
        try:
            response = requests.get(alt_url, timeout=5, verify=False)
            print(f"✓ Найден доступный URL: {alt_url} (статус: {response.status_code})")
        except:
            pass


def main():
    """Основная функция диагностики"""
    print("=" * 60)
    print("Диагностика подключения к Tikal API")
    print("=" * 60)
    
    base_url = TIKAL_CONFIG['base_url']
    parsed = urlparse(base_url)
    hostname = parsed.hostname
    scheme = parsed.scheme
    port = parsed.port or (443 if scheme == 'https' else 80)
    
    print(f"\nПроверяемый URL: {base_url}")
    print(f"Hostname: {hostname}")
    print(f"Схема: {scheme}")
    print(f"Порт: {port}")
    
    # 1. Проверка DNS
    print("\n" + "-" * 60)
    print("1. Проверка DNS")
    print("-" * 60)
    dns_ok = check_dns(hostname)
    
    if not dns_ok:
        print("\n❌ DNS не разрешается. Проверьте правильность hostname.")
        return
    
    # 2. Проверка порта
    print("\n" + "-" * 60)
    print("2. Проверка доступности порта")
    print("-" * 60)
    port_ok = check_port(hostname, port, timeout=5)
    
    if not port_ok:
        print(f"\n⚠ Порт {port} недоступен. Возможные причины:")
        print("   - Сервер не запущен")
        print("   - Файрвол блокирует подключение")
        print("   - Используется другой порт")
    
    # 3. Проверка HTTP подключения
    print("\n" + "-" * 60)
    print("3. Проверка HTTP/HTTPS подключения")
    print("-" * 60)
    
    # Пробуем с verify=False для самоподписанных сертификатов
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    http_ok = check_http(base_url, timeout=10)
    
    # 4. Проверка альтернативных URL
    if not http_ok:
        print("\n" + "-" * 60)
        print("4. Поиск альтернативных URL")
        print("-" * 60)
        check_alternative_urls(base_url)
    
    # Итоги
    print("\n" + "=" * 60)
    print("ИТОГИ ДИАГНОСТИКИ")
    print("=" * 60)
    
    if dns_ok and port_ok and http_ok:
        print("✓ Все проверки пройдены успешно!")
        print("  API должен быть доступен.")
    else:
        print("✗ Обнаружены проблемы с подключением.")
        print("\nРекомендации:")
        print("1. Убедитесь, что сервер Tikal запущен")
        print("2. Проверьте правильность URL в config.py")
        print("3. Проверьте настройки файрвола/сети")
        print("4. Если используется самоподписанный сертификат, добавьте его в систему")
        print("5. Попробуйте использовать HTTP вместо HTTPS (если поддерживается)")
        print("\nЕсли сервер находится в локальной сети, используйте внутренний IP адрес")


if __name__ == '__main__':
    main()

