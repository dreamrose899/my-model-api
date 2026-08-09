from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)

# إعداد توثيق Swagger / OpenAPI
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda rule: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "template_folder": "swagger",
    "specs_route": "/apidocs/"
}

template = {
    "swagger": "2.0",
    "info": {
        "title": "Model Prediction API",
        "description": "API لتشغيل النماذج وتحليل البيانات مع دعم الفترة التجريبية والمفاتيح المدفوعة.",
        "version": "1.0.0"
    },
    "host": "my-model-api-s7y2.onrender.com",
    "basePath": "/",
    "schemes": ["https"]
}

swagger = Swagger(app, config=swagger_config, template=template)

USAGE_TRACKER = {}
FREE_LIMIT = 5

PAID_API_KEYS = [
    "USER_PAID_KEY_999"
]

USDT_WALLET = "TWDJD3VtTFFVpZjKhtucMHXvdZjMnrYcep"
USDT_NETWORK = "TRC20"
PRICE_USD = "10 USDT"

@app.route('/predict', methods=['POST'])
def predict():
    """
    إرسال بيانات للتحليل أو التنبؤ
    ---
    tags:
      - Prediction Service
    parameters:
      - name: X-API-KEY
        in: header
        type: string
        required: false
        description: مفتاح الاشتراك المدفوع (اختياري للفترة التجريبية)
      - name: body
        in: body
        required: true
        schema:
          type: object
          example:
            data: "sample input"
    responses:
      200:
        description: نجاح الطلب (تجريبي أو مدفوع)
      402:
        description: انتهاء المحاولات المجانية وتطلب الدفع
      500:
        description: خطأ داخلي في السيرفر
    """
    try:
        data = request.get_json(silent=True) or {}
        user_ip = request.remote_addr
        api_key = request.headers.get('X-API-KEY')

        # 1. العميل المدفوع
        if api_key in PAID_API_KEYS:
            return jsonify({
                "status": "success",
                "message": "Piece is valid (Paid Access)",
                "is_passed": 1,
                "confidence": 0.98,
                "received_input": data
            }), 200

        # 2. الاستخدام المجاني
        user_usage = USAGE_TRACKER.get(user_ip, 0)

        # 3. انتهاء الفترة التجريبية
        if user_usage >= FREE_LIMIT:
            return jsonify({
                "status": "payment_required",
                "message": "Free trial completed. Send payment to continue.",
                "payment_details": {
                    "currency": "USDT",
                    "price": PRICE_USD,
                    "network": USDT_NETWORK,
                    "wallet_address": USDT_WALLET,
                    "instructions": "Send transaction hash to support to receive your X-API-KEY"
                }
            }), 402

        # 4. معالجة الطلب التجريبي
        USAGE_TRACKER[user_ip] = user_usage + 1
        remaining = FREE_LIMIT - USAGE_TRACKER[user_ip]

        return jsonify({
            "status": "success",
            "message": "Piece is valid (Free Trial)",
            "is_passed": 1,
            "confidence": 0.98,
            "remaining_free_requests": remaining,
            "received_input": data
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
