import requests

url = "http://127.0.0.1:3000/skripsi/api/receive_data_ac/"
headers = {"Content-Type": "application/json"}
data = {
    "tempout": 1000000,
    "humiout": 6000000,
    "tempac": 22000000,
    "modeac": 3
}

response = requests.post(url, json=data, headers=headers)
print(response.status_code, response.json())