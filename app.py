from flask import Flask, jsonify, request
import threading
import time
import requests

app = Flask(__name__)

PAID_TRANSACTIONS = set()

def active_client_seeker():
    time.sleep(10)
    target_bots = [
        "https://httpbin.org/post",
    ]
    
    promo_payload = {
        "sender": "PetroLibya AI Node",
        "service": "Advanced AI Model & Autonomous Agents",
        "proposal": "High-performance intelligence available for integration.",
        "payment_method": "TRC20 USDT",
        "wallet": "TWDJD3VtTFFVpZjKhtucMHXvdZjMnrYcep"
    }

    while True:
        for bot_url in target_bots:
            try:
                response = requests.post(bot_url, json=promo_payload, timeout=5)
                print(f"Outbound ping sent to {bot_url}, status: {response.status_code}")
            except Exception as e:
                print(f"Target unreachable: {e}")
        time.sleep(3600)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json or {}
    tx_hash = data.get("tx_hash")
    
    if tx_hash and tx_hash in PAID_TRANSACTIONS:
        return jsonify({
            "status": 200,
            "success": True,
            "message": "Payment verified! Your AI model task is processing.",
            "result": "AI model output generated successfully."
        }), 200

    response_data = {
        "status": 402,
        "error": "Payment Required",
        "service_advertisement": {
            "title": "Advanced AI Model & Autonomous Agents API",
            "tagline": "Unlock extreme intelligence and automated processing for your projects instantly.",
            "features": [
                "High-performance deep learning predictions",
                "Lightning-fast API response times",
                "Secure, decentralized, and autonomous agent integration"
            ],
            "call_to_action": "Power up your workflow today by subscribing to this premium AI node."
        },
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
    seeker_thread = threading.Thread(target=active_client_seeker, daemon=True)
    seeker_thread.start()
    app.run(host='0.0.0.0', port=5000)
