from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(silent=True) or {}
        
        # استجابة نموذج الفحص
        response_data = {
            "status": "success",
            "message": "Piece is valid",
            "is_passed": 1,
            "confidence": 0.98,
            "received_input": data
        }
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

