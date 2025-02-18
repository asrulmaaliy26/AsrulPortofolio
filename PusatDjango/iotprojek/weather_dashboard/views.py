import requests
from django.shortcuts import render
from django.http import JsonResponse

API_URL = "http://127.0.0.1:8000/iot/weatherapi/getapi/"  # Sesuaikan dengan API cuaca yang telah dibuat

def fetch_weather_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None
    return None

def weather_dashboard(request):
    data = fetch_weather_data()
    return render(request, 'weather_dashboard/index.html', {'weather_data': data})

def get_weather_json(request):
    data = fetch_weather_data()
    return JsonResponse(data)
