from flask import Flask, request, jsonify

app = Flask(__name__)

# سجل تتبع الاستخدام المجاني
USAGE_TRACKER = {}
FREE_LIMIT = 5  # عدد المحاولات المجانية

# قائمة المفاتيح المدفوعة للعملاء
PAID_API_KEYS = [
    "USER_PAID_KEY_999",
]

# بيانات محفظتك للتحصيل بالـ USDT
USDT_WALLET = "TWDJD3VtTFFVpZjKhtucMHXvdZjMnrYcep"
USDT_NETWORK = "Polygon"
PRICE_USD = "10 USDT"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(silent=True) or {}
        user_ip = request.remote_addr
        api_key = request.headers.get('X-API-KEY')

        # 1. إذا كان العميل يملك مفتاح اشتراك مدفوع
        if api_key in PAID_API_KEYS:
            return jsonify({
                "status": "success",
                "message": "Piece is valid (Paid Access)",
                "is_passed": 1,
                "confidence": 0.98,
                "received_input": data
            }), 200

        # 2. متابعة الاستخدام المجاني
        user_usage = USAGE_TRACKER.get(user_ip, 0)

        # 3. إذا انتهت الفترة التجريبية
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

        # 4. معالجة الطلب التجريبي المجاني
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


