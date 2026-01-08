"""
Пример создания webhook сервера для приема CDR от Tikal
"""

from flask import Flask, request, jsonify
from tikal_client.services.cdr import CDRWebhookHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/tikal/cdr', methods=['POST', 'GET'])
def handle_cdr():
    """
    Обработчик webhook для получения CDR от Tikal
    
    Tikal будет отправлять данные в поле 'data' в формате:
    - JSON
    - XML
    - Key-value pairs
    """
    try:
        # Получаем данные запроса
        if request.method == 'POST':
            if request.is_json:
                request_data = request.json
                format_type = 'json'
            else:
                # Форма или key-value
                request_data = request.form.to_dict()
                format_type = 'keyvalue'
        else:
            # GET запрос
            request_data = request.args.to_dict()
            format_type = 'keyvalue'
        
        logger.info(f"Received CDR data: {request_data}")
        
        # Определяем формат данных
        data_string = request_data.get('data', '')
        if data_string:
            # Пытаемся определить формат
            if data_string.strip().startswith('<'):
                format_type = 'xml'
            elif data_string.strip().startswith('{'):
                format_type = 'json'
            else:
                format_type = 'keyvalue'
        
        # Обрабатываем CDR данные
        cdr_handler = CDRWebhookHandler()
        cdr_data = cdr_handler.handle_webhook_request(request_data, format_type)
        
        logger.info(f"Parsed CDR: {cdr_data}")
        
        # Здесь можно сохранить данные в БД, отправить в CRM и т.д.
        # Например:
        # save_to_database(cdr_data)
        # send_to_crm(cdr_data)
        
        # Возвращаем успешный ответ
        return jsonify({
            'status': 'success',
            'message': 'CDR received and processed'
        }), 200
    
    except Exception as e:
        logger.error(f"Error processing CDR: {e}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/tikal/cdr/test', methods=['GET'])
def test_cdr():
    """Тестовая страница для проверки webhook"""
    return """
    <h1>Tikal CDR Webhook Test</h1>
    <p>Webhook endpoint: /tikal/cdr</p>
    <p>Methods: POST, GET</p>
    <p>Expected data format:</p>
    <pre>
    {
        "data": "{\\"agent_id\\": 123, \\"caller_id\\": \\"+1234567890\\", ...}"
    }
    </pre>
    <p>Or XML:</p>
    <pre>
    {
        "data": "&lt;cdr&gt;&lt;agent_id&gt;123&lt;/agent_id&gt;...&lt;/cdr&gt;"
    }
    </pre>
    """


if __name__ == '__main__':
    print("=" * 70)
    print("Tikal CDR Webhook Server")
    print("=" * 70)
    print("\nWebhook URL: http://your-server.com/tikal/cdr")
    print("Test page: http://localhost:5000/tikal/cdr/test")
    print("\nStarting server on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("\n" + "=" * 70)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

