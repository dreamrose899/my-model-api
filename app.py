from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({
        "status": 402,
        "error": "Payment Required",
        "payment_protocol": {
            "method": "TRC20",
            "address": "TWDJD3VtTFFVpZjKhtucMHXvdZjMnrYcep"
        }
    }), 402

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
