import requests

url = "http://127.0.0.1:8000/skripsi/api/receive_data_ac/"
headers = {"Content-Type": "application/json"}
data = {
    "tempout": 12,
    "humiout": 12,
    "tempac": 12,
    "modeac": 12
}

response = requests.post(url, json=data, headers=headers)
print(response.status_code, response.json())