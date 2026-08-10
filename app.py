from flask import Flask, jsonify, request

app = Flask(__name__)

# قاعدة بيانات مؤقتة لتخزين معاملات الزبائن المدفوعة (يمكن ربطها بقاعدة بيانات حقيقية لاحقاً)
PAID_TRANSACTIONS = set()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json or {}
    tx_hash = data.get("tx_hash")
    
    # إذا قام الزبون بإرسال رقم المعاملة وتحققنا منه
    if tx_hash and tx_hash in PAID_TRANSACTIONS:
        return jsonify({
            "status": 200,
            "success": True,
            "message": "Payment verified! Your AI model task is processing.",
            "result": "AI model output generated successfully."
        }), 200

    # إذا لم يدفع أو لم يرسل رقم المعاملة، يتم إرجاع طلب الدفع والبحث عن زبون جديد
    response_data = {
        "status": 402,
        "error": "Payment Required",
        "message": "Searching for client payment... Please send the required fee to process your request.",
        "payment_details": {
            "network": "Tron (TRC20)",
            "currency": "USDT",
            "amount_required": "1.00",
            "address": "TWDJD3VtTFFVpZjKhtucMHXvdZjMnrYcep"
        },
        "instructions": "Send 1 USDT to the address above, then send your request again including your 'tx_hash' to unlock the service."
    }
    
    return jsonify(response_data), 402

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
