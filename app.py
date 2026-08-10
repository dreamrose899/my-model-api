from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    user_data = request.json or {}
    
    response_data = {
        "status": 402,
        "error": "Payment Required",
        "message": "Access to this AI model requires a valid transaction hash.",
        "payment_details": {
            "network": "Tron (TRC20)",
            "currency": "USDT",
            "amount_required": "1.00", 
            "address": "TWDJD3VtTFFVpZjKhtucMHXvdZjMnrYcep"
        },
        "instructions": "Send the exact amount to the address above, then send your transaction hash to verify and unlock the API."
    }
    
    return jsonify(response_data), 402

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
