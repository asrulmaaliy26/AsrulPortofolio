from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import now
import random

def get_weather_data(request):
    weather_conditions = ['Cerah', 'Berawan', 'Hujan', 'Badai', 'Kabut']
    data = {
        "jam": now().strftime('%H:%M:%S'),
        "hari": now().strftime('%A'),
        "tanggal": now().strftime('%Y-%m-%d'),
        "suhu": round(random.uniform(20, 35), 2),
        "kelembapan": round(random.uniform(50, 100), 2),
        "status_cuaca": random.choice(weather_conditions)
    }
    return JsonResponse(data)

# Create your views here.
def index(request):
    return render(request, 'weather_api/index.html')
