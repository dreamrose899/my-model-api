import requests
import json

API_URL = "https://my-model-api-s7y2.onrender.com/predict"

def run_agent_task(task_type, payload, api_key=None):
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-KEY"] = api_key
    
    data = {
        "agent_id": "Bot_Dreamrose_01",
        "task_type": task_type,
        "payload": payload
    }
    
    print(f"[*] Agent sending task: {task_type}...")
    
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        result = response.json()
        
        if response.status_code == 200:
            print("[+] Task success! Execution result:", result.get("execution_result"))
        elif response.status_code == 402:
            print("[!] Payment Required! Agent instructions:")
            print(json.dumps(result.get("payment_protocol"), indent=2))
        else:
            print("[!] Error:", result.get("message"))
            
    except Exception as e:
        print("[-] Connection failed:", e)

if __name__ == "__main__":
    run_agent_task("classification", {"input": "test_data_001"})
