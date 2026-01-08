"""
Веб-сервис для создания звонков из Zoho CRM через Tikal API
Версия для Production развертывания (Railway, Render, и т.д.)
Использует переменные окружения для конфигурации
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import io
import logging

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from tikal_client.tikal_client_v2 import TikalClientV2
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)

app = Flask(__name__)
CORS(app)  # Разрешаем запросы из Zoho

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация из переменных окружения (для production)
TIKAL_BASE_URL = os.environ.get('TIKAL_BASE_URL', 'http://arielsip.com')
TIKAL_API_KEY = os.environ.get('TIKAL_API_KEY', 'c18950499e5838743873737478ff1de9')
TIKAL_FORMAT = os.environ.get('TIKAL_FORMAT', 'json')


def create_tikal_client():
    """Создает клиент Tikal API"""
    return TikalClientV2(
        base_url=TIKAL_BASE_URL,
        api_key=TIKAL_API_KEY,
        format=TIKAL_FORMAT
    )


@app.route('/health', methods=['GET'])
def health():
    """Проверка работоспособности сервиса"""
    return jsonify({
        'status': 'ok',
        'service': 'Zoho Call Service',
        'tikal_api': TIKAL_BASE_URL,
        'environment': os.environ.get('ENVIRONMENT', 'production')
    })


@app.route('/api/call/create', methods=['POST'])
def create_call():
    """
    Создает звонок через Tikal API
    
    Параметры запроса (JSON):
    - agent_id: ID агента (обязательно)
    - phone_number: Номер телефона (обязательно)
    - custom1: Пользовательское поле 1 (опционально)
    - custom2: Пользовательское поле 2 (опционально)
    - zoho_contact_id: ID контакта в Zoho (опционально, для логирования)
    
    Пример запроса:
    {
        "agent_id": "6701",
        "phone_number": "0508155492",
        "custom1": "zoho_contact_123",
        "custom2": "campaign_456"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Проверка обязательных полей
        agent_id = data.get('agent_id')
        phone_number = data.get('phone_number') or data.get('dest_num')
        
        if not agent_id:
            return jsonify({
                'success': False,
                'error': 'agent_id is required'
            }), 400
        
        if not phone_number:
            return jsonify({
                'success': False,
                'error': 'phone_number is required'
            }), 400
        
        # Дополнительные параметры
        custom1 = data.get('custom1', '')
        custom2 = data.get('custom2', '')
        zoho_contact_id = data.get('zoho_contact_id', '')
        
        # Создаем клиент и звонок
        client = create_tikal_client()
        
        logger.info(f"Creating call: agent_id={agent_id}, phone={phone_number}")
        
        result = client.calls.originate(
            agent_id=agent_id,
            dest_num=phone_number,
            custom1=custom1 or zoho_contact_id,
            custom2=custom2
        )
        
        client.close()
        
        # Проверяем результат
        if result.get('data', {}).get('status', {}).get('code') == '200':
            return jsonify({
                'success': True,
                'message': 'Call created successfully',
                'data': result.get('data', {}),
                'agent_id': agent_id,
                'phone_number': phone_number
            }), 200
        else:
            error_msg = result.get('data', {}).get('status', {}).get('message', 'Unknown error')
            return jsonify({
                'success': False,
                'error': error_msg,
                'data': result
            }), 400
    
    except Exception as e:
        logger.error(f"Error creating call: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/call/status', methods=['GET'])
def call_status():
    """Проверка статуса сервиса"""
    try:
        client = create_tikal_client()
        # Простая проверка подключения
        client.close()
        
        return jsonify({
            'status': 'ok',
            'tikal_api': TIKAL_BASE_URL,
            'service': 'Zoho Call Service',
            'environment': os.environ.get('ENVIRONMENT', 'production')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # Получаем порт из переменной окружения (для Railway, Render и т.д.)
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 70)
    print("📞 Zoho Call Service - Production Version")
    print("=" * 70)
    print(f"\n🌐 Сервис запущен на порту: {port}")
    print(f"📋 Endpoints:")
    print(f"   GET  /health - проверка работоспособности")
    print(f"   POST /api/call/create - создание звонка")
    print(f"   GET  /api/call/status - статус сервиса")
    print(f"\n💡 Используйте этот сервис для интеграции с Zoho CRM")
    print("=" * 70)
    print()
    
    # Запуск сервера
    app.run(host='0.0.0.0', port=port, debug=False)
