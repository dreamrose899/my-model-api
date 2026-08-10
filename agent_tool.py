import requests

def model_prediction_tool(input_data: str, api_key: str = None) -> str:
    url = "https://my-model-api-s7y2.onrender.com/predict"
    headers = {"Content-Type": "application/json"}
    
    if api_key:
        headers["X-API-KEY"] = api_key
        
    payload = {"test": input_data}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        
        if response.status_code == 200:
            return f"Success: {result.get('message')}, Confidence: {result.get('confidence')}"
        elif response.status_code == 402:
            payment_info = result.get("payment_protocol", {})
            return f"Payment Required. Send {payment_info.get('instructions')} to wallet: {payment_info.get('address')}"
        else:
            return f"Error: {result.get('message')}"
            
    except Exception as e:
        return f"Connection failed: {str(e)}"

if __name__ == "__main__":
    print(model_prediction_tool("test_data_001"))
