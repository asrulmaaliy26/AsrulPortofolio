import datetime
from pathlib import Path
from django.shortcuts import render
from fitur.scraping.views import get_bmkg_data
from mlprojek.prediksi.views import get_hasil_prediksi_data

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorSmartACData
from .helper import process_sensor_data

import random
# Create your views here.

is_receiving = True

def index(request):
    return render(request, 'skripsi/index.html')

def data(request):
    context = get_bmkg_data(request) 
    # Cek jika terjadi error saat mengambil data
    if 'error' in context:
        return render(request, 'scraping/datascrapingbmkg.html', {'error': context['error']})
    return render(request, 'skripsi/data.html', context)

def prediksi_list(request):
    """Menampilkan halaman dengan data prediksi"""
    result = get_hasil_prediksi_data()

    if "error" in result:
        return render(request, "skripsi/prediksi.html", {"error": result["error"]}, status=result["status"])

    return render(request, "skripsi/prediksi.html", {"files": result["files"]})

def dashboard(request):
    return render(request, 'skripsi/dashboard.html')

@csrf_exempt
def receive_data_ac(request):
    return process_sensor_data(request, allow_extra_fields=False)

def get_data_ac(request):
    """ Mengambil data dari database dan mengembalikannya dalam format JSON """
    data = SensorSmartACData.objects.order_by('-timestamp').values("timestamp","tempout", "humiout", "tempac", "modeac", "hasilpred")
    return JsonResponse(list(data), safe=False)